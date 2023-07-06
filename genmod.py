#!/bin/env python
import getopt, sys
import os
import random
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import proclib as p
from scipy.ndimage import interpolation,uniform_filter1d
from operator import itemgetter
import math
from colorama import Fore, init

init()

# ^ define selection arrays


#
# # ^ define finctions
# def aorgUp(key, val):
#     global aorg
#     if key not in xkeys:
#         aorg[key] = val;
#     else:
#         p.errprint(f"-------------------SKIPPING---- {key}")
#


def showhelp():
    print("help")
    rs = """
    -h, --help          show help
    -f, --filename      setting file

"""
    print(rs)
    exit()


# [                               MAIN                                       ]

# - defaults

locationpath = "/home/jw/src/sdw/x"
dirname = os.getcwd()
basename = False

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv,
        "hf:",
        [
            "help",
            "file=",
        ],
    )
except Exception as e:
    print(str(e))
for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-f", "--file"):
        locationpath = arg
# --------------------------------------------------------------------------
basename,dirname,fspec,srcfile = p.getFnames((locationpath))
srcfile = f"{dirname}/{basename}"

p.errprint(f"dirname: {dirname}")
p.errprint(f"basename: {basename}")
p.errprint(f"srcfile:{srcfile}")
p.errprint(f"fspec:{fspec}")

f = open(srcfile)
aorg = json.load(f)

# ^parse into array
samp_sch = aorg["sampler_schedule"]
seed_sch = aorg["seed_schedule"]

"""
0:          (s), 
1:          (-1), 
"max_f-2":  (-1), 
"max_f-1":  (s)

"""
def splitEmbList(s):
    rs = []
    # print(Fore.RED + s + Fore.RESET)
    p.errprint("")
    # samp_sch_matches = list(re.findall('([0-9]*):....([A-Za-z0-9+\s]*)',seed_sch,re.DOTALL))
    # samp_sch_matches = list(re.findall('(.*), (.*)', seed_sch,re.DOTALL))
    sch_items = s.split(",")  #

    for si in sch_items:
        sip = si.split(":")
        val = sip[1].strip()
        val = val.strip("(")
        val = val.strip(")")
        val = val.replace('"', "")
        rs.append([sip[0], val])
        # print(isip,val)
    # rs = sorted(rs)
    # pprint(rs)
    # print("")
    return rs


# [Rebuild "seed_scheduler" ---------------------------------------------------------------------------------------------

# ^ Get current onbjecty
# sch_list = splitEmbList(aorg['sampler_schedule'])

# ^ Get total number of frames
max_frames = aorg["max_frames"]
# ^ Get prompt keyframs
prompts = aorg["prompts"]
promptFrames = []
for key in prompts:
    promptFrames.append(int(key))
# pprint(promptFrames)
# exit()

# ^ make new element list
newList = []

seedVal = 1
# for frameNum in promptFrames:
for i in range(max_frames):
    newList.append([i, seedVal])
    # ^ increment seed
    seedVal += 1
# pprint(newList)

"""
seed_schedule need to look like:  
    "0:(s), 1:(-1), \"max_f-2\":(-1), \"max_f-1\":(s)"
or
    "0:(1), 1:(2), 3:(3), 4:(4)"    
"""

# ^ Make vals
strVal = ""
for s in newList:
    strVal += f"{s[0]}:({s[1]}),"

aorg["seed_schedule"] = strVal.strip(",")

aorgOut = json.dumps(aorg, indent=4)


# ----------------------------------------------------------------------------------------------------------------------

# [Rebuild "rotation_3d_z" --------------------------------------------------------------------------------------
# ^ Get current onbjecty
sch_list = splitEmbList(aorg["rotation_3d_z"])

# ^ Get total number of frames
max_frames = aorg["max_frames"]
# ^ Get prompt keyframs
prompts = aorg["prompts"]
promptFrames = []
for key in prompts:
    promptFrames.append(int(key))
# pprint(promptFrames)
# exit()

# ^ make new element list
newList = []

rotVal = 1
# for frameNum in promptFrames:
for i in range(max_frames):
    newList.append([i, rotVal])
    # ^ increment seed
    rotVal += 1
# pprint(newList)

"""
rotation_3d_z need to look like:  
    0: ((sin(((t*2)*3.14)/180)*2))
or
    "0:(0.0), 1:(0.1), 3:(0.2), 4:(0.3)"    
"""

# ^ Make vals

# def tryit(kwargs,arg,default):
#     try:
#         rs = kwargs[arg]
#     except:
#         rs = default
#     return rs
def normcurve(xAxis,**kwargs):
    cycles = p.tryit(kwargs,"cycles",0)
    amin = p.tryit(kwargs,"min",0)
    amax = p.tryit(kwargs,"max",1)

    rotAry = []

    i=0
    div = 250
    while (i < div*2):
        x = i #xAxis[i][0]
        seg = x % div
        deg = seg * (90 / (div - 1))
        adj = math.sin(math.radians(deg))
        rotAry.append(adj)
        if (x % (div-1)) == 0 and i > 0:
            for j in range(div):
                i += 1
                rotAry.append(rotAry[div-(j+1)])
        i+=1

    rotAry2 = []
    for k in range(cycles):
        for r in rotAry:
            rotAry2.append(r)
        for r in rotAry:
            rotAry2.append(r*-1)

    rotAry2 = p.np_normalize(rotAry2, amin,amax)
    x = np.array(rotAry2+rotAry2.copy()+rotAry2.copy())
    i = len(xAxis)
    z = i / len(x)
    rotAryResize = interpolation.zoom(x,z)

    finalAry = []
    for i in range(len(rotAryResize)):
        finalAry.append([xAxis[i][0],rotAryResize[i]])

    strVal = ""
    for s in finalAry:
        strVal += f"{s[0]}:({round(s[1]*10)/10}),"

    return strVal, finalAry

def modcurve(ary):
    # ^ Add a little bit of randomness to the values in the array
    for i in range(len(ary)):
        ary[i][1] = random.uniform(ary[i][1] * 1, ary[i][1] * 1.618)

    # ^ split areray into x and y data arrays
    xdat = list(map(itemgetter(0), ary))
    ydat = list(map(itemgetter(1), ary))

    # ^ smooth the data
    y_smooth = uniform_filter1d(ydat, size=100)

    # ^ normalize to a range... needs both to return correct array size
    y_smooth = p.normalize(y_smooth)
    y_smooth = p.np_normalize(np.array(y_smooth), -5, 5)

    # ^ show the arrat
    plt.plot(xdat, y_smooth)
    plt.show()

    # ^ remergde into list or lists
    for i in range(len(ary)):
        ary[i][0] = xdat[i]
        ary[i][1] = y_smooth[i]

    # ^ make proper string for the config file
    strVal = ""
    for s in ary:
        strVal += f"{s[0]}:({round(s[1]*10)/10}),"

    return strVal, ary

def rndcurve(ary):
    # ^ Add a little bit of randomness to the values in the array
    # for i in range(len(ary)):
    #     ary[i][1] = random.uniform(ary[i][1] * 1, ary[i][1] * 1.618)

    #^ make random curve
    cyc = random.randint(2,30)
    cycary = []
    for i in range(cyc):
        cycary.append(random.randint(0,1000))
    x = np.array(cycary)
    i = len(ary)
    z = i / len(x)
    cycResize = interpolation.zoom(x,z)
    # print(cycResize)

    # ^ split areray into x and y data arrays
    xdat = list(map(itemgetter(0), ary))
    ydat = cycResize

    # ^ smooth the data
    y_smooth = uniform_filter1d(ydat, size=100)

    # ^ normalize to a range... needs both to return correct array size
    y_smooth = p.normalize(y_smooth)
    y_smooth = p.np_normalize(np.array(y_smooth), -5, 5)

    # ^ show the arrat
    plt.plot(xdat, y_smooth)
    plt.show()

    # ^ remergde into list or lists
    for i in range(len(ary)):
        ary[i][0] = xdat[i]
        ary[i][1] = y_smooth[i]

    # ^ make proper string for the config file
    strVal = ""
    for s in ary:
        strVal += f"{s[0]}:({round(s[1]*10)/10}),"

    return strVal, ary

def rot_3d_z_jittery_left(newlist):
    """
    create a slightly jittery rotation that tends to the left
    """
    i = 0
    newZary = []
    strVal = ""
    while i < len(newList):
        amin = -5
        amax = 5
        ri = random.randint(amin, amax)
        newZary.append([i, p.cycle_in_range(amin, amax, ri) / 10])
        i += 1

    for s in newZary:
        strVal += f"{s[0]}:({s[1]}),"

    return strVal


# def newrot3d(newList):
#     """
#     create a slightly jittery rotation that tends to the left
#     """
#     i = 0
#     newZary =
#     strVal = ""
#     while i < len(newList):
#         amin = -5
#         amax = 5
#         ri = random.randint(amin, amax)
#         newZary.append([i, p.cycle_in_range(amin, amax, ri) / 10])
#         i += 1
#
#     for s in newZary:
#         strVal += f"{s[0]}:({s[1]}),"
#
#     return strVal


# strVal = rot_3d_z_jittery_left(newList)
strVal, finalAry = normcurve(newList, cycles=3,min=-6,max=6)
# strVal, finalAry = modcurve(finalAry)
strVal, finalAry = rndcurve(finalAry)
# print(strVal)
# exit()
aorg["rotation_3d_z"] = strVal.strip(",")
aorgOut = json.dumps(aorg, indent=4)

# ----------------------------------------------------------------------------------------------------------------------
print(aorgOut)
