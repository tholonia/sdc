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
from proclib import prun, splitnonalpha, getID, procTime, cleanTree, cleanWildcard, errprint
init()
import time
import shutil


#^ define selection arrays

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -i, --id          ID number
    -d, --dir     directory
    -s  --settingsfile
'''
    print(rs)
    exit()

#[ MAIN ]

fromfile = "sdw/xy_36x6.txt"
id = "000000000000000"
dir = "/tmp"
rifedir = "/home/jw/src/rife"

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

errprint(f"Reading Settings File: {fromfile}")

sam_sch = json.dumps(aorg['sampler_schedule'])
chk_sch = json.dumps(aorg['checkpoint_schedule'])
prm_sch = aorg['prompts']

# matches = re.findall('(.*[0-9]*):...([A-Za-z0-9+\s]*).*',sam_sch,re.DOTALL)
tsam_matches = list(re.findall('([0-9]*):....([A-Za-z0-9+\s]*)',sam_sch,re.DOTALL))
tchk_matches = list(re.findall('([0-9]*):....([A-Za-z0-9+\s]*)',chk_sch,re.DOTALL))

#^ convert to lists (from tuples)
sam_matches = [list(ele) for ele in tsam_matches]
chk_matches = [list(ele) for ele in tchk_matches]
# pprint(sam_matches)
# exit()


#^ build ckpt list of lists fpr sampler and ckpt

prm_matches = []
for p in prm_sch:
    # print(prm_sch[p])
    desc = list(re.findall('(\[.*\])', prm_sch[p], re.DOTALL))
    # print(desc)
    prm_matches.append([p,desc[0]])

prm_pairs = []
for i in range(len(prm_matches)):
    try:
        _from = int(prm_matches[i][0])
        _to = int(prm_matches[i+1][0])
        _prm = prm_matches[i][1]
        prm_pairs.append([_from, _to, _prm])
    except:
        pass

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



# cleanTree(f"{rifedir}/images")

srcfile = f"{id}.mp4"
timeStart = time.time()
cleanWildcard(f"{dir}/*.png")
print(Fore.GREEN + f"Extracting images from {srcfile} to {dir}" + Fore.RESET, end="",file=sys.stderr)
cmd = f"ffmpeg -loglevel warning -i {srcfile} -r 15/1 {dir}/{id}_%05d.png"
prun(cmd)
errprint(f"   ({procTime(timeStart)})")

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

timeStart = time.time()
print(Fore.CYAN + f"Applying Sampler Label", end="")
for i in range(len(filenums)):
    filename = f"{id}_{ (i+1):05d}.png"
    for pair in sam_pairs:
        if i>=pair[0] and  i<pair[1]:
            label = f"{pair[2]}"
            label=label.replace(" ","_")
            # print(f"{filename} -> {label}")
            fontsize = int(512 / 21)
            # errprint(Fore.CYAN+f"Updating: {filename} with {label}"+Fore.RESET)
            cmd1=f"convert {dir}/{filename}  -background PaleVioletRed	 -pointsize {fontsize} -fill maroon label:{label} -gravity Center -append /tmp/outlabel.png"
            prun(cmd1)
            cmd2=f"mv /tmp/outlabel.png {dir}/{filename}"
            prun(cmd2)
print(f"   ({procTime(timeStart)})")

timeStart = time.time()
print(Fore.YELLOW + f"Applying Checkpoint Label", end="")
for i in range(len(filenums)):
    filename = f"{id}_{(i+1):05d}.png"
    for pair in chk_pairs:
        if i>=pair[0] and  i<pair[1]:
            label = f"{pair[2]}"
            label=label.replace(" ","_")
            # print(f"{filename} -> {label}")
            fontsize = int(512 / 21)
            # errprint(Fore.YELLOW+f"Updating: {filename} with {label}"+Fore.RESET)
            cmd1=f"convert {dir}/{filename}  -background SlateGray2	  -pointsize {fontsize} -fill NavyBlue label:{label} -gravity Center -append /tmp/outlabel.png"
            prun(cmd1)
            cmd2=f"mv /tmp/outlabel.png {dir}/{filename}"
            prun(cmd2)
print(f"   ({procTime(timeStart)})")

timeStart = time.time()
print(Fore.MAGENTA + f"Applying Checkpoint Label", end="")
for i in range(len(filenums)):
    filename = f"{id}_{(i+1):05d}.png"
    for pair in prm_pairs:
        if i>=pair[0] and  i<pair[1]:
            label = f"{pair[2]}"
            label=label.replace(" ","_")
            # print(f"{filename} -> {label}")
            fontsize = int(512 / 35)
            # errprint(Fore.MAGENTA+f"Updating: {filename} with {label}"+Fore.RESET)
            cmd1=f"convert {dir}/{filename}  -background SlateGray2	  -pointsize {fontsize} -fill NavyBlue label:{label} -gravity Center -append /tmp/outlabel.png"
            prun(cmd1)
            cmd2=f"mv /tmp/outlabel.png {dir}/{filename}"
            prun(cmd2)
print(f"   ({procTime(timeStart)})")

# #^ stitch video
timeStart = time.time()
print(Fore.GREEN + f"Stitching video" + Fore.RESET, end="",file=sys.stderr)
cmd = f"ffmpeg -y -loglevel warning -framerate 15 -pattern_type glob -i {dir}/*.png  -c:v libx264 -pix_fmt yuv420p /tmp/out.mp4"
prun(cmd)
cmd = f"mv /tmp/out.mp4 {dir}/labeled_{id}.mp4"
prun(cmd)
errprint(f"   ({procTime(timeStart)})")
cleanWildcard(f"{dir}/*.png")