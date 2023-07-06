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
init()

init()

timestamp = round(time.time())

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -Q, --sequence      xxx
    -f, --x             xxx
'''
    # print(rs)
    # exit()



locationpath = "/home/jw/src/sdc/test.mp4"
dirname = os.getcwd()
basename = False
keyname = "duration"
verbose = False
srcfile = False
sequence = False
testonly = False
# pprint(sys.argv)
# exit()

print("args:",len(sys.argv))
if len(sys.argv) == 0:
    showhelp()

#^ if there is only one argument with no flags, then assume it is a filename
if len(sys.argv) <3:
    print("1args")
    pprint(sys.argv)
    filename =  sys.argv[1]
    basename = os.path.basename(locationpath)
    dirname = os.path.dirname(locationpath)

    fspec = False
else:
    print("multiargs")
    pprint(sys.argv)
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hvtQ:y:", [
            "help",
            "verbose",
            "testonly",
            "sequence=",
            "xxx=",
            "yyy=",

        ])
    except Exception as e:
        print(str(e))

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            showhelp();
        if opt in ("-v", "--verbose"):
            verbose = True;
        if opt in ("-t", "--testonly"):
            testonly = True;
        if opt in ("-Q", "--sequence"):
            sequence = arg
            print(sequence)
        if opt in ("-y", "--yyy"):
            interx = int(arg)


basename = os.path.basename(filename)
dirname = os.path.dirname(filename)
if not dirname:
    dirname = os.getcwd()
fspec = False



print(f"dirname: {dirname}")
print(f"basename: {basename}")
print(f"srcfile:{srcfile}")
print(f"fspec:{fspec}")

#^ order is important
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
    dirname = os.getcwd()
    fspec = "rel"
else:
    print(f"Bad path argument or '{dirname}/{basename}' does not exist")
    exit()

srcfile = f"{dirname}/{basename}"

print(f"dirname: {dirname}")
print(f"basename: {basename}")
print(f"srcfile:{srcfile}")
print(f"fspec:{fspec}")

id = getID(filename)

# for sq in sequence:
#     if sq == 'a':
#         print("Running process 'a'")
#     if sq == 'b':
#         print("Running process 'b'")
#     if sq == 'c':
#         print("Running process 'c'")
#     print(sq)
