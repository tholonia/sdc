#!/bin/env python
import os
import sys
import getopt
import json
import subprocess
from pprint import pprint
from colorama import init, Fore
import urllib.parse
import glob
from proclib import prun
import zlib
import snappy
import codecs
import base64
from base64 import b64encode, b64decode
import traceback
import re
init()

def getId(filename):
    fnum = []
    #^ get any 14 char string pefore a perios
    fnum = re.findall("[\_\-\.]*([\d]{14})[\_\-\.]*",filename,re.DOTALL)
    id = fnum[0]
    return id

def errprint(str):
    print(str, file=sys.stderr)

def dumpdata(file):
    try:
        cmd = f"mediainfo --OUTPUT=JSON  {file} > /tmp/media.json"  # ^ save video metadata
        os.system(cmd)
    except Exception as e:
        errprint(str(e))
        errprint(f"Can't get mediainfo for {dir}/{video}")
        exit()


def showhelp():
    errprint("help")
    rs = '''
    -h, --help          show help
    -a, --add           add file
    -v, --video         video file
    -A, --auto          automatically add settings based on ID
    -c, --check         check ALL mp4 files in CURRENT directory
'''
    errprint(rs)
    exit()

settings_file = False
video = False
dir = ""
auto = False
check = False

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "ha:xv:Ac", [
        "help",
        "add=",
        "video=",
        "auto",
        "check",
    ])
except Exception as e:
    errprint(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-c", "--check"):
        check = True
    if opt in ("-a", "--add"):
        settings_file = arg
        if not os.path.exists(settings_file):
            errprint(f"Oops... no setting file named {settings_file} exists. Aborting")
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
    # id = video.split(".")[0]
    id = getId(video)
    settings_file = f"{dir}/{id}_settings.txt"
    if not os.path.exists(settings_file):
        errprint(f"Oops... no setting file named {settings_file} exists. Metadata untouched.")
        exit()
    else:
        errprint(f"Automatically adding {settings_file}")

def getdata(file):
    # print(file)
    #^ create the initial mediainfo file, which may or may not have configFile info in it
    dumpdata(file)
    try:
        f = open("/tmp/media.json","rb") #^ read binary
        mediainfo = f.read()
        mediainfo = mediainfo.decode("UTF-8")
        media_json =  json.loads(mediainfo) # ^ load into JSON object
        # ^ get the specific 'configFile' field, which is base64 encoded
        b64_configField = media_json['media']['track'][0]['extra']['configFile'][3:-2]
        b64_configField += (4 - (len(b64_configField) % 4)) * '='
        zipped_configField=base64.urlsafe_b64decode(b64_configField)
        ascii_configField =  snappy.decompress(zipped_configField).decode('UTF-8')
        #^ test it
        dataObj = json.loads(ascii_configField)
        out_json = json.dumps(dataObj,indent=4)
        # errprint(Fore.MAGENTA)
        # pprint(out_json)
        # errprint(Fore.RESET)
        return dataObj
    except Exception as e:
        return False
        # traceback.print_exc()
#! ADDING A SETTINGS FILE
if settings_file:
    #^ load the JSON settings files
    with open(settings_file, 'r') as file:
        setting_data = file.read()
    #^ compress the data
    snappy_data = snappy.compress(setting_data)
    #^ base64 encode it
    udata = base64.urlsafe_b64encode(snappy_data)
    #^ add the compressed data to the video
    cmd = f"ffmpeg -y -i {dir}/{video} -movflags use_metadata_tags -metadata configFile='{udata}' /tmp/out.mp4"
    prun(cmd, debug=False)

    cmd = f"cp {dir}/{video} /tmp/{video}.BAK"
    prun(cmd)
    errprint(f"back in /tmp/{video}.BAK")

    cmd = f"mv /tmp/out.mp4 {dir}/{video}"
    prun(cmd)
    errprint("Data Encoded")
#! NO SETTINSG FILE, SO ONLY VALIDATING
else:
    if not check:
        dataObj = getdata(f"{dir}/{video}")
        if dataObj:
            # print(1,dataObj)
            out_json = json.dumps(dataObj, indent=4)
            errprint(Fore.GREEN)
            print(out_json)
            errprint(Fore.RESET)
        else:
            errprint(
                Fore.RED + f"Setting metadata appears to not exist in " + Fore.YELLOW + f"{os.getcwd()}/{video}" + Fore.RESET)
            # msg = f"EMPTY: Run 'metaconfig.py -v {video} -a <settings file>"
            # errprint(Fore.RED+msg+Fore.RESET)

if check:
    files = glob.glob("*.mp4")
    for f in files:
        dataObj = getdata(f)
        if dataObj:
            i=1
        else:
            id = f.split(".")[0]
            batcmd = f"locate {id}_settings.txt"
            # errprint(batcmd)
            # exit()
            try:
                result = subprocess.check_output(batcmd, shell=True).decode('UTF-8')
                msg = f"metaconfig.py -v {f} -a {result}"
                errprint(Fore.MAGENTA + msg + Fore.RESET)
            except:
                errprint(Fore.RED + f"{f} has no settings file available" + Fore.RESET)
                # traceback.print_exc()



