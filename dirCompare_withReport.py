#!/usr/bin/env python
from filecmp import dircmp
import sys, subprocess

#DIR_1="/tmp/test2/repo1"
#DIR_2="/tmp/test2/repo2"

DIR_1=sys.argv[1]
DIR_2=sys.argv[2]
DIFF_REPORT="diffReport.txt"

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

#print header
print_header()

# differen files
for i in different_list:
    print_info(status="DIFFERENT", filename=i['name'], dir1=i['dir1_path'], dir2=i['dir2_path'])

##just for different files generate deatiled report
print_diff_report(different_list=different_list)

#common files/subdirectories
for i in common_list:
    print_info(status="NO-DIFF", filename=i['name'], dir1=i['dir1_path'], dir2=i['dir2_path'])

#only in DIR1
for i in dir1_only_list:
    print_info(status="ONLY-DIR1", filename=i['name'], dir1=i['dir1_path'], dir2="")

#only in DIR2
for i in dir2_only_list:
    print_info(status="ONLY-DIR2", filename=i['name'], dir1="", dir2=i['dir2_path'])
  
