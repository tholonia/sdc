#!/bin/env python

import os, sys, getopt
import ffmpeg
from pprint import pprint
from tempfile import mktemp
import proclib as p


def showhelp():
    print("help")
    rs = f"""
    -h, --help          Help  
"""
    print(rs)
    exit()


basedir = os.getcwd()
project = os.getcwd().split("/")[-1]
argv = sys.argv[1:]
debug = False

videofile = False
bannerimg = False

dirs = os.getcwd().split("/")
controlnet = dirs[-1]
sampler = dirs[-2]
model = dirs[-3]
labeltext = f"{model}~+~{sampler}~+~{controlnet}"

try:
    opts, args = getopt.getopt(
        argv,
        "hv:b:d",
        ["help", "video=" "banner=","debug"],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-v", "--video"):
        videofile = arg
    if opt in ("-b", "--banner"):
        bannerimg = arg
    if opt in ("-d", "--debug"):
        debug=True
    if opt in ("-t", "--text"):
        labeltext = arg

vdat = ffmpeg.probe(videofile)
# pprint(vdat)
# exit()
duration = round(float(vdat["format"]["duration"]))
# pprint(vdat["streams"][0]['height'])

height = int(vdat["streams"][0]['height'])
width = int(vdat["streams"][0]['width'])

# pprint(vdat)
# exit()

duration = round(float(vdat["format"]["duration"]))


# get dimensions, title



# make label


label_tmpfile = f"{mktemp()}_label.png"
label_tmpvid = f"{mktemp()}_vid.mp4"
output = "/tmp/outbanner.mp4"

cmd = f'magick -background black -fill yellow -pointsize 25 -gravity center  -font Carlito-Regular -size {width}x50  label:"{labeltext}" {label_tmpfile}'
p.prunlive(cmd,debug = debug)
# create video of label
cmd = f"ffmpeg -y -loglevel error -loop 1 -i /tmp/tmp.png -c:v libx264 -t {duration} -pix_fmt yuv420p -vf scale={width}:50 {label_tmpvid}"
p.prunlive(cmd,debug = debug)

# combine the two videos vertically
cmd = f'ffmpeg -y -loglevel warning  -i {label_tmpvid} -i {videofile} -fps_mode passthrough -filter_complex "[0:v][1:v]"vstack=inputs=2:shortest=1"[outv]" -map "[outv]" {output}'
p.prunlive(cmd,debug = debug)

mdirs = p.split_path(videofile)
cmd = f"mv {output} {mdirs['dirname']}/banner_{mdirs['basename']}"
# print(cmd)
p.prunlive(cmd,debug = debug)
