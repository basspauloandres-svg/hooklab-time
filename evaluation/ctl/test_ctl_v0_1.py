#!/usr/bin/env python3
from ctl_v0_1 import Observation, ContinuousTempoLayer

def linear(a,b,dur,step=.5):
    out=[]; t=0.0
    while t<=dur:
        out.append(Observation(t,a+(b-a)*(t/dur),1.0,'synthetic_local_tempo'))
        t+=step
    return out

def constant(bpm,dur,step=.5): return linear(bpm,bpm,dur,step)

def abrupt(a,b,at,dur,step=.5):
    out=[]; t=0.0
    while t<=dur:
        out.append(Observation(t,a if t<at else b,1.0,'synthetic_local_tempo'))
        t+=step
    return out

ctl=ContinuousTempoLayer()
cases={
 'MB01_proxy':constant(120,32),
 'MB02_proxy':linear(80,140,40),
 'MB03_proxy':linear(140,70,40),
 'MB04_proxy':abrupt(120,80,20,40),
}
for name,obs in cases.items():
    r=ctl.run(obs); s=r['summary']; print(name,s,'disc=',r['discontinuities'])

# Pre-implementation structural assertions, not final scientific thresholds.
r1=ctl.run(cases['MB01_proxy']); assert r1['summary']['discontinuity_count']==0
r2=ctl.run(cases['MB02_proxy']); assert r2['summary']['discontinuity_count']==0
r3=ctl.run(cases['MB03_proxy']); assert r3['summary']['discontinuity_count']==0
r4=ctl.run(cases['MB04_proxy']); assert r4['summary']['discontinuity_count']==1
print('CTL v0.1 proxy structural tests: PASS')
