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
    rs = f'''
    -h, --help          show help
    -d, --debug          debug
    -v, --videofile     filename
    
    -Q, --sequence      select which processes to deployand in what order, default = 'SISCFM'

    -R, --cropto        crop to <wwidth>@<ratio>  Ex: 512@16:9
    -X, --xframes       add x interpolated frames
    -T, --tfilter       apply toss filter, values are 0.0 to 1.0, default = 0.5
    -V, --iversion      choose which version if interpolation.  Opensa are '1' or '2', default is 1
                        '-V 1' uses JPG format (default)
                        '-V 2' uses PNG format (and takes up massively more space)
    -K, --keep          Keep ever nth frame when tossing                        
    -Y, --fps           Extraction FPS                        

    -m, --usetmpdir     tmpdir to use
    -A, --AVI           use lossless AVI format
    -Z, --compress      convert AVI to MP4
    -W, --rotcolor      rotate colors
    
-Q, --sequence examples:
                        OCFUM        smooth -> crop -> fade -> metadata
                        ETISCFUM     extract -> toss -> interp -> stitch -> crop -> fade -> metadata
             (default)  EISCFM       extract -> interp -> stitch -> crop -> fade -> metadata
                        EIS          extract -> interp -> stitch
                        M            Add metadata only
                        EISC         Interpolate -> crop 
                        C            Crop only
                        
                            
                        E   Extract images from video (at {fps} fps)   (V>I)  -Y, --fps <n>
                        W   Rotate colors                           (I>I) 
                        O   Smooth (ETIS loop)                      (V>nV) 
                        T   Toss by filter                          (I>nI) -K,--keep <n>
                        I   Interpolate                             (I>nI) -X, --xframes = <n>, -T, --tfilter <0.0 - 1.0>
                        S   Stitch                                  (I>V)
                        P   Perlabel                                (V>nV)
                        C   Crop                                    (V>nV) -R, --cropto <width>@<ratio>, default = 512@16:9
                        F   Fade                                    (V>V)
                        U   Upscale                                 (V>nV)
                        M   Add Metadata                            (V)
                        Z   Convert from AVI to MP4                 (V>nV)
                            
                        V = video, I = Images, > = transform
                        (V-nV) = "video to new video"
                        (V-V) = "video to same video"
                        (V-I) = "video to images"
                        (I-nI) = "Images to new images"
    
                        'cropto' example args:
                        
                            512@16:9   convert 512x512 to 512x288
                            768@16:9   convert 768x520 to 768x432
    
'''
    print(rs)
    exit()


filename = f"{g.sdcdir}/test.mp4"
keyname = "duration"
interpx = 20
tossFilter = 0.5 #0.5
debug = False
keep = False
cropwidth = 512
cropratio = "16:9"
cropheight = 288
sequence = "XISCFM"
avi2mp4 = False
iversion = 1
ext = "mp4"
fps = g.fps
rotcolor = False
if len(sys.argv) == 1:
    showhelp()

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hdv:f:Q:X:T:V:K:R:m:AZY:W", [
        "help",
        "debug",
        "videofile=",
        "sequence=",
        "xframes=",
        "tfilter=",
        "iversion=",
        "cropto=",
        "usetmpdir=",
        "lossless",
        "compress",
        "fps=",
        "rotcolor",

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
    if opt in ("-A", "--lossless"):
        ext="avi"
    if opt in ("-Z", "--compress"):
        avi2mp4=True
    if opt in ("-Y", "--fps"):
        fps = int(arg)
    if opt in ("-W", "--rotcolor"):
        rotcolor = True

    if opt in ("-K", "--keep"):
        keep=int(arg)
    if opt in ("-X", "--xframes"):
        interpx=int(arg)
    if opt in ("-T", "--tfilter"):
        tossFilter = float(arg)
    if opt in ("-V", "--iversion"):
        iversion = int(arg)
    if opt in ("-R", "--cropto"):
        cropwidth, cropheight = p.cropdims(arg)
    if opt in ("-m", "--tmpdir"):
        g.tmpsir = arg


basename, dirname, fspec, srcfile = p.getFnames(filename)


print(f"dirname: {dirname}")
print(f"basename: {basename}")
print(f"srcfile:{srcfile}")

# exit()


# ID=`echo ${FILENAME}|grep -o '[^/]*\.{ext}'|awk -F"." '{print $1}'`
id = p.getID(filename)

dest_filename = f"{dirname}/scaled_{id}.{ext}"
if os.path.exists(dest_filename):
    print(Fore.MAGENTA+f"File {dest_filename} already exists"+Fore.RESET)
    x = input(Fore.CYAN+"Delete (y/n)"+Fore.RESET)
    if x=='y':
        os.remove( f"{dirname}/scaled_{id}.{ext}")
    else:
        exit()

print(Fore.RED)
print(f"┌──────────────────────────────────────────────")
print(f"│INPUT: {srcfile}")
print(f"└──────────────────────────────────────────────")
print(Fore.RESET)


# p.cleanTree2("/fstmp")
try:os.mkdir("/fstmp/images")
except:pass
try:os.mkdir("/fstmp/filtered")
except:pass
try:os.mkdir("/fstmp/tossed")
except:pass
try:os.mkdir("/fstmp/frames")
except:pass

imgdir = ""
for q in sequence:
    match q:
        case "E": #[E]xtract]  IN:video OUT:images
            # print(f"srcfile={srcfile}")
            #@ convert to AVI is MP4
            if srcfile.find(".mp4") != -1:
                cmd = f"ffmpeg -i {srcfile} -y -loglevel warning -c:v libx264 -c:a libmp3lame -crf 0 {g.tmpdir}/wasmp4.avi"
                p.prun(cmd,debug=debug)
                srcfile = f"{g.tmpdir}/wasmp4.avi"
                # input("waiting...")

            # if "T" in sequence:
            #     #^ if tossing is ON
            #     cmd = f"ffmpeg -y -loglevel warning -i {srcfile} -vf mpdecimate=hi=6400:lo=1200:frac=0.3,setpts=N/FRAME_RATE/TB  -vcodec libx264 -crf 0 {g.tmpdir}/tmp.avi"
            #     # cmd = f"ffmpeg -y -loglevel warning -i {srcfile} -vf mpdecimate=hi=12800:lo=1200:frac=0.33,setpts=N/FRAME_RATE/TB -vcodec libx264 -crf 0 {g.tmpdir}/tmp.avi"
            #     p.prun(cmd,debug=debug)
            #     srcfile = f"{g.tmpdir}/tmp.avi"
            #     # input("waiting...")
            #     if os.path.isfile(f"{g.tmpdir}/wasmp4.avi"):
            #         os.system(f"rm {g.tmpdir}/wasmp4.avi")

            imgdir = p.runExtract(srcfile,debug=debug,ext=ext,fps=fps,did=id[:2])
            print(Fore.CYAN+f"Extracted {srcfile}"+Fore.RESET)
            time.sleep(2)
        case "W": #[E] Rotate Color]  IN:images OUT:images
            cmd = "rotcolor.py"
            p.prun(cmd,debug=debug)
        case "T": #[T]oss]  IN:images OUT:images
            imgdir, pctTossed, totalImg, filtered, tossed = p.runToss(imgdir,tossFilter,debug=debug, keep=keep)
            print(Fore.CYAN + f"Processed {totalImg}, Kept {filtered} in {g.tmpdir}/filtered, tossed {tossed} in {g.tmpdir}/tossed ({pctTossed}%)"+Fore.RESET)
            time.sleep(2)
        case "O": #[sm[O]oth]  IN:file OUT:file
            print(Fore.CYAN + f"Tossing {srcfile}"+Fore.RESET)
            if not debug == False:
                D="-d"
            else:
                D=""
            print("————————————————————————————————————————————— [1/8] ————————————————————————————————————————————————————")
            imgdir = p.runExtract(srcfile, debug=debug, ext=ext)
            imgdir, pctTossed, totalImg, filtered, tossed = p.runToss(imgdir, tossFilter, debug=debug, keep=2)
            imgdir, totalImg = p.runInterp(8, imgdir=imgdir, version=2, debug=debug)

            p.cleanTree2("/fstmp/tossed")

            # cmd = f"makeauto.py -v {srcfile}          -Q ETI -V 2 -K 2 -X 8 -A {D}" #^ extract to /fstmp/images
            # p.prun(cmd,debug=debug)
            # p.cleanTree2("/fstmp/images")
            # cmd = "mv /fstmp/frames/* /fstmp/images"
            # os.system(cmd)
            # time.sleep(2)
            print(f"————————————————————————————————————————————— [2/8] ———————————————————————————————————————————————————— ")
            # exit()
            # imgdir = "/fstmp/images"
            imgdir, pctTossed, totalImg, filtered, tossed = p.runToss(imgdir, tossFilter, debug=debug, keep=3)
            imgdir, totalImg = p.runInterp(7, imgdir=imgdir, version=2, debug=debug)

            p.cleanTree2("/fstmp/images")
            cmd = "mv /fstmp/frames/* /fstmp/images"
            os.system(cmd)
            time.sleep(2)
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q TI -V 2 -K 3 -X 7 -A {D}"

            print("————————————————————————————————————————————— [3/8] ————————————————————————————————————————————————————")
            imgdir, pctTossed, totalImg, filtered, tossed = p.runToss(imgdir, tossFilter, debug=debug, keep=4)
            imgdir, totalImg = p.runInterp(6, imgdir=imgdir, version=2, debug=debug)
            p.cleanTree2("/fstmp/images")
            cmd = "mv /fstmp/frames/* /fstmp/images"
            os.system(cmd)
            time.sleep(2)
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q TI -V 2 -K 4 -X 6 -A {D}"
            print("————————————————————————————————————————————— [4/8] ————————————————————————————————————————————————————")
            imgdir, pctTossed, totalImg, filtered, tossed = p.runToss(imgdir, tossFilter, debug=debug, keep=5)
            imgdir, totalImg = p.runInterp(5, imgdir=imgdir, version=2, debug=debug)
            p.cleanTree2("/fstmp/images")
            cmd = "mv /fstmp/frames/* /fstmp/images"
            os.system(cmd)
            time.sleep(2)
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q TI -V 2 -K 5 -X 5 -A {D}"
            print("————————————————————————————————————————————— [5/8] ————————————————————————————————————————————————————")
            imgdir, pctTossed, totalImg, filtered, tossed = p.runToss(imgdir, tossFilter, debug=debug, keep=6)
            imgdir, totalImg = p.runInterp(4, imgdir=imgdir, version=2, debug=debug)
            p.cleanTree2("/fstmp/images")
            cmd = "mv /fstmp/frames/* /fstmp/images"
            os.system(cmd)
            time.sleep(2)
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q TI -V 2 -K 6 -X 4 -A {D}"
            print("————————————————————————————————————————————— [6/8] ————————————————————————————————————————————————————")
            imgdir, pctTossed, totalImg, filtered, tossed = p.runToss(imgdir, tossFilter, debug=debug, keep=7)
            imgdir, totalImg = p.runInterp(3, imgdir=imgdir, version=2, debug=debug)
            p.cleanTree2("/fstmp/images")
            cmd = "mv /fstmp/frames/* /fstmp/images"
            os.system(cmd)
            time.sleep(2)
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q TI -V 2 -K 7 -X 3 -A {D}"
            print("————————————————————————————————————————————— [7/8] ————————————————————————————————————————————————————")
            imgdir, pctTossed, totalImg, filtered, tossed = p.runToss(imgdir, tossFilter, debug=debug, keep=8)
            imgdir, totalImg = p.runInterp(2, imgdir=imgdir, version=2, debug=debug)
            p.cleanTree2("/fstmp/images")
            cmd = "mv /fstmp/frames/* /fstmp/images"
            os.system(cmd)
            time.sleep(2)
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q TI -V 2 -K 8 -X 2 -A {D}"
            print("————————————————————————————————————————————— [8/8] ————————————————————————————————————————————————————")
            imgdir, totalImg = p.runInterp(6, imgdir=imgdir, version=2, debug=debug)
            srcfile = p.runStitch(imgdir, version=2, ext=ext, debug=debug)


            # print("————————————————————————————————————————————— [1/8] ————————————————————————————————————————————————————")
            # cmd = f"makeauto.py -v {srcfile}          -Q ETIS -V 2 -K 2 -X 8 -A {D}"
            # p.prun(cmd,debug=debug)
            # print("————————————————————————————————————————————— [2/8] ————————————————————————————————————————————————————")
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q ETIS -V 2 -K 3 -X 7 -A {D}"
            # p.prun(cmd,debug=debug)
            # print("————————————————————————————————————————————— [3/8] ————————————————————————————————————————————————————")
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q ETIS -V 2 -K 4 -X 6 -A {D}"
            # p.prun(cmd,debug=debug)
            # print("————————————————————————————————————————————— [4/8] ————————————————————————————————————————————————————")
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q ETIS -V 2 -K 5 -X 5 -A {D}"
            # p.prun(cmd,debug=debug)
            # print("————————————————————————————————————————————— [5/8] ————————————————————————————————————————————————————")
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q ETIS -V 2 -K 6 -X 4 -A {D}"
            # p.prun(cmd,debug=debug)
            # print("————————————————————————————————————————————— [6/8] ————————————————————————————————————————————————————")
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q ETIS -V 2 -K 7 -X 3 -A {D}"
            # p.prun(cmd,debug=debug)
            # print("————————————————————————————————————————————— [7/8] ————————————————————————————————————————————————————")
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q ETIS -V 2 -K 8 -X 2 -A {D}"
            # p.prun(cmd,debug=debug)
            # print("————————————————————————————————————————————— [8/8] ————————————————————————————————————————————————————")
            # cmd = f"makeauto.py -v {g.tmpdir}/stitched.{ext}  -Q EIS -V 2 -X 2 -A {D}"
            # p.prun(cmd,debug=debug)

            # if ext == "avi":
            #     cmd=f"ffmpeg -loglevel panic -i {g.tmpdir}/stitched.avi {g.tmpdir}/stitched.mp4"
            #     p.prun(cmd,debug=debug)
            srcfile=f"{g.tmpdir}/stitched.{ext}"

            print(Fore.CYAN + f"Tossed to {srcfile}"+Fore.RESET)
            time.sleep(2)

        case "I": #[I]nterpolate] IN:images OUT:images
            imgdir, totalImg = p.runInterp(interpx, imgdir=imgdir,version=iversion,debug=debug)
            print(Fore.CYAN + f"Interpolated images (V{iversion}) by {interpx}, {totalImg} total images " + Fore.RESET)
            time.sleep(2)
        case "S": #[S]titch  IN:images OUT:video
            srcfile = p.runStitch(imgdir,version=iversion,ext=ext,debug=debug)
            print(Fore.CYAN+f"Stitched images in {dirname} to {srcfile} "+Fore.RESET)
            time.sleep(2)
        case "P": #[P]erlabel
            srcfile = p.runPerlabel(srcfile,ext=ext,debug=debug)
            print(Fore.CYAN+f"Perlabeled {srcfile}"+Fore.RESET)
            time.sleep(2)
        case "C": #[C]rop
            srcfile = p.runCrop(srcfile,cropwidth,cropheight,ext=ext,debug=debug)
            print(Fore.CYAN+f"Cropped to {srcfile} to {cropwidth}x{cropheight}"+Fore.RESET)
            time.sleep(2)
        case "F": #[F]ade
            srcfile = p.runFade(f"{srcfile}",ext=ext,debug=debug)
            print(Fore.CYAN+f"Faded to {srcfile}"+Fore.RESET)
            time.sleep(2)
        case "U": #[U]pscale
            srcfile = p.runUpscale(srcfile,ext=ext,debug=debug)
            print(Fore.CYAN+f"Upscaled to {srcfile}"+Fore.RESET)
            time.sleep(2)
        case "M": #[M]etadata
            metaFile=p.runMeta(srcfile,f"{dirname}/{id}_settings.txt",debug=debug)
            print(Fore.CYAN+f"Updating metadata on {srcfile}"+Fore.RESET)
            time.sleep(2)
        case "Z": #[compress]
            outfile = srcfile.replace("avi", "mp4")
            cmd = f"ffmpeg -loglevel warning -y -i  -vcodec hevc_nvenc {srcfile} {outfile}"
            p.prun(cmd, debug=debug)
            srcfile = outfile

#^ 'M' must happen AFTER everything else as envelope is NOT saved
print(Fore.GREEN)
print(f"┌──────────────────────────────────────────────")
print(f"│OUTPUT:  vlc {srcfile}")
print(f"└──────────────────────────────────────────────")
print(Fore.RESET)











# echo "---------------------------------------------------------------------"
# echo "OUTPUT:   ${DIR}/scaled_${ID}.{ext} "
# echo "---------------------------------------------------------------------"
# #/bin/rm out.{ext} > /dev/null 2>&1
# #/bin/rm -rf ${DIR}/${ID}_upscaled > /dev/null 2>&1
# #/bin/rm -rf ${DIR}/${ID}*.png > /dev/null 2>&1
# #/bin/rm -rf ${DIR}/${ID}.{ext} > /dev/null 2>&1
# #/bin/rm -rf ${DIR}/${ID}_RIFE_x10_slomo_x10.{ext} > /dev/null 2>&1
#
# #Must clean, can use up to 35 GB
# /bin/rm -rf ${rifedir}/images
# /bin/rm -rf ${rifedir}/frames
#
#
