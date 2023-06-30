#!/bin/env python
import random
import getopt, sys
import json
import os
from pprint import pprint
import genlib as g

# ^ define selection arrays

# inOrder = True

# all = fish
# all = biology


def rot_left(l, n):
    return l[n:] + l[:n]


def rot_right(l, n):
    return l[n:] - l[:n]


def shiftary(a):
    a = list(a)
    loops = random.choice([1,2,3,4]) #^ '4' is arbitray, and assume there are at least classes of type (biology, insects, etc)
    for j in range(loops):
        items = a[:5] #^ 5 is half of 10, which is the the number of elements in easy class aray (of biology, insects, etc)
        for item in items:
            a.remove(item)
            a.append(item)
    return a
def errprint(str):
    print(str, file=sys.stderr)


# ^ define finctions
def aorgUp(key, val):
    global aorg
    if key not in xkeys:
        aorg[key] = val;
    else:
        errprint(f"-------------------SKIPPING---- {key}")


def rn(a, idx):
    rv = a[idx]
    return rv


def r(a, **kwargs):
    global inOrder
    try:
        lastr = kwargs['lastr']
    except:
        lastr = False
    try:
        idx = kwargs['idx']
    except:
        idx = False

    if inOrder == 1:
        # return rn(a,idx)
        thisIdx = idx % len(a)
        rv = a[thisIdx]
        # errprint(f"{thisIdx},{a[thisIdx]}")
        return rv
    else:
        rv = random.choice(a)
        # errprint(f">>> {rv} : {lastr}")
        if rv == lastr:
            # errprint(f"\t research")
            rv = r(a, lastr=lastr)
        return rv


def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    
    -c, --count         number of unique objects/pairs
    -m,  --mult          frames per entry
    -s, --steps         pair transformations
    
    -t,  --type          type pof set ("micro", "bio", "animalsl")
    -S, --show          list of keys to show, ex. "key,key,key..."
    -X, --exclude       list of keys to exclude, ex. "key,key,key..."
    -o, --ordered       sequential (def random)    
    Varios 'types' are:
        "cells":    [cells]                      different cell-like things
        "bio":      [biology]
        "animals":  [snakes,fish,birds,animals]     (default)
        "reptiles"  [snakes]
        "insects"   [insects]
        "swamp"     [insects,snakes,fish]

    
'''
    print(rs)
    exit()


# [                               MAIN                                       ]

# - defaults
count = 10
mult = 10
sample_offset = round(mult/3)
checkpoint_offset = round((mult/3)*2)

steps = 10
runtime = 1.0
lines = False
showkey = False
xkeys = []
fps = 15
settype = "animals"
fromfile = "/home/jw/src/sdw/rando2_settings.txt"

lastr = False
lastc = False
lastpre = False
lastadj = False
lastverbs = False
lastall0 = False
lastall1 = False
lastplaces = False
lastbg = False
inOrder = 0

commandline = ' '.join(sys.argv)

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hc:m:t:f:s:X:S:o", [
        "help",
        "count=",
        "mult=",
        "type=",
        "from=",
        "show=",
        "exclude=",
        "steps=",
        "ordered",
    ])
except Exception as e:
    print(str(e))
for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-c", "--count"):
        count = int(arg)
    if opt in ("-o", "--ordered"):
        inOrder = 1
    if opt in ("-m", "--mult"):
        mult = int(arg)
        sample_offset = round(mult / 3)
        checkpoint_offset = round((mult / 3) * 2)
    if opt in ("-S", "--steps"):
        steps = int(arg)
    if opt in ("-f", "--from"):
        fromfile = arg
    if opt in ("-s", "--show"):
        showkey = arg
    if opt in ("-X", "--exclude"):
        xkeys = arg.split(",")
    if opt in ("-t", "--type"):
        settype = arg


# pprint(opts)

# all = g.birds + g.clothes + g.fish + g.flowers + g.instruments + g.snakes + g.things
# if settype == "animals":
#     all = g.birds + g.clothes + g.fish + g.flowers + g.instruments + g.snakes + g.things
#
# if settype=="micro":
#     all = g.biology

#--------------------------------------------------------------------------
uniall = []
alters1 = []
alters2 = []
nl = []
if settype == "cells":arrays = [g.cells]
if settype == "bio":arrays = [g.biology]
if settype == "animals":arrays = [g.snakes,g.fish,g.birds,g.animals]
if settype == "reptiles":arrays = [g.snakes]
if settype == "insects":arrays = [g.insects]
if settype == "swamp":arrays = [g.insects,g.snakes,g.fish]
if settype == "test":arrays = [g.test,g.test[::-1]]
if settype == "ordered1":arrays = [g.ordered1+g.ordered1]
if settype == "birds":arrays = [g.birds]
if settype == "fish":arrays = [g.fish]
if settype == "flowers":arrays = [g.flowers]
if settype == "dna":arrays = [g.dna]

if inOrder == 0:
    random.shuffle(arrays) #^ randomize the elements
    for a in arrays:
        nl=nl+a
        random.shuffle(a)
        # nl = random.sample(a, 10) #^ get just the first 10 (that means every array in genlib must have at least 10 items)
else:
    for a in arrays:
        nl = a[:14] #^ get just the first 14 as there will never be a count > 14

nl = nl[:14]
nl.reverse()
for i in nl:
    uniall.append(i)

uniall.reverse()

errprint(f"UNIALL-1: {uniall}")


# ^ load original template into JSON array
f = open(fromfile)
aorg = json.load(f)

#- make prompts
aprompts = {}

# ^ first build array of pairs
# ary1 = g.fish + g.birds
# ary2 = g.flowers + g.snakes

# ary1=g.uniall1
# ary2=g.uniall2


pairs = []
# alters = [ary1, ary2]


newall0 = r(uniall, lastr=lastall0, idx=0)
uniall = rot_left(uniall,1)  #^ offset arrays so there are no dups in the pairs
newall1 = r(uniall, lastr=newall0, idx=0)


# errprint(f"{newall0} -----------> {newall1}")

for i in range(1, count + 1):
    pairs.append(f"{newall1}:{newall0}")
    newall0 = newall1
    # newall0 = r(uniall, lastr=lastall0, idx=0)
    uniall = rot_left(uniall,1)
    newall1 = r(uniall, lastr=newall1, idx=False)
    lastall0 = newall0
    lastall1 = newall1

prelist = []
for i in range(count):
    pair = pairs[i]
    newpre = r(g.pre, lastr=lastpre, idx=i)
    newadj = r(g.adj, lastr=lastadj, idx=i)
    newverbs = r(g.verbs, lastr=lastverbs, idx=i)
    newplaces = r(g.places, lastr=lastplaces, idx=i)
    newbg = r(g.background, lastr=lastbg, idx=i)


    for j in range(steps):
        prelist.append(f"{newpre} of a  [{pair}: {round(j / steps, 2)}]")
    prelist.append(f"{newpre} of a  [{pair}: {1.0}]")

    lastpre = newpre
    lastadj = newadj
    lastverbs = newverbs
    lastplaces = newplaces
    lastbg = newbg

for i in range(len(prelist)):
    aprompts[i * mult] = f"{prelist[i]}"

aorgUp('prompts', aprompts)

#- make models
line = ""

for i in range(len(prelist)):
    newidx = (mult*i)+checkpoint_offset
    if newidx > (mult*i):
        newidx=newidx-mult
        if newidx < 0: newidx = 0

    newr = r(g.models, lastr=lastr, idx=i)
    line = line + f"{newidx}: (\"{newr}\"),"
    if i == len(prelist) - 1:
        line = line.strip(",")
    lastr = newr

aorgUp('checkpoint_schedule', line)

#- make samplers
line = ""
for i in range(len(prelist)):
    newidx = (mult*i)+sample_offset
    if newidx > (mult*i):
        newidx=newidx-mult
        if newidx < 0: newidx = 0
    newr = r(g.sampler, lastr=lastr, idx=i)
    line = line + f"{newidx}: (\"{newr}\"),"
    if i == len(prelist) - 1:
        line = line.strip(",")
    lastr = newr

aorgUp('sampler_schedule', line)

# [  here is where we set other vars ]

ttime = (count * mult * 5) + (count * 5)  # ^ time estimation
errprint(f"TOTAL RUN TIME: {ttime / 60}")


#- settings overrides
aorgUp('commandline', commandline)
max_frames = len(prelist) * mult
aorgUp("max_frames", max_frames )
errprint(f"max_frames: {max_frames}, x20: {max_frames * 20}")
max_ix_frames = (max_frames * 20) - 20
errprint(f"max_ix_frames (ix=20): {max_ix_frames}")




# aorg["translation_x"] = "0: (0)"
# aorg["seed"] = -1
# aorg["batch_name"] = "batch3"
# aorg["diffusion_cadence"]=4
# aorg["fps"]=60
# aorg["animation_prompts_positive"] = ""
# aorg["animation_prompts_negative"] = "nsfw, nude, human, man, woman, boy, girl, hands, face",

# errprint(f"Total Frames: {max_frames}   x20Ix: {max_frames * 20}")


# ^ rotation 1
# rot1 = False
# if rot1:
#     aorg["translation_x"] = "0:(2.5)",
#     aorg["translation_y"] = "0: (0)",
#     aorg["translation_z"] = "0:((0.125*(cos(120/15*3.141*t/30))+0.0))",
#     aorg["transform_center_x"] = "0: (0.5)",
#     aorg["transform_center_y"] = "0: (0.5)",
#     aorg["rotation_3d_x"] = "0: (0)",
#     aorg["rotation_3d_y"] = "0:(-0.5)",
#     aorg["rotation_3d_z"] = "0: (0)",


pgen = json.dumps(aorg, indent=4)
print(pgen)
# print(showkey)
if showkey:
    keys = showkey.split(",")
    # pprint(keys)
    for key in keys:
        errprint(f"-[{key}]-------------------------------------------------------")
        pgen = json.dumps(aorg[key], indent=4)
        if key == "sampler_schedule":
            items = pgen.split(",")
            for item in items:
                errprint(item)
        else:
            errprint(pgen)
