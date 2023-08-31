#!/bin/env python

for m in range(1,5):
    f = 0
    t = 0
    for i in range(100):
        if i%m==0: f+=1
        else: t+=1
    print(f"m={m}",f"f={f}",f"t={t}",f"%={t/f*100}")
    
    