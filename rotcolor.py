#!/bin/env python
import getopt,sys
import os
from pprint import pprint
import glob
from colorama import init, Fore, Back
import proclib as p
import procvars as g
from PIL import Image, ImagePalette
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import shutil
import random
init()


#^ define selection arrays

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -i, --id          ID number
    -d, --dir     directory
    -s  --settingsfile
    -t  --tmpdir
'''
    print(rs)
    exit()

#[ MAIN ]




id = False
srcfile_dir = False
imgdir = f"{g.tmpdir}/images"

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hi:d:i:", [
        "help",
        "id=",
        "dir=",
        "imgdir=",
    ])
except Exception as e:
    print(str(e))
for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-i", "--id"):
        id = arg
    if opt in ("-d", "--dir"):
        srcfile_dir = arg
    if opt in ("-i", "--imgdir"):
        imgdir = arg

roldir = f"{imgdir}/rolled"

try: p.cleanWildcard(roldir+"/*")
except: pass
try:os.mkdir(roldir)
except: pass


print(f"Getting all files in {imgdir}/*.png")
gfiles = glob.glob(f"{imgdir}/*.png") #^ get the list of files, full path name
gfiles.sort()
ci = 100

for gfile in gfiles:
    basename = os.path.basename(gfile)
    img = Image.open(gfile)
    # img = img.convert('RGB')
    # pixels = img.load()
    delta = 1
    for i in range(img.size[0]): # For each pixel:
        for j in range(img.size[1]):
            cdelta = delta * i
            thisrgb = img.getpixel((i,j))
            r= p.cycle_in_range(thisrgb[0]+i+int(j/1),0,255)
            g= p.cycle_in_range(thisrgb[1]+int(j/2),0,255)
            b= p.cycle_in_range(thisrgb[2]+int(j/3),0,255)


            grey = 0.299 * r + 0.587 * g + 0.114 * b


            # print(thisrgb)
            # pixels[i,j] = (100,200,70)
            img.putpixel( (i,j),  (r,g,b) )
    img.save(f"{roldir}/{basename}")
    img.close()
    print(f"\trolled: {roldir}/{basename}",end="\r")
    # ci +=1

#^ now move the rolled files back to images for further processijng
gfiles = glob.glob(f"{roldir}/*.png") #^ get the list of files, full path name
gfiles.sort()
i=0
for gfile in gfiles:
    basename = os.path.basename(gfile)
    shutil.copy(gfile, f"{imgdir}")
