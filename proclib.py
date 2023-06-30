import sys
import subprocess
from colorama import init, Fore, Back
from pprint import pprint
import re
import time
import shutil
import os
import glob
import procvars as g
init()

def getFnames(filename):
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    fspec = False
    if os.path.isabs(filename):
        basename = os.path.basename(filename)
        dirname = os.path.dirname(filename)
        fspec = "abs"
    elif os.path.isfile(filename):
        basename = filename
        dirname = "."
        fspec = "rel"
    elif os.path.isdir(filename):
        dirname = filename
        basename = False
        fspec = "dir"
    else:
        print("Bad path argumentment")
        exit()
    srcfile = f"{dirname}/{basename}"
    return basename,dirname,fspec,srcfile

def getFilesize(file_name):
    file_stats = os.stat(file_name)
    bytes = file_stats.st_size
    mbytes = file_stats.st_size / (1024 * 1024)
    return(f"{mbytes:0.2f} MB")
def errprint(str):
    print(str, file=sys.stderr)

def getID(filename):
    noext = filename.replace(".mp4","")
    parts = noext.split("/")
    return(parts[-1])
    # # fnum = re.findall("[\d]*_(\d\d\d\d\d\d\d\d\d).png", filename, re.DOTALL)
    # fnum = re.findall("[\d]{14}.png", filename, re.DOTALL)
    # pprint(filename,fnum)
    # exit()
    # # return re.split('[\d]{14}^a-zA-Z0-9]', s)
    # return re.split('[\d]{14}]', str)
    # p = splitnonalpha(filename)
    # pprint(p)
    # # id = p[-2]
    # # print(id)
    # exit()


def cleanWildcard(w):
    files = glob.glob(w)
    for file in files:
        os.remove(file)
def cleanTree(tdir):
    try:
        shutil.rmtree(tdir)
    except Exception as e:
        print(e)
        pass
    try:
        shutil.rmtree(tdir)
    except Exception as e:
        print(e)
        pass
    os.mkdir(tdir)
def procTime(t):
    secs = round(time.time() - t)
    mins = round(secs/600)/10
    if secs < 60:
        return f"{secs} secs"
    if mins >=1:
        return f"{min} mins"

def splitnonalpha(s):
    return re.split('[^a-zA-Z0-9]', s)
   # return  ('[^a-zA-Z0-9]',s)
   # pos = 1
   # while pos < len(s) and s[pos].isalpha():
   #    pos+=1
   # return (s[:pos], s[pos:])


def prun(cmd, **kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False

    if debug:
        print("\n"+'──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
        print(Fore.YELLOW + cmd + Fore.RESET)
    scmd = cmd.split()
    if debug:
        process = subprocess.Popen(scmd)
    else:
        process = subprocess.Popen(scmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    process.wait()
    # rs = subprocess.call(scmd)
    # rs = subprocess.check_call(scmd)
    # if rs != 0:
    #     print(Fore.RED)
    #     print(Fore.YELLOW+cmd+Fore.RESET)
    #     # raise RuntimeError(stderr)



    # process = subprocess.Popen(scmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate()
    # process.wait()
    # if process.returncode != 0:
    #     print(Fore.RED)
    #     print(Fore.YELLOW+cmd+Fore.RESET)
    #     raise RuntimeError(stderr)
    #
    # ^ alternative python call
    # probe=ffmpeg.probe(srcfile)
    # time = float(probe['streams'][0]['duration']) // 1
    # # print(time)
    # # exit()
    # width = probe['streams'][0]['width']
    # parts = 1
    # intervals = time // parts
    # intervals = int(intervals)
    # print(f"Intervals: {intervals}")
    # interval_list = [(i * intervals, (i + 1) * intervals) for i in range(parts)]
    # print(f"Interval_list: {interval_list}")
    # # exit()
    #
    # i = 0
    # for item in interval_list:
    #   (
    #     ffmpeg
    #     .input(srcfile, ss=item[1])
    #     .filter('scale', width, -1)
    #     .output(f"{rifedir}/images/{i:09d}.png", vframes=1)
    #     .run()
    #   )
    #   i += 1