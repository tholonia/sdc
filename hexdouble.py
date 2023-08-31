#!/bin/env python
from glob import glob
import os,re

files = glob("/home/jw/src/hexani/A_MINT/A_CBvers/cbv2.dots_prizeB/ORG/*.png")
files.sort()

for f in files:
    fname = os.path.basename(f)
    dname = os.path.dirname(f)
    pts = re.split("-|\.|png]",fname)
    num = float(f"{pts[1]}.{pts[2]}")

    newnum = abs(180-(360-num))+180
    # print(pts, num, newnum)

    cmd = f"cp out_hex-{pts[1]}.{pts[2]}.png out_hex-{newnum:06.1f}.png"
    print(cmd)
