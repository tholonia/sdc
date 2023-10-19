#!/bin/env python
import math
import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
import proclib as p
import math as m
from tempfile import mktemp

init()

def showhelp():
    print("help")
    rs = """
    -h, --help          show help
    -f, --filename      fulle or partial filename Ex: /tnp/*.mp4"
    -D, --destdir       directory
    -v, --verbose
    -g, --grid          XxY
"""
    print(rs)
    exit()



path = "./*.mp4"
pathparts = p.split_path(path)
filepath = pathparts["dirname"]
filename = pathparts["basename"]
destdir = os.getcwd() + "/out"
verbose = False
ffmpeg_verbose = "-loglevel error"
Xr = 512
Yr = 512
Xg = 1
Yg = 1
grid = "3x2"


argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hf:D:vg:",
        ["help", "filename=", "destdir=", "verbose", "grid="],
    )
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-f", "--filename"):
        pathparts = p.split_path(arg)
        filepath = pathparts["dirname"]
        filename = pathparts["basename"]
    if opt in ("-D", "--destdir"):
        destdir = arg
    if opt in ("-v", "--verbose"):
        verbose = True
        ffmpeg_verbose = "-loglevel warning"
    if opt in ("-g", "--grid"):
        parts = str(arg).split("x")
        grid = arg
        Xg = int(parts[0])
        Yg = int(parts[1])
        # print(f"grid => Xg/Yh:{Xg}/{Yg}")


def cleanpre():
    for f in glob.glob("/tmp/tmp*vgrid*"):
        os.unlink(f)
    cleanpost()

def cleanpost():
    for f in glob.glob("/tmp/tmp*output*"):
        os.unlink(f)
def chunks(l, n):
    tary = [l[i : i + n] for i in range(0, len(l), n)]

    return tary

def merge_h(vids, Xg, Yg, count,all_grids):
    hcounts = []
    output_fn = f"{mktemp()}_output"

    # print(f"{len(vids[-1])}/vids:", vids)
    for Y in range(Yg):
        """
        We 'try' here because we assume any error is a index error because there were not enough elements to fill the array.
        By 'passing' the error, we force ffmpeg to fill in the empty spaces or eliminate empty rows
        """

        try:
            rowVids = vids[Y]
            print(
                Fore.GREEN
                + f"Merging {len(rowVids)} videos into row {Y+1}."
                + Fore.RESET
            )
            cmd = f"ffmpeg {ffmpeg_verbose} -y "
            for X in range(len(rowVids)):
                cmd += f" -i {rowVids[X]} "
            xtra = f" -fps_mode passthrough -filter_complex [0]pad=iw+5:color=black[left];[left][1]hstack=inputs={len(rowVids)} {output_fn}_{Y}.mp4"
            cmd += xtra
            hcounts.append(Y)
            p.prun(cmd, debug=verbose)
        except:
            pass
        # print(hcounts)
    if len(vids[-1]) >= Xg:
        print(
            Fore.GREEN
            + f"Merging {len(hcounts)} rows to "
            + Fore.CYAN
            + f"{destdir}/vgrid_{count+1}_of_{all_grids}.mp4"
            + Fore.RESET
            + "."
        )
        cmd = f"ffmpeg -y {ffmpeg_verbose} "
        for h in hcounts:
            cmd += f" -i {output_fn}_{h}.mp4"
        xtra = f" -fps_mode passthrough -filter_complex [0:v][1:v]vstack=inputs={len(hcounts)}:shortest=1[outv] -map [outv] {destdir}/vgrid_{count+1}_of_{all_grids}.mp4"
        cmd += xtra
        p.prun(cmd, debug=verbose)
    else:
        print(
            Fore.GREEN
            + f"Merging remaining {len(vids[-1])} videos to "
            + Fore.CYAN
            + f"{destdir}/vgrid_{count+1}_of_{all_grids}.mp4"
            + Fore.RESET
            + "."
        )
        cmd = f"mv {output_fn}_{hcounts[-1]}.mp4 {destdir}/vgrid_{count+1}_of_{all_grids}.mp4"
        p.prun(cmd, debug=verbose)


# [------------------------------------------------------------------------------

cleanpre()
vgrid_fn = f"{mktemp()}_vgrid"
vids = glob.glob(filename)
vids.sort()
total_vids = len(vids)
missing = (Xg * Yg) - (len(vids) % (Xg * Yg))
remainder = int(((total_vids/(Xg * Yg))-int(total_vids/(Xg * Yg)))*(Xg * Yg))
full_grids = m.floor(total_vids/(Xg * Yg))
all_grids = m.ceil(total_vids/(Xg * Yg))

print(Fore.WHITE + f"Merging {total_vids} into {full_grids} {grid} grids with a partial grid of {remainder} videos")

vids = chunks(vids, Xg)
total_row_vids = len(vids)

vids = chunks(vids, Yg)
total_col_vids = len(vids)

for i in range(len(vids)):
    print(Fore.WHITE + f"CREATING GRID {i+1}/{all_grids}")
    merge_h(vids[i], Xg, Yg, i, all_grids)

cleanpost()
