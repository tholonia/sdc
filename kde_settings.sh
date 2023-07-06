#!/bin/bash
/home/jw/src/sdc/metaconfig.py -v $1 > /tmp/kdeprobe.txt  2>&1  && /bin/subl /tmp/kdeprobe.txt
