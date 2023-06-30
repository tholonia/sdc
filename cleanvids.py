#!/bin/env python

import os, sys, glob, getopt
from colorama import init, Fore, Back
from pprint import pprint
import ffmpeg
import subprocess
import shutil
from proclib import prun, splitnonalpha, getID, procTime, getFilesize, getFnames, cleanTree, cleanWildcard
import time
import procvars as g

init()
cleanTree(f"{g.rifedir}/images")
cleanTree(f"{g.rifedir}/frames")
cleanTree(f"{g.esgrandir}/results")
cleanWildcard("/tmp/*.mp4")
cleanWildcard("/tmp/*.BAK")

