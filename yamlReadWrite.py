#!/usr/bin/env python
import yaml
from pathlib import Path
import shutil

#xlist = [{"name": "vishwa"}]
bl_dict = {}
x= '#      some comment'
nil_dict = {"file10":1,"file 11":2,"file12":3, "file1":0}
il_dict = {}
to_dump = {}
with open("test.yaml", 'r') as yl:
    data = yaml.load(yl, Loader=yaml.FullLoader)
    print(data)
    #yl.write(yaml.dump(xlist))
    #yaml.dump(xlist,yl)
    for i in data['blacklist']:
        bl_dict[i] = 1
    for i in data['ignorelist']:
        il_dict[i] = 1

for key in nil_dict.keys():
    if key in bl_dict.keys():
        print(f"{key} file in blacklist adding it to list")
        il_dict[str(f"{key}{x}")] = 1
    else:
        print(f"{key} file not in blacklist not adding it to list")

with open("test.yaml", 'w') as ylw:
    bl_keys = list(bl_dict.keys())
    il_keys = list(il_dict.keys())
    to_dump['blacklist'] = []
    to_dump['ignorelist'] = []
    to_dump['blacklist'] = bl_keys
    to_dump['ignorelist'] = il_keys
    print(bl_keys)
    print(il_keys)
    yaml.dump(to_dump,ylw)

