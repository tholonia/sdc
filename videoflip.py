#!/bin/env python

import ffmpeg
import getopt, sys

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -i, --input         input file
    -o, --output         output file
'''
    print(rs)

inputfile = False
outputfile = False

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hi:o:", [
        "help",
        "--input",
        "--output",
    ])
except Exception as e:
    print(str(e))
for opt, arg in opts:
    if opt in ("-h", "--help"):
        inputfile = arg
    if opt in ("-i", "--input"):
        showhelp()
    if opt in ("-o", "--output"):
        outputfile = arg






stream = ffmpeg.input(inputfile)
stream = ffmpeg.hflip(stream)
stream = ffmpeg.output(stream, outputfile)
ffmpeg.run(stream)

