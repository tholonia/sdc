#!/bin/env python

import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
import ffmpeg
import subprocess
import shutil
from proclib import prun, splitnonalpha, getID, procTime, getFilesize
import time
from colorama import Fore, init
import proclib as p
import procvars as g

init()

timestamp = round(time.time())

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -a, --adjust        gamma, contrast, brightness, saturation ex: "1.2:::"      
    -f, --file          filename      
                        
'''
    print(rs)
    exit()



locationpath = os.getcwd()
dirname = os.getcwd()
basename = False
verbose = False
srcfile = False
testonly = False

adj_gamma = 1.2
adj_brightness = 0.1
adj_saturation=1.2
adj_contrast=1.2


if len(sys.argv) == 0:
    showhelp()

#^ if there is only one argument with no flags, then assume it is a filename
pprint(sys.argv)
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hf:a:g:b:c:s:", [
        "help",
        "filename=",
        "adjust=",
        "gamma=",
        "brightness=",
        "saturation=",
        "contrast=",

    ])
except Exception as e:
    p.errprint(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp();
    if opt in ("-f", "--filename"):
        locationpath = arg;
    if opt in ("-g", "--gamma"):
        adj_gamma = float(arg)
    if opt in ("-b", "--brightness"):
        adj_brightness = float(arg)
    if opt in ("-s", "--saturation"):
        adj_saturation = float(arg)
    if opt in ("-c", "--contrast"):
        adj_contrast = float(arg)

basename,dirname,fspec,srcfile = p.getFnames(locationpath)

srcfile = f"{dirname}/{basename}"

print(f"dirname: {dirname}")
print(f"basename: {basename}")
print(f"srcfile:{srcfile}")
print(f"fspec:{fspec}")

id = getID(basename)

destname = f"{dirname}/adj_{basename}"
destname = destname.replace(".avi",".mp4")

cmd = f"ffmpegC -y -loglevel panic -i {srcfile} -vf eq=gamma={adj_gamma}:contrast={adj_contrast}:brightness={adj_brightness}:saturation={adj_saturation} {destname}"
p.prun(cmd,debug=True)
