#!/usr/bin/env python3
"""Monte Carlo stress harness for phase_restart_v0_2_robust.
Deterministic seed. MB06 should restart; MB07 should continue.
"""
import random
from phase_restart_v0_2_robust import robust_phase_restart

def seq(start,ibi,n): return [start+i*ibi for i in range(n)]
def jitter(xs,sigma,rng): return [x+rng.gauss(0,sigma) for x in xs]
def trial(case,sigma,miss_prob,rng):
    if case=='MB06':
        ibi=.6; last=11.65; post=seq(15.25,ibi,8); expected=True
    else:
        ibi=60/105; last=11.678571; # choose first post event on extrapolated clock
        k=round((20.0-last)/ibi); first=last+k*ibi; post=seq(first,ibi,8); expected=False
    post=jitter(post,sigma,rng)
    kept=[x for x in post if rng.random()>=miss_prob]
    r=robust_phase_restart(last,kept,ibi,True)
    return r['phase_restart']==expected,r

def run(n=1000):
    rng=random.Random(20260820)
    rows=[]
    for sigma in [0,.003,.005,.010,.020]:
        for miss in [0,.05,.10,.20]:
            for case in ['MB06','MB07']:
                ok=0; undec=0
                for _ in range(n):
                    good,r=trial(case,sigma,miss,rng); ok+=good; undec+=r.get('reason')=='insufficient'
                rows.append((case,sigma,miss,ok,n,undec))
    return rows
if __name__=='__main__':
    print('case\tsigma_s\tmiss_prob\tcorrect\tn\tinsufficient')
    for r in run(): print('\t'.join(map(str,r)))
