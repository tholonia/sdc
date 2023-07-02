#!/bin/env python

import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
import ffmpeg
import subprocess
import shutil
from proclib import prun, splitnonalpha, getID, procTime, getFilesize, getFnames, cleanTree, cleanWildcard
import time
import procvars as g
import glob

init()

def cleanAll(d):
    nfiles = len(glob.glob(f"{d}/**/*", recursive=True))
    print(f"Cleaning {nfiles} file from {d}")
    cleanTree(d)
def cleanWild(d):
    nfiles = len(glob.glob(f"{d}/*"))
    print(f"Cleaning {nfiles} file from {d}")
    cleanTree(d)
def cleanTrash():
    d = '/home/jw/.local/share/Trash/**/*'
    files = glob.glob(d, recursive=True)
    nfiles = len(files)
    # pprint(files)
    print(f"Cleaning {nfiles} file from {d}")
    for f in files:
        cmd = f"rm -rf {f}"
        # print(cmd)
        os.system(cmd)
    d = '/run/user/1000/kio-fuse-jnwddn/trash/**/*'
    files = glob.glob(d, recursive=True)
    nfiles = len(files)
    # pprint(files)
    print(f"Cleaning {nfiles} file from {d}")
    for f in files:
        cmd = f"rm -rf {f}"
        # print(cmd)
        os.system(cmd)




cleanAll(f"{g.rifedir}/frames")
cleanAll(f"{g.esgrandir}/results")
cleanWild("/tmp/*.mp4")
cleanWild("/tmp/images")
cleanWild("/tmp/frames")
cleanWild("/home/jw/src/Real-ESRGAN/results")
cleanTrash()

