import sys
import subprocess
from colorama import init, Fore, Back
from pprint import pprint
import re
import time
import shutil
import os
import glob
import cv2
import procvars as g
import time
import ffmpeg
import json
import random
init()

def rot_left(l, n):
    return l[n:] + l[:n]


def rot_right(l, n):
    return l[n:] - l[:n]


def shiftary(a):
    a = list(a)
    loops = random.choice([1,2,3,4]) #^ '4' is arbitray, and assume there are at least classes of type (biology, insects, etc)
    for j in range(loops):
        items = a[:5] #^ 5 is half of 10, which is the the number of elements in easy class aray (of biology, insects, etc)
        for item in items:
            a.remove(item)
            a.append(item)
    return a
def viduration(filename,**kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False
    keyname = False
    probe = ffmpeg.probe(filename)
    video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
    if keyname == "all":
        pprint(video_streams[0])
        exit()
    else:
        dur_sec = video_streams[0]['duration']
        return int(round(float(dur_sec))), dur_sec
def runExtract(filename,**kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False

    cleanTree(f"{g.tmpdir}/images")
    cleanTree(f"{g.tmpdir}/frames")
    timeStart = time.time()
    print(Fore.GREEN+f"Extracting images from {filename} to {g.tmpdir}/images"+Fore.RESET,end="",flush=True)
    cmd = f"ffmpeg -loglevel warning -i {filename} -r 15/1 {g.tmpdir}/images/%05d.png"
    #cmd_2 = f"ffpb -i {srcfile} -r 15/1 {args['tmpdir']}/images/%05d.png"
    prun(cmd,debug=debug)
    fct = glob.glob(f"{g.tmpdir}/images/*")
    print(f"   ({procTime(timeStart)}), {len(fct)} images")
    return f"{g.tmpdir}/images"

def runToss(location,tossFilter,**kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False

    cleanTree(f"{g.tmpdir}/filtered")
    cleanTree(f"{g.tmpdir}/tossed")
    timeStart = time.time()
    print(Fore.GREEN+f"Tossing similar frames in {g.tmpdir}/images"+Fore.RESET,end="",flush=True)
    cmd = f"toss.py -v {location} -f {tossFilter}"
    prun(cmd,debug=debug)
    fct = glob.glob(f"{g.tmpdir}/images/*")
    print(f"   ({procTime(timeStart)}), {len(fct)} images")

    totalFiles = len(glob.glob(f"{g.tmpdir}/images/*.png"))
    filtered = len(glob.glob(f"{g.tmpdir}/filtered/*.png"))
    tossed = totalFiles - filtered

    pctTossed = round(tossed/totalFiles * 100)

    return f"{g.tmpdir}/filtered", pctTossed, totalFiles


def runInterp(interpx,**kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False

    try:
        version = kwargs['version']
    except:
        version = 1



    timeStart = time.time()
    print(Fore.GREEN+f"Interpolating images from {g.tmpdir}/images to {g.tmpdir}/frames"+Fore.RESET,end="",flush=True)
    cmd = False
    if version == 1:
        cmd = f"{g.rifedir}/interpolate.py --input {g.tmpdir}/images/ --output {g.tmpdir}/frames/ --buffer 0 --multi {interpx} --change 0.01 --model {g.tmpdir}/rife/flownet-v46.pkl"
    if version == 2:
        cmd = f"{g.rifedir}/interpV2.py --ext png --input {g.tmpdir}/images/ --output {g.tmpdir}/frames/ --buffer 0 --multi {interpx} --change 0.01 --model {g.rifedir}/rife/flownet-v46.pkl"

    prun(cmd,debug=debug)
    print(f"   ({procTime(timeStart)})")
    totalImg = len(glob.glob(f"{g.tmpdir}/frames/*"))
    return f"{g.tmpdir}/frames", totalImg

def runStitch(dirname, **kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False
    # try:
    #     ext = kwargs['ext']
    # except:
    #     ext = "jpg"

    #^ what kind of files?
    imgs = glob.glob(f"{dirname}/*.png")
    if len(imgs)==0:
        ext = "jpg"
    else:
        ext = "png"

    timeStart = time.time()
    print(Fore.GREEN+f"Stitching images in {dirname}"+Fore.RESET,end="",flush=True)
    cmd = f"ffmpeg -y -loglevel warning -framerate 15 -pattern_type glob -i {dirname}/*.{ext} -c:v libx264 -pix_fmt yuv420p  {g.tmpdir}/out_{g.uid}.mp4"
    prun(cmd,debug=debug)
    fs = getFilesize(f"{g.tmpdir}/out_{g.uid}.mp4")
    print(f"   ({procTime(timeStart)}), {fs}")
    cmd = f"cp {g.tmpdir}/out_{g.uid}.mp4 {g.tmpdir}/stitched.mp4"
    prun(cmd,debug=debug)

    return f"{g.tmpdir}/out_{g.uid}.mp4", f"{g.tmpdir}/stitched.mp4"


def runPerlabel(filename,**kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False

    cleanTree(f"{g.tmpdir}/images")
    cleanTree(f"{g.tmpdir}/frames")
    id = getID(filename)
    timeStart = time.time()
    print(Fore.GREEN+f"Labeling images in {filename}"+Fore.RESET,end="",flush=True)
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    nameonly = basename.replace(".mp4","")

    cmd= f"perlabel.py -d {dirname} -i {basename} -s {dirname}/{nameonly}_settings.txt"
    prun(cmd,debug=debug)
    print(f"   ({procTime(timeStart)})")
    return f"{g.tmpdir}/labeled_{id}.mp4"

def runCrop(filename,x,y, **kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False
    fid = getID(filename)
    timeStart = time.time()
    print(Fore.GREEN + f"Cropping/Scaling to {x}x{y} (/tmp/scaled_{g.uid}_{fid}.mp4)" + Fore.RESET, end="",flush=True)
    # #^ see https://superuser.com/questions/1474942/ffmpeg-cropping-invalid-too-big-or-non-positive-size-for-width for ewhy these args are so complex
    # cmd = f'ffmpeg -y -loglevel warning -i /tmp/out_{g.uid}.mp4 -vf scale=(iw*sar)*max(2040.1/(iw*sar)\,1150.1/ih):ih*max(2040.1/(iw*sar)\,1150.1/ih),crop=2040:1150 /tmp/scaled_{g.uid}_{fid}.mp4'
    outfile = f"/tmp/scaled_{g.uid}_{fid}.mp4"
    cmd = f'ffmpeg -y -loglevel warning -i {filename} -vf scale=(iw*sar)*max({x}.1/(iw*sar)\,{y}.1/ih):ih*max({x}.1/(iw*sar)\,{y}.1/ih),crop={x}:{y} {outfile}'
    prun(cmd,debug=debug)
    fs = getFilesize(outfile)
    print(f"   ({procTime(timeStart)}), {fs}")
    return outfile
def runUpscale(srcfile, **kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False

    timeStart = time.time()
    print(Fore.GREEN + f"Upscaling 4x ({srcfile})" + Fore.RESET,end="",flush=True)
    cmd = f'/home/jw/src/sdc/upscale.sh {srcfile} > /dev/null 2>&1'
    prun(cmd,debug=True)
    dest = f"{g.esgrandir}/results/{os.path.basename(srcfile)}"
    dest = dest.replace(".mp4","_out.mp4")
    fs = getFilesize(dest)
    print(f"   ({procTime(timeStart)}), {fs}")
    cmd = f"mv /home/jw/src/Real-ESRGAN/results/{os.path.basename(srcfile)} {os.path.dirname(srcfile)}/4x_{os.path.basename(srcfile)}"
    prun(cmd)

    return f"{os.path.dirname(srcfile)}/4x_{os.path.basename(srcfile)}"

def runFade(filename, **kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False
    fid = getID(filename)
    timeStart = time.time()
    print(Fore.GREEN + f"Fading in/out ({filename})..." + Fore.RESET,end="",flush=True)

    vdurInt, vdur = viduration(filename)
    fadeinTime = 3
    fadeoutTime = 5
    startFout = vdurInt-fadeoutTime
    cmd = f'ffmpeg -loglevel warning -y -i {filename} -vf fade=t=in:st=0:d={fadeinTime} -c:a copy {g.tmpdir}/fout_{g.uid}.mp4'
    prun(cmd,debug=debug)
    cmd = f'ffmpeg -loglevel warning -y -i {g.tmpdir}/fout_{g.uid}.mp4 -vf fade=t=out:st={startFout}:d={fadeoutTime} -c:a copy {g.tmpdir}/fout2_{g.uid}.mp4'
    prun(cmd, debug=debug)
    cmd = f"mv {g.tmpdir}/fout2_{g.uid}.mp4 {filename}"
    prun(cmd, debug=debug)

    print(f"   ({procTime(timeStart)})")
    return filename
def runMeta(filename,settingsFile, **kwargs):
    try:
        debug = kwargs['debug']
    except:
        debug = False

    timeStart = time.time()
    print(Fore.GREEN + f"Embedding metadata" + Fore.RESET,end="",flush=True)
    cmd=f"{g.sdcdir}/metaconfig.py -v {filename} -a {settingsFile}"
    prun(cmd,debug=debug)
    timeProc = time.time() - timeStart
    print(f"   ({timeProc})")



def normalize(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    normalized = [(x - minimum) / (maximum - minimum) for x in numbers]
    return normalized
def Diff_img(img0, img):
    '''
    This function is designed for calculating the difference between two
    images. The images are convert it to an grey image and be resized to reduce the unnecessary calculating.
    '''
    # Grey and resize
    img0 =  cv2.cvtColor(img0, cv2.COLOR_RGB2GRAY)
    img =  cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img0 = cv2.resize(img0, (320,200), interpolation = cv2.INTER_AREA)
    img = cv2.resize(img, (320,200), interpolation = cv2.INTER_AREA)
    # Calculate
    Result = (abs(img - img0)).sum()
    return Result

def getId(filename):
    fnum = []
    #^ get any 14 char string pefore a perios
    fnum = re.findall("[\_\-\.]*([\d]{14})[\_\-\.]*",filename,re.DOTALL)
    id = fnum[0]
    return id

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
        # print(e)
        pass
    try:
        shutil.rmtree(tdir)
    except Exception as e:
        # print(e)
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
    #     .output(f"{tmpdir}/images/{i:09d}.png", vframes=1)
    #     .run()
    #   )
    #   i += 1