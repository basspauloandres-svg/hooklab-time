#!/usr/bin/env python3
"""CTL v0.6: robust event-level clock with median interval gating.
Designed after v0.5 noise stress. Uses local median/MAD of inter-event intervals,
requires persistent interval-regime mismatch, and does not use meter/accent.
"""
from dataclasses import dataclass
from statistics import median

@dataclass
class Config:
    history:int=7
    persistence:int=2
    rel_change:float=.12
    mad_mult:float=5.0
    min_mad_s:float=.004

def mad(xs):
    if not xs:return 0.0
    m=median(xs); return median([abs(x-m) for x in xs])

def detect(events,cfg=Config()):
    if len(events)<cfg.history+cfg.persistence+1:return []
    ibis=[events[i]-events[i-1] for i in range(1,len(events))]
    out=[]; pending=[]; seg_start=0
    for i in range(cfg.history,len(ibis)):
        hist=ibis[max(seg_start,i-cfg.history):i]
        if len(hist)<3:continue
        center=median(hist); spread=max(mad(hist),cfg.min_mad_s)
        x=ibis[i]; rel=abs(x-center)/max(center,1e-9); z=abs(x-center)/spread
        mismatch=rel>=cfg.rel_change and z>=cfg.mad_mult
        pending.append((i,x,center,rel,z)) if mismatch else pending.clear()
        if len(pending)>=cfg.persistence:
            # Require new intervals to agree with each other more than with old regime.
            recent=[p[1] for p in pending[-cfg.persistence:]]
            rc=median(recent)
            if max(abs(v-rc) for v in recent) <= max(.02*rc,2*cfg.min_mad_s):
                first=pending[-cfg.persistence][0]
                t=events[first+1]
                out.append({'t':t,'old_ibi':center,'new_ibi':rc,'old_bpm':60/center,'new_bpm':60/rc,'relative_change':abs(rc-center)/center})
                seg_start=i+1; pending=[]
    return out
