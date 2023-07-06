#!/bin/env python
import os.path

import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import shutil
import json
import getopt, sys
from colorama import init, Fore, Back
from proclib import prun, cleanTree, cleanWildcard, getId, normalize, Diff_img, runExtract, runInterp, runStitch
import procvars as g
init()

# https://karobben.github.io/2021/04/10/Python/opencv-v-sm/
def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -d, --debug
    -r, --reuse         reuse last data 
    -f, --filter        filter all below this (0.0 - 1.0) default 0.1
    -k, --keep          keep every nth frame
    -v, --video         video file OR directory of extracted images
'''
    print(rs)
    exit()


reuseData = False
filter = False
keep = False
dirname = False
argv = sys.argv[1:]
locationpath = False
basename = ""
debug = False

try:
    opts, args = getopt.getopt(argv, "hrf:k:v:d", [
        "help",
        "reuse",
        "filter=",
        "keep=",
        "video=",
        "debug=",
    ])
except Exception as e:
    print(str(e))
for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-d", "--debug"):
        debug = True
    if opt in ("-v", "--video"):
        locationpath = arg
    if opt in ("-f", "--filter"):
        filter = float(arg)
    if opt in ("-k", "--keep"):
        keep = int(arg)
    if opt in ("-d", "--dirname"):
        dirname = arg
    if opt in ("-r", "--reuse"):
        reuseData = True
        if not reuseData:
            if os.path.exists(f"{g.tmpdir}/rsAry.json"):
                os.remove(f"{g.tmpdir}/rsAry.json")

if os.path.isdir(locationpath):
    dirname = locationpath
    basename = False
    fspec = "dir"
elif os.path.isabs(locationpath):
    basename = os.path.basename(locationpath)
    dirname = os.path.dirname(locationpath)
    fspec = "abs"
elif os.path.isfile(locationpath):
    basename = locationpath
    dirname = "."
    fspec = "rel"
else:
    print(f"Bad path argument or '{dirname}/{basename}' does not exist")
    exit()

print(f"dirname: {dirname}")
print(f"basename: {basename}")
print(f"fspec:{fspec}")


if fspec != "dir":
    print("Is a file")
    srcfile = f"{dirname}/{basename}"
    runExtract(srcfile)
    # exit()

#^ get list of
files = glob.glob(f"{g.tmpdir}/images/*.png")
files = sorted(files)

#^ check for existing data file
if os.path.exists(f"{dir}/rsAry.json"):
    f = open(f"{dir}/rsAry.json")
    rsAry = json.load(f)
    print(f"Reading stored data... ({len(rsAry)} items)")

# make sure there is a directory for filtering abd backup

# cleanTree(f"{g.tmpdir}/filtered")
# cleanTree(f"{g.tmpdir}/tossed")

rsAry = []  # ^ array that hols filenames and diffs
nAry = []  # ^ just for diffs

for i in range(1, len(files)):
    print(i,end="\r")
    if filter != False:
        rs = Diff_img(cv2.imread(files[i - 1]), cv2.imread(files[i]))
    else:
        rs = -1
    rs = rs * 1 #^ to convert from numpy int to python int
    rsAry.append([rs,files[i-1],files[i],0]) #^ 0 is a placeholder
    nAry.append(int(rs))

#^ create normalized diff values
if filter != False:
    nmAry = normalize(nAry)
else:
    nmAry = nAry
#^ and update the array of files
for i in range(len(nmAry)):
    rsAry[i][3]=nmAry[i]

jsonFile = open(f"{g.tmpdir}/rsAry.json", "w")
jsonFile.write(json.dumps(rsAry))
jsonFile.close()
print(f"Created stored data ({len(rsAry)} items)...")


#- START FILTERING


fcount = 0
if keep != False:
    i=0
    for item in rsAry:
        if i%keep!=0:
            if os.path.exists(item[1]):
                print(Fore.RED+f"Keep Tossed: {item[1]} to {g.tmpdir}/tossed"+Fore.RESET)
                cmd=f"cp {item[1]} {g.tmpdir}/tossed"
                prun(cmd,debug=debug)
                # shutil.copy(item[1], f"{g.tmpdir}/tossed")
                fcount +=1
        else:
            print(Fore.GREEN + f"Keep Filtered: {item[1]} to {g.tmpdir}/filtered" + Fore.RESET)
            cmd = f"cp {item[1]} {g.tmpdir}/filtered"
            prun(cmd, debug=debug)
            # shutil.copy(item[1], f"{g.tmpdir}/filtered")
        i+=1

if filter != False:
    for item in rsAry:
        # print(item)
        if item[3] < filter:
            if os.path.exists(item[1]):
                shutil.copy(item[1], f"{g.tmpdir}/tossed")
                print(Fore.RED+f"Delta Tossed: {item[1]}"+Fore.RESET)
                fcount +=1
        else:
            print(Fore.GREEN + f"Delta Filtered: {item[1]}" + Fore.RESET)
            shutil.copy(item[1], f"{g.tmpdir}/filtered")

filteredCt = len(glob.glob(f"{g.tmpdir}/filtered/*"))
tossedCt = len(glob.glob(f"{g.tmpdir}/tossed/*"))
orgCt = len(rsAry)

print(f"Original: {orgCt} "+Fore.GREEN+f"Remaining: {filteredCt}, "+Fore.RED+f", Pct Removed: {tossedCt/(filteredCt+tossedCt)*100:.2f}%")

if fspec != "dir":
    stichedVid = runStitch(f"{g.tmpdir}/filtered", debug=True, ext="png")
    print(f"Output: {stichedVid}")
