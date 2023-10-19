#!/bin/env python

import json
import os
import proclib as p
from pprint import pprint
import getopt
import glob
from colorama import init, Fore

output_path = "/home/jw/src/sdc/settings/preprocs/canny"

# [ load list or preprocessor
basedir = "/home/jw/src/sdc/settings/preprocs"
os.chdir(basedir)
prp_list_fn = "pres_alpha.txt"

# [ load jsoin of base settings
settings_fn = "base_settings.json"
settings_fp = open(settings_fn, "r")
model = "canny"

# [ load preprocessors into list
prp_list = [line.rstrip() for line in open(prp_list_fn)]
sorted(prp_list)

# [ load settings file into dict
settings_dict = json.load(settings_fp)

init()


def showhelp():
    print("help")
    rs = f"""
    -s, --script        Create LABEL.sh script (def: True)
    -g, --gen           Regenerate xfg files (def: True)
    -p, --pregened      Process only files that have already been generated (def: False)
    -h, --help          Help
    
    {__file__}  => Generate .xfg files and LABEL.sh script for all UNprocessed files
    
    {__file__} -g  => Generate .xfg files only for all UNprocessed files
    {__file__} -s  => Generate LABEL.sh only for all UNprocessed files

    {__file__} -p  => Generate .xfg files and LABEL.sh script for all processed files
    {__file__} -sp  => Generate LABEL.sh only for all processed files
    {__file__} -gp  => Generate .xfg files only for all processed files
    
"""
    print(rs)
    exit()


import sys
from pprint import pprint
from colorama import init, Fore
import proclib as p

init()

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hsgp",
        [
            "help",
            "script",
            "gen",
            "pregened",
        ],
    )
except Exception as e:
    print(str(e))

do_gen = True
do_script = True
pregened = False

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-s", "--script"):
        do_script = False
    if opt in ("-g", "--gen"):
        do_gen = False
    if opt in ("-p", "--pregened"):
        pregened = True

if not do_gen:
    # [ wipe existing xfg files
    for f in sorted(glob.glob("*.xfg")):
        print(Fore.RED + f">>> Deleting {f}" + Fore.RESET, file=sys.stderr)
        os.unlink(f)


prp_list = [line.rstrip() for line in open(prp_list_fn)]
prp_cleaned = []
comment="#"
for line in prp_list:
    if line[0] != "#":  # skip comments
        if pregened == True:
            if line[0] == ">":
                prp_cleaned.append(line[1:])
        else:
            if line[0] != ">":
                line = line.split(comment,1)[0]
                prp_cleaned.append(line)

# pprint(prp_cleaned)
# exit()
fontsize = 20

for prp in prp_cleaned:
    settings_dict["cn_1_module"] = prp
    settings_dict["batch_name"] = prp
    config_data = json.dumps(settings_dict, indent=4)
    if not do_gen:
        with open(f"{prp}_settings.xfg", "w") as outfile:
            outfile.write(config_data)
        print(
            Fore.GREEN + f">>> Wrote {prp}_settings.xfg" + Fore.RESET,
            file=sys.stderr,
        )
    label = f"#LABEL {prp}\nffmpeg -y -loglevel warning -i {output_path}/{prp}/1_FILM_x6.mp4 -vf \"drawtext=fontfile=/usr/share/fonts/noto/NotoSerif-Black.ttf:text='canny/{prp}':fontcolor=white:fontsize={fontsize}:box=1:boxcolor=black@1.0:boxborderw=5:x=(w-text_w)/2:y=(text_h)\" -codec:a copy {output_path}/{prp}.mp4"
    border = f"#BORDER {prp}\nffmpeg  -y -loglevel warning -i {output_path}/{prp}.mp4 -filter_complex \"[0]pad=w=10+iw:h=10+ih:x=5:y=5:color=black\" /tmp/X.mp4; mv /tmp/X.mp4 {output_path}/{prp}.mp4;"

    if not do_script:
        print(label)
        print(border)
        print("#-----------------------------------------------------------------------\n")
        # p.prun(cmd, debug=debug)
