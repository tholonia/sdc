#!/bin/bash

for i in `seq 10`; 
do 
	echo "~/src/sdc/genpair.py --count 6 --mult 6 --steps 6 -f sdw/rando2_settings.txt  -s prompts > xx_${i}"
done & 



