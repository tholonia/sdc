#!/bin/env python

import os,sys,glob,getopt
from colorama import init, Fore, Back
from pprint import pprint
import ffmpeg
import subprocess
init()

def errprint(str):
    print(str, file=sys.stderr)

def prun(cmd,track):
    print(f"({track})"+Fore.YELLOW+cmd+Fore.RESET)
    scmd = cmd.split()
    process = subprocess.Popen(scmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stderr)
        raise RuntimeError(stderr)
def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -v, --videofile     filename
    -k, --key           only 'all' supported, default is 'duration'
'''
    print(rs)
    exit()
filename = "/home/jw/src/sdc/zzzzz.mp4"
keyname = "duration"
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hv:k:", [
        "help",
        "videofile=",
        "key=",
    ])
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp();
    if opt in ("-v", "--videofile"):
        filename = arg
    if opt in ("-k", "--key"):
        keyname = arg

# errprint(f"viduration: filename: {filename}")
probe = ffmpeg.probe(filename)
video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
if keyname == "all":
    pprint(video_streams[0])
    exit()
else:
    dur_sec = video_streams[0]['duration']
    print(int(round(float(dur_sec))), dur_sec, filename)

