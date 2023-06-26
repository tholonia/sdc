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
init()

# https://karobben.github.io/2021/04/10/Python/opencv-v-sm/
def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    
    -n, --new         data store
    -f, --filter      filter all below this (0.0 - 1.0) default 0.1
    -d, --dir      directory, defailt "."
'''
    print(rs)
    exit()

def normalize(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    normalized = [(x - minimum) / (maximum - minimum) for x in numbers]
    return normalized
def Diff_img(img0, img):
    '''
    This function is designed for calculating the difference between two
    images. The images are convert it to an grey image and be resized to reduce the unnecessary calculating.
    '''
    # Grey and resize
    img0 =  cv2.cvtColor(img0, cv2.COLOR_RGB2GRAY)
    img =  cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img0 = cv2.resize(img0, (320,200), interpolation = cv2.INTER_AREA)
    img = cv2.resize(img, (320,200), interpolation = cv2.INTER_AREA)
    # Calculate
    Result = (abs(img - img0)).sum()
    return Result


newData = False
filter = 0.1
dir = "."
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hnf:d:", [
        "help",
        "new",
        "filter=",
        "directory=",
    ])
except Exception as e:
    print(str(e))
for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-d", "--directory"):
        dir = arg
    if opt in ("-f", "--filter"):
        filter = float(arg)
    if opt in ("-n", "--new"):
        newData = True
        if os.path.exists(f"{dir}/rsAry.json"):
            os.remove(f"{dir}/rsAry.json")

#^ get list of
files = glob.glob(f"{dir}/*.png")
files = sorted(files)

#^ check for existing data file
if os.path.exists(f"{dir}/rsAry.json"):
    f = open(f"{dir}/rsAry.json")
    rsAry = json.load(f)
    print(f"Reading stored data... ({len(rsAry)} items)")

# make sure there is a directory for filtering abd backup
if not os.path.exists(f"{dir}/filtered"):
    os.makedirs(f"{dir}/filtered")
    print(f"Making dir '{dir}/filtered'")
else:
    print(f"Wiping dir '{dir}/filtered'")
    os.system(f"/bin/rm -rf {dir}/filtered")
if not os.path.exists(f"{dir}/tossed"):
    os.makedirs(f"{dir}/tossed")
    print(f"Making dir '{dir}/tossed'")
else:
    os.system(f"/bin/rm -rf {dir}/tossed")
    print(f"Wiping dir '{dir}/tossed'")

rsAry = []  # ^ array that hols filenames and diffs
nAry = []  # ^ just for diffs

for i in range(1, len(files)):
# for i in range(1, 10):
    print(i,end="\r")
    rs = Diff_img(cv2.imread(files[i - 1]), cv2.imread(files[i]))
    rs = rs * 1 #^ to convert from numpy int to python int
    rsAry.append([rs,files[i-1],files[i],0]) #^ 0 is a placeholder
    nAry.append(int(rs))

#^ create normalized diff values
nmAry = normalize(nAry)
#^ and update the array of files
for i in range(len(nmAry)):
    rsAry[i][3]=nmAry[i]

jsonFile = open(f"{dir}/rsAry.json", "w")
jsonFile.write(json.dumps(rsAry))
jsonFile.close()
print(f"Created stored data ({len(rsAry)} items)...")


#- START FILTERING

fcount = 0
gcount = 0



for item in rsAry:
    # print(item)
    if item[3] < filter:
        if os.path.exists(item[1]):
            shutil.copy(item[1], f"{dir}/tossed")
            print(Fore.RED+f"Tossed: {item[1]}"+Fore.RESET)
            fcount +=1
        else:
            print(Fore.GREY+f"Phantom : {item[1]}"+Fore.RESET)
            gcount +=1
    else:
        print(Fore.GREEN + f"Filtered: {item[1]}" + Fore.RESET)
        shutil.copy(item[1], f"{dir}/filtered")

left = glob.glob(f"{dir}/filtered/*.png")
orgCt = len(rsAry)

print(f"Original: {orgCt},Remaining: {len(left)}, Filtered: {fcount}, Total filtered: {gcount+fcount}, Pct Removed: {((gcount+fcount)/orgCt)*100:.2f}%")
