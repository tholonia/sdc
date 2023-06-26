#!/bin/bash
DUR=`viduration.py -v /home/jw/src/sdc/safe/vids/finished/20230626102335.mp4|awk '{print $3}'`
#echo ${DUR}
PDUR=$((-5+$DUR))
#echo ${PDUR}
ffmpeg -loglevel warning -y -i $1 -vf 'fade=t=in:st=0:d=3' -c:a copy /tmp/fout.mp4
ffmpeg -loglevel warning -y -i /tmp/fout.mp4 -vf "fade=t=out:st=${PDUR}:d=5" -c:a copy /tmp/fout2.mp4
