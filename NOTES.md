#!/bin/bash

### Video instructions for SD training

https://www.youtube.com/watch?v=Ep4T8fyy2LE
	11:24 setting up hypernet



## Convert (imagemagick/ffmpeg)
Resise to width keeing the height proportional
`mogrify -resize 768x *.gif`

Remove all empty space around image
`for f in *.gif; do echo $f; convert $f -flatten -fuzz 1% -trim +repage $f; done`

rescale (use ffmpeg to use CUDA)

`for f in *.gif; do echo $f; ffmpeg -y -loglevel warning -i $f -vf scale=-1:512 out_$f ; done`

fill out

`for f in ./img*.png; do echo $f;convert $f  -resize 768x512 -background black -gravity center -extent 768x512 $f ; done`


convert while ot trans to black

mogrify -background black -alpha background -alpha off -negate -transparent white *.gif 


`??`

for f in ./*.png; do echo $f;convert $f -fuzz 45% -transparent black $f ; done




## pacman

reinstall ffmpeg, first uninstall with 
```
sudo pacman -Rdd ffmpeg
```



# ffmpeg examples



## AVI to MP4



```html
ffmpeg -i input.avi -c:v libx264 -preset slow -crf 19 -c:a libvo_aacenc -b:a 128k
```

## Fix dark image

https://ffmpeg.org/pipermail/ffmpeg-user/2019-March/043686.html

`ffplay -loglevel panic -i stitched.mp4 -vf "lutyuv=y=val*1.9"`

or

- create lookup table from image: (make copy of image as this overwrites the original)

- apply to video



- `convert hald:2 lut.png`

- `ffmpeg -i in.mp4 -vf "movie=lut.png, [in] haldclut" -crf 19 out_lut.mp4`

- `ffmpeg -i in.mp4 -vf eq=gamma=1.1:contrast=1.03:brightness=0.01:saturation=1.2 -crf 19 out_lut_adj.mp4`

### Retime videos to be the same length

with sound
```
 ffmpeg -i /fstmp/stitched.avi -filter_complex "setpts=PTS/(120/30);atempo=78.000/30" output.avi
```
without sound
```
 ffmpeg -i IN.mp4 -filter_complex "setpts=PTS/(120/30)" OUT.mp4
```
where 120 mand 30 are teh duration in secs




Use with ` -vcodec hevc_nvenc `

### Get FPS
```
ffmpeg -i /fstmp/stitched.avi 2>&1 | sed -n "s/.*, \(.*\) fp.*/\1/p"

ffprobe -v 0 -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate /fstmp/stitched.avi
```

### Contrast,Gamma,etc

```
ffmpeg -i IN.mp4-filter_complex "[0:v]eq=contrast=1:brightness=0:saturation=1:gamma=1:
gamma_r=1:gamma_g=1:gamma_b=1:gamma_weight=1[outv]" OUT.mp4
```

### Crop

to square 720x720 from x=280,y=0

```
ffmpeg -i line_true_open.m4v -vf "crop=720:720:280:0" squared.m4v
```
### Crop to new aspect ratio
Convert `1:1 to 1:1,777
i.e. 512x512 to 512x287 aspectratio 1:1.777
i.e. 2048x2048 to 2048x1150 aspectratio 1:1.777

```
ffmpeg -i input.mp4 -vf "crop=512:287:0:114" output.mp4
```
from 2048x2048 video
```
ffmpeg -i input.mp4 -vf "crop=2040:1150:0:450" output.mp4
```


see https://superuser.com/questions/1474942/ffmpeg-cropping-invalid-too-big-or-non-positive-size-for-width for why these args are so complex
```
ffmpeg -y -loglevel panic -i input.mp4 
-vf "scale=(iw*sar)*max(2040.1/(iw*sar)\,1150.1/ih):ih*max(2040.1/(iw*sar)\,1150.1/ih), crop=2040:1150" output.mp4 < /dev/null
```

### Video to GIF

```
ffmpeg -ss 30 -t 3 -i input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif
```
- -ss 30, skip first 30m seconds
- -t 3 , make a 3 sec gif

### Make a blank video of n seconds

`ffmpeg -f lavfi -i color=c=black:s=2040x1150:r=25/1 -f lavfi -i anullsrc=cl=mono:r=48000 -c:v h264 -c:a pcm_s16be -t 3 out.mov`

or 

`ffmpeg -t 5.35 -s 2040x1150 -f rawvideo -pix_fmt rgb24 -r 15 -i /dev/zero empty.mp4`


### Speedup/slowdown a video
`ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" output.mp4`  # speed up
`ffmpeg -i input.mp4 -vf "setpts=2*PTS" output.mp4`  # slow down

### Make square (to largest side)

```
ffmpeg -i input.mp4 -lavfi '[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16' -vb 800K output.mp4
```

### Scale to 512x512
(The  '!' sometimes causes errors... not sure why)

```
ffmpeg -i output.mp4 -s 512x512! -c:a copy output512.mp4
```
To resize withotu loosing quality in an AVI, need to add `-c:v huffyuv -pix_fmt yuv422p`
```
ffmpeg -i /fstmp/stitched.avi -filter_complex "setpts=PTS*1" -c:v huffyuv -pix_fmt yuv422p /fstmp/output.avi
```

### Extract frames (for 360 frames from a 17:11 min video)
```
ffmpeg -i  inout.mp4  -r 0.35/1 %09d.png
ffmpeg -i  input.mp4  -r 15/1 %09d.png
```

### Get n secods of video

```
ffmpeg -ss [start] -i in.mp4 -t [duration] -map 0 -c copy out.mp4

ffmpeg -t 30 -i inputfile.mp3 -acodec copy outputfile.mp3
```



### Fade in/out,

(start at sec=10, take 5 to fade)

```
ffmpeg -y -i input.mp4 -vf "fade=t=out:st=10:d=5" -c:a copy out2.mp4
```
(start at sec=0, take 3 to fade)

```
ffmpeg -y -i input.mp4 -vf 'fade=t=in:st=0:d=3' -c:a copy out.mp4
```


### Reversing a video
```
ffmpeg -i originalVideo.mp4 -vf reverse reversedVideo.mp4
```

### Joining 2 videos (of same specs)

`ffmpeg -i "concat:input1|input2" -codec copy output.mkv`

### Change res without changing aspect 

`ffmpeg -i input.mp4 -vf scale=1280:-1 output.mp4`

### Make videos from images

```

ffmpeg -framerate 15 -pattern_type glob -i '*.png'  -c:v libx264 -pix_fmt yuv420p out.mp4 
```

lossless

```
 ffmpeg -framerate 15 -pattern_type glob -i '*.png'  -c:v huffyuv  -pix_fmt yuv422p out.avi
```

### Extract frames from videos

```
ffmpeg -i file.mp4 -r 15/1 $filename%09d.png

```

SD's ffmpeg command to stich images together

```
['/home/jw/miniforge3/lib/python3.10/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux64-v4.2.2', '-y', '-r', '60.0', '-start_number', '0', '-i', '/home/jw/store/src/sdw/outputs/img2img-images/batch3/20230617133611_%09d.png', '-frames:v', '1089', '-c:v', 'libx264', '-vf', 'fps=60.0', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'slow', '-pattern_type', 'sequence', '-vcodec', 'libx264', '/home/jw/store/src/sdw/outputs/img2img-images/batch3/20230617133611.mp4']
```
This can be reduced to...
```
ffmpeg -y -r 60.0 -start_number 0 -i %09d.png -frames:v 1089 -c:v libx264 -vf fps=60.0 -pix_fmt yuv420p -crf 17 -preset slow -pattern_type sequence -vcodec libx264 out.mp4'
```

### Label, stitch and interpolate 

Commandline to label, stich, and interpolate frames, where:

- Current dir is  `~/BATCH3`
- Backup images in `./`x
- ID of file is `20230622193341`
- Output file - "out.mp4"
- Interpolated output is `i20_out.mp4`
- Settings file name (in `~/src/sdw/x1`) 

```
cd ~/BATCH3
cp x/* ./ 
~/src/sdc/perlabel.py -d . -i 20230622193341 -s ~/src/sdc/sdw/x1
ffmpeg -y -framerate 15 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4
~/src/rife/INTERP out.mp4 20

```



# Utilities



### RIFE (`~/src/rife/MAKEAUTO,~/src/rife/MAKE`)

1) Extract images from video
2)  Interpolate by 20
3)  Stitch frames
4)  Crop to 2040x1150

- `~/src/sdw/MAKEAUTO /path/input.mp4`

cd /home/jw/src/rife/

./MAKE /tmp/input.mp4 video  (or)
./MAKE images/

### BASH 'for' loop
```
for i in `seq 1000000`; do echo `ls -1 -t *.png |head -1`;cp `ls -1 -t *.png |head -1` .last.png;sleep 5; done

for f in ./*.c; do echo "Processing $f file..."; done
```


### Merge videos (`~/src/sdc/mergevid.py`)

for 1.7:7 aspest (512x278)

- `~/src/sdc/mergevid_512x512.py --dir ~/BATCH3/x  --destdir ~/BATCH3/x --rename c=3s=n.mp4 --verbose `

the `--res 512x278` is the dimesion the indivudual files get resize to before beign merged

for 1:1 aspest (512x512)
- `~/src/sdc/mergevid_512x512.py`

### Interpolation (`~/src/rife/INTERP`)

- `~/src/rife/INTERP /home/jw/src/sdc/sdw/outputs/frame-upscaling/20230626041141/20230626041141.mp4_Upscaled_x4.mp4 20`

### Compare settings file
Compare current file to original shipped file

- `~/src/sdw/cfgdelta.py --config new_settings.txt`

Compare current file to another file 

- `~/src/sdw/cfgdelta.py --config new_settings.txt --compare old_settings.txt --short`



### (`proc_all.sh, proc_run.sh`)

- `sh -x ./procall 20230624150700 `PWD`/20230624150700_settings.txt 3 48\n`



### Settings generation (`~/src/sdc./genpair.py`)

- `~/src/sdc/genpair.py  --type test --count 4 --mult 6 --steps 5 -f sdw/x_ins -s prompts `



### Labeling videos (`~/src/sdc/label.py`)

-  `~/src/sdc/label.py -f ./24.mp4  -l "c\=3\,s\=24"\n`

  *Does not work on some heavily interpolated videos*

### Labeling frames in a a video (`~/src/sdc/perlabel.py`)

- `~/src/sdc/perlabel.py -d ~/BATCH3/step -i 005 -s ~/src/sdw/x_ins`

### Video duration (`~/src/sdc/dursec`)

- `viduration.py -v input.mp4`

### Filter frames by difference (`~/src/sdc/toss.py`, `~/src/sdc/toss.sh, )

- `./toss.py -d ~/BATCH3 -f 0.5 -n`

- `~/src/sdc/toss.sh ~/BATCH3/20230625165144.mp4 0.5`

### Cropping videos (`~/src/rife/CROP`)

Crop video, either 512x512 or 2048x2048 to 

- `~/src/rife/CROP input.mp4`

### Misc

##  (`~/src/sdc`)

`filecheck.py`

`firstlast.py`

`gen.py`

`interpolate.sh`

`livemanage.sh`

`loopmerge.sh`

`multigen.sh`

`PENV`

`run`

`smooth.py`

`stego.py`

`dursec.py` (appears broken)`

`vstego.py`

##  (`~/src/rife`)

`CROP`

`fwatch.py`

`MAKELOOP` *attempt to make end of video math beginning of video - not working*

`run`

`SIZEDN`

`SIZEUP`

`upscale_lomem.py`

`upscale.py`

`interpolate.py`





## SEE ALSO
```
sdc/xfade
sdc/interpolate

```



# General Process...

Batch run SD, all images end up in 'batch3'

This produces

`nnnnnnnnnnnnnn.mp4` in 512x512 resolution and 

`nnnnnnnnnnnnnn_Upscaled_x4.mp4` in 2048x2048 resulution

#### To sizeup a video (from 1:1 to wideview):

`~/src/rife/SIZEUP /path/input.mp4`

- converts 512x512 to 2049x1150



#### To size down a video (from wideview to wideview)

`~/src/rife/SIZEDN /path/input.mp4`

- converts to 2049x1150 to 512x287

#### To crop All images in a dir from 1:1 to wideview 

`ls /path/*.mp4|awk '{print "~/src/rife/CROP "$1}'|sh`

#### To create the slower interpolated  version:

`~/src/rife/INTERP /path/input.mp4 20`

- 20 is the number of interpolated frames that will be created

#### To create per-image labels and videos

extract images 

```
cd ~/BATCH3/steps
fmpeg -i 00500000000000.mp4 -r 15/1 005_%09d.png
~/src/sdc/perlabel.py -d ~/BATCH3/steps -i 005 -s ~/src/sdw/x_ins|sh
```
stitch video

`ffmpeg -framerate 15 -pattern_type glob -i '*.png'  -c:v libx264 -pix_fmt yuv420p out.mp4 `



#### To filter out similar images

`~/src/sdcv/toss.py -d ~/BATCH3 -f 0.5 -n`

- `-n` creates and saves a new a new dataset
- delete frames are saved in `/tmp/tossed`
- saved frames are saves in `/tmp/filtered`

`ffmpeg -framerate 15 -pattern_type glob -i '/tmp/filtered/*.png'  -c:v libx264 -pix_fmt yuv420p ~/BATCH3/fout.mp4 `

`ffmpeg -framerate 15 -pattern_type glob -i '/tmp/tossed/*.png'  -c:v libx264 -pix_fmt yuv420p ~/BATCH3/tout.mp4 `

**Then interpolate to lengthen time**

`~/src/rife/INTERP ~/BATCH3/fout.mp4 20`
`~/src/rife/INTERP ~/BATCH3/out.mp4 20`

