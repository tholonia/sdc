#!/bin/bash

if [ "${1}" = "-h" ]; then
  cat << EOF
  ${0} <full path>
EOF
  exit
fi

DIR=$(dirname $1)
FILENAME=$(basename $1)
echo "Dir: ${DIR}"
echo "File: ${FILENAME}"

FILENAME=$1
if [ "${FILENAME}" = "" ]; then
  echo "Missing filename"
  exit
fi
ho "Fading: ${FILENAME}"

DUR=`viduration.py -v ${FILENAME}|awk '{print $1}'`

ffmpeg -loglevel warning -y -i ${FILENAME} -vf "fade=t=in:st=0:d=3" -c:a copy /tmp/fout.mp4
ffmpeg -loglevel warning -y -i /tmp/fout.mp4 -vf "fade=t=out:st=${PDUR}:d=5" -c:a copy /tmp/fout2.mp4

mv /tmp/fout2.mp4 ${FILENAME}
