#!/bin/env python

import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
import ffmpeg
import subprocess
import shutil
from PIL import Image, ImageOps, UnidentifiedImageError, ImageFile
import proclib as p
import proclib
from proclib import prun, splitnonalpha, getID, procTime, getFilesize
import time
from colorama import Fore, init
init()

ImageFile.LOAD_TRUNCATED_IMAGES = True

timestamp = round(time.time())

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -d, --dir           dir
'''
    print(rs)
    exit()



locationpath = os.getcwd()
dirname = False
basename = False

verbose = False

# print("args:",len(sys.argv))
if len(sys.argv) == 0:
    showhelp()

#^ if there is only one argument with no flags, then assume it is a filename
if len(sys.argv) <3:
    # print("1args")
    # pprint(sys.argv)
    filename =  sys.argv[0]
    basename = os.path.basename(locationpath)
    dirname = os.path.dirname(locationpath)

    fspec = False
else:
    print("multiargs")
    pprint(sys.argv)
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hvd:", [
            "help",
            "verbose",
            "dir",
        ])
    except Exception as e:
        print(str(e))

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            showhelp();
        if opt in ("-v", "--verbose"):
            debug = True;
        if opt in ("-d", "--dir"):
            locationpath = True;


basename,dirname,fspec,srcfile = proclib.getFnames(locationpath)

p.errprint(f"dirname: {dirname}")
p.errprint(f"basename: {basename}")
p.errprint(f"srcfile:{srcfile}")
p.errprint(f"fspec:{fspec}")
id = getID(filename)
p.errprint(f"ID: [{id}]")

#-------------------------------------------------------------------------


#^ first make thumbs

css = """
<style>
img {
    float: left;
    width: 50px;
    /* height: 50px;*/
    /* prob. you dont need this */
    padding: 5px;
    margin: 5px;
    border:1px solid red;
}
</style>
"""
dirs = [x[0] for x in os.walk(dirname) if x[0] != "."]

# all_imgs = False
ct = 1
border_color = "black"

topfile = open("ALL_ALLFILES.html","w")

for d in dirs:
    png_imgs = glob.glob(f"{d}/*.png")
    gif_imgs = glob.glob(f"{d}/*.gif")
    jpg_imgs = glob.glob(f"{d}/*.jpg") #^ too many
    all_imgs = png_imgs+jpg_imgs+gif_imgs
    # all_imgs = png_imgs+jpg_imgs
    #^ now have all images in this dir
    # print(len(all_imgs))

    cropped_imgs = []
    for i in all_imgs:
        if i.find("cropped") != -1:
            cropped_imgs.append(i)
    all_imgs = cropped_imgs

    #^ we really onyl want to cropped images


    if len(all_imgs) > 0:
        if not os.path.exists(f"/tmp{d}"):
            p.errprint(Fore.CYAN + f"making: /tmp{d}" + Fore.RESET)
            try: os.makedirs(f"/tmp{d}")
            except: pass


        #^ create thumbs
        page = open(f"{d}/_ALLIMGS.html","w")

        page.write(css)
        page.write(f"\n<h2>{d}</h2>\n")
        all_imgs = sorted(all_imgs)
        for img in all_imgs:
            timg = f"/tmp{img}"
            if timg.find(".png") != -1:
                border_color="pink"
            if timg.find(".gif") != -1:
                border_color="green"
            if timg.find(".jpg") != -1:
                border_color="black"

            if not os.path.exists(timg):
                try:
                    pimg = Image.open(img)
                    pimg.thumbnail((50,50))
                    if verbose:
                        p.errprint(Fore.GREEN + f"({ct}) Saving to: {timg}" + Fore.RESET)
                    else:
                        p.errprint(ct,end="\r")
                    pimg.save(timg)
                    page.write(f"<a target='_blank' href='{img}'><img style='border:2px solid {border_color}' src='{timg}'></a>\n")
                    # print(f"<a target='_blank' href='{img}'><img style='border:2px solid {border_color}' src='{timg}'></a>",end="")
                except UnidentifiedImageError:
                    os.remove(img)
                    p.errprint(Fore.MAGENTA+f"Removing: {img}"+Fore.RESET)
                except Image.DecompressionBombError:
                    p.errprint(Fore.RED+f"Image too big: {img}"+Fore.RESET)
                except Image.DecompressionBombWarning:
                    p.errprint(Fore.RED+f"Image too big: {img}"+Fore.RESET)
            ct += 1
        page.write("<div style='clear: both'></div>\n")
        page.close()
        p.errprint(Fore.WHITE + f"Wrote file {d}/_ALLIMGS.html" + Fore.RESET)
        topfile.write(f"<a href='{d}/_ALLIMGS.html' target='_blank'>{d}</a></br>\n")
        topfile.flush()
topfile.close()
