#!/bin/bash
~/bin/starttime

declare -A checkpoints
checkpoints=(
#more realistic
    [anythin]="anythingV3_fp16.ckpt"                    # less colors, more details and diversion
    [deliber]="deliberate_v2.safetensors"               # most realistic and detailed
    [abyssor]="abyssorangemix3AOM3_aom3a1b.safetensors" # less colors, very creative
    [meinami]="meinamix_meinaV9.safetensors"            # dark
    [elldret]="elldrethsRetroMix_v10.safetensors"       # realistic, boring
    [dreamsh]="dreamshaper_5BakedVae.safetensors"       # realistic, boring
    [Protoge]="Protogen_V2.2.ckpt"                      # a bit boring, but looks liek something

# abstract (objects no identfiable, but has pattern)
    [HassanB]="HassanBlend1.4_Safe.safetensors"
    [f222.ck]="f222.ckpt"
    [v1-5-pr]="v1-5-pruned-emaonly.safetensors"
    [realist]="realisticVisionV20_v20.safetensors"

# nonsense
    [sd-v1-4]="sd-v1-4.ckpt"
    [openjou]="openjourney-v4.ckpt"
    [dreamli]="dreamlike-photoreal-2.0.ckpt"
    [modelsh]="modelshoot-1.0.safetensors"
)

#echo $checkpoint
#for key in "${!checkpoints[@]}"; do echo "$key"; done
#for i in ${!checkpoints[@]}; do
#  echo "element $i is ${checkpoints[$i]}"
#done

#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function clean() {
      /bin/rm outputs/batch/* > /dev/null 2>&1
}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_image() {
    checkpoint=${checkpoints[$1]}
    F=$2
    ./tester_cfg.py --noani   --before "a realistic photograph of " --after ": intricate, highly detailed, photo-realistic, focused, "
    start=0
    while (( start < $F)); do
      seed=`bigrand`
      ARGS1="max_frames=1|animation_mode=None|seed=${seed}|custom_settings_file=settings/tester_cfg.json|skip_video_for_run_all=1|diffusion_cadence=1"
#      echo "------------------------------------------------------------"
#      echo "./run.py -a $ARGS1 --checkpoint ${checkpoint}"
#      echo "------------------------------------------------------------"
      echo ${checkpoint} > /tmp/title
      ./run.py -a $ARGS1 --checkpoint ${checkpoint}
      T=`cat /tmp/tstamp`
      mv outputs/batch/${T}_batch_00000_${seed}.png outputs/batch/${1}_${seed}.png
      (( start += 1 ))
    done
}

#---------------------------------------------------------!redo-------------------------------------------------------
function test_strengthsch() {
    checkpoint=${checkpoints[$1]}
    F="1100"
    seed_behavior=$2
    ./tester_cfg.py
    ARGS1="custom_settings_file=settings/tester_cfg.json|steps=15|seed_behavior=${2}"

    SCH="0:(0.0),100:(0.1),200:(0.2),300:(0.3),400:(0.4),500:(0.5),600:(0.6),700:(0.7),800:(0.8),900:(0.9),1000:(1.0)"

    # [ control ]
    echo "control\nstrength/noise_sch=0.5/0.5" > /tmp/title;
    ARGS2="noise_schedule=0:(0.5)|strength_schedule=0:(0.5)"
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
    # [ strength_schedule ]
    echo "strength_schedule\n0.0-1.0 (by 0.1, n=0)" > /tmp/title;
    ARGS2="noise_schedule=0:(0.0)|strength_schedule=$SCH";
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
    # [ noise_schedule ]
    echo "noise_schedule\n0.0-1.0 (by 0.1, s=0)" > /tmp/title;
    ARGS2="strength_schedule=0:(0.0)|noise_schedule=$SCH";
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
    # [ strength/noise_schedule ]
    echo "strength/noise_schedule\nn=0-1, s=1-0 (by 0.1)" > /tmp/title;
    ARGS2="noise_schedule=$SCH";
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_strength_noise_${2}_${1}.mp4
}
#---------------------------------------------------------------------------------------------------------------------
function test_scale() {
    #v SCALE
    checkpoint=${checkpoints[$1]}
    F="220"
    ./tester_cfg.py --mono # make new config
    ARGS1="custom_settings_file=settings/tester_cfg.json"

    echo "$1\nscale=2" > /tmp/title; ARGS2="scale=2";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
#    echo "./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}"
    echo "$1\nscale=10" > /tmp/title; ARGS2="scale=10";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "$1\nscale=20" > /tmp/title; ARGS2="scale=20";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "$1\nscale=30" > /tmp/title; ARGS2="scale=30";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "$1\nscale=40" > /tmp/title; ARGS2="scale=40";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}

    echo "$1\nscale=50" > /tmp/title; ARGS2="scale=50";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "$1\nscale=60" > /tmp/title; ARGS2="scale=60";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "$1\nscale=70" > /tmp/title; ARGS2="scale=70";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "$1\nscale=80" > /tmp/title; ARGS2="scale=80";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "$1\nscale=90" > /tmp/title; ARGS2="scale=90";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_scale_${1}_8k.mp4
#    read -p "Press [Enter] key to start backup..."
}

#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_perspective() {
  checkpoint=${checkpoints[$1]}
    F="220"
    ./tester_cfg.py  --rotset 3 --before "a lithograph drawing of " --after " M. C. Escher, highly detailed,  " # make new config
    ARGS1="custom_settings_file=settings/tester_cfg.json|seed=949975187" # or 387260541

    #^ confusing :/
    echo "perspective\ncontrol" > /tmp/title
    ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    echo "perspective_flip_theta\n0-1 (by 0.1)" > /tmp/title;ARGS2="perspective_flip_theta=0:(0.0),20:(0.1),40:(0.2),60:(0.3),80:(0.4),100:(0.5),120:(0.6),140:(0.7),160:(0.8),180:(0.9),200:(1.0)";
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

    echo "perspective_flip_gamma\n0-1 (by 0.1)" > /tmp/title;ARGS2="perspective_flip_gamma=0:(0.0),20:(0.1),40:(0.2),60:(0.3),80:(0.4),100:(0.5),120:(0.6),140:(0.7),160:(0.8),180:(0.9),200:(1.0)";
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

    echo "perspective_flip_fv\n0-1 (by 0.1)" > /tmp/title;ARGS2="perspective_flip_fv=0:(0.0),20:(0.1),40:(0.2),60:(0.3),80:(0.4),100:(0.5),120:(0.6),140:(0.7),160:(0.8),180:(0.9),200:(1.0)";
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_perspectives_${1}.mp4
}

#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_depth() {
    checkpoint=${checkpoints[$1]}
    F="100"
    ./tester_cfg.py  # make new config
    ARGS1="custom_settings_file=settings/tester_cfg.json"

    echo "use_depth_warping\nTrue"  > /tmp/title; ARGS2="use_depth_warping=1";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "use_depth_warping\nFalse" > /tmp/title; ARGS2="use_depth_warping=0";./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_depth_${1}.mp4
}

#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_diffusion() {
    checkpoint=${checkpoints[$1]}
    F="100"
    ./tester_cfg.py  # make new config
    ARGS1="custom_settings_file=settings/tester_cfg.json"

    echo "diffusion_cadence\n1" > /tmp/title; ARGS2="diffusion_cadence=1"; ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "diffusion_cadence\n2" > /tmp/title; ARGS2="diffusion_cadence=2"; ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "diffusion_cadence\n3" > /tmp/title; ARGS2="diffusion_cadence=3"; ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "diffusion_cadence\n4" > /tmp/title; ARGS2="diffusion_cadence=4"; ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "diffusion_cadence\n5" > /tmp/title; ARGS2="diffusion_cadence=5"; ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "diffusion_cadence\n6" > /tmp/title; ARGS2="diffusion_cadence=6"; ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "diffusion_cadence\n7" > /tmp/title; ARGS2="diffusion_cadence=7"; ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "diffusion_cadence\n8" > /tmp/title; ARGS2="diffusion_cadence=8"; ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_diffusion_${1}.mp4
}


#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_seed() {
    checkpoint=${checkpoints[$1]}
    F="200"
    ./tester_cfg.py --mono  # make new config
    ARGS1="custom_settings_file=settings/tester_cfg.json"

    echo "seed_behavior\niter"      > /tmp/title; ARGS2="seed_behavior=iter";      ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "seed_behavior\nrandom"    > /tmp/title; ARGS2="seed_behavior=random";    ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "seed_behavior\nladder"    > /tmp/title; ARGS2="seed_behavior=ladder";    ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "seed_behavior\nalternate" > /tmp/title; ARGS2="seed_behavior=alternate"; ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_seed_${1}.mp4

    #! what do these do?
    #seed_resize
    #    "subseed": 40964096,
    #    "subseed_strength": 0,
    #    "seed_enable_extras": true,
    #    "seed_resize_from_w": 0,
    #    "seed_resize_from_h": 0,
}

#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_trans() {
    checkpoint=${checkpoints[$1]}
    F="200"
    ./tester_cfg.py  # make new config
    ARGS1="custom_settings_file=settings/tester_cfg.json"

    echo "translation-x\n0:(-1)[,1:(1)]" > /tmp/title; ./run.py -a max_frames=${F}\|$ARGS1 --checkpoint ${checkpoint} -X "0:(-1),1:(1),2:(-1),3:(1),4:(-1),5:(1),6:(-1),7:(1),8:(-1),9:(1),10:(-1),11:(1),12:(-1),13:(1),14:(-1),15:(1),16:(-1),17:(1),18:(-1),19:(1),20:(-1),21:(1)"
    echo "translation-y\n0:(-1)[,1:(1)]" > /tmp/title; ./run.py -a max_frames=${F}\|$ARGS1 --checkpoint ${checkpoint} -Y "0:(-1),1:(1),2:(-1),3:(1),4:(-1),5:(1),6:(-1),7:(1),8:(-1),9:(1),10:(-1),11:(1),12:(-1),13:(1),14:(-1),15:(1),16:(-1),17:(1),18:(-1),19:(1),20:(-1),21:(1)"
    echo "translation-z\n0:(-1)[,1:(1)]" > /tmp/title; ./run.py -a max_frames=${F}\|$ARGS1 --checkpoint ${checkpoint} -Z "0:(-1),1:(1),2:(-1),3:(1),4:(-1),5:(1),6:(-1),7:(1),8:(-1),9:(1),10:(-1),11:(1),12:(-1),13:(1),14:(-1),15:(1),16:(-1),17:(1),18:(-1),19:(1),20:(-1),21:(1)"

    ./mergevid.py -D safe/vids --rename EX_translations_${1}.mp4
}

#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_rots() {
    checkpoint=${checkpoints[$1]}
    F="200"

#    ./tester_cfg.py --rotset 1  # make new config
#    ARGS1="custom_settings_file=settings/tester_cfg.json|seed=2708858290"
#    echo "rotation\n#1" > /tmp/title; ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}
#
#    ./tester_cfg.py --rotset 2 # make new config
#    ARGS1="custom_settings_file=settings/tester_cfg.json|seed=2708858290"
#    echo "rotation\n#2" > /tmp/title; ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ./tester_cfg.py --rotset 3 # make new config
    ARGS1="custom_settings_file=settings/tester_cfg.json|seed=2708858290"
    echo "rotation\n#3" > /tmp/title; ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ./tester_cfg.py --rotset 4 # make new config
    ARGS1="custom_settings_file=settings/tester_cfg.json|seed=2708858290"
    echo "rotation\n#4" > /tmp/title; ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_rotations_${1}.mp4
}

#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_f() {
    checkpoint=${checkpoints[$1]}
    F="20"


#^ ran out of memory...  f=1 need H/W of 128/128, f=2 256/256 steps=15, some other error with f=32
    ARGS1="custom_settings_file=settings/tester_cfg.json|H=128|W=128|steps=15"

    ./tester_cfg.py --mono   --before "a realistic photograph of " --after ": intricate, highly detailed, photo-realistic, focused, 4k resolution"  # make new config
    echo "f\nf=1" > /tmp/title
    ./run.py -a max_frames=${F}\|f=1\|diffusion_cadence=8\|$ARGS1 --checkpoint ${checkpoint}

    ./tester_cfg.py --mono   --before "a realistic photograph of " --after ": intricate, highly detailed, photo-realistic, focused, 4k resolution"  # make new config
    echo "f\nf=2" > /tmp/title
    ./run.py -a max_frames=${F}\|f=2\|diffusion_cadence=8\|$ARGS1 --checkpoint ${checkpoint}

    echo "f\nf=4" > /tmp/title
    ./tester_cfg.py --mono   --before "a realistic photograph of " --after ": intricate, highly detailed, photo-realistic, focused, 4k resolution"  # make new config
    ./run.py -a max_frames=${F}\|f=4\|diffusion_cadence=8\|$ARGS1 --checkpoint ${checkpoint}

    echo "f\nf=8" > /tmp/title
    ./tester_cfg.py --mono   --before "a realistic photograph of " --after ": intricate, highly detailed, photo-realistic, focused, 4k resolution"  # make new config
    ./run.py -a max_frames=${F}\|f=8\|diffusion_cadence=8\|$ARGS1 --checkpoint ${checkpoint}

    ./tester_cfg.py --mono   --before "a realistic photograph of " --after ": intricate, highly detailed, photo-realistic, focused, 8k resolution"  # make new config
    echo "f\nf=16" > /tmp/title
    ./run.py -a max_frames=${F}\|f=16\|diffusion_cadence=8\|$ARGS1 --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_f_${1}.mp4
}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_stillness() {
    checkpoint=${checkpoints[$1]}
    F="200"
    ./tester_cfg.py --mono  # make new config
    ARGS1="custom_settings_file=settings/tester_cfg.json|scale=2|seed_bahavior=fixed"

    echo "stillness\n$1" > /tmp/title
    ./run.py -a max_frames=${F}\|diffusion_cadence=8\|$ARGS1 --checkpoint ${checkpoint}
    mv outputs/batch/*.mp4 safe/tmp

}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_border() {
    checkpoint=${checkpoints[$1]}
    F="110"
    ./tester_cfg.py  --before "an drawing of " --after ", paul gauguin, intricate, highly detailed"
#    ./tester_cfg.py  --before "an drawing of " --after ": intricate, highly detailed"
#    ./tester_cfg.py

    ARGS1="custom_settings_file=settings/tester_cfg.json|border=wrap"
    echo "border\nwrap" > /tmp/title
    ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ARGS1="custom_settings_file=settings/tester_cfg.json|border=replicate"
    echo "border\nreplicate" > /tmp/title
    ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_border_${1}.mp4
}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_midasweight() {
    checkpoint=${checkpoints[$1]}
    F="110"
    ./tester_cfg.py  --rotset 3 --before "a painting of " --after ", rembrandt style, intricate, highly detailed"

    ARGS1="custom_settings_file=settings/tester_cfg.json|midas_weight=-1|use_depth_warping=0"
    echo "midas_weight\n-1 (use_depth_warping=False)" > /tmp/title
    ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ARGS1="custom_settings_file=settings/tester_cfg.json|midas_weight=-1"
    echo "midas_weight\n-1 (use_depth_warping=True)" > /tmp/title
    ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ARGS1="custom_settings_file=settings/tester_cfg.json|midas_weight=-0.66"
    echo "midas_weight\n-0.66 (use_depth_warping=True)" > /tmp/title
    ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ARGS1="custom_settings_file=settings/tester_cfg.json|midas_weight=0"
    echo "midas_weight\n0 (use_depth_warping=True)" > /tmp/title
    ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ARGS1="custom_settings_file=settings/tester_cfg.json|midas_weight=0.33"
    echo "midas_weight\n0.33 (use_depth_warping=True)"> /tmp/title
    ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ARGS1="custom_settings_file=settings/tester_cfg.json|midas_weight=1.0"
    echo "midas_weight\n1.0 (use_depth_warping=True)"> /tmp/title
    ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_midasweight_${1}.mp4
}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_nearfar() {
    checkpoint=${checkpoints[$1]}
    F="1000"
    ./tester_cfg.py --rotset 3   --before "a science photograph of " --after ", intricate, highly detailed"
    ARGS1="custom_settings_file=settings/tester_cfg.json"

    echo "near_plane/far_plane\n200/200" >     /tmp/title; ARGS2="near_plane=200|far_plane=200";     ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "near_plane/far_plane\n10000/10000" > /tmp/title; ARGS2="near_plane=10000|far_plane=10000"; ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "near_plane/far_plane\n200/10000" >   /tmp/title; ARGS2="near_plane=200|far_plane=10000";   ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "near_plane/far_plane\n10000/200" >   /tmp/title; ARGS2="near_plane=10000|far_plane=200";   ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "near_plane/far_plane\n1/10" >        /tmp/title; ARGS2="near_plane=1|far_plane=10";        ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}
    echo "near_plane/far_plane\n1/10000" >     /tmp/title; ARGS2="near_plane=1|far_plane=10000";     ./run.py -a max_frames=${F}\|$ARGS1\|$ARGS2 --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_nearfar_${1}.mp4
}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_fov() {
    checkpoint=${checkpoints[$1]}
    F="1000"
    ./tester_cfg.py --rotset 5   --before "a science drawing of " --after ", michaelangelo, intricate, highly detailed"
    ARGS1="custom_settings_file=settings/tester_cfg.json"

#    echo "FOV\n-200" > /tmp/title; ARGS2="fov=-200";  ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
#    echo "FOV\n-80" > /tmp/title; ARGS2="fov=-80";  ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
#    echo "FOV\n-30" > /tmp/title; ARGS2="fov=-30";  ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
    echo "FOV\n-10" > /tmp/title; ARGS2="fov=-10";  ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

#    echo "FOV\200" > /tmp/title; ARGS2="fov=200";./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
#    echo "FOV\n80" > /tmp/title; ARGS2="fov=80"; ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
#    echo "FOV\n30" > /tmp/title; ARGS2="fov=30"; ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
#    echo "FOV\n10" > /tmp/title; ARGS2="fov=10"; ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_fov_${1}.mp4
}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_spiral() {
    checkpoint=${checkpoints[$1]}
    F="300"
    calc="-0.35*(cos(3.141*t/25)**100)+0.8" #^ adds a low-strength change every 25 frames
    ./tester_cfg.py --rotset 5   --before "A nature photograph " --after ",in the style of ansel adams, hyper-realistic, detailed, photography, award winning, documentary, wildlife"
    ARGS1="custom_settings_file=settings/tester_cfg.json"
    #^ create alternate rotating z-rolls ever 50 frames
    EXTREMETY=`bigrand -L 1 -H 5 -d 10`
    FPR="80"
    T1="0:(${EXTREMETY})"
    for (( c=1; c<=($F/$FPR); c=c+2 ))
    do
        EXTREMETY=`bigrand -L 1 -H 5 -d 10`
        let d=(c*$FPR)
#        echo "$d,-${EXTREMETY}"
        T1="$T1,$d:(-${EXTREMETY})"
    done

    let S=($FPR*2)
    T2=""
    for (( c=3; c<=($F/$FPR); c=c+2 ))
    do
        if [ "$c" != "0" ]; then
          EXTREMETY=`bigrand -L 1 -H 5 -d 10`
          let d=(c*$FPR-$FPR)
#          echo "$d,+${EXTREMETY}"
          T2="$T2,$d:(${EXTREMETY})"
        fi
    done
    echo $T1$T2

    echo "test_spiral\n$1" > /tmp/title;
    ARGS2="fov=-10|strength_schedule=0:($calc)|translation_z=0:(-1)|rotation_3d_z=$T1$T2";
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint} --nolabel
    echo $ARGS2

    ./mergevid.py -D safe/vids --rename EX_spiral_${1}.mp4
}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_padding() {
    checkpoint=${checkpoints[$1]}
    F="1000"
    ./tester_cfg.py --rotset 3   --before "a psychedelic painting of " --after ", intricate, highly detailed"
    ARGS1="custom_settings_file=settings/tester_cfg.json"

    echo "padding_mode\nborder" >     /tmp/title; ARGS2="padding_mode=border";  ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
    echo "padding_mode\nreflection" > /tmp/title; ARGS2="padding_mode=reflection"; ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}
    echo "padding_mode\nzeros" >      /tmp/title; ARGS2="padding_mode=zeros"; ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_padding_mode_${1}.mp4
}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_path5() {
    checkpoint=${checkpoints[$1]}
    F="360"
    ./tester_cfg.py --rotset 5   --before "a psychedelic painitng of " --after ", paul gauguin, intricate, highly detailed"
    calc="-0.35*(cos(3.141*t/25)**100)+0.8" #^ adds a low-strength change every 25 frames
    ARGS1="custom_settings_file=settings/tester_cfg.json|strength_schedule=0:($calc)|padding_mode=reflection|fov=40|H=256|W=256"

    echo "path\n5" > /tmp/title;
    ./run.py -a "max_frames=${F}|$ARGS1" --checkpoint ${checkpoint} --nolabel

    ./mergevid.py -D safe/vids --rename EX_path5_${1}.mp4
}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_iter() {
    checkpoint=${checkpoints[$1]}
    F="360"
    ARGS1="custom_settings_file=settings/tester_cfg.json|fov=40|H=256|W=256"

    ARGS2="animation_mode=3D"
    echo "animation_mode\n3D" > /tmp/title;
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

    ARGS2="animation_mode=3D|interpolate_x_frames=99"
    echo "animation_mode\n3D,interpolate_x_frames=99 " > /tmp/title;
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

    ARGS2="animation_mode=Interpolation|interpolate_x_frames=99"
    echo "animation_mode\nInterpolation (x=99)" > /tmp/title;
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

    ARGS2="animation_mode=3D|interpolate_key_frames=True"
    echo "animation_mode\n3D (int_KF,x=99)" > /tmp/title;
    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

#    ARGS2="animation_mode=Interpolation|interpolate_key_frames=True" #^ this combination crashes: "ypeError: unsupported operand type(s) for -: 'str' and 'str'"
#    echo "animation_mode\nInterpolation (int_KF,x=99)" > /tmp/title;
#    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_path5_${1}.mp4
}
#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_prompts() {
    checkpoint=${checkpoints[$1]}
    F="100"
    ARGS1="max_frames=${F}|custom_settings_file=settings/tester_cfg.json"

    C="0"
    ./tester_cfg.py --promptset "prompt_$C" --before "a photograph of " --after "hyper-realistic, detailed, award winning, documentary, wildlife" --keys 3 --frames $F
    echo "prompt_$C\nroses,dasies,weeds" > /tmp/title;
    ./run.py -a "$ARGS1" --checkpoint ${checkpoint}

    C="1"
    ./tester_cfg.py --promptset "prompt_$C" --before "a photograph of " --after "hyper-realistic, detailed, award winning, documentary, wildlife" --keys 3 --frames $F
    echo "prompt_$C\nroses300,dasies030,weeds003" > /tmp/title;
    ./run.py -a "$ARGS1" --checkpoint ${checkpoint}

    C="2"
    ./tester_cfg.py --promptset "prompt_$C" --before "a photograph of " --after "hyper-realistic, detailed, award winning, documentary, wildlife" --keys 3 --frames $F
    echo "prompt_$C\nroses033,dasies303,weeds330" > /tmp/title;
    ./run.py -a "$ARGS1" --checkpoint ${checkpoint}

    ./mergevid.py -D safe/vids --rename EX_prompts_${1}.mp4
}

#[──────────────────────────────────────────────────────────────────────────────────────────────────────]
#[──────────────────────────────────────────────────────────────────────────────────────────────────────]
#[──────────────────────────────────────────────────────────────────────────────────────────────────────]

declare -a totest=("deliber")
#declare -a totest=("anythin"  "deliber" )
#declare -a totest=("anythin" "deliber" "abyssor" "meinami" "elldret" "dreamsh" "Protoge")
#declare -a totest=("anythin" "deliber" "abyssor" "meinami" "elldret" "dreamsh" "Protoge" "HassanB" "f222.ck" "v1-5-pr" "realist" "sd-v1-4" "openjou" "dreamli" "modelsh")


#[ 'test_scale' CREATE A TEST MERGDE FOR EACH MODEL
#clean
#for idx in "${totest[@]}"
#do
#    test_scale $idx
#done
#v─────────────────────────────────────────────────

#[ 'test_scale' CREATE A TEST MERGDE FOR EACH MODEL
#clean
#for idx in "${totest[@]}"
#do
#    test_stillness $idx       #! FILES ARE MOVED TO safe/tmp IN THE FUNCTION
#done
#  clean                       #! WIPE ALL FILES
#  mv safe/tmp/* outputs/batch #! MOVED THE TMP FILES BACK
#  ./mergevid.py               #! MERGE IT
#  mv outputs/batch/merged.mp4 safe/vids/EX_stillness.mp4 #! MOVE AND RENAME

#v────────────────────────────────────────────────]


#[ 'NORMAL' TESTS ]
for idx in "${totest[@]}"
do
    clean
#- PASSED
    clean;test_image $idx "6" #^ make 5 image of a random seed ! THESE ARE NOT PRESERVED AND REMAIN IN THE BATCH DIR !!!
#    clean;test_seed $idx
#    clean;test_f $idx
#    clean;test_diffusion $idx
#    clean;test_trans $idx        #RMX
#    clean;test_rots $idx         #RMX
#    clean;test_depth $idx        #RMX
#    clean;test_perspective $idx  #RMX

#- PENDING
#     clean;test_strengthsch $idx fixed #! RMX ?? confusing
#     clean;test_strengthsch $idx iter #! RMX ?? confusing
#     clean;test_strengthsch $idx ladder #! RMX ?? confusing
#     clean;test_strengthsch $idx alternate #! RMX ?? confusing

#     clean;test_border $idx        #^ RMX   NICE
#     clean;test_midasweight $idx   #^ RMX
#     clean;test_fov $idx           #^ RMX


#     clean;test_padding $idx         #^ RMX
#     clean;test_nearfar $idx      #^ RMX    #^ don't see any change  REDO
#-TESTS
#     clean;test_path5 $idx      #^ RMX    #^ don't see any change  REDO
#     clean;test_iter $idx      #^ RMX    #^ don't see any change  REDO
#     clean;test_prompts $idx      #^ RMX    #^ don't see any change  REDO
done

declare -a totest=("anythin" "deliber" "abyssor" "meinami" "elldret" "dreamsh" "Protoge" "HassanB" "f222.ck" "v1-5-pr" "realist" "sd-v1-4" "openjou" "dreamli" "modelsh")
for idx in "${totest[@]}"
do
    clean
      clean;test_spiral $idx           #^ RMX
done

#v───────────────]


aplay /home/jw/store/src/jmcap/ohlc/assets/ready.wav > /dev/null 2>&1

echo "------------------------ TOTAL TIME"
~/bin/endtime
