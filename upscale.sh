#!/bin/bash
cd /home/jw/src/Real-ESRGAN

./inference_realesrgan_video.py -n RealESRGAN_x2plus -i $1 --face_enhance
#./inference_realesrgan.py -n RealESRGAN_x4plus -i $1 --face_enhance > /dev/null 2>&1
cd -
