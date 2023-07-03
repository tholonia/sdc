#!/bin/env python

import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
import ffmpeg
import subprocess
import shutil
# from proclib import prun, splitnonalpha, getID, procTime, getFilesize, getFnames, cleanTree, cleanWildcard
import proclib as p
import time
import procvars as g

init()

g.uid = round(time.time())

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -d, --debug          debug
    -v, --videofile     filename
    
    -Q, --sequence      select which processes to deployand in what order, default = 'SISCFM'

    -X, --xframes       add x interpolated frames
    -T, --tfilter       apply toss filter, values are 0.0 to 1.0, default = 0.5
    -V, --iversion      choose which version if interpolation.  Opensa are '1' or '2', default is 1
                        '-V 1' uses JPG format (default)
                        '-V 2' uses PNG format (and takes up massively more space)


-Q, --sequence examples:
                        ETISCFUM     extract -> toss -> interp -> stitch -> crop -> fade -> metadata
             (default)  EISCFM       extract -> interp -> stitch -> crop -> fade -> metadata
                        EIS          extract -> interp -> stitch
                        M            Add metadata only
                        EISC         Interpolate -> crop 
                        C            Crop only
                        
                            
                        E   Extract images from video (at 15 fps)   (V>I)
                        T   Toss by filter                          (I>nI)
                        I   Interpolate                             (I>nI)
                        S   Stitch                                  (I>V)
                        P   Perlabel                                (V>nV)
                        C   Crop                                    (V>nV)
                        F   Fade                                    (V>V)
                        U   Upscale                                 (V>nV)
                        M   Add Metadata                            (V>V)
    
                        V = video, I = Images, > = transform
                        (V-nV) = "video to new video"
                        (V-V) = "video to same video"
                        (V-I) = "video to images"
                        (I-nI) = "Images to new images"
    
    
'''
    print(rs)
    exit()


filename = f"{g.sdcdir}/test.mp4"
keyname = "duration"
interpx = 20
tossFilter = 0.5
debug = False
sequence = "XISCFM"
iversion = 1

if len(sys.argv) == 1:
    showhelp()

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hdv:f:Q:X:T:V:", [
        "help",
        "debug",
        "videofile=",
        "sequence=",
        "xframes=",
        "tfilter=",
        "iversion=",

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
    if opt in ("-Q", "--sequence"):
        sequence = arg

    if opt in ("-X", "--xframes"):
        interpx=int(arg)
    if opt in ("-T", "--tfilter"):
        tossFilter = float(arg)
    if opt in ("-V", "--iversion"):
        iversion = int(arg)

basename, dirname, fspec, srcfile = p.getFnames(filename)


print(f"dirname: {dirname}")
print(f"basename: {basename}")
print(f"srcfile:{srcfile}")

# exit()


# ID=`echo ${FILENAME}|grep -o '[^/]*\.mp4'|awk -F"." '{print $1}'`
id = p.getID(filename)

dest_filename = f"{dirname}/scaled_{id}.mp4"
if os.path.exists(dest_filename):
    print(Fore.MAGENTA+f"File {dest_filename} already exists"+Fore.RESET)
    x = input(Fore.CYAN+"Delete (y/n)"+Fore.RESET)
    if x=='y':
        os.remove( f"{dirname}/scaled_{id}.mp4")
    else:
        exit()

print(Fore.RED)
print(f"┌──────────────────────────────────────────────")
print(f"│INPUT: {srcfile}")
print(f"└──────────────────────────────────────────────")
print(Fore.RESET)

imgdir = ""
for q in sequence:
    match q:
        case "E": #[E]
            imgdir = p.runExtract(srcfile,debug=debug)
            print(Fore.CYAN+f"Extracted {srcfile}"+Fore.RESET)
        case "T": #[T]
            imgdir, pctTossed, totalImg = p.runToss(imgdir,tossFilter,debug=debug)
            print(Fore.CYAN + f"Filter {tossFilter} tossed {pctTossed}% ({round(totalImg*(pctTossed/100))}) of {totalImg} images" + Fore.RESET)
        case "I": #[I]
            imgdir, totalImg = p.runInterp(interpx, version=iversion,debug=debug)
            print(Fore.CYAN + f"Interpolated images (V{iversion}) by {interpx}, {totalImg} total images " + Fore.RESET)
        case "S": #[S]
            srcfile, namedfile = p.runStitch(imgdir,debug=debug)
            print(Fore.CYAN+f"Stitched images in {dirname} to {srcfile} ({namedfile})"+Fore.RESET)
        #- temporarily disabled
        case "P": #[P]
            srcfile = p.runPerlabel(srcfile,debug=debug)
            print(Fore.CYAN+f"Perlabeled {srcfile}"+Fore.RESET)
        case "C": #[C]
            srcfile = p.runCrop(srcfile,512,278,debug=debug)
            print(Fore.CYAN+f"Cropped to {srcfile} to 512x278"+Fore.RESET)
        case "F": #[F]
            srcfile = p.runFade(f"{srcfile}",debug=debug)
            print(Fore.CYAN+f"Faded to {srcfile}"+Fore.RESET)
        case "U": #[U]
            srcfile = p.runUpscale(srcfile,debug=debug)
            print(Fore.CYAN+f"Upscaled to {srcfile}"+Fore.RESET)
        case "M": #[M]
            metaFile=p.runMeta(srcfile,f"{dirname}/{id}_settings.txt",debug=debug)
            print(Fore.CYAN+f"Updating metadata on {srcfile}"+Fore.RESET)

#^ 'M' must happen AFTER everything else as envelope is NOT saved
print(Fore.GREEN)
print(f"┌──────────────────────────────────────────────")
print(f"│OUTPUT:  vlc {srcfile}")
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
