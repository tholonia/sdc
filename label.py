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
init()


def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -f, --file          video
    -l, --label         label
'''
    print(rs)


filename = False
filepath = "./"
label = False
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hf:l:", [
        "help",
        "file=",
        "label=",
    ])
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
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
    print(cmd)
    # exit()
    prun(cmd)


def prun(cmd):
    cmd = fr'{cmd}'
    print("["+cmd+"]")
    scmd = cmd.split()
    # pprint(scmd)
    process = subprocess.Popen(scmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stderr)
        raise RuntimeError(stderr)

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



starttime = time.time()

print(f"{filepath}/{filename}")

print(f"Probing: {filepath}/{filename}")
probe = ffmpeg.probe(f"{filepath}/{filename}")
video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]

fontsize = int(video_streams[0]['coded_width']/15)

print(Fore.CYAN+f"modifying files..."+Fore.RESET)
modify(filepath,filename,label,fontsize)
update()

endtime = time.time()

print(Fore.RED+f"TIME: {endtime-starttime}"+Fore.RESET)

# cleanpost()

