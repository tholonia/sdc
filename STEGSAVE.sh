#!/bin/bash
ID=$1
TXT=$2
NOTES=$3
./stego.py --image ~/BATCH3/${ID}  --textfile ~/src/sdw/${TXT} --notes $3 --encode

#./stego.py -i ~/BATCH3/${ID}_000000000.png  -t ~/src/sdw/${TXT} -e
