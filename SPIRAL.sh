#!/bin/bash
~/bin/starttime

CLR_RED="\e[0;49;31m"
CLR_GRE="\e[0;49;32m"
CLR_YEL="\e[0;49;33m"
CLR_BLU="\e[0;49;34m"
CLR_MAG="\e[0;49;35m"
CLR_CYA="\e[0;49;36m"
CLR_WHI="\e[0;49;37m"
CLR_RESET="\e[0m"



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
    [ghostmi]="ghostmix_v20Bakedvae.safetensors"
    [chillou]="chilloutmix_NiPrunedFp32Fix.safetensors"

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

# beta
    [3Guofen]="3Guofeng3_v33.safetensors"
    [psyflow]="psymelon_flower/psymelon_flower_3400.safetensors"
    [V2th_42]="V2th/V2th_4200.safetensors"
    [bezier_]="bezier/bezier_8100.safetensors"
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
#function test_spiral_1() {
#    checkpoint=${checkpoints[$1]}
#    F="300"
#    calc="-0.35*(cos(3.141*t/25)**100)+0.8" #^ adds a low-strength change every 25 frames
#    ./spiral_cfg.py --rotset "spiral_1"   --BEFORE "A nature photograph " --AFTER ",in the style of ansel adams, hyper-realistic, detailed, photography, award winning, documentary, wildlife"
#    ARGS1="custom_settings_file=settings/spiral_cfg.json"
#    #^ create alternate rotating z-rolls ever 50 frames
#    EXTREMETY=`bigrand -L 1 -H 5 -d 10`
#    FPR="80"
#    T1="0:(${EXTREMETY})"
#    for (( c=1; c<=($F/$FPR); c=c+2 ))
#    do
#        EXTREMETY=`bigrand -L 1 -H 5 -d 10`
#        let d=(c*$FPR)
##        echo "$d,-${EXTREMETY}"
#        T1="$T1,$d:(-${EXTREMETY})"
#    done
#
#    let S=($FPR*2)
#    T2=""
#    for (( c=3; c<=($F/$FPR); c=c+2 ))
#    do
#        if [ "$c" != "0" ]; then
#          EXTREMETY=`bigrand -L 1 -H 5 -d 10`
#          let d=(c*$FPR-$FPR)
##          echo "$d,+${EXTREMETY}"
#          T2="$T2,$d:(${EXTREMETY})"
#        fi
#    done
#    echo $T1$T2
#
#    echo "test_spiral\n$1" > /tmp/title;
#    ARGS2="fov=-10|strength_schedule=0:($calc)|translation_z=0:(-1)|rotation_3d_z=$T1$T2";
#    ./run.py -a "max_frames=${F}|$ARGS1|$ARGS2" --checkpoint ${checkpoint} --nolabel
#    echo $ARGS2
#
#    ./mergevid.py -D safe/vids --rename SP1_${1}.mp4
#}

#-───────────────────────────────────────────────────────────────────────────────────────────────────────
function test_spiral_2() {
    C_OPT=$2
    C_SAMP=$3
    checkpoint=${checkpoints[$1]}
    F="300"
#    strength_calcs="-0.65*(cos(3.141*t/25)**100)+0.8" #^ adds a low-strength change every 25 frames
    strength_calcs=".3"
    noise_calcs="0"
    zoom_calcs="-0.35*(cos(3.141*t/25)**100)+0.8" #^ adds a low-strength change every 25 frames
    trans_x_calcs="-0.65*(cos(3.141*t/25)**100)+0.0" #^ adds a low-strength change every 25 frames
    trans_y_calcs="-0.65*(cos(3.141*t/25)**100)+0.0" #^ adds a low-strength change every 25 frames

    BEFORE=""
    AFTER=""
    NEGS=""

    if [ $C_OPT = "PREPOST" ]; then
        BEFORE="photography portrait of a "
        AFTER=",front lighting, hyper-realistic, detailed, black flat background"
#        NEGS="hands:0 logo:0 signature:0 watermark:0 words:0 letters:0 ANGRY:0 UGLY:0 BAD:0 EVIL:0"
        NEGS=""
    fi
    if [ $C_OPT = "PREKEYS" ]; then
        BEFORE="front lighting, hyper-realistic, detailed, black flat background, photography portrait of a "
        AFTER=""
    fi


#    AFTER=",in the style of National Geopgrphic, hyper-realistic, detailed, color-balanced, photography, award winning, documentary, wildlife"
#    ./spiral_cfg.py --keys 26 --frames $F --rotset spiral_1  --promptset embeds --BEFORE "$BEFORE" --AFTER "$AFTER"




    ARGS1="custom_settings_file=settings/spiral_cfg.json"
    #^ create alternate rotating z-rolls ever 50 frames
    EXTREMETY=`bigrand -L 1 -H 5 -d 10`
    FPR="80" #^ frames per roll
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
#    echo $T1$T2

    echo "$1" > /tmp/title;

#    INT=""
#    INT="interpolate_x_frames=10|animation_mode=Interpolation|zoom=0:(1)"
#    ARGS2="${INT}fov=20|translation_z=0:($zoom_calcs)|translation_x=0:($trans_x_calcs)|translation_y=0:($trans_y_calcs)|strength_schedule=0:($noise_calcs)|strength_schedule=0:($noise_calcs)|rotation_3d_z=$T1$T2";
#    echo "$ARGS1|$ARGS2"

FDELTA=40
C=0

#x=":"
#y=":1"
x=""
y=""

cat << EOF > settings/spiral_cfg.json

{
    "W":512,
    "H": 512,
    "f": 8,
    "fps": 12,
    "steps": 15,
    "max_frames": ${F},
    "seed": -1,
    "XXX_interpolate_x_frames": $FDELTA,
    "XXX_animation_mode": "Interpolation",
    "animation_mode": "None",
    "zoom": "0:(0)",
    "fov": 20,
    "diffusion_cadence": 8,
    "XXX_translation_z": "0:($zoom_calcs)",
    "XXX_translation_x": "0:($trans_x_calcs)",
    "XXX_translation_y": "0:($trans_y_calcs)",
    "strength_schedule": "0:($strength_calcs)",
    "noise_schedule": "0:($noise_calcs)",
    "XXX_rotation_3d_z": "$T1$T2",
    "model_config": "v2-inference.yaml",
    "sampler": "$C_SAMP",

    "prompts": [
        "simple 2D flat colorful  painting of many large leaves and flowers in the jungle with flowers and hanging grapes and berries of many colors, high contrrasl 2-dimensional "
    ],
    "xxanimation_prompts": {
        "$((C=C+$FDELTA))": "${x}single animal cell${y} ${NEGS}",
        "$((C=C+$FDELTA))": "${x}a single animal cell meiosis${y} ${NEGS}",
        "$((C=C+$FDELTA))": "${x}Protozoa${y} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}flatworm${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}hagfish${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}lungfish${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}frog${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}lizard${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}marsupial${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}rodent${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}rabbit${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}lemur${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}panther${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}wolf${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}bear${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}ape${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}gibbon${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}chimpanzee${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}handsome and attractive man with beard${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} ${x}handsome and attractive bald alien${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} community of ${x}people${y}",

        "$((C=C+$FDELTA))": "photograph of a ${x}small town${y} ${NEGS}",
        "$((C=C+$FDELTA))": "photograph of a ${x}big city${y} ${NEGS}",
        "$((C=C+$FDELTA))": "map of ${x}south america${y} ${NEGS}",
        "$((C=C+$FDELTA))": "map of the ${x}world${y} ${NEGS}",
        "$((C=C+$FDELTA))": "photograph of ${x}earth from space${y} ${NEGS}",

        "$((C=C+$FDELTA))": "${BEFORE} ${x}solar system${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${BEFORE} large science fiction space station mother ship traveling towards the milkyway${y} ${AFTER} ${NEGS}",
        "$((C=C+$FDELTA))": "${x}universe${y} ${NEGS}",
        "$((C=C+$FDELTA))": "${x}single animal cell${y} ${NEGS}"
    },
    "X":{}
}
EOF

    ./run.py -a $ARGS1 --checkpoint ${checkpoint}  --nolabel

    echo -en $CLR_MAG
    echo "./run.py -a $ARGS1 --checkpoint ${checkpoint}  --nolabel"
    echo -en $CLR_RESET

    FILENAME="${CONFIG_OPT}_${C_SAMP}_${1}.mp4"
    FILENAME_FADE="fade_${CONFIG_OPT}_${C_SAMP}_${1}.mp4"

    ./mergevid.py -D safe/vids --rename ${FILENAME}

#    DUR=`./dursec.py ${FILENAME}`
#    FO=$((DUR-3))
#
#    echo -en $CLR_YEL
#    echo "ffmpeg -y -i ${FILENAME} -vf fade=t=in:st=0:d=3 -c:a copy out.mp4"
#    echo -en $CLR_RESET
#    ffmpeg -y -i ${FILENAME} -vf fade=t=in:st=0:d=3 -c:a copy out.mp4
#
#
#    echo -en $CLR_YEL
#    echo "ffmpeg -y -i ${FILENAME} -vf fade=t=in:st=0:d=3 -c:a copy out.mp4"
#    echo -en $CLR_RESET
#    ffmpeg -y -i out.mp4 -vf fade=t=out:st=${FO}:d=3 -c:a copy ${FILENAME_FADE}.mp4

}


#-───────────────────────────────────────────────────────────────────────────────────────────────────────
#! all
#declare -a totest=("ghostmi" "Chillou" "anythin" "deliber" "abyssor" "meinami" "elldret" "dreamsh" "Protoge" "HassanB" "f222.ck" "v1-5-pr" "realist" "sd-v1-4" "openjou" "dreamli" "modelsh")

#^ GROUPS
#"abyssor","anythin"  #^ always faded, greyish, smokey
# Protoge             #^ was black and white, but details and clear
#"deliber" "HassanB" "elldret"
#"meinami"
#"dreamli"            ^#^ colorful, realistic
#"realist" "sd-v1-4" "openjou"
#"v1-5-pr" "modelsh"
#"f222.ck"
#"dreamsh"

#! good
declare -a totest=( "chillou" "Protoge" "dreamli" "realist" "deliber" "v1-5-pr" "dreamsh" ) #^prefered per group
#declare -a totest=("psyflow" "V2th_42" "bezier_")


#declare -a samps=("klms" "dpm2" "dpm2_ancestral" "heun" "euler" "euler_ancestral" "plms" "ddim" "dpm_fast" "dpm_adaptive" "dpmpp_2s_a" "dpmpp_2m")
declare -a samps=("ddim")

for CONFIG_OPT in "$@"
do
    for idx in "${totest[@]}"
    do
    #    clean
    #    clean;test_spiral_1 $idx

        for samp in "${samps[@]}"
        do
#            clean
            test_spiral_2 $idx $CONFIG_OPT $samp
        done
    done
done

aplay /home/jw/store/src/jmcap/ohlc/assets/ready.wav > /dev/null 2>&1

echo "------------------------ TOTAL TIME"
~/bin/endtime

