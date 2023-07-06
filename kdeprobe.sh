#!/bin/bash

/home/jw/miniforge3/bin/ffprobe -show_streams  -print_format json $1 > /tmp/kdeprobe.txt
/bin/kate /tmp/kdeprobe.txt



