#!/bin/env python

from colorama import init, Fore, Back
from pprint import pprint
import proclib as p
import procvars as g
import os
init()

os.system("mv /home/jw/src/sdw/outputs/img2img-images/batch3/*settings.txt /home/jw/src/sdc/settings 2> /dev/null")
os.system("mv /home/jw/src/sdw/outputs/img2img-images/batch3/*srt /home/jw/src/sdc/settings 2> /dev/null")

os.system("mv /home/jw/src/sdc/safe/QUEUE/*srt /home/jw/src/sdc/settings 2> /dev/null")
os.system("mv /home/jw/src/sdc/safe/QUEUE/*settings.txt /home/jw/src/sdc/settings 2> /dev/null")

print("moved all settings files to ~/src/sdc/settings")

p.cleanTree2("/fstmp")
p.cleanWildcard("/tmp/*.PNG")
p.cleanWildcard("/tmp/*.png")
p.cleanWildcard("/tmp/*.BAK")
p.cleanTree2(f"{g.rifedir}/frames")
p.cleanTree2(f"{g.esgrandir}/results")
p.cleanTree2('/home/jw/.local/share/Trash')
p.cleanTree2('/home/jw/store/.Trash-1000')
# p.cleanTree2('/run/user/1000/kio-fuse-jnwddn/trash/')

