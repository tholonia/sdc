#!/bin/bash

ID=$1
CFG=$2
S=$3
M=$4
#. /home/jw/store/src/sdc/PENV

cd ~/BATCH3

function makevids() {
    rm *.png
    echo "=============================================== Extract imgs === (ffmpeg -loglevel warning -y -i `pwd`/${ID}.mp4  -r 15/1 ${ID}_%09d.png)"
    ffmpeg -loglevel warning -y -i `pwd`/${ID}.mp4  -r 15/1 ${ID}_%09d.png
    echo "=============================================== Add piv labels = (~/src/sdc/perlabel.py -d `pwd` -i ${ID} -s `pwd`/${ID}_settings.txt > tmp.sh)"
    ~/src/sdc/perlabel.py -d `pwd` -i ${ID} -s `pwd`/${ID}_settings.txt > tmp.sh
    echo "=============================================== Run tmp.sh ===== (sh -x ./tmp.sh)"
    sh -x ./tmp.sh
    echo "=============================================== Stitch Video === (ffmpeg -y -loglevel warning -framerate 15 -pattern_type glob -i '*.png'  -c:v libx264 -pix_fmt yuv420p R${ID}.mp4)"
    ffmpeg -y -loglevel warning -framerate 15 -pattern_type glob -i '*.png'  -c:v libx264 -pix_fmt yuv420p R${ID}.mp4
    echo "=============================================== Interp frames == (INTERP `pwd`/R${ID}.mp4 ${S})"
    INTERP `pwd`/R${ID}.mp4 ${S}
    echo "=============================================== Label video ==== (~/src/sdc/label.py -f `pwd`/i${S}_R${ID}.mp4  -l del-m@${M}-s@${S})"
    ~/src/sdc/label.py -f `pwd`/i${S}_R${ID}.mp4  -l del-m@${M}-s@${S}
    echo "=============================================== Clean PNGs ===== (rm *.png)"
    rm *.png
}

function mergevids() {
    echo "=========================================== Preparing tmp (rm -rf tmp/;mkdir tmp/;cp ~/src/sdc/zzzzz.mp4 tmp/;cp i*.mp4 tmp/) ====="
    rm -rf tmp/
    mkdir tmp/
    cp ~/src/sdc/zzzzz.mp4 tmp/
    cp i*.mp4 tmp/
    echo "=========================================== Merging ===== (mergevid_512x512.py --dir `pwd`/tmp --destdir `pwd`/tmp --rename merge_temp.mp4 --verbose)"
    mergevid_512x512.py --dir `pwd`/tmp --destdir `pwd`/tmp --rename merge_temp.mp4 --verbose
}

makevids
mergevids

DPM__ 2M
DPM2 a