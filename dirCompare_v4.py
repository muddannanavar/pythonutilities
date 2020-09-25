#!/usr/bin/env python
from filecmp import dircmp
import sys, subprocess, re

#DIR_1="/tmp/test2/repo1"
#DIR_2="/tmp/test2/repo2"

DIR_1=sys.argv[1]
DIR_2=sys.argv[2]
DIFF_REPORT="diffReport.txt"
CONSOLIDATED_REPORT="ConsolidateCompareReport.txt"

#result = dircmp(DIR_1, DIR_2)
different_list = []
common_list = []
dir1_only_list = []
dir2_only_list = []

def get_diff_files(dcmp):
    for name in dcmp.diff_files:
        #print(f"diff file {name} in {dcmp.left} and {dcmp.right}")
        diff_file = {'name':name, 'dir1_path':dcmp.left, 'dir2_path': dcmp.right}
        different_list.append(diff_file)
    for name in dcmp.common:
        #print(f"common file {name} in {dcmp.left} and {dcmp.right}")
        common_file = {'name':name, 'dir1_path':dcmp.left, 'dir2_path': dcmp.right}
        common_list.append(common_file)
    for name in dcmp.left_only:
        #print (f"only in dir1 {name} in {dcmp.left}")
        dir1_only = {'name':name, 'dir1_path':dcmp.left}
        dir1_only_list.append(dir1_only)
    for name in dcmp.right_only:
        #print (f"only in dir2 {name} in {dcmp.right}")   
        dir2_only = {'name':name, 'dir2_path':dcmp.right}   
        dir2_only_list.append(dir2_only)
    for sub_dcmp in dcmp.subdirs.values():
        get_diff_files(sub_dcmp)

def print_header():
    print ("\nDiff report")
    print ("="*40)
    print(f"{'status':12}|{'name':30}|{'dir1_path':40}|{'dir2_path':40}")
    print ("-"*120)    

def print_info(status="", filename="", dir1="", dir2=""):
    print(f"{status:12}|{filename:40}|{dir1:40}|{dir2:40}")

def get_diff(l_file, r_file):
    diff_msg=""
    diff_cmd = f"diff {l_file} {r_file}"
    try:
        diff_output=subprocess.check_output(diff_cmd, stderr=subprocess.STDOUT, shell=True)
        diff_msg=diff_output
    except subprocess.CalledProcessError as e:
        diff_msg=e.output.decode("utf-8")

    return diff_msg  

def print_diff_report(different_list):
    with open(DIFF_REPORT, 'w') as f:
        for i in different_list:
            l_file = f"{i['dir1_path']}/{i['name']}"
            r_file = f"{i['dir2_path']}/{i['name']}"
            diff_cmd = f"diff {l_file} {r_file}"
            f.write(f"Diff - {l_file} vs {r_file}\n")
            f.write("="*20 + "\n")
            try:
                diff_output=subprocess.check_output(diff_cmd, stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError as e:
                f.write(e.output.decode("utf-8"))    


dcmp = dircmp(DIR_1, DIR_2) 
get_diff_files(dcmp) 

nodiffaddon={}
diffaddon={}

with open(CONSOLIDATED_REPORT, 'w') as cr:
    cr.write(f"\nAdd ons in {DIR_1} but not in {DIR_2}\n")
    counter = 1
    for i in dir1_only_list:
        dir_path=i['dir1_path'].replace(DIR_1,'.')
        file_name = i['name']
        file_path=f"{dir_path}/{file_name}" 
        addon_extract=re.search('/addon/(.+?)/.*', file_path)
        if addon_extract:
            addon_name = addon_extract.group(1)        
            diffaddon[addon_name] = 'IN-DIR1-LIST'
            print(diffaddon[addon_name])
        cr.write(f"{' ':10}{counter}. {dir_path}/{file_name}\n")
        counter += 1


    cr.write(f"\nAdd ons in {DIR_2} but not in {DIR_1}\n")
    counter = 1
    for i in dir2_only_list:
        dir_path=i['dir2_path'].replace(DIR_2,'.')
        file_name = i['name']
        file_path=f"{dir_path}/{file_name}" 
        addon_extract=re.search('/addon/(.+?)/.*', file_path)
        if addon_extract:
            addon_name = addon_extract.group(1)        
            diffaddon[addon_name] = 'IN-DIR2-LIST'              
        cr.write(f"{' ':10}{counter}. {dir_path}/{file_name}\n")
        counter += 1

    for i in different_list:
        dir_path=i['dir1_path'].replace(DIR_1,'.')
        file_name = i['name']
        file_path=f"{dir_path}/{file_name}"           
        addon_extract=re.search('/addon/(.+?)/.*', file_path)
        if addon_extract:
            addon_name = addon_extract.group(1)        
            diffaddon[addon_name] = 'IN-DIFF-LIST'


    cr.write(f"\nAdd ons in both locations & no difference: {DIR_2} and {DIR_1}\n\n")
    counter = 1
    cr.write(f"{' ':8}NO-DIFF\n")
    for i in common_list:
        addon_extract=re.search('/addon/(.+?)/.*', i['dir1_path'])
        if addon_extract:
            addon_name = addon_extract.group(1)
            if not (addon_name in diffaddon.keys()):
                nodiffaddon[addon_name] = "NO-DIFF"
    
    for key in nodiffaddon:
        cr.write(f"{' ':10}{counter}. {key}\n")
        counter += 1

    cr.write(f"\nAdd ons in both locations & different: {DIR_2} and {DIR_1}\n")
    counter = 1
    for i in different_list:
        l_file = f"{i['dir1_path']}/{i['name']}"
        r_file = f"{i['dir2_path']}/{i['name']}"
        dir_path=i['dir1_path'].replace(DIR_1,'.')
        file_name = i['name']
        cr.write(f"\n{' ':10}{counter}. {dir_path}/{file_name}\n")
        for line in get_diff(l_file=l_file, r_file=r_file).splitlines():
            cr.write(f"{' ':12}{line}\n")
        counter += 1