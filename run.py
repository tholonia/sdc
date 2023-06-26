#!/bin/env python

# %%
# !! {"metadata":{
# !!   "id": "ByGXyiHZWM_q"
# !! }}
"""
# **Deforum Stable Diffusion v0.7**
[Stable Diffusion](https://github.com/CompVis/stable-diffusion) by Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, Bj?rn Ommer and the [Stability.ai](https://stability.ai/) Team. [K Diffusion](https://github.com/crowsonkb/k-diffusion) by [Katherine Crowson](https://twitter.com/RiversHaveWings). Notebook by [deforum](https://discord.gg/upmXXsrwZc)

"""
# %%
# !! {"metadata":{
# !!   "cellView": "form",
# !!   "id": "IJjzzkKlWM_s"
# !! }}
#@markdown **NVIDIA GPU**

import json
import time
import sys
from pprint import pprint
import getopt
import glob
from colorama import init, Fore, Back
from ns_utils import Loader, Dumper, object_hook, nsEncoder
import os
import subprocess
from base64 import b64encode

init()

sub_p_res = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.free', '--format=csv,noheader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
print(f"{sub_p_res[:-1]}")

# %%
# !! {"metadata":{
# !!   "id": "UA8-efH-WM_t"
# !! }}
"""
# Setup
"""
# %%
# !! {"metadata":{
# !!   "cellView": "form",
# !!   "id": "vohUiWo-I2HQ"
# !! }}
#@markdown **Environment Setup**

# [ ───────────────────────────────────────────────
# [  DEFINE FUNCTIONS .............................
# [ ───────────────────────────────────────────────



def prun(cmd):
    print(cmd)
    try:
        scmd = cmd.split()
    except:
        scmd = cmd

    process = subprocess.Popen(scmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stderr)
        raise RuntimeError(stderr)
def isNum(ary,key):
    s=ary[key]

    if type(s) == list:
        return s
    if type(s) == tuple:
        return s
    if type(s) == dict:
        return s
    #
    # print(f"---------------------------------------------------------------------- '{key}' in:[{s}]", end="")
    try:
        f=float(s)
        try:
            i=int(s)
            # print(f" = integer [{i}] ")
            return i
        except ValueError:
            # print(f" = decimal [{f}] ")
            return f
    except ValueError:
        # print("")
        return s

def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -a, --arglist       name=var,... (no spaces) ex:  W:256,H=256,steps=15
                        'name' can be any key in settings.
    '''
    print (rs)
    exit()
def savevar(var,fn):
    with open(fn, 'w') as f:
        f.write(var)


def setup_environment():
    # Check if it's a Google Colab environment
    try:
        ipy = get_ipython()
    except:
        ipy = 'could not get_ipython'

    if 'google.colab' in str(ipy):

        # Start the timer
        start_time = time.time()

        # Installing the necessary packages
        packages = [
            'torch==2.0.0 torchvision torchaudio triton xformers',
            'einops==0.4.1 pytorch-lightning==1.7.7 torchdiffeq torchsde omegaconf',
            'ftfy timm transformers open-clip-torch omegaconf torchmetrics',
            'safetensors kornia accelerate jsonmerge matplotlib resize-right',
            'scikit-learn numpngw'
        ]

        for package in packages:
            print(f"..installing {package}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + package.split())

        # Cloning the github repository
        subprocess.check_call(['git', 'clone', 'https://github.com/deforum-art/deforum-stable-diffusion'])

        # Modifying the python file
        with open('deforum-stable-diffusion/src/k_diffusion/__init__.py', 'w') as f:
            f.write('')

        # Extending the system path
        sys.path.extend([
            'deforum-stable-diffusion/',
            'deforum-stable-diffusion/src',
        ])

        # End the timer
        end_time = time.time()

        # Print the time it took
        print(f"..environment set up in {end_time - start_time:.0f} seconds")

    else:
        sys.path.extend([
            'src'
        ])
        print("..skipping setup")

def Root():
    models_path = "models/Stable-diffusion" #@param {type:"string"}
    configs_path = "configs" #@param {type:"string"}
    output_path = "outputs" #@param {type:"string"}
    mount_google_drive = False #@param {type:"boolean"}
    models_path_gdrive = "/content/drive/MyDrive/AI/models" #@param {type:"string"}
    output_path_gdrive = "/content/drive/MyDrive/AI/StableDiffusion" #@param {type:"string"}

    #@markdown **Model Setup**
    map_location = "cuda" #@param ["cpu", "cuda"]
    model_config = "v1-inference.yaml" #@param ["custom","v2-inference.yaml","v2-inference-v.yaml","v1-inference.yaml"]
    model_checkpoint =  new_checkpoint #@param ["custom","v2-1_768-ema-pruned.ckpt","v2-1_512-ema-pruned.ckpt","768-v-ema.ckpt","512-base-ema.ckpt","Protogen_V2.2.ckpt","v1-5-pruned.ckpt","v1-5-pruned-emaonly.ckpt","sd-v1-4-full-ema.ckpt","sd-v1-4.ckpt","sd-v1-3-full-ema.ckpt","sd-v1-3.ckpt","sd-v1-2-full-ema.ckpt","sd-v1-2.ckpt","sd-v1-1-full-ema.ckpt","sd-v1-1.ckpt", "robo-diffusion-v1.ckpt","wd-v1-3-float16.ckpt"]
    custom_config_path = "" #@param {type:"string"}
    custom_checkpoint_path = "" #@param {type:"string"}
    return locals()

def DeforumArgs():
    # @markdown **Image Settings**
    W = 512  # @param
    H = 512  # @param
    W, H = map(lambda x: x - x % 64, (W, H))  # resize to integer multiple of 64
    bit_depth_output = 8  # @param [8, 16, 32] {type:"raw"}

    # @markdown **Sampling Settings**
    seed = -1  # @param
    sampler = 'euler_ancestral'  # @param ["klms","dpm2","dpm2_ancestral","heun","euler","euler_ancestral","plms", "ddim", "dpm_fast", "dpm_adaptive", "dpmpp_2s_a", "dpmpp_2m"]
    steps = 50  # @param
    scale = 7  # @param
    ddim_eta = 0.0  # @param
    dynamic_threshold = None
    static_threshold = None

    # @markdown **Save & Display Settings**
    save_samples = True  # @param {type:"boolean"}
    save_settings = False  # @param {type:"boolean"}
    display_samples = True  # @param {type:"boolean"}
    save_sample_per_step = False  # @param {type:"boolean"}
    show_sample_per_step = False  # @param {type:"boolean"}

    # @markdown **Prompt Settings**
    prompt_weighting = True  # @param {type:"boolean"}
    normalize_prompt_weights = True  # @param {type:"boolean"}
    log_weighted_subprompts = False  # @param {type:"boolean"}

    # @markdown **Batch Settings**
    n_batch = 1  # @param
    if "batch_name" not in pairs:
        batch_name = "batch"  # @param {type:"string"}
    else:
        batch_name = pairs['batch_name']
    # filename_format = "{timestring}_{index}_{prompt}.png" #@param ["{timestring}_{index}_{seed}.png","{timestring}_{index}_{prompt}.png"]
    filename_format = "{timestring}_{index}.png"  # @param ["{timestring}_{index}_{seed}.png","{timestring}_{index}_{prompt}.png"]

    seed_behavior = "iter"  # @param ["iter","fixed","random","ladder","alternate"]
    seed_iter_N = 1  # @param {type:'integer'}
    make_grid = False  # @param {type:"boolean"}
    grid_rows = 2  # @param
    # outdir = get_output_folder(root.output_path, batch_name)
    # outdir = get_output_folder(root.output_path, batch_name)
    outdir = "outputs/batch"

    # @markdown **Init Settings**
    use_init = False  # @param {type:"boolean"}
    strength = 0.1  # @param {type:"number"}
    strength_0_no_init = True  # Set the strength to 0 automatically when no init image is used
    init_image = "https://cdn.pixabay.com/photo/2022/07/30/13/10/green-longhorn-beetle-7353749_1280.jpg"  # @param {type:"string"}
    # Whiter areas of the mask are areas that change more
    use_mask = False  # @param {type:"boolean"}
    use_alpha_as_mask = False  # use the alpha channel of the init image as the mask
    mask_file = "https://www.filterforge.com/wiki/images/archive/b/b7/20080927223728%21Polygonal_gradient_thumb.jpg"  # @param {type:"string"}
    invert_mask = False  # @param {type:"boolean"}
    # Adjust mask image, 1.0 is no adjustment. Should be positive numbers.
    mask_brightness_adjust = 1.0  # @param {type:"number"}
    mask_contrast_adjust = 1.0  # @param {type:"number"}
    # Overlay the masked image at the end of the generation so it does not get degraded by encoding and decoding
    overlay_mask = True  # {type:"boolean"}
    # Blur edges of final overlay mask, if used. Minimum = 0 (no blur)
    mask_overlay_blur = 5  # {type:"number"}

    # @markdown **Exposure/Contrast Conditional Settings**
    mean_scale = 0  # @param {type:"number"}
    var_scale = 0  # @param {type:"number"}
    exposure_scale = 0  # @param {type:"number"}
    exposure_target = 0.5  # @param {type:"number"}

    # @markdown **Color Match Conditional Settings**
    colormatch_scale = 0  # @param {type:"number"}
    colormatch_image = "https://www.saasdesign.io/wp-content/uploads/2021/02/palette-3-min-980x588.png"  # @param {type:"string"}
    colormatch_n_colors = 4  # @param {type:"number"}
    ignore_sat_weight = 0  # @param {type:"number"}

    # @markdown **CLIP\Aesthetics Conditional Settings**
    clip_name = 'ViT-L/14'  # @param ['ViT-L/14', 'ViT-L/14@336px', 'ViT-B/16', 'ViT-B/32']
    clip_scale = 0  # @param {type:"number"}
    aesthetics_scale = 0  # @param {type:"number"}
    cutn = 1  # @param {type:"number"}
    cut_pow = 0.0001  # @param {type:"number"}

    # @markdown **Other Conditional Settings**
    init_mse_scale = 0  # @param {type:"number"}
    init_mse_image = "https://cdn.pixabay.com/photo/2022/07/30/13/10/green-longhorn-beetle-7353749_1280.jpg"  # @param {type:"string"}

    blue_scale = 0  # @param {type:"number"}

    # @markdown **Conditional Gradient Settings**
    gradient_wrt = 'x0_pred'  # @param ["x", "x0_pred"]
    gradient_add_to = 'both'  # @param ["cond", "uncond", "both"]
    decode_method = 'linear'  # @param ["autoencoder","linear"]
    grad_threshold_type = 'dynamic'  # @param ["dynamic", "static", "mean", "schedule"]
    clamp_grad_threshold = 0.2  # @param {type:"number"}
    clamp_start = 0.2  # @param
    clamp_stop = 0.01  # @param
    grad_inject_timing = list(range(1, 10))  # @param

    # @markdown **Speed vs VRAM Settings**
    cond_uncond_sync = True  # @param {type:"boolean"}

    n_samples = 1  # doesnt do anything
    precision = 'autocast'
    C = 4
    f = 8

    prompt = ""
    timestring = ""
    init_latent = None
    init_sample = None
    init_sample_raw = None
    mask_sample = None
    init_c = None
    seed_internal = 0

    return locals()

def DeforumAnimArgs():
    skip_video_for_run_all = False
    # @markdown ####**Animation:**
    animation_mode = '3D'  # @param ['None', '2D', '3D', 'Video Input', 'Interpolation'] {type:'string'}
    max_frames = 100  # @param {type:"number"}
    border = 'replicate'  # @param ['wrap', 'replicate'] {type:'string'}

    # @markdown ####**Motion Parameters:**
    angle = "0:(0)"  # @param {type:"string"}
    zoom = "0:(1.04)"  # @param {type:"string"}
    # translation_x = "0:(10*sin(2*3.14*t/10))"  # @param {type:"string"}
    if xtrx:
        translation_x = xtrx
    if ytrx:
        translation_y = ytrx
    if ztrx:
        translation_z = ztrx

    translation_x = "0:(10*sin(2*3.14*t/10))"  # @param {type:"string"}
    translation_y = "0:(0)"  # @param {type:"string"}
    translation_z = "0:(10)"  # @param {type:"string"}

    rotation_3d_x = "0:(0)"  # @param {type:"string"}
    rotation_3d_y = "0:(0)"  # @param {type:"string"}
    rotation_3d_z = "0:(0)"  # @param {type:"string"}
    flip_2d_perspective = False  # @param {type:"boolean"}
    perspective_flip_theta = "0:(0)"  # @param {type:"string"}
    perspective_flip_phi = "0:(t%15)"  # @param {type:"string"}
    perspective_flip_gamma = "0:(0)"  # @param {type:"string"}
    perspective_flip_fv = "0:(53)"  # @param {type:"string"}
    noise_schedule = "0: (0.02)"  # @param {type:"string"}
    strength_schedule = "0: (0.65)"  # @param {type:"string"}
    contrast_schedule = "0: (1.0)"  # @param {type:"string"}
    hybrid_video_comp_alpha_schedule = "0:(1)"  # @param {type:"string"}
    hybrid_video_comp_mask_blend_alpha_schedule = "0:(0.5)"  # @param {type:"string"}
    hybrid_video_comp_mask_contrast_schedule = "0:(1)"  # @param {type:"string"}
    hybrid_video_comp_mask_auto_contrast_cutoff_high_schedule = "0:(100)"  # @param {type:"string"}
    hybrid_video_comp_mask_auto_contrast_cutoff_low_schedule = "0:(0)"  # @param {type:"string"}

    # @markdown ####**Unsharp mask (anti-blur) Parameters:**
    kernel_schedule = "0: (5)"  # @param {type:"string"}
    sigma_schedule = "0: (1.0)"  # @param {type:"string"}
    amount_schedule = "0: (0.2)"  # @param {type:"string"}
    threshold_schedule = "0: (0.0)"  # @param {type:"string"}

    # @markdown ####**Coherence:**
    color_coherence = 'Match Frame 0 LAB'  # @param ['None', 'Match Frame 0 HSV', 'Match Frame 0 LAB', 'Match Frame 0 RGB', 'Video Input'] {type:'string'}
    color_coherence_video_every_N_frames = 1  # @param {type:"integer"}
    diffusion_cadence = '1'  # @param ['1','2','3','4','5','6','7','8'] {type:'string'}

    # @markdown ####**3D Depth Warping:**
    use_depth_warping = True  # @param {type:"boolean"}
    midas_weight = 0.3  # @param {type:"number"}
    near_plane = 200
    far_plane = 10000
    fov = 40  # @param {type:"number"}
    padding_mode = 'border'  # @param ['border', 'reflection', 'zeros'] {type:'string'}
    sampling_mode = 'bicubic'  # @param ['bicubic', 'bilinear', 'nearest'] {type:'string'}
    save_depth_maps = False  # @param {type:"boolean"}

    # @markdown ####**Video Input:**
    video_init_path = '/content/video_in.mp4'  # @param {type:"string"}
    extract_nth_frame = 1  # @param {type:"number"}
    overwrite_extracted_frames = True  # @param {type:"boolean"}
    use_mask_video = False  # @param {type:"boolean"}
    video_mask_path = '/content/video_in.mp4'  # @param {type:"string"}

    # @markdown ####**Hybrid Video for 2D/3D Animation Mode:**
    hybrid_video_generate_inputframes = False  # @param {type:"boolean"}
    hybrid_video_use_first_frame_as_init_image = True  # @param {type:"boolean"}
    hybrid_video_motion = "None"  # @param ['None','Optical Flow','Perspective','Affine']
    hybrid_video_flow_method = "Farneback"  # @param ['Farneback','DenseRLOF','SF']
    hybrid_video_composite = False  # @param {type:"boolean"}
    hybrid_video_comp_mask_type = "None"  # @param ['None', 'Depth', 'Video Depth', 'Blend', 'Difference']
    hybrid_video_comp_mask_inverse = False  # @param {type:"boolean"}
    hybrid_video_comp_mask_equalize = "None"  # @param  ['None','Before','After','Both']
    hybrid_video_comp_mask_auto_contrast = False  # @param {type:"boolean"}
    hybrid_video_comp_save_extra_frames = False  # @param {type:"boolean"}
    hybrid_video_use_video_as_mse_image = False  # @param {type:"boolean"}

    # @markdown ####**Interpolation:**
    interpolate_key_frames = False  # @param {type:"boolean"}
    interpolate_x_frames = 4  # @param {type:"number"}

    # @markdown ####**Resume Animation:**
    resume_from_timestring = False  # @param {type:"boolean"}
    resume_timestring = "20220829210106"  # @param {type:"string"}

    return locals()

# [ END DEFINES ]

#@markdown **Get Arguments**
tstart = time.time()
argv = sys.argv[1:]
pairs={}
pair_str = ""
argslist = False
xtrx = False
ytrx = False
ztrx = False
nolabel = False
fps=12
new_checkpoint = "anythingV3_fp16.ckpt"
try:
    opts, args = getopt.getopt(argv, "ha:c:X:Y:Z:n", [
        "help",
        "arglist=",
        "checkpoint=",
        "xtrx=",
        "ytrx=",
        "ztrx=",
        "nolabel",
    ])
except Exception as e:
    print(str(e))

for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp();
    if opt in ("-c", "--checkpoint"):
        new_checkpoint = arg;
    if opt in ("-a", "--arglist"):
        strAry=arg.split("|")
        for strVal in strAry:
            # print(strVal)
            pair = strVal.split("=")
            name =pair[0]
            val = pair[1]
            pairs[name]=val
            pair_str=str(pair)
            pair_str = pair_str.replace(" ","_")
            print(Fore.YELLOW+f"SETTING: {name}={val}"+Fore.RESET)
    if opt in ("-X", "--xtrx"):
        xtrx = arg;
    if opt in ("-Y", "--ytrx"):
        ytrx = arg;
    if opt in ("-Z", "--ztrx"):
        ztrx = arg;
    if opt in ("-n", "--nolabel"):
        nolabel = True;


setup_environment()

import torch
import random
import gc
import os
import clip
import google
from IPython import display
from helpers.render import render_animation, render_input_video, render_image_batch, render_interpolation
from helpers.aesthetics import load_aesthetics_model
from types import SimpleNamespace
from helpers.save_images import get_output_folder
from helpers.settings import load_args
from helpers.model_load import make_linear_decode, load_model, get_model_output_paths

# %%
# !! {"metadata":{
# !!   "cellView": "form",
# !!   "id": "0D2HQO-PWM_t"
# !! }}
#@markdown **Path Setup**

root = Root()
root = SimpleNamespace(**root)
root.models_path, root.output_path = get_model_output_paths(root)
root.model, root.device = load_model(root, load_on_run_all=True, check_sha256=True, map_location=root.map_location)

# %%
# !! {"metadata":{
# !!   "id": "6JxwhBwtWM_t"
# !! }}

# [ SETTINGS ]

# %%
# !! {"metadata":{
# !!   "cellView": "form",
# !!   "id": "E0tJVYA4WM_u"
# !! }}
# %%
# !! {"metadata":{
# !!   "id": "i9fly1RIWM_u"
# !! }}

prompts = []
# prompts = [
#     "an old fashioned photography camera"
#    "a beautiful portrait of a woman by Artgerm, trending on Artstation",
# ]

animation_prompts = {}
# animation_prompts = {
#     0: "a modern film camera"
#     # 20: "a beautiful banana, trending on Artstation",
#     # 30: "a beautiful coconut, trending on Artstation",
#     # 40: "a beautiful durian, trending on Artstation",
# }

# %%
# !! {"metadata":{
# !!   "cellView": "form",
# !!   "id": "XVzhbmizWM_u"
# !! }}

#@markdown **Load Settings**

override_settings_with_file = True #@param {type:"boolean"}
settings_file = "custom" #@param ["custom", "512x512_aesthetic_0.json","512x512_aesthetic_1.json","512x512_colormatch_0.json","512x512_colormatch_1.json","512x512_colormatch_2.json","512x512_colormatch_3.json"]

# [ Override vars with config settings ]

#! set setting file name
if 'custom_settings_file' in pairs:
    print(Fore.YELLOW+f">>> Loading {pairs['custom_settings_file']}"+Fore.RESET)
    custom_settings_file = pairs['custom_settings_file']
else:
    custom_settings_file = "settings/settings.txt"  # @param {type:"string"}

#! get the vals from the code
args_dict = DeforumArgs()
anim_args_dict = DeforumAnimArgs()

#! now get them from the settings file
#! not clear where/how these do the overwriting
if override_settings_with_file:
    load_args(args_dict, anim_args_dict, settings_file, custom_settings_file, verbose=False)

#! create a class-like namespace
args = SimpleNamespace(**args_dict)
anim_args = SimpleNamespace(**anim_args_dict)

#! override with commandline
for key in list(pairs.keys()):
    setattr(args,key,isNum(pairs,key))
    setattr(anim_args,key,isNum(pairs,key))

if xtrx:
    setattr(anim_args,'translation_x',xtrx)
if ytrx:
    setattr(anim_args,'translation_y',ytrx)
if ztrx:
    setattr(anim_args,'translation_z',ztrx)

#! explicity assign the prompt to whatever is in the cfg file
with open(custom_settings_file, "r") as f:
    jdata = json.loads(f.read())
    if "animation_prompts" in jdata:
        setattr(anim_args, "animation_prompts", jdata["animation_prompts"])
        animation_prompts = jdata["animation_prompts"]
    if "prompts" in jdata:
        setattr(args,"prompts",jdata["prompts"])
        prompts = jdata["prompts"]

    # if anim_args.animation_mode == 'None':
    #     setattr(args, "prompts", jdata["animation_prompts"])
    #     prompts=animation_prompts

# print(Fore.RED+json.dumps(args,cls=nsEncoder,indent=4)+Fore.RESET)
# print(Fore.GREEN+json.dumps(anim_args,cls=nsEncoder,indent=4)+Fore.RESET)

# x=input("waiting...")

# args.timestring = time.strftime('%Y%m%d%H%M%S')+"_"+args_dict['tag']
tstamp = time.strftime('%H%M%S')

args.timestring = tstamp+"_"+args.batch_name
savevar(tstamp,"/tmp/tstamp")

# args.timestring = time.strftime('%H%M%S')+"_"+args_dict['tag']+"_"+args.batch_name
args.strength = max(0.0, min(1.0, args.strength))


#! rewrite tyhe settings file
# save settings for the batch
settings_filename = f"safe/{args.timestring}_settings.txt"
with open(settings_filename, "w+", encoding="utf-8") as f:
    s = {**dict(args.__dict__), **dict(anim_args.__dict__)}
    json.dump(s, f, ensure_ascii=False, indent=4)



# Load clip model if using clip guidance
if (args.clip_scale > 0) or (args.aesthetics_scale > 0):
    root.clip_model = clip.load(args.clip_name, jit=False)[0].eval().requires_grad_(False).to(root.device)
    if (args.aesthetics_scale > 0):
        root.aesthetics_model = load_aesthetics_model(args, root)

if args.seed == -1:
    args.seed = random.randint(0, 2**32 - 1)
if not args.use_init:
    args.init_image = None
if args.sampler == 'plms' and (args.use_init or anim_args.animation_mode != 'None'):
    print(f"Init images aren't supported with PLMS yet, switching to KLMS")
    args.sampler = 'klms'
if args.sampler != 'ddim':
    args.ddim_eta = 0

if anim_args.animation_mode == 'None':
    anim_args.max_frames = 1
elif anim_args.animation_mode == 'Video Input':
    args.use_init = True

# clean up unused memory
gc.collect()
torch.cuda.empty_cache()

# dispatch to appropriate renderer
if anim_args.animation_mode == '2D' or anim_args.animation_mode == '3D':
    render_animation(args, anim_args, animation_prompts, root)
elif anim_args.animation_mode == 'Video Input':
    render_input_video(args, anim_args, animation_prompts, root)
elif anim_args.animation_mode == 'Interpolation':
    render_interpolation(args, anim_args, animation_prompts, root)
else:
    render_image_batch(args, prompts, root)

# %%
# !! {"metadata":{
# !!   "id": "gJ88kZ2-WM_v"
# !! }}
"""
# Create Video From Frames
"""

# %%
# !! {"metadata":{
# !!   "cellView": "form",
# !!   "id": "XQGeqaGAWM_v"
# !! }}


skip_video_for_run_all = False #@param {type: 'boolean'}
#@markdown **Manual Settings**
use_manual_settings = False #@param {type:"boolean"}
image_path = "/content/drive/MyDrive/AI/StableDiffusion/2023-01/StableFun/20230101212135_%05d.png" #@param {type:"string"}
mp4_path = "/content/drive/MyDrive/AI/StableDiffusion/2023-01/StableFun/20230101212135.mp4" #@param {type:"string"}
render_steps = False  #@param {type: 'boolean'}
path_name_modifier = "x0_pred" #@param ["x0_pred","x"]
make_gif = False
bitdepth_extension = "exr" if args.bit_depth_output == 32 else "png"

if not args_dict['save_settings']:
    os.system(f"rm {args.outdir}/*.txt")


print(Fore.YELLOW+f"anim_args.skip_video_for_run_all = [{anim_args.skip_video_for_run_all}]"+Fore.RESET)
print(Fore.YELLOW+f"anim_args.animation_mode = [{anim_args.animation_mode}]"+Fore.RESET)

print(Fore.RED+f"image_path = [{image_path}]"+Fore.RESET)

if anim_args.skip_video_for_run_all == True or anim_args.animation_mode == "None":
        print('Skipping video creation, uncheck skip_video_for_run_all if you want to run it')
        # if nolabel != False:
        files = glob.glob(f"outputs/batch/*{args.batch_name}*.png")
        for f in files:
            cmd = f"convert {f} -background black  -pointsize 48  -fill white label:{args.batch_name} -gravity Center -append {f}"
            print(Fore.GREEN+cmd+Fore.RESET)
            prun(cmd)
else:
    print(f"{image_path} -> {mp4_path}")

    if use_manual_settings:
        max_frames = "200" #@param {type:"string"}
    else:
        if render_steps: # render steps from a single image
            fname = f"{path_name_modifier}_%05d.png"
            all_step_dirs = [os.path.join(args.outdir, d) for d in os.listdir(args.outdir) if os.path.isdir(os.path.join(args.outdir,d))]
            newest_dir = max(all_step_dirs, key=os.path.getmtime)
            image_path = os.path.join(newest_dir, fname)
            print(f"Reading images from {image_path}")
            mp4_path = os.path.join(newest_dir, f"{args.timestring}_{path_name_modifier}.mp4")
            max_frames = str(args.steps)
        else: # render images for a video
            image_path = os.path.join(args.outdir, f"{args.timestring}_%05d.{bitdepth_extension}")
            print(Fore.CYAN+image_path+Fore.RESET)

            mp4_path = os.path.join(args.outdir, f"{args.timestring}.mp4")
            max_frames = str(anim_args.max_frames)

    # make video

    with open('/tmp/tstamp', 'r') as f:
        WC = f.read().strip()
    with open('/tmp/title', 'r') as f:
        TITLE = f.read().strip().replace("\n","\\n") # no spaces allowed in label, otherwise 'convert' crashes (fixable)


    cmd = [
        'ffmpeg',
        '-y',
        '-vcodec', bitdepth_extension,
        '-r', str(fps),
        '-start_number', str(0),
        '-i', image_path,
        # '-frames:v', max_frames,
        '-c:v', 'libx264',
        '-vf',
        f'fps={fps}',
        '-vf',
        f'scale=1024:1024',
        '-pix_fmt', 'yuv420p',
        '-crf', '17',
        '-preset', 'veryfast',
        '-pattern_type', 'sequence',
        mp4_path
    ]
    cmdline = f"ffmpeg -y -vcodec {bitdepth_extension} -r {str(fps)} -start_number {str(0)} -i {image_path}  -c:v libx264 -vf fps={str(fps)} -vf scale=1024:1024 -pix_fmt yuv420p -crf 17 -preset veryfast -pattern_type sequence  {mp4_path}"

    print(Fore.GREEN+cmdline+Fore.RESET)

    prun(cmd)
    # process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = process.communicate()
    # if process.returncode != 0:
    #     print(stderr)
    #     raise RuntimeError(stderr)

    if nolabel == False:
        label = TITLE.replace(' ','~')
        cmd=f'ffmpeg -loglevel panic  -y -i {mp4_path}  -vf drawtext=fontfile=/usr/share/fonts/noto/NotoSerif-Black.ttf:text=\'{label}\':fontcolor=white:fontsize=35:box=1:boxcolor=black@1.0:boxborderw=5:x=(w-text_w)/2:y=(h-text_h) -codec:a copy /tmp/out2.mp4'
        prun(cmd)
        os.system(f"mv /tmp/out2.mp4 {mp4_path}")


    mp4 = open(mp4_path,'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    display.display(display.HTML(f'<video controls loop><source src="{data_url}" type="video/mp4"></video>') )
    
    if make_gif:
         gif_path = os.path.splitext(mp4_path)[0]+'.gif'
         cmd_gif = [
             'ffmpeg',
             '-y',
             '-i', mp4_path,
             '-r', str(fps),
             gif_path
         ]
         process_gif = subprocess.Popen(cmd_gif, stdout=subprocess.PIPE, stderr=subprocess.PIPE)








# %%
# !! {"metadata":{
# !!   "cellView": "form",
# !!   "id": "MMpAcyrYWM_v"
# !! }}
skip_disconnect_for_run_all = True #@param {type: 'boolean'}

if skip_disconnect_for_run_all == True:
    print('Skipping disconnect, uncheck skip_disconnect_for_run_all if you want to run it')
else:
    from google.colab import runtime
    runtime.unassign()
tend = time.time()

print(Fore.RED+f"TOTAL TIME: {tend-tstart}"+Fore.RESET)

cmd = "aplay /home/jw/store/src/jmcap/ohlc/assets/ping.wav"
os.system(cmd)



# %%
# !! {"main_metadata":{
# !!   "accelerator": "GPU",
# !!   "colab": {
# !!     "provenance": []
# !!   },
# !!   "gpuClass": "standard",
# !!   "kernelspec": {
# !!     "display_name": "Python 3.10.6 ('dsd')",
# !!     "language": "python",
# !!     "name": "python3"
# !!   },
# !!   "language_info": {
# !!     "codemirror_mode": {
# !!       "name": "ipython",
# !!       "version": 3
# !!     },
# !!     "file_extension": ".py",
# !!     "mimetype": "text/x-python",
# !!     "name": "python",
# !!     "nbconvert_exporter": "python",
# !!     "pygments_lexer": "ipython3",
# !!     "version": "3.10.8"
# !!   },
# !!   "orig_nbformat": 4,
# !!   "vscode": {
# !!     "interpreter": {
# !!       "hash": "b7e04c8a9537645cbc77fa0cbde8069bc94e341b0d5ced104651213865b24e58"
# !!     }
# !!   }
# !! }}


#[ LOAD TIMES]
# 33.4368371963501  PROCESSING: 0675_anythingV3_fp16.ckpt
# 39.2281756401062  PROCESSING: 0675_modelshoot-1.0.safetensors
# 40.1274733543396  PROCESSING: 0675_abyssorangemix3AOM3_aom3a1b.safetensors
# 49.8161563873291  PROCESSING: 0675_elldrethsRetroMix_v10.safetensors
# 38.00232005119324  PROCESSING: 0675_f222.ckpt
# 38.25042915344238  PROCESSING: 0675_deliberate_v2.safetensors
# 38.29533767700195  PROCESSING: 0675_openjourney-v4.ckpt
# 38.59497308731079  PROCESSING: 0675_realisticVisionV20_v20.safetensors
# 38.84548902511597  PROCESSING: 0675_dreamlike-photoreal-2.0.ckpt
# 45.05635690689087  PROCESSING: 0675_Protogen_V2.2.ckpt
# 47.89648413658142  PROCESSING: 0675_meinamix_meinaV9.safetensors
# 50.15274477005005  PROCESSING: 0675_v1-5-pruned-emaonly.safetensors
# 66.51517939567566  PROCESSING: 0675_dreamshaper_5BakedVae.safetensors
# 37.683664083480835  PROCESSING: 0675_sd-v1-4.ckpt
# 50.614134311676025  PROCESSING: 0675_HassanBlend1.4_Safe.safetensors