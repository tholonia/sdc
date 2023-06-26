#!/bin/env python
# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
from PIL import Image
import getopt, sys
import shutil
from datetime import datetime
import time
import uuid
import os
from pprint import pprint

def errprint(str):
    print(str, file=sys.stderr)
def showhelp():
    print("help")
    rs = '''
    -h, --help          show help

    -i, --image
    -t  --textfile
    -e, --encode
    -d  --decode
    -n  --notes
'''
    print(rs)


# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


# Encode data into image
def encode(imagename,textfile):
    image = Image.open(imagename, 'r')

    with open(textfile,'r') as file:
        data = file.read()
    newimg = image.copy()
    image.close()
    encode_enc(newimg, data)

    newimg.save(imagename)
    errprint(f"Saved: {imagename}")

# Decode the data in the image
def decode(imagename):
    image = Image.open(imagename, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

toencode = False
todecode = False
textfile = False
imagename = False
notes=""
# Main Function
argv = sys.argv[1:]
# print(sys.argv)

try:
    opts, args = getopt.getopt(argv, "hi:t:edn:", [
        "help",
        "image=",
        "textfile=",
        "encode",
        "decode",
        "notes=",
    ])
except Exception as e:
    print(str(e))
for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-n", "--notes"):
        notes = arg
    if opt in ("-i", "--image"):
        imagename = arg
        if not os.path.exists(imagename):
            errprint(f"ERROR: {imagename} does not exist")
            exit()
        else:
            errprint(f"FOUND: {imagename}")

    if opt in ("-t", "--textfile"):
        textfile = arg
        if not os.path.exists(textfile):
            errprint(f"ERROR: {textfile} does not exist")
            exit()
        else:
            errprint(f"FOUND: {textfile}")

    if opt in ("-e", "--encode"):
        toencode = True
        nowtime = datetime.now()
        tstamp = nowtime.isoformat().split('.')[0]
        dst = f"/home/jw/src/sdc/record/{tstamp}_{notes}.png"
        # subtract Datetime from epoch datetime
        errprint(f"ENCODING TO: {dst}")

    if opt in ("-d", "--decode"):
        todecode = True





if toencode:
    shutil.copy(imagename,dst)
    encode(dst,textfile)
if todecode:
    print(decode(imagename))
