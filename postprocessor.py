#!/home/jw/miniforge3/bin/python

#help("modules")
import os
print("VENV="+os.environ['VIRTUAL_ENV'],flush=True)
import sys
sys.path.append("/home/jw/src/sdc")
import proclib as p
import pickle
from pprint import pprint
from colorama import init, Fore
init()



pickle_in = open("/tmp/post.pickle","rb")
pdict = pickle.load(pickle_in)
pprint(pdict["batch_name"])

try:
    pp = str(pdict["batch_name"]).split("_")
    ID=pp[1]
except:
    ID=False

location = f"/home/jw/src/sdw/outputs/img2img-images/{pdict['batch_name']}/{ID}.mp4"


cmd = "/bin/aplay /home/jw/src/sdc/settings/RESOURCES/sound1.wav"
for i in range(3):
    os.system(cmd)


#cmd = f"/home/jw/src/sdc/P_vidlabel.py -f {location} -F 50 -l 'This~is~a~test'"
# print(Fore.YELLOW + cmd + Fore.RESET)
# p.prun(cmd)



