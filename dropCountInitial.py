#!/bin/env python

from glob import glob
import json


count = len(glob("/fstmp/images/*png"))
countFile = open("/tmp/count.json","w")
countFile.write(json.dumps(count))
countFile.close()






