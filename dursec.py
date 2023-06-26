#!/bin/env python
import sys
import ffmpeg

filename = str(sys.argv[1]).strip(",")
vdat = ffmpeg.probe(filename)

print(round(float(vdat['format']['duration'])), end="")


