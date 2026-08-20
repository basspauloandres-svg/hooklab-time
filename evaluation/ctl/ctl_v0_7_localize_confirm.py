#!/usr/bin/env python3
"""CTL v0.7 — robust event regime detection with honest time semantics.
`localized_t` estimates the start of the first confirmed changed interval.
`confirmed_t` is when sufficient later evidence exists to confirm it.
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

def _mad(xs):
    m=median(xs); return median([abs(x-m) for x in xs]) if xs else 0.0

def detect(events,cfg=Config()):
    if len(events)<cfg.history+cfg.persistence+1:return []
    ibis=[events[i]-events[i-1] for i in range(1,len(events))]
    out=[]; pending=[]; seg_start=0
    for i in range(cfg.history,len(ibis)):
        hist=ibis[max(seg_start,i-cfg.history):i]
        if len(hist)<3: continue
        center=median(hist); spread=max(_mad(hist),cfg.min_mad_s)
        x=ibis[i]; rel=abs(x-center)/max(center,1e-9); z=abs(x-center)/spread
        if rel>=cfg.rel_change and z>=cfg.mad_mult: pending.append((i,x,center))
        else: pending=[]
        if len(pending)>=cfg.persistence:
            recent=[p[1] for p in pending[-cfg.persistence:]]; rc=median(recent)
            coherent=max(abs(v-rc) for v in recent)<=max(.02*rc,2*cfg.min_mad_s)
            if coherent:
                first_i=pending[-cfg.persistence][0]
                out.append({
                    'localized_t':events[first_i],
                    'confirmed_t':events[i+1],
                    'confirmation_latency_s':events[i+1]-events[first_i],
                    'old_ibi_s':center,'new_ibi_s':rc,
                    'old_bpm':60/center,'new_bpm':60/rc,
                    'relative_change':abs(rc-center)/center
                })
                seg_start=i+1; pending=[]
    return out
