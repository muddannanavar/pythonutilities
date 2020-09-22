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

def print_diff_files(dcmp):
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
        print_diff_files(sub_dcmp)

dcmp = dircmp(DIR_1, DIR_2) 
print_diff_files(dcmp) 

#different files/subdirectories
print ("\nDifferent files/sub-directory")
print ("="*40)
print(f"{'name':30}|{'dir1_path':40}|{'dir2_path':40}")
print ("-"*120)

#capture diff resutl to DIFF_REPORT file
with open(DIFF_REPORT, 'w') as f:
    for i in different_list:
        #print(f"{i}")
        print(f"{i['name']:30}|{i['dir1_path']:40}|{i['dir2_path']:40}")
        l_file = f"{i['dir1_path']}/{i['name']}"
        r_file = f"{i['dir2_path']}/{i['name']}"
        diff_cmd = f"diff {l_file} {r_file}"
        f.write(f"Diff - {l_file} vs {r_file}\n")
        f.write("="*20 + "\n")
        try:
            diff_output=subprocess.check_output(diff_cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            f.write(e.output.decode("utf-8"))

#common files/subdirectories
print ("\n\nCommon files/sub-directory")
print ("="*40)
print(f"{'name':30}|{'dir1_path':40}|{'dir2_path':40}")
print ("-"*120)
for i in common_list:
    #print(f"{i}")
    print(f"{i['name']:30}|{i['dir1_path']:40}|{i['dir2_path']:40}")

#only in DIR1
print ("\n\nOnly in DIR1")
print ("="*40)
print(f"{'name':30}|{'dir1_path':40}")
print ("-"*70)
for i in dir1_only_list:
    #print(f"{i}")
    print(f"{i['name']:30}|{i['dir1_path']:40}")

#only in DIR2
print ("\nOnly in DIR2")
print ("="*40)
print(f"{'name':30}|{'dir2_path':40}")
print ("-"*70)
for i in dir2_only_list:
    #print(f"{i}")
    print(f"{i['name']:30}|{i['dir2_path']:40}")