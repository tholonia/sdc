#!/bin/env python
import os
import sys
import getopt
import json
import subprocess
from pprint import pprint
from colorama import init, Fore
import urllib.parse
init()

def errprint(str):
    print(str, file=sys.stderr)
def prun(cmd):
    scmd = cmd.split()
    process = subprocess.Popen(scmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        errprint(stderr)
        raise RuntimeError(stderr)
def showhelp():
    errprint("help")
    rs = '''
    -h, --help          show help
    -a, --add           add file
    -v, --video         video file
    -A, --auto         automatically add settings based on ID
'''
    errprint(rs)
    exit()

addfile = False
video = False
dir = ""
auto = False
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "ha:xv:A", [
        "help",
        "add=",
        "video=",
        "auto",
    ])
except Exception as e:
    errprint(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-a", "--add"):
        addfile = arg
        if not os.path.exists(addfile):
            errprint(f"Oops... no setting file exists. Aborting")
            exit()
    if opt in ("-A", "--auto"):
        auto = True
    if opt in ("-v", "--video"):
        if os.path.isabs(arg):
            video = os.path.basename(arg)
            dir = os.path.dirname(arg)
        elif os.path.isfile(arg):
            video = arg
            dir = "."
            if not os.path.exists(f"{dir}/{video}"):
                errprint(f"Missing: {dir}/{video} check the path")
                exit()
        else:
            os.path.isdir(arg)
            dir = arg
            video = False
            errprint("You entered directory only")
            exit()

if auto:
    id = video.split(".")[0]
    addfile = f"{dir}/{id}_settings.txt"
    if not os.path.exists(addfile):
        errprint(f"Oops... no setting file exists. Aborting")
        exit()
    else:
        errprint(f"Automatically adding {addfile}")

if addfile:
    with open(addfile, 'r') as file:
        data = file.read()
    data = urllib.parse.quote(data)# data.replace("\n","xEOLx")
    # print(data)
    # exit()
    # cdata = data.encode('ascii')
    # b64data = str(base64.b64encode(cdata))

    # cmd = f"ffmpeg -y -i {video} -metadata config_file='{b64data}' -map 0 -c copy out.mp4"
    cmd = f"ffmpeg -y -i {dir}/{video} -movflags use_metadata_tags -metadata configFile='{data}' /tmp/out.mp4"
    prun(cmd)

    cmd = f"cp {dir}/{video} /tmp/{video}.BAK"
    prun(cmd)
    errprint(f"back in /tmp/{video}.BAK")

    cmd = f"mv /tmp/out.mp4 {dir}/{video}"
    prun(cmd)
    errprint("Data Encoded")
else:
    try:
        cmd = f"mediainfo --OUTPUT=JSON  {dir}/{video} > /tmp/media.json"
        errprint(cmd)
        os.system(cmd)
    except Exception as e:
        errprint(str(e))
        errprint(f"Can't get mediainfo for {dir}/{video}")
        exit()

    try:
        f = open("/tmp/media.json")
        mediainfo = json.load(f)
        configData = mediainfo['media']['track'][0]['extra']['configFile']
        asciidata = urllib.parse.unquote(configData)
        asciidata = asciidata.rstrip("'")
        asciidata = asciidata.lstrip("'")
        dataObj = json.loads(asciidata)
        print(json.dumps(dataObj, indent=4))
    except Exception as e:
        errprint(str(e))
        errprint(f"Setting metadata appears to not exist in {dir}/{video}")
        exit()