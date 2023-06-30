#!/bin/env python

import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
import ffmpeg
import subprocess
import shutil
from proclib import prun, splitnonalpha, getID, procTime, getFilesize, getFnames, cleanTree, cleanWildcard
import time
import procvars as g

init()

timestamp = round(time.time())

def runExtract(filename):
    cleanTree(f"{g.rifedir}/images")
    cleanTree(f"{g.rifedir}/frames")
    timeStart = time.time()
    print(Fore.GREEN+f"Extracting images from {filename} to {g.rifedir}/images"+Fore.RESET,end="",flush=True)
    cmd = f"ffmpeg -loglevel warning -i {filename} -r 15/1 {g.rifedir}/images/%05d.png"
    #cmd_2 = f"ffpb -i {srcfile} -r 15/1 {args['rifedir']}/images/%05d.png"
    prun(cmd,debug=debug)
    fct = glob.glob(f"{g.rifedir}/images/*")
    print(f"   ({procTime(timeStart)}), {len(fct)} images")

def runInterp(filename,interpx):
    timeStart = time.time()
    print(Fore.GREEN+f"Interpolating images from {filename} to {g.rifedir}/images"+Fore.RESET,end="",flush=True)
    cmd = f"{g.rifedir}/interpolate.py --input {g.rifedir}/images/ --output {g.rifedir}/frames/ --buffer 0 --multi {interpx} --change 0.01 --model {g.rifedir}/rife/flownet-v46.pkl"
    prun(cmd,debug=debug)
    print(f"   ({procTime(timeStart)})")

def runStitch():
    timeStart = time.time()
    print(Fore.GREEN+f"Stitching interpolated images (/tmp/out_{timestamp}.mp4)"+Fore.RESET,end="",flush=True)
    cmd = f"ffmpeg -y -loglevel warning -framerate 15 -pattern_type glob -i {g.rifedir}/frames/*.jpg -c:v libx264 -pix_fmt yuv420p  /tmp/out_{timestamp}.mp4"
    prun(cmd,debug=debug)
    fs = getFilesize(f"/tmp/out_{timestamp}.mp4")
    print(f"   ({procTime(timeStart)}), {fs}")
    return f"/tmp/out_{timestamp}.mp4"

def runCrop(filename,x,y):
    timeStart = time.time()
    print(Fore.GREEN + f"Cropping/Scaling to {x}x{y} (/tmp/scaled_{timestamp}_{id}.mp4)" + Fore.RESET, end="",flush=True)
    # #^ see https://superuser.com/questions/1474942/ffmpeg-cropping-invalid-too-big-or-non-positive-size-for-width for ewhy these args are so complex
    # cmd = f'ffmpeg -y -loglevel warning -i /tmp/out_{timestamp}.mp4 -vf scale=(iw*sar)*max(2040.1/(iw*sar)\,1150.1/ih):ih*max(2040.1/(iw*sar)\,1150.1/ih),crop=2040:1150 /tmp/scaled_{timestamp}_{id}.mp4'
    outfile = f"/tmp/scaled_{timestamp}_{id}.mp4"
    cmd = f'ffmpeg -y -loglevel warning -i {filename} -vf scale=(iw*sar)*max({x}.1/(iw*sar)\,{y}.1/ih):ih*max({x}.1/(iw*sar)\,{y}.1/ih),crop={x}:{y} {outfile}'
    prun(cmd,debug=debug)
    fs = getFilesize(outfile)
    print(f"   ({procTime(timeStart)}), {fs}")
    return outfile
def runUpscale(srcfile):
    timeStart = time.time()
    print(Fore.GREEN + f"Upscaling 4x ({srcfile})" + Fore.RESET,end="",flush=True)
    cmd = f'/home/jw/src/sdc/upscale.sh {srcfile} > /dev/null 2>&1'
    prun(cmd,debug=True)
    dest = f"{g.esgrandir}/results/{os.path.basename(srcfile)}"
    dest = dest.replace(".mp4","_out.mp4")
    fs = getFilesize(dest)
    print(f"   ({procTime(timeStart)}), {fs}")

def runFade(filename):
    timeStart = time.time()
    print(Fore.GREEN + f"Fading in/out ({filename})" + Fore.RESET,end="",flush=True)
    cmd = f"{g.sdcdir}/fadeinout.sh {filename}"
    prun(cmd,debug=debug)
    print(Fore.GREEN + f"Moving to {dirname}/scaled_{id}.mp4" + Fore.RESET,end="",flush=True)
    cmd = f"mv {filename} {dirname}/scaled_{id}.mp4"
    prun(cmd,debug=debug)
    finalFile = f"{dirname}/scaled_{id}.mp4"
    fs = getFilesize(finalFile)
    print(f"   ({procTime(timeStart)}), {fs}")
    return finalFile
def runMeta(filename,settingsFile):
    timeStart = time.time()
    print(Fore.GREEN + f"Embedding metadata" + Fore.RESET,end="",flush=True)
    cmd=f"{g.sdcdir}/metaconfig.py -v {filename} -a {settingsFile}"
    prun(cmd,debug=debug)
    timeProc = time.time() - timeStart
    print(f"   ({timeProc})")

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -v, --videofile     filename
    -f, --xframes       add x interpolted frames
    -Q, --sequence      select which processes to deploy
                        Ex: 
                        XISCFUM     runs all the processes
                        XISCFM      runs all the processes except Upscaling (DEFAULT)
                        EIS         interpolate only
                        M           add metadata only
                        EISC        Interpolate and crop 
                        C           Crop only
                        
                            
                        X   Extract
                        I   Interpolate
                        S   Stitch
                        C   Crop 
                        F   Fade
                        U   Upscale
                        M   Metadata
    
    
    
'''
    print(rs)
    exit()


filename = f"{g.sdcdir}/test.mp4"
keyname = "duration"
interpx = 20
debug = False
sqeuence = "XISCFM"

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hdv:f:Q:", [
        "help",
        "debug",
        "videofile=",
        "xframes=",
        "sequence=",

    ])
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp();
    if opt in ("-d", "--debug"):
        debug = True
    if opt in ("-v", "--videofile"):
        filename = arg
    if opt in ("-f", "--xframes"):
        interx=int(arg)
    if opt in ("-Q", "--sequence"):
        sequence = arg


basename, dirname, fspec, srcfile = getFnames(filename)


print(f"dirname: {dirname}")
print(f"basename: {basename}")
print(f"srcfile:{srcfile}")




# ID=`echo ${FILENAME}|grep -o '[^/]*\.mp4'|awk -F"." '{print $1}'`
id = getID(filename)

dest_filename = f"{dirname}/scaled_{id}.mp4"
if os.path.exists(dest_filename):
    print(Fore.MAGENTA+f"File {dest_filename} already exists"+Fore.RESET)
    x = input(Fore.CYAN+"Delete (y/n)"+Fore.RESET)
    if x=='y':
        os.remove( f"{dirname}/scaled_{id}.mp4")
    else:
        exit()

print(Fore.GREEN)
print(f"┌──────────────────────────────────────────────")
print(f"│INPUT: {filename}")
print(f"└──────────────────────────────────────────────")
print(Fore.RESET)

if "X" in sqeuence: runExtract(srcfile)                                    #[X]
if "I" in sqeuence:runInterp(filename, interpx)                            #[I]
if "S" in sqeuence:srcfile = runStitch()                                   #[S]
if "C" in sqeuence:srcfile = runCrop(srcfile,512,278)                      #[C]
if "F" in sqeuence:srcfile = runFade(srcfile)                              #[F]
if "U" in sqeuence:runUpscale(srcfile)                                     #[U]
if "M" in sqeuence:metaFile=runMeta(srcfile,f"{dirname}/{id}_settings.txt")#[M]
#^ 'M' must happen AFTER everything else as envelope is NOT saved
print(Fore.GREEN)
print(f"┌──────────────────────────────────────────────")
print(f"│OUTPUT:   {srcfile}")
print(f"└──────────────────────────────────────────────")
print(Fore.RESET)











# echo "---------------------------------------------------------------------"
# echo "OUTPUT:   ${DIR}/scaled_${ID}.mp4 "
# echo "---------------------------------------------------------------------"
# #/bin/rm out.mp4 > /dev/null 2>&1
# #/bin/rm -rf ${DIR}/${ID}_upscaled > /dev/null 2>&1
# #/bin/rm -rf ${DIR}/${ID}*.png > /dev/null 2>&1
# #/bin/rm -rf ${DIR}/${ID}.mp4 > /dev/null 2>&1
# #/bin/rm -rf ${DIR}/${ID}_RIFE_x10_slomo_x10.mp4 > /dev/null 2>&1
#
# #Must clean, can use up to 35 GB
# /bin/rm -rf ${rifedir}/images
# /bin/rm -rf ${rifedir}/frames
#
#
