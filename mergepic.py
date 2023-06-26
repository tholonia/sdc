#!/bin/env python

import os,sys,glob,getopt
from colorama import init, Fore, Back
from pprint import pprint
import ffmpeg
import subprocess
init()


def prun(cmd):
    print(Fore.YELLOW+cmd+Fore.RESET)
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
    -d, --dir           directory
    -D, --destdir           directory
    -r, --rename           rename
'''
dir = "./outputs/batch"
destdir = "./safe/vids"
rename = False
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hd:r:D:", [
        "help",
        "dir=",
        "destdir=",
        "rename=",
    ])
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp();
    if opt in ("-d", "--dir"):
        dir = arg
    if opt in ("-r", "--rename"):
        rename = arg
    if opt in ("-D", "--destdir"):
        destdir = arg






def cleanpre():
    cleanpost()
    if os.path.exists(f"{dir}/merged.png"): os.unlink(f"{dir}/merged.png")
def cleanpost():
    if os.path.exists(f"{dir}/o1.png"): os.unlink(f"{dir}/o1.png")
    if os.path.exists(f"{dir}/o2.png"): os.unlink(f"{dir}/o2.png")
    if os.path.exists(f"{dir}/o3.png"): os.unlink(f"{dir}/o3.png")


def merge_h(width,vids,count):
    #! create the horizontal elements
    pprint(vids)

    #! ch3eck res

    cmd = f"ffmpeg -y "
    for vid in vids:
        cmd = cmd + f"-i {vid} "
    cmd = cmd + f' -y -loglevel panic -filter_complex [0]pad=iw+5:color=black[left];[left][1]hstack=inputs={width} {dir}/o{count}.png'
    print(Fore.GREEN+cmd+Fore.RESET)
    prun(cmd)
    # os.system(cmd)

    return f"{dir}/o{count}.png"
def merge_v(vids):
    #! combine the hor elements vertically
    cmd = f"ffmpeg -y "
    for vid in vids:
        cmd = cmd + f"-i {vid} "
    cmd = cmd + f' -filter_complex [0:v][1:v]vstack=inputs={len(vids)}:shortest=1[outv] -map [outv] {dir}/merged.png'
    print(Fore.GREEN + cmd + Fore.RESET)
    prun(cmd)
    # os.system(cmd)

    return(f"{dir}/merged.png")

cleanpre()
vids = glob.glob(f"{dir}/*.png")

print(f"{dir}/*.png")
vids.sort()
num_of_vids = len(vids)

print(f"Merge {num_of_vids} video")
print(vids)
if num_of_vids == 1:
    cmd = f"mv {vids[0]} {dir}/merged.png"
    cmd = f"mv {vids[0]} {dir}/merged.png"
    print(Fore.GREEN + cmd + Fore.RESET)
    prun(cmd)
    # os.system(cmd)

if num_of_vids == 2:
    f1 = merge_h(2, vids[:2], 1)
    cmd = f"mv {dir}/o1.png {dir}/merged.png"
    print(Fore.GREEN + cmd + Fore.RESET)
    prun(cmd)
    # os.system(cmd)

if num_of_vids == 3:
    f1 = merge_h(3, vids, 1)
    cmd = f"mv {dir}/o1.png {dir}/merged.png"
    print(Fore.GREEN + cmd + Fore.RESET)
    prun(cmd)
    # os.system(cmd)

if num_of_vids == 4:
    f1 = merge_h(2, vids[:2], 1)
    f2 = merge_h(2, vids[2:4], 2)
    f3 = merge_v([f1, f2])

if num_of_vids == 5:
    f1 = merge_h(5, vids, 1)
    cmd = f"mv {dir}/o1.png {dir}/merged.png"
    prun(cmd)
    # os.system(cmd)

if num_of_vids == 6:
    f1 = merge_h(3, vids[:3], 1)
    f2 = merge_h(3, vids[3:6], 2)
    f3 = merge_v([f1, f2])

if num_of_vids == 10:
    f1 = merge_h(5, vids[:5], 1)
    f2 = merge_h(5, vids[5:10], 2)
    f3 = merge_v([f1, f2])

if num_of_vids == 8:
    f1 = merge_h(4, vids[:4], 1)
    f2 = merge_h(4, vids[4:8], 2)
    f3 = merge_v([f1, f2])

if num_of_vids == 15:
    f1 = merge_h(5, vids[:5], 1)
    f2 = merge_h(5, vids[5:10], 2)
    f3 = merge_h(5, vids[10:15], 3)
    f4 = merge_v([f1, f2, f3])

if num_of_vids == 12:
    f1 = merge_h(4, vids[:4], 1)
    f2 = merge_h(4, vids[4:8], 2)
    f3 = merge_h(4, vids[8:12], 3)
    f4 = merge_v([f1, f2, f3])

if rename:
    print(f"MOVING: {dir}/merged.png -> {destdir}/{rename}")
    os.system(f"mv {dir}/merged.png {destdir}/{rename}")

cleanpost()

