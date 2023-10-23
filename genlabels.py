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
from tempfile import mktemp

sys.path.append("/home/jw/src/sdc/settings/preprocs")
import preprocessors as pre
import contextlib
init()

def showhelp():
    print("help")
    rs = f"""
    -h, --help          Help  
    -m, --mode          "6x1","6x3","8x4"
    -o --output        save output to filename
"""
    print(rs)
    exit()


basedir = os.getcwd()

project = os.getcwd().split("/")[-1]
mode = "6x1"
Xg = 6
Yg = 1
gs = Xg*Yg
output_fn = "RUN"
confirm = True
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hm:so:",
        [
            "help",
            "mode=",
            "skipconfirm",
        ],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-m", "--mode"):
        mode = arg
        Xg=int(arg.split("x")[0])
        Yg=int(arg.split("x")[1])
        gs = Xg*Yg
    if opt in ("-s", "--skipconfirm"):
        confirm = False
    if opt in ("-o", "--output"):
        output = arg

if confirm:
    input(
        "#Make sure you are in the directory that holds the output directories of Deforum"
    )

print(Fore.CYAN + f"basedir:" + Fore.WHITE + basedir + Fore.RESET, file=sys.stderr)
print(Fore.CYAN + f"name:" + Fore.WHITE + project + Fore.RESET, file=sys.stderr)
print(Fore.CYAN + f"mode:" + Fore.WHITE + mode + Fore.RESET, file=sys.stderr)


# [ SET DIRECTORIES
os.chdir(basedir)


# [ load json of base settings
settings_fn = "INPUT_VIDEO.json"
settings_fp = open(settings_fn, "r")
settings_dict = json.load(settings_fp)

# prp_list = [line.rstrip() for line in open(prp_list_fn)]
prp_cleaned = pre.prp_list["ALL"][:gs]
# print(gs)
# pprint(prp_cleaned)
# exit()

fontsize = 20
b_list = []
l_list = []

output_fh = open(output_fn,"w")
for prp in prp_cleaned:
    tmpfile = f"{mktemp()}.mp4"
    settings_dict["cn_1_module"] = prp
    settings_dict["batch_name"] = prp
    config_data = json.dumps(settings_dict, indent=4)

    if prp == "INPUT_VIDEO":
        color = "red"
        project_name = project
    elif prp == "ORG_VIDEO":
        color = "violet"
        project_name = None
    else:
        color = "black"
        project_name = project

    label = f'magick -background darkgray -fill black -pointsize 25 -gravity center  -font Carlito-Regular -size 512x25  label:"{project_name}/{prp}"   /tmp/label.png; \n'
    label += f'ffmpeg  -y -loglevel warning -i {prp}/x_1_FILM_x6.mp4 -i /tmp/label.png -filter_complex "[0:v][1:v] overlay=0:0" -pix_fmt yuv420p -c:a copy {tmpfile}; \n'
    label += f"mv {tmpfile} {prp}.mp4; \n"
    label += f'echo "----[LABEL] {project_name}/{prp}-------------------------------------"\n'

    border = f"ffmpeg -y -loglevel warning -i {prp}.mp4 -vf drawbox=x=0:y=0:w=in_w:h=512:color={color} {tmpfile}; mv {tmpfile} {prp}.mp4\n"
    border += f'echo "----[BORDER] {project_name}/{prp} -------------------------------------"\n'

    l_list.append(label)
    b_list.append(border)
for l in l_list:
    output_fh.write(l)
    output_fh.write("\n")
for b in b_list:
    output_fh.write(b)

output_fh.close()