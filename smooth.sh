#!/bin/bash -x

FILE=$1
PTS=$2

#~/src/sdc/label.py -f $FILE -l original

ffmpeg -loglevel panic -y -i ${FILE}  -vf "setpts=${PTS}*PTS"  /tmp/outs.mp4
~/src/sdc/interpolate /tmp outs.mp4
mv /tmp/_FIN_outs.mp4 ./slowed_${PTS}_${FILE}

#~/src/sdc/label.py -f rife_slow_interp.mp4 -l RIFE_slow_interpolated

