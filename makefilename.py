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

# import ffprobe
import proclib as p
import json
import re

init()


def showhelp():
    print("help")
    rs = """
    -h, --help          show help
    -d, --debug         debug
    -f, --filename     ex: /dir/name*txt
    -t --termsd         ex: cfg=>cfg_schedule:tn=>cn_2_weight
"""
    print(rs)


def xterms(termStr):
    terms = {}
    tps = str(termStr).split(":")
    for t in tps:
        ts = str(t).split("=>")
        terms[ts[0]] = ts[1]
    return terms


# filename = "*.txt"
# filepath = "./"
filename = "/home/jw/src/sdw/outputs/img2img-images/tangkMask/*.txt"
# filepath = "./"
debug = False
fontsize = 20
terms = "cfg=>cfg_scale_schedule:tn=>cn_2_weight"
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hdf:t:",
        [
            "help",
            "debug",
            "file=",
            "terms=",
        ],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-d", "--debug"):
        debug = True
    if opt in ("-t", "--terms"):
        terrms = arg
    if opt in ("-f", "--file"):
        filename = arg

# pathparts = p.split_path(filename)
# filepath, filename = os.path.split(arg)
pathparts = p.split_path(filename)
filepath = pathparts["dirname"]
filename = pathparts["basename"]

termsAry = xterms(terms)
print("filepath: ", filepath)
print("filename:", filename)
print("terms:", termsAry)

files = glob.glob(f"{filepath}/{filename}")

for file in files:
    print(file)
    with open(file, "r") as file:
        data = json.load(file)
    namestr = ""
    # print(f"{file}")

    for t in termsAry:
        val = re.findall("\(([\d+].*)\)", data[termsAry[t]])
        namestr = namestr + f"{t}={val[0]}_"

    print("\t\t", namestr.strip("_")+".txt")
