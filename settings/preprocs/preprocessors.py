# @formatter:off
"""
#[ Create New instance

cd /home/jw/src/sdc/settings/preprocs
#v create firs <model>, <model>/<sampler>,<model>/<sampler>/<CN>
#v cd <model>/<sampler>/<CN>

cp /home/jw/src/sdc/settings/preprocs/INPUT_VIDEO.json ./
#! check/edit  values !! REMEMBER TO CHANGE MODEL IN UI
grep "cn_1_enabled\|cn_1_module\|cn_1_model\|sd_model_name\|sampler\":" /dev/null *.json
#v edit values if necessary
#! create ORG_VIDEO.json
cat INPUT_VIDEO.json| perl -p -e 's/\"cn_1_enabled\": true,/\"cn_1_enabled\": false,/gmi' > ORG_VIDEO.json
#! create XFGs
genxfg.py -m 6x1 -S
#! run batch or XFG and JSON

#[ List vwhat has been done
cd /home/jw/src/sdc/settings/preprocs
find -name "vgrid*.mp4"  #! all unbannered
find -name "banner_*6x1*.mp4"  #! all 6x1 bannered
find -name "banner_*6x3*.mp4"  #! all 6x3 bannered


#[Opt & Clean
#!clean interpolated frames
find -name "interpolated*" -exec rm -rf {} \;
#! clean uninterpolated video
find -name "1.mp4" -exec rm -rf {} \;
#!make new
find |grep FILM|awk -F"/" '{print "HandBrakeCLI -v error -i "$2"/"$3" -o "$2"/x_"$3}' > HB
sh -x ./HB
#!clean dups
find |grep x_x_ |awk '{print "rm "$0}'|sh
#! clean unoptimized video
find -name "*1_FILM*mp4"  #list
find -name "1_FILM*mp4" -exec rm -rf {} \;  #delete



#[For finished videos:
ln -fs /home/jw/src/sdc/settings/preprocs/MAKE ./  #!one time only
./MAKE -m 6x1 -c  #! make 6x1 strip

    #!manually
    cd /home/jw/src/sdc/settings/preprocs/canny/
    genbatch.py -p > RUN.sh
    sh -x ./RUN.sh
    mergevidX.py -f "*.mp4" -g 6x3

#[ Add Banner
#! MUST be in working dir above 'out'
addbanner.py -v out/vgrid-6x1_1_of_1.mp4

"""

# genbatch.py -g"       To make xfg for unfinished

prp_list = {
   "ALL": [
        "ORG_VIDEO",
        "INPUT_VIDEO",
        "canny",
        "dw_openpose_full",
        "lineart",
        "mlsd",             #[ 6x1
        "pidinet",
        "scribble_xdog",    #[8   8x1

        "depth",
        "depth_leres",
        "depth_leres++",
        "depth_zoe",
        "hed",
        "hed_safe",
        "inpaint",
        "inpaint_only",
        "inpaint_only+lama",
        "lineart_anime",    #[18    6x3

        "lineart_anime_denoise",
        "lineart_coarse",
        "lineart_standard",
        "mediapipe_face",
        "openpose",
        "openpose_face",
        "openpose_faceonly",
        "openpose_full",
        "openpose_hand",
        "pidinet_safe",
        "pidinet_scribble",
        "pidinet_sketch",
        "scribble_hed",
        "segmentation",  #[32   8x4

        "shuffle",
        "normal_bae",
        "normal_map",
        "oneformer_ade20k",
        "oneformer_coco",
        "recolor_intensity",
        "recolor_luminance",
        "blur_gaussian",
        "color",
        "invert",
        "revision_clipvision",
        "revision_ignore_prompt",
        "threshold",
   ],


    "BROKEN": [
        #  anything with 'reference' crashes, usually around frame 46
        "reference_adain",
        "reference_adain+attn",
        "reference_only",
        #  anything wirg 'clip' crashes
        "clip_vision",
        #  anything with 'tile' crashes
        "tile_colorfix",
        "tile_colorfix+sharp",
        "tile_resample",
        #
        "ip-adapter_clip_sd15",
        "ip-adapter_clip_sdxl",
    ],
}
