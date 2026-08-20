#!/usr/bin/env python3
"""Tactus octave resolver v0.1.
Consumes onset/event times plus salience. Tests whether a fast periodic layer contains
an alternating salience pattern that supports a slower every-other-event tactus.
No meter/accent/downbeat logic is used.
"""
from statistics import median

def _mad_ratio(xs):
    m=median(xs)
    if m<=0:return 1e9
    return median([abs(x-m) for x in xs])/m

def resolve(events,salience_ratio_thr=1.7,regularity_thr=.12):
    """events: list of {'t': seconds, 'salience': positive float}."""
    if len(events)<8:return {'state':'UNCERTAIN','reason':'insufficient_events'}
    t=[float(e['t']) for e in events]; s=[float(e['salience']) for e in events]
    base_ibi=median([t[i]-t[i-1] for i in range(1,len(t))])
    base_bpm=60/base_ibi
    candidates=[]
    for parity in (0,1):
        tp=t[parity::2]; sp=s[parity::2]; so=s[1-parity::2]
        if len(tp)<4 or len(so)<3:continue
        ibi2=[tp[i]-tp[i-1] for i in range(1,len(tp))]
        ratio=median(sp)/max(median(so),1e-12)
        regularity=_mad_ratio(ibi2)
        candidates.append({'parity':parity,'salience_ratio':ratio,'regularity':regularity,'half_bpm':60/median(ibi2)})
    if not candidates:return {'state':'UNCERTAIN','reason':'insufficient_parity_evidence'}
    best=max(candidates,key=lambda x:x['salience_ratio'])
    if best['salience_ratio']>=salience_ratio_thr and best['regularity']<=regularity_thr:
        return {'state':'HALF_TIME_SUPPORTED','selected_bpm':best['half_bpm'],'base_layer_bpm':base_bpm,**best}
    return {'state':'BASE_LAYER_SUPPORTED','selected_bpm':base_bpm,'base_layer_bpm':base_bpm,**best}
