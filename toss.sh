#!/bin/bash -x

FILE=$1
DIR=`date +%Y%M%d%H%M%S`

FILTER=$2
REMAKE=$3

if [ "$FILTER" = "" ]; then
  FILTER="0.5"
fi
if [ "$REMAKE" = "" ]; then
  REMAKE="-n"
fi
FILENAME=$(basename $1)

mkdir /tmp/${DIR}
cp ${FILE} /tmp/${DIR}
cd /tmp/${DIR}
ffmpeg -y -i ${FILENAME} -r 15/1 %09d.png

ls -al /tmp/${DIR}/${FILENAME}
~/src/sdc/toss.py -d /tmp/${DIR} -f ${FILTER} ${REMAKE}

ffmpeg -y -framerate 15 -pattern_type glob -i "/tmp/${DIR}/filtered/*.png"  -c:v libx264 -pix_fmt yuv420p ~/BATCH3/T${FILTER}_${FILENAME}
 
 