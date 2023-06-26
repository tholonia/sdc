#!/bin/env python

import os,sys,glob,getopt
from colorama import init, Fore, Back
from pprint import pprint
import ffmpeg
import subprocess
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
    -d, --dir           directory
    -D, --destdir           directory
    -r, --rename           rename
    -v, --verbose
    -R, --res           resolution n (nxn)
'''
dir = "./outputs/batch"
destdir = "./safe/vids"
rename = False
verbose = "-loglevel panic"
resolution = 512

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hd:r:D:vR:", [
        "help",
        "dir=",
        "destdir=",
        "rename=",
        "verbose",
        "res=",
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
    if opt in ("-v", "--verbose"):
        verbose = "-loglevel info"
    if opt in ("-R", "--resolution"):
        resolution = int(arg)






def cleanpre():
    cleanpost()
    if os.path.exists(f"/tmp/merged.mp4"): os.unlink(f"/tmp/merged.mp4")
def cleanpost():
    if os.path.exists(f"/tmp/o1.mp4"): os.unlink(f"/tmp/o1.mp4")
    if os.path.exists(f"/tmp/o2.mp4"): os.unlink(f"/tmp/o2.mp4")
    if os.path.exists(f"/tmp/o2.mp4"): os.unlink(f"/tmp/o2.mp4")
    if os.path.exists(f"/tmp/o3.mp4"): os.unlink(f"/tmp/o3.mp4")
    if os.path.exists(f"/tmp/output.mp4"): os.unlink(f"/tmp/output.mp4")
    if os.path.exists(f"/tmp/output1.mp4"): os.unlink(f"/tmp/output1.mp4")
    if os.path.exists(f"/tmp/output2.mp4"): os.unlink(f"/tmp/output2.mp4")
    if os.path.exists(f"/tmp/output3.mp4"): os.unlink(f"/tmp/output3.mp4")


def merge_h(width,vids,count):
    #! create the horizontal elements
    pprint(vids)

    #! check res to make sure this is a square, otherwise resize
    for v in vids:
        print(Fore.MAGENTA+f"VIDEO {v}"+Fore.RESET)
        probe = ffmpeg.probe(v)
        video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
        # pprint(video_streams[0]['coded_width'])
        if video_streams[0]['coded_width'] != video_streams[0]['coded_height']:
            print(Fore.MAGENTA + f"Adjusting square dimensions for {v}" + Fore.RESET)

            cmd = f"ffmpeg -y {verbose} -i {v} -r 15 -s {video_streams[0]['coded_width']}x{video_streams[0]['coded_width']} -an /tmp/outx.mp4"
            prun(cmd)
            cmd = f"mv /tmp/outx.mp4 {v}"
            prun(cmd)
        else:
            print(Fore.MAGENTA+f"Square Dimensions OK for {v}"+Fore.RESET)

        #! now make sure is 512x512
        if video_streams[0]['coded_width'] != resolution:
            print(Fore.MAGENTA + f"Resizing to {resolution}x{resolution} for {v}" + Fore.RESET)
            cmd = f"ffmpeg -y {verbose} -i {v}  -s 512x512 -c:a copy /tmp/outxa.mp4"
            prun(cmd)
            cmd = f"mv /tmp/outxa.mp4 {v}"
            prun(cmd)

    cmd = f"ffmpeg -y {verbose} "
    for vid in vids:
        cmd = cmd + f"-i {vid} "
    cmd = cmd + f'-filter_complex [0]pad=iw+5:color=black[left];[left][1]hstack=inputs={width} /tmp/output{count}.mp4'
    prun(cmd)
    # os.system(cmd)

    #! fix the fps to 15
    cmd = f"ffmpeg -y {verbose}  -i /tmp/output{count}.mp4 -filter:v fps=15 /tmp/o{count}.mp4"


    print("(3)"+Fore.GREEN+cmd+Fore.RESET)
    os.system(cmd)
    return f"/tmp/o{count}.mp4"
def merge_v(vids):
    #! combine the hor elements vertically
    cmd = f"ffmpeg -y {verbose} "
    for vid in vids:
        cmd = cmd + f"-i {vid} "
    cmd = cmd + f' -filter_complex [0:v][1:v]vstack=inputs={len(vids)}:shortest=1[outv] -map [outv] /tmp/merged.mp4'
    prun(cmd)
    # os.system(cmd)

    return(f"{dir}/merged.mp4")

cleanpre()
vids = glob.glob(f"{dir}/*.mp4")

print(f"{dir}/*.mp4")
vids.sort()
num_of_vids = len(vids)

print(f"Merge {num_of_vids} video")
print(vids)
if num_of_vids == 1:
    cmd = f"mv {vids[0]} /tmp/merged.mp4"
    print("(5)"+Fore.GREEN + cmd + Fore.RESET)
    prun(cmd)
    # os.system(cmd)

if num_of_vids == 2:
    f1 = merge_h(2, vids[:2], 1)
    cmd = f"mv /tmp/o1.mp4 /tmp/merged.mp4"
    print("(6)"+Fore.GREEN + cmd + Fore.RESET)
    prun(cmd)
    # os.system(cmd)

if num_of_vids == 3:
    f1 = merge_h(3, vids, 1)
    cmd = f"mv /tmp/o1.mp4 /tmp/merged.mp4"
    print("(7)"+Fore.GREEN + cmd + Fore.RESET)
    prun(cmd)
    # os.system(cmd)

if num_of_vids == 4:
    f1 = merge_h(2, vids[:2], 1)
    f2 = merge_h(2, vids[2:4], 2)
    f3 = merge_v([f1, f2])

if num_of_vids == 5:
    f1 = merge_h(5, vids, 1)
    cmd = f"mv /tmp/o1.mp4 /tmp/merged.mp4"
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
    print(f"MOVING: /tmp/merged.mp4 -> {destdir}/{resolution}_{rename}")
    os.system(f"mv /tmp/merged.mp4 {destdir}/{resolution}_{rename}")

cleanpost()

