#!/bin/env python

import os
import sys
import glob
import getopt
import subprocess
import time
from pprint import pprint
from colorama import init, Fore
import ffmpeg
import proclib as p
init()


def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -d, --debug         debug
    -f, --file          video
    -l, --label         label
'''
    print(rs)


filename = False
filepath = "./"
label = False
debug= False

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hdf:l:", [
        "help",
        "debug",
        "file=",
        "label=",
    ])
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-d", "--debug"):
        debug = True
    if opt in ("-f", "--file"):
        filepath,filename = os.path.split(arg)
        # print(filepath,filename)
    if opt in ("-l", "--label"):
        label = arg
def clean():
    if os.path.exists(f"/tmp/splits"):
        os.system("rm -rf /tmp/splits")
        os.system("mkdir  /tmp/splits")
def modify(filepath,filename,label,fontsize):
    # label = label.replace("_", " ")
    if filepath == "":
        filepath = "."
    # cmd = f"ffmpeg -loglevel info   -y -i {filepath}/{filename}  -vf drawtext=fontfile=/usr/share/fonts/noto/NotoSerif-Black.ttf:text={label}:fontcolor=white:fontsize={fontsize}:box=1:boxcolor=black@1.0:boxborderw=5:x=(w-text_w)/2:y=(h-text_h) -codec:a copy /tmp/outlabel.mp4"
    cmd = f"ffmpeg -loglevel info   -y -i {filepath}/{filename}  -vf drawtext=fontfile=/usr/share/fonts/noto/NotoSerif-Black.ttf:text={label}:fontcolor=white:fontsize={fontsize}:box=1:boxcolor=black@1.0:boxborderw=5:x=(w-text_w)/2:y=(text_h) -codec:a copy /tmp/outlabel.mp4"
    p.prun(cmd,debug=debug)
def update():
    cmd = f"mv {filepath}/{filename} /tmp/{filename}.BAK"
    os.system(cmd)
    cmd = f"mv /tmp/outlabel.mp4 {filepath}/{filename}"
    os.system(cmd)
    print(Fore.YELLOW+f"FINISHED: {filename}"+Fore.RESET)

if not filename:
    print("Missing filename")
    exit()
if not label:
    print("Missing label")
    exit()

print(f"Probing: {filepath}/{filename}")
probe = ffmpeg.probe(f"{filepath}/{filename}")
video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
fontsize = int(video_streams[0]['coded_width']/15)
# print(Fore.CYAN+f"modifying files..."+Fore.RESET)
modify(filepath,filename,label,fontsize)
update()
