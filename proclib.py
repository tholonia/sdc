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
import numpy as np
init()

#[ UTIITY Funtions                                                ]
def tryit(kwargs,arg,default):
    try:
        rs = kwargs[arg]
    except:
        rs = default
    return rs
def prun(cmd, **kwargs):
    debug = tryit(kwargs,'debug',False)

    if debug:
        # print("\n"+'──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────')
        print(Fore.YELLOW +">>> "+ cmd + Fore.RESET)
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

#[ OBJECT  Funtions                                                ]
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
    debug = tryit(kwargs,'debug',False)
    # try:
    #     debug = kwargs['debug']
    # except:
    #     debug = False
    keyname = False
    probe = ffmpeg.probe(filename)
    video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
    if keyname == "all":
        pprint(video_streams[0])
        exit()
    else:
        dur_sec = video_streams[0]['duration']
        return int(round(float(dur_sec))), dur_sec

#[ CLEAB Routinns                                                   ]
def cleanWildcard(w):
    try:
        files = glob.glob(w)
        for file in files:
            os.remove(file)
    except:
        pass
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
def cleanAll(d):
    nfiles = len(glob.glob(f"{d}/**/*", recursive=True))
    print(f"Cleaning {nfiles} file from {d}")
    cleanTree(d)
def cleanTrash():
    d = '/home/jw/.local/share/Trash/**/*'
    try:
        files = glob.glob(d, recursive=True)
        nfiles = len(files)
        # pprint(files)
        print(f"Cleaning {nfiles} file from {d}")
        for f in files:
            f.replace(" ","\\ ")
            f.replace("\(","\\(")
            cmd = f"rm -rf {f}"
            # print(cmd)
            os.system(cmd)
    except:
        pass

    d = '/run/user/1000/kio-fuse-jnwddn/trash/**/*'
    try:
        files = glob.glob(d, recursive=True)
        nfiles = len(files)
        # pprint(files)
        print(f"Cleaning {nfiles} file from {d}")
        for f in files:
            cmd = f"rm -rf {f}"
            # print(cmd)
            os.system(cmd)
    except:
        pass
#[SUBRPOCESS Routines                                          ]
def runExtract(filename,**kwargs):
    debug = tryit(kwargs,'debug',False)
    # try:
    #     debug = kwargs['debug']
    # except:
    #     debug = False

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
    debug = tryit(kwargs,'debug',False)
    keep = tryit(kwargs,'keep',False)

    cleanTree(f"{g.tmpdir}/filtered")
    cleanTree(f"{g.tmpdir}/tossed")

    timeStart = time.time()
    print(Fore.GREEN+f"Tossing similar frames in {g.tmpdir}/images"+Fore.RESET,end="",flush=True)

    # cmd = f"toss.py -v {location} -f {tossFilter}"
    cmd = f"toss.py -v {location} -k {keep}"
    prun(cmd,debug=debug)


    fct = glob.glob(f"{g.tmpdir}/images/*")
    print(f"   ({procTime(timeStart)}), {len(fct)} images")

    totalFiles = len(glob.glob(f"{g.tmpdir}/images/*.png"))
    filtered = len(glob.glob(f"{g.tmpdir}/filtered/*.png"))
    tossed = len(glob.glob(f"{g.tmpdir}/tossed/*.png"))
    try:
        pctTossed = round(tossed/totalFiles * 100)
    except Exception as e:
        print(f"totalFiles: {totalFiles}")
        print(f"filtered: {filtered}")
        print(f"tossed: {tossed}")
        print(e)
        pass
    #^ mv filtered frames ti /tmp/images where interpolatio expects to find them,
    cleanTree(f"{g.tmpdir}/frames")
    cmd = f"mv {g.tmpdir}/filtered/* {g.tmpdir}/frames/"
    os.system(cmd)
    return f"{g.tmpdir}/filtered", pctTossed, totalFiles, filtered, tossed
def runInterp(interpx,**kwargs):
    debug = tryit(kwargs,'debug',False)
    version = tryit(kwargs,'version',1)

    cleanTree(f"{g.tmpdir}/frames")


    timeStart = time.time()
    print(Fore.GREEN+f"Interpolating images from {g.tmpdir}/images to {g.tmpdir}/frames"+Fore.RESET,end="",flush=True)
    cmd = False
    if version == 1:
        cmd = f"{g.rifedir}/interpolate.py --input {g.tmpdir}/images/ --output {g.tmpdir}/frames/ --buffer 0 --multi {interpx} --change 0.01 --model {g.rifedir}/rife/flownet-v46.pkl"
    if version == 2:
        cmd = f"{g.rifedir}/interpV2.py --ext png --input {g.tmpdir}/images/ --output {g.tmpdir}/frames/ --buffer 0 --multi {interpx} --change 0.01 --model {g.rifedir}/rife/flownet-v46.pkl"

    prun(cmd,debug=debug)
    print(f"   ({procTime(timeStart)})")
    totalImg = len(glob.glob(f"{g.tmpdir}/frames/*"))
    return f"{g.tmpdir}/frames", totalImg
def runStitch(dirname, **kwargs):
    debug = tryit(kwargs,'debug',False)
    version = tryit(kwargs,'version',1)

    #^ what kind of files?
    imgs = glob.glob(f"{dirname}/*.png")

    ext = "jpg"
    if version == 2:
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
    debug = tryit(kwargs,'debug',False)
    cleanTree(f"{g.tmpdir}/images")
    cleanTree(f"{g.tmpdir}/frames")
    id = getID(filename)
    timeStart = time.time()
    print(Fore.GREEN+f"Labeling images in {filename}"+Fore.RESET,end="",flush=True)
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    nameonly = basename.replace(".mp4","")

    cmd= f"perlabel.py -d {dirname} -i {id} -s {dirname}/{nameonly}_settings.txt"
    prun(cmd,debug=debug)
    print(f"   ({procTime(timeStart)})")
    return f"{g.tmpdir}/labeled_{id}.mp4"
def runCrop(filename,x,y, **kwargs):
    debug = tryit(kwargs,'debug',False)

    # try:
    #     debug = kwargs['debug']
    # except:
    #     debug = False
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
    debug = tryit(kwargs,'debug',False)
    # try:
    #     debug = kwargs['debug']
    # except:
    #     debug = False

    timeStart = time.time()
    print(Fore.GREEN + f"Upscaling 4x ({srcfile})" + Fore.RESET,end="",flush=True)
    cmd = f'/home/jw/src/sdc/upscale.sh {srcfile}' # > /dev/null 2>&1'
    prun(cmd,debug=debug)
    dest = f"{g.esgrandir}/results/{os.path.basename(srcfile)}"
    dest = dest.replace(".mp4","_out.mp4")
    fs = getFilesize(dest)
    print(f"   ({procTime(timeStart)}), {fs}")
    outfile = srcfile.replace(".mp4","_out.mp4")
    cmd = f"mv /home/jw/src/Real-ESRGAN/results/{os.path.basename(outfile)} {os.path.dirname(srcfile)}/4x_{os.path.basename(srcfile)}"
    prun(cmd,debug=True)

    return f"{os.path.dirname(srcfile)}/4x_{os.path.basename(srcfile)}"
def runFade(filename, **kwargs):
    debug = tryit(kwargs,'debug',False)
    # try:
    #     debug = kwargs['debug']
    # except:
    #     debug = False
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
    debug = tryit(kwargs,'debug',False)

    # try:
    #     debug = kwargs['debug']
    # except:
    #     debug = False

    timeStart = time.time()
    print(Fore.GREEN + f"Embedding metadata" + Fore.RESET,end="",flush=True)
    cmd=f"{g.sdcdir}/metaconfig.py -v {filename} -a {settingsFile}"
    prun(cmd,debug=debug)
    timeProc = time.time() - timeStart
    print(f"   ({timeProc})")
#[MATH Routines                                                      ]
def bezier_curve(control_points, number_of_curve_points):
    return [
        bezier_point(control_points, t)
        for t in (
            i / (number_of_curve_points - 1) for i in range(number_of_curve_points)
        )
    ]
def bezier_point(control_points, t):
    if len(control_points) == 1:
        result, = control_points
        return result
    control_linestring = zip(control_points[:-1], control_points[1:])
    return bezier_point([(1 - t) * p1 + t * p2 for p1, p2 in control_linestring], t)
def cycle_in_range(number, amin, amax, invert=False):
    try:
        mod_num = number % amax
    except:
        mod_num = 0

    try:
        mod_num2 = number % (amax * 2)
    except:
        mod_num2 = 0

    new_val1 = abs(mod_num2 - (mod_num * 2))

    old_min = 0
    old_min = 0
    old_max = amax
    new_max = amax
    new_min = amin

    try:
        new_value = ((new_val1 - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    except:
        new_value = 0

    new_value = amax - new_value if invert else new_value

    return (round(new_value))
def np_normalize(x, amin,amax): #newRange=(0, 1)):  # x is an array. Default range is between zero and one
    xmin, xmax = np.min(x), np.max(x)  # get max and min from input array
    norm = (x - xmin) / (xmax - xmin)  # scale between zero and one

    # if newRange == (0, 1):
    #     return norm  # wanted range is the same as norm
    # elif newRange != (0, 1):
    return (norm * (amax - amin) + amin)  # scale to a different range.
    # add other conditions here. For example, an error message
def normalize(numbers, **kwargs):
    minimum = min(numbers)
    maximum = max(numbers)

    normalized = [(x - minimum) / (maximum - minimum) for x in numbers]
    return normalized
#[VIDEO Functions                                                      ]
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
#[Name wrangling                                                     ]
def getID(filename):
    noext = filename.replace(".mp4","")
    parts = noext.split("/")
    return(parts[-1])
def getFnames(locationpath):
    print(locationpath)
    basename = os.path.basename(locationpath)
    dirname = os.path.dirname(locationpath)
    if not dirname:
        dirname = os.getcwd()
        locationpath = dirname+"/"+basename

    fspec = False

    # ^ order is important
    if os.path.isdir(locationpath):
        dirname = locationpath
        basename = False
        fspec = "dir"
    elif os.path.isabs(locationpath):
        basename = os.path.basename(locationpath)
        dirname = os.path.dirname(locationpath)
        fspec = "abs"
    elif os.path.isfile(locationpath):
        basename = locationpath
        dirname = os.getcwd()
        fspec = "rel"
    else:
        print(f"Bad {fspec} path argument or '{dirname}/{basename}' does not exist")
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
def procTime(t):
    secs = round(time.time() - t)
    mins = round(secs/600)/10
    if secs < 60:
        return f"{secs} secs"
    if mins >=1:
        return f"{min} mins"
def splitnonalpha(s):
    return re.split('[^a-zA-Z0-9]', s)
