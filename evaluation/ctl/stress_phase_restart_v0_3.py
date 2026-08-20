#!/usr/bin/env python3
import random
from phase_restart_v0_3_uncertain import resolve

def seq(start,ibi,n): return [start+i*ibi for i in range(n)]
def jitter(xs,s,r): return [x+r.gauss(0,s) for x in xs]
def trial(case,sigma,miss,r):
    if case=='MB06b': ibi=.6; last=11.65; post=seq(15.40,ibi,8); expected='CLOCK_STOP_RESTART'
    else:
        ibi=60/105; last=11.678571; k=round((20-last)/ibi); post=seq(last+k*ibi,ibi,8); expected='CLOCK_CONTINUES'
    kept=[x for x in jitter(post,sigma,r) if r.random()>=miss]
    out=resolve(last,kept,ibi,True)
    return out['state'],expected

def run(n=2000):
    r=random.Random(20260820); rows=[]
    for sigma in [0,.005,.010,.020]:
      for miss in [0,.10,.20,.30,.40]:
       for case in ['MB06b','MB07']:
        correct=wrong=uncertain=0
        for _ in range(n):
            state,expected=trial(case,sigma,miss,r)
            if state=='UNCERTAIN': uncertain+=1
            elif state==expected: correct+=1
            else: wrong+=1
        rows.append({'case':case,'jitter_s':sigma,'miss_prob':miss,'n':n,'correct':correct,'wrong':wrong,'uncertain':uncertain})
    return rows
if __name__=='__main__':
 import json; print(json.dumps(run(),indent=2))
