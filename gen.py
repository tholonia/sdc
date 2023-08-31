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

init()

timestamp = round(time.time())

def showhelp():
    print("help")
    rs = '''
    -h, --help          help
    -f, --from          from settinsg file
    -t, --to            to settings file
    -s, --subject       <subject>:<count><mult>:<step> ex: cells:6:6:6

    ./gen.py -f last -t new -s cells:6:6:6 -M


'''
    print(rs)
    exit()



locationpath = os.getcwd()
dirname = os.getcwd()
basename = False
verbose = False
srcfile = False


fromfile = "sdw/last"
tofile = "sdw/new"
subject = False
count = 6
mult = 6
step = 6
runmod = False

if len(sys.argv) == 1:
    showhelp()


argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hf:t:s:M", [
        "help",
        "from=",
        "to=",
        "subject=",
        "runmod",


    ])
except Exception as e:
    p.errprint(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-f", "--fromfile"):
        fromfile = f"sdw/{arg}"
    if opt in ("-t", "--tofile"):
        tofile = f"sdw/{arg}"
    if opt in ("-s", "--subject"):
        pts = arg.split(":")
        subject = pts[0]
        count = pts[1]
        mult = pts[2]
        steps = pts[3]
    if opt in ("-M", "--runmod"):
        runmod = True


cmd = f"genpair.py  --type {subject}  --count {count} --mult {mult} --steps {steps} -f {fromfile}  -s prompts > {tofile}"
print(cmd)
os.system(cmd)
time.sleep(2)
if runmod == True:
    cmd = f"genmod.py -f ${tofile} > {tofile}2"
    print(cmd)
    os.system(cmd)

print("Loaded from "+Fore.YELLOW+fromfile+Fore.RESET)
print("Saved to "+Fore.GREEN+tofile+Fore.RESET)
if runmod == True:
    print("Mode file as "+Fore.RED+f"{tofile}2"+Fore.RESET)

