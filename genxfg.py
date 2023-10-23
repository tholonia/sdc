#!/bin/python

import json
import getopt
import os
import proclib as p
from pprint import pprint
import getopt
import glob
from colorama import init, Fore
import sys

sys.path.append("/home/jw/src/sdc/settings/preprocs")
import preprocessors as pre

init()


def showhelp():
    print("help")
    rs = f"""
    -h, --help          Help
    -m, --mode          ex: 6x1
    -S, --skipconfirm
    
    {__file__}  => Generate .xfg files
    
"""
    print(rs)
    exit()


basedir = os.getcwd()
mode = "6x1"
confirm = True
X = 6
Y = 1

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hm:S",
        ["help", "mode=", "skipconfirm"],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-m", "--mode"):
        mode = arg
        X = int(arg.split("x")[0])
        Y = int(arg.split("x")[1])
    if opt in ("-S", "--skipconfirm"):
        confirm = False

if confirm:
    input(
        "#Make sure you are in the directory that holds the output directories of Deforum"
    )


project_name = os.getcwd().split("/")[-1]  #! use folder name
print(Fore.CYAN + f"basedir:" + Fore.WHITE + basedir + Fore.RESET, file=sys.stderr)
print(Fore.CYAN + f"name:" + Fore.WHITE + project_name + Fore.RESET, file=sys.stderr)
print(Fore.CYAN + f"mode:" + Fore.WHITE + mode + Fore.RESET, file=sys.stderr)


# [ wipe existing xfg files
for f in sorted(glob.glob("*.xfg")):
    print(Fore.RED + f">>> Deleting {f}" + Fore.RESET, file=sys.stderr)
    os.unlink(f)


# [ load json of base settings
settings_fn = "INPUT_VIDEO.json"
settings_fp = open(settings_fn, "r")
settings_dict = json.load(settings_fp)

prp_cleaned = pre.prp_list["ALL"]
prp_cleaned = prp_cleaned[:X*Y]
fontsize = 20

for prp in prp_cleaned:
    settings_dict["cn_1_enabled"] = True
    settings_dict["cn_1_module"] = prp
    settings_dict["batch_name"] = prp
    config_data = json.dumps(settings_dict, indent=4)

    with open(f"{prp}_settings.xfg", "w") as outfile:
        outfile.write(config_data)
    print(
        Fore.GREEN + f">>> Wrote {prp}.xfg" + Fore.RESET,
        file=sys.stderr,
    )
