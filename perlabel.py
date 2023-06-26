#!/bin/env python
import random
import getopt,sys
import json
import os
from pprint import pprint
import re
import glob
import subprocess
from colorama import init, Fore, Back
import ffmpeg
init()



#^ define selection arrays

def prun(cmd):
    print(Fore.YELLOW+cmd+Fore.RESET)
    scmd = cmd.split()
    process = subprocess.Popen(scmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stderr)
        raise RuntimeError(stderr)

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -i, --id          ID number
    -d, --dir     directory
    -s  --settingsfile
'''
    print(rs)

#[ MAIN ]

fromfile = "sdw/xy_36x6.txt"
id = "000000000000000"
dir = "/tmp"

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hi:d:s:", [
        "help",
        "id=",
        "dir=",
        "settings=",
    ])
except Exception as e:
    print(str(e))
for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-i", "--id"):
        id = arg
    if opt in ("-d", "--dir"):
        dir = arg
    if opt in ("-s", "--settings"):
        fromfile = arg

#^ load original template into JSON array
f = open(fromfile)
aorg = json.load(f)

sam_sch = json.dumps((aorg['sampler_schedule']))
chk_sch = json.dumps((aorg['checkpoint_schedule']))
# pprint(chk_sch)
# exit()

# matches = re.findall('(.*[0-9]*):...([A-Za-z0-9+\s]*).*',sam_sch,re.DOTALL)
tsam_matches = list(re.findall('([0-9]*):....([A-Za-z0-9+\s]*)',sam_sch,re.DOTALL))
tchk_matches = list(re.findall('([0-9]*):....([A-Za-z0-9+\s]*)',chk_sch,re.DOTALL))

#^ convert to lists (from tuples)
sam_matches = [list(ele) for ele in tsam_matches]
chk_matches = [list(ele) for ele in tchk_matches]

#^ build ckpt list of lists fpr sampler and ckpt

sam_pairs = []
for i in range(len(sam_matches)):
    try:
        _from = int(sam_matches[i][0])
        _to = int(sam_matches[i+1][0])
        _sam = sam_matches[i][1]
        if aorg["enable_sampler_scheduling"] == False:
            _sam = aorg['sampler']
        try:
            sam_pairs.append([_from,_to,_sam])
        except:
            pass
    except:
        pass

chk_pairs = []
for i in range(len(chk_matches)):
    try:
        _from = int(chk_matches[i][0])
        _to = int(chk_matches[i+1][0])
        _chk = chk_matches[i][1]
        if aorg["enable_checkpoint_scheduling"] == False:
            _chk = aorg['sd_model_name']
        try:
            chk_pairs.append([_from,_to,_chk])
        except:
            pass
    except:
        pass
gfiles = glob.glob(f"{dir}/*.png")
# print(f"{dir}/*.png",gfiles)
filenums = []
for gfile in gfiles:
    # fnum = re.findall("[\d]*_(\d\d\d\d\d\d\d\d\d).png",gfile,re.DOTALL)
    # filenums.append(int(fnum[0]))
    fnum = re.findall(".*.png",gfile,re.DOTALL)
    filenums.append(fnum[0])

# print(filenums)
# colorname at https://magickstudio.imagemagick.org/Color.html
# colorname at https://magickstudio.imagemagick.org/Color.htm


for i in range(len(filenums)):
    filename = f"{id}_{ (i+1):09d}.png"
    for pair in sam_pairs:
        if i>=pair[0] and  i<pair[1]:
            label = f"{pair[2]}"
            label=label.replace(" ","_")
            # print(f"{filename} -> {label}")
            fontsize = int(512 / 21)
            cmd1=f"convert {dir}/{filename}  -background PaleVioletRed	 -pointsize {fontsize} -fill maroon label:{label} -gravity Center -append /tmp/outlabel.png"
            # print(cmd1)
            # prun(cmd)
            cmd2=f"mv /tmp/outlabel.png {dir}/{filename}"
            print(f"{cmd1} && {cmd2}")
            # os.system(cmd)

for i in range(len(filenums)):
    filename = f"{id}_{(i+1):09d}.png"
    for pair in chk_pairs:
        if i>=pair[0] and  i<pair[1]:
            label = f"{pair[2]}"
            label=label.replace(" ","_")
            # print(f"{filename} -> {label}")
            fontsize = int(512 / 21)
            cmd1=f"convert {dir}/{filename}  -background SlateGray2	  -pointsize {fontsize} -fill NavyBlue label:{label} -gravity Center -append /tmp/outlabel.png"
            # print(cmd1)
            # prun(cmd)
            cmd2=f"mv /tmp/outlabel.png {dir}/{filename}"
            print(f"{cmd1} && {cmd2}")
            # os.system(cmd)



#
# pprint(pairs)
#
#

# ([\w+\s])
#
# ([0-9]*:).*[\(\"](.*)"\)+