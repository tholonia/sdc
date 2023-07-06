#!/bin/env python

from colorama import init, Fore, Back
from pprint import pprint
import proclib as p
import procvars as g
init()

p.cleanAll(f"{g.rifedir}/frames")
p.cleanAll(f"{g.esgrandir}/results")
p.cleanWildcard("/tmp/*.mp4")
p.cleanWildcard("/tmp/images")
p.cleanWildcard("/tmp/frames")
p.cleanWildcard("/home/jw/src/Real-ESRGAN/results")
p.cleanTrash()

