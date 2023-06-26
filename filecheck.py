#!/bin/env python
import os
from pprint import pprint
import time
import getopt, sys
from colorama import init, Fore, Back
import subprocess
import glob
import time
init()

def prun(cmd):
    print("(0)"+Fore.YELLOW+cmd+Fore.RESET)
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
    -f, -filepattern
'''
    print(rs)

filename = "/home/jw/src/sdw/outputs/img2img-images/batch3/20230620164715_Upscaled_x4.mp4"

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hf:", [
        "help",
        "filename=",
    ])
except Exception as e:
    print(str(e))
for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-f", "--filename"):
        filepattern = arg

filename = False
while not filename:
    files = glob.glob("/home/jw/src/sdw/outputs/img2img-images/batch3/*_Upscaled_x4.mp4")
    # print(files)
    if len(files) > 0:
        filename = files[0]
        print(f"Found {filename}")
        file_stats = os.stat(filename)

        fsize = 0
        mtime = 0

        while fsize != file_stats.st_size or mtime != file_stats.st_mtime:
            # print(f"checking {file_name}")
            file_stats = os.stat(filename)
            fsize = file_stats.st_size
            mtime = file_stats.st_mtime
            time.sleep(3)

        print("READY")
        prun("./MAKEAUTO /home/jw/src/sdw/outputs/img2img-images/batch3")
        prun(f"mv {filename} {filename}.BAK")
        # prun(f"/bin/rm {filename} {filename}.BAK")
        filename = False
    else:
        time.sleep(3)


