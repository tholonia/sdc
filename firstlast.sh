#!/bin/bash
for file in $(ls ~/BATCH3/20230625212114.mp4)
do
	#create output file name
	of_start=`echo $file | sed s/.mp4/_01.jpg/`
	of_end=`echo $file | sed s/.mp4/_02.jpg/`
	#parse ffprobe output to get the frame count in the video file
	frame_count=`ffprobe -show_streams "$file" 2> /dev/null | grep nb_frames | head -1 | cut -d \= -f 2`
	#parse ffprobe output to get the creation_time
	ts_start=`ffprobe -show_streams "$file" 2> /dev/null | grep creation_time | head -1 | cut -d \= -f 2`
	#parse ffprobe output to get video time duration
	duration=`ffprobe -show_streams "$file" 2> /dev/null | grep duration= | head -1 | cut -d \= -f 2`
	#cut time duration to keep only the subsecond value
	end_subsec=`echo ${duration} | cut -d \. -f 2`
	#concatenate
	ts_end_shift="0:0:0 0:0:${duration}"
	#delete old files if present
	rm -f "$of_start"
	rm -f "$of_end"
	#get the last frame id
	let "frame_count = $frame_count - 1"
	#extract first frame to a jpg file
	ffmpeg -i $file -vf "select=\'eq(n\,0)" $of_start
	#insert creation date as DateTimeOriginal exif tag
	exiftool -DateTimeOriginal="${ts_start}" $of_start -overwrite_original 
	#extract last frame to a jpg file
	ffmpeg -i $file -vf select=\'eq\(n,$frame_count\) -vframes 1 $of_end
	#insert creation date as DateTimeOriginal exif tag and shift it with the video time lenght
	exiftool -DateTimeOriginal="${ts_start}" $of_end -overwrite_original
	exiftool -DateTimeOriginal+="${ts_end_shift}" $of_end -overwrite_original
	#insert	subsecond timestamp
	exiftool -SubSecTimeOriginal="${end_subsec}" $of_end -overwrite_original

done
