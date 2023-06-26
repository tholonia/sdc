#!/bin/bash
#D="safe/vids"
#F="PREPOST_ddim_chillou.mp4"

D=$1  # directory
F=$2  # filename

#^ make 60 fps
echo "ffmpeg -y -i ${D}/${F} -filter:v "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120'"  /tmp/out.mp4"
ffmpeg -y -i ${D}/${F} -filter:v "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=120'"  /tmp/out.mp4
#ffmpeg -y -i ${D}/${F} -crf 1 -vf "minterpolate=fps=60:mi_mode=blend:me_mode=bidir:vsbmc=1"  /tmp/out.mp4
#^ make 2x
#ffmpeg -y -i /tmp/out.mp4  -vf 'setpts=2*PTS'  /tmp/out2.mp4
#^ interpolate
cp /tmp/out.mp4 ${D}/_FIN_${F}
# ffmpeg -y -i /tmp/out2.mp4  -filter:v "minterpolate=mi_mode=2" ${D}/_FIN_${F}

