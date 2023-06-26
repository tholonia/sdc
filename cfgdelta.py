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

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -f, --config        filename
    -c, --compare       compare against filename
    -s, --short         truncate long data
'''
    print(rs)
    exit()
orgcfgfile = "/home/jw/src/sdc/sdw/deforum_settings.txt.ORG"
cfgfile = "/home/jw/src/sdc/sdw/x3"
dir = "."
short = -1

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hf:c:s", [
        "help",
        "compare=",
        "config=",
        "short",
    ])
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-s", "--short"):
        short = 80
    if opt in ("-f", "--config"):
        if os.path.isabs(arg):
            cfgfile = os.path.basename(arg)
            dir = os.path.dirname(arg)
        elif os.path.isfile(arg):
            cfgfile = arg
            dir = "."
            if not os.path.exists(f"{dir}/{cfgfile}"):
                print(f"Missing: {dir}/{cfgfile} check the path")
                exit()
        else:
            os.path.isdir(arg)
            dir = arg
            cfgfile = False
            print("You entered directory only")
            exit()
    if opt in ("-c", "--compare"):
        if os.path.isabs(arg):
            orgcfgfile = os.path.basename(arg)
            orgdir = os.path.dirname(arg)
        elif os.path.isfile(arg):
            orgcfgfile = arg
            orgdir = "."
            if not os.path.exists(f"{orgdir}/{orgcfgfile}"):
                print(f"Missing: {orgdir}/{orgcfgfile} check the path")
                exit()
        else:
            os.path.isdir(arg)
            orgdir = arg
            orgcfgfile = False
            print("You entered directory only")
            exit()

f = open(cfgfile, 'r')
newdata = json.load(f)
f = open(orgcfgfile, 'r')
orgdata = json.load(f)
print(Fore.RED,end="")
print("┌──────────────────────────────────────────────")
print("│\t",cfgfile,f"(New file -> {cfgfile})")
print("└──────────────────────────────────────────────")
print(Fore.YELLOW,end="")
print("┌──────────────────────────────────────────────")
print("│\t",orgcfgfile,f"(Org file -> {orgcfgfile})")
print("└──────────────────────────────────────────────")
print(Fore.RESET)
for item in orgdata:
    if orgdata[item] != newdata[item]:
        orgitem = str(orgdata[item])[:short]
        newitem = str(newdata[item])[:short]
        print(f"[{item}]")
        print(f"\t",Fore.RED,orgitem)
        print(f"\t",Fore.YELLOW,newitem,Fore.RESET)
