#!/bin/bash

# ls ~/BATCH3/*.png|awk -F"[./_]" '{print "proc_all.sh "$5" `pwd`/"$5"_settings.txt    3 48   6 24   12 12   24 6   48 3" }'


proc_all.sh 20230625024146 `pwd`/20230625024146_settings.txt 	3 48
proc_all.sh 20230625025257 `pwd`/20230625025257_settings.txt 	6 24
proc_all.sh 20230625025835 `pwd`/20230625025835_settings.txt 	12 12
proc_all.sh 20230625030123 `pwd`/20230625030123_settings.txt 	24 6
proc_all.sh 20230625030251 `pwd`/20230625030251_settings.txt 	48 3
