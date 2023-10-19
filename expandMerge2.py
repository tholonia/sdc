#!/bin/env python

import os
import sys
import getopt
import glob
import proclib as p
import shutil as sh
import time


#! --------------------------------------------------------------------------
def showhelp():
    print("help")
    rs = """
    -h, --help                  help
    -c, --clean                 default = False : wipe all 
    -d, --dir    <dir>          default = cwd 
    -D, --dryrun <print|on|off> default = off
"""
    print(rs)
    exit()


DRYRUN = False  # "print"
CLEAN = False
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hd:D:c",
        [
            "help",
            "dir=",
            "dryrun=",
            "clean"
        ],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-c", "--clean"):
        CLEAN = True
    if opt in ("-d", "--dir"):
        dir = arg
    if opt in ("-D", "--drydun"):
        if arg == "on":
            DRYRUN = True
        if arg == "off":
            DRYRUN = False
        if arg == "print":
            DRYRUN = "print"


#! clean all existing MP4s
#! --------------------------------------------------------------------------
if CLEAN:
    files = glob.glob("*.mp4", recursive=False)
    for f in files:
        os.unlink(f)


#! get subvars based on filename
#! --------------------------------------------------------------------------
dir = os.getcwd()
dirparts = dir.split("/")
s_label = dirparts[len(dirparts) - 1]


print(f"# Using directory [{dir}]\n")


#! copy all the videos to the home dir
#! --------------------------------------------------------------------------
files = glob.glob("**/*mp4", recursive=True)
fcount = len(files)
fcounter = 1
for f in files:
    if f.find("30fps") == -1:
        t_label = f.split("/")[0]
        newname = f"{t_label}"
        cmd = f"cp {f} ./{newname}.mp4"
        p.prun(cmd, debug=True, dryrun=DRYRUN)

        cmd = f"ffmpeg -loglevel warning -y -i {newname}.mp4 -crf 10 -vf minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1  {newname}_30fps.mp4"
        p.prun(cmd, debug=True, dryrun=DRYRUN)

        #! then label them
        cmd = f"vidlabel.py -f {dir}/{newname}_30fps.mp4 -l {newname}"
        p.prun(cmd, debug=True, dryrun=DRYRUN)
        print("\n")

#! mergse these files
#! --------------------------------------------------------------------------
time.sleep(5)
cmd = f"mergevid_512x512.py -f {dir}/*30fps.mp4"
p.prun(cmd, debug=True, dryrun=DRYRUN)

#! mv merged file to current dir
#! --------------------------------------------------------------------------
cmd = f"mv /tmp/merged.mp4 ./Mx_{dirparts[-1]}.mp4"
p.prun(cmd, debug=True, dryrun=DRYRUN)

print("\n")
