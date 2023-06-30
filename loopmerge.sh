#!/bin/bash -x
F1=$1
F2=$2

if [ "$F1" = "" ]; then
	echo "Missing filename 1"
	exit
fi	
if [ "$F2" = "" ]; then
	F2="$F1"
fi	

# copy end frame of v1
#ffmpeg -loglevel warning -y -sseof -3 -i `pwd`/20230625140347.mp4 -update 1 -q:v 1 /tmp/00_LFRAME.png
ffmpeg -sseof -3 -i `pwd`/20230625140347.mp4 -vsync 0 -q:v 31 -update true /tmp/00_LFRAME.png
cp /tmp/00_LFRAME.png /tmp/01_LFRAME.png
cp /tmp/00_LFRAME.png /tmp/02_LFRAME.png
cp /tmp/00_LFRAME.png /tmp/03_LFRAME.png
cp /tmp/00_LFRAME.png /tmp/04_LFRAME.png
cp /tmp/00_LFRAME.png /tmp/05_LFRAME.png
cp /tmp/00_LFRAME.png /tmp/06_LFRAME.png
cp /tmp/00_LFRAME.png /tmp/07_LFRAME.png
cp /tmp/00_LFRAME.png /tmp/08_LFRAME.png


#copy first frame of v2
ffmpeg -loglevel warning -y -i `pwd`/20230625140347.mp4 -vf "select=eq(n\,0)" -q:v 3 /tmp/01_FFRAME.png
cp /tmp/01_FFRAME.png /tmp/01_FFRAME.png
cp /tmp/01_FFRAME.png /tmp/02_FFRAME.png
cp /tmp/01_FFRAME.png /tmp/03_FFRAME.png
cp /tmp/01_FFRAME.png /tmp/04_FFRAME.png
cp /tmp/01_FFRAME.png /tmp/05_FFRAME.png
cp /tmp/01_FFRAME.png /tmp/06_FFRAME.png
cp /tmp/01_FFRAME.png /tmp/07_FFRAME.png
cp /tmp/01_FFRAME.png /tmp/08_FFRAME.png

#mergem them

ffmpeg -loglevel warning -y -framerate 15 -pattern_type glob -i '/tmp/*FRAME.png'  -c:v libx264 -pix_fmt yuv420p /tmp/FL.mp4

#interpolate them

~/src/rife/INTERP /tmp/FL.mp4 30

#merge all three videso together

echo "file '`pwd`/${F1}'" > /tmp/catvid
echo "file '/tmp/i30_FL.mp4'" >> /tmp/catvid


ffmpeg -loglevel warning -y -safe 0 -f concat -i /tmp/catvid -c copy `pwd`/LP_${F1}output.mp4


