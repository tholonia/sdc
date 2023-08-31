#!/bin/env python
import getopt, sys
import os
import random
import json
from pprint import pprint
import proclib as p
from scipy.ndimage import interpolation,uniform_filter1d
from operator import itemgetter
import math
from colorama import Fore, init
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


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


def findPV(s,thresh):

    # Input signal
    t = np.arange(len(s))
    series = s#0.3*np.sin(t)+0.7*np.cos(2*t)-0.5*np.sin(1.2*t)

    # Threshold value (for height of peaks and valleys)
    # thresh = 2

    # Find indices of peaks
    peak_idx, _ = find_peaks(series, height=thresh)

    # Find indices of valleys (from inverting the signal)
    valley_idx, _ = find_peaks(-series, height=thresh)

    # Plot signal
    plt.plot(t, series)

    # Plot threshold
    plt.plot([min(t), max(t)], [thresh, thresh], '--')
    plt.plot([min(t), max(t)], [-thresh, -thresh], '--')

    # Plot peaks (red) and valleys (blue)
    plt.plot(t[peak_idx], series[peak_idx], 'r.')
    plt.plot(t[valley_idx], series[valley_idx], 'b.')

    peaks = len(series[peak_idx])
    valleys = len(series[valley_idx])

    return peaks,valleys

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

def modcurve(ary, xlabel,ylabel):
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
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.show()

    # ^ remergde into list or lists
    for i in range(len(ary)):
        ary[i][0] = xdat[i]
        ary[i][1] = y_smooth[i]

    # ^ make proper string for the config file
    strVal = ""
    for s in ary:
        strVal += f"{s[0]}:({round(s[1]*10)/10}),"

    return strVal, ary

def rndcurve(ary,xlabel,ylabel,limits):
    # ^ Add a little bit of randomness to the values in the array
    # for i in range(len(ary)):
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
    # limits = 5
    thresh=limits/3

    #^ check for poeaks and valleys

    # plt.show()
    y_smooth = p.normalize(y_smooth)
    y_smooth = p.np_normalize(np.array(y_smooth), limits * -1, limits)
    peaks,valleys = findPV(y_smooth,thresh)


    # ^ show the arrat
    # plt.plot(xdat, y_smooth)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # plt.show()

    # ^ remergde into list or lists
    for i in range(len(ary)):
        ary[i][0] = xdat[i]
        ary[i][1] = y_smooth[i]

    # ^ make proper string for the config file
    strVal = ""
    for s in ary:
        strVal += f"{s[0]}:({round(s[1]*10)/10}),"

    return strVal, ary, peaks,valleys

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


# [Rebuild "seed_scheduler" ---------------------------------------------------------------------------------------------

# ^ Get current onbject
# sch_list = splitEmbList(aorg['sampler_schedule'])

# ^ Get total number of frames
max_frames = aorg["max_frames"]
# ^ Get prompt keyframes
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

def findCurve(sch_list,limits,field):
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

    # limits = 4
    # strVal = rot_3d_z_jittery_left(newList)
    strVal, finalAry = normcurve(newList, cycles=3,min=limits*-1,max=limits)


    # strVal, finalAry = modcurve(finalAry)
    strVal, finalAry,peaks,valleys = rndcurve(finalAry,"Frame Number",field,limits)
    # print(strVal)
    # exit()
    return strVal,finalAry,peaks,valleys

# [Rebuild "rotation_3d_z" --------------------------------------------------------------------------------------
field ="rotation_3d_z"
found = False

minpeaks = 3
minvalleys=3

while found == False:
    strVal,finalAry,peaks,valleys = findCurve(splitEmbList(aorg[field]),4,field)
    # p.errprint(f"({peaks},{valleys})... searching for peaks and valleys >= {4/3}")
    # if peaks in [2,3,4] and valleys in [2,3,4]:
    if peaks >= minpeaks and valleys >= minvalleys:
        found = True
        p.errprint(f"rotation_3dz: {peaks}/{valleys}")

aorg[field] = strVal.strip(",")
aorgOut = json.dumps(aorg, indent=4)


# # [Rebuild "rotation_3d_y" --------------------------------------------------------------------------------------
field ="rotation_3d_y"
found = False

while found == False:
    strVal,finalAry,peaks,valleys = findCurve(splitEmbList(aorg[field]),1,field)
    # p.errprint(f"({peaks},{valleys})... searching for peaks and valleys >= {4/3}")
    # if peaks in [2,3,4] and valleys in [2,3,4]:
    if peaks >= minpeaks and valleys >= minvalleys:
        found = True
        p.errprint(f"rotation_3dy: {peaks}/{valleys}")

aorg[field] = strVal.strip(",")
aorgOut = json.dumps(aorg, indent=4)



# # [Rebuild "rotation_3d_x" --------------------------------------------------------------------------------------
field ="rotation_3d_x"
found = False

while found == False:
    strVal,finalAry,peaks,valleys = findCurve(splitEmbList(aorg[field]),1,field)
    # p.errprint(f"({peaks},{valleys})... searching for peaks and valleys >= {4/3}")
    # if peaks in [2,3,4] and valleys in [2,3,4]:
    if peaks >= minpeaks and valleys >= minvalleys:
        found = True
        p.errprint(f"rotation_3dx: {peaks}/{valleys}")

aorg[field] = strVal.strip(",")
aorgOut = json.dumps(aorg, indent=4)

print(aorgOut)
