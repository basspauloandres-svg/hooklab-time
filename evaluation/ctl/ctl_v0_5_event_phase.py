#!/usr/bin/env python3
"""CTL v0.5 — event-level IBI/phase discontinuity detector for Phase A.

Designed for MB01-MB04. It uses onset-event times directly instead of only
6 s tempo windows. The goal is early abrupt-change localization while retaining
continuous accelerando/ritardando as drift.

This module does NOT solve tactus octave ambiguity, meter/downbeat/accent,
silence, fermata, or attack-dropout semantics.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable, Optional
import math

@dataclass
class Config:
    history_intervals: int = 5
    confirmation_intervals: int = 2
    relative_prediction_error: float = 0.15
    new_regime_cv_max: float = 0.08


def _fit_line(xs, ys):
    xm=sum(xs)/len(xs); ym=sum(ys)/len(ys)
    den=sum((x-xm)**2 for x in xs)
    m=sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/den if den else 0.0
    a=ym-m*xm
    return a,m


def _mean(v): return sum(v)/len(v)
def _std(v):
    mu=_mean(v)
    return math.sqrt(sum((x-mu)**2 for x in v)/len(v))


def detect_discontinuities(onset_times: Iterable[float], config: Optional[Config]=None):
    cfg=config or Config()
    on=sorted(float(x) for x in onset_times)
    if len(on)<cfg.history_intervals+cfg.confirmation_intervals+1:
        return {"ctl_version":"0.5-event-phase","config":asdict(cfg),"discontinuities":[]}
    ibis=[on[i+1]-on[i] for i in range(len(on)-1)]
    mids=[(on[i+1]+on[i])/2 for i in range(len(on)-1)]
    out=[]; segment_start=0; i=cfg.history_intervals
    while i <= len(ibis)-cfg.confirmation_intervals:
        h0=max(segment_start,i-cfg.history_intervals)
        if i-h0<cfg.history_intervals:
            i+=1; continue
        xs=mids[h0:i]; ys=ibis[h0:i]
        a,m=_fit_line(xs,ys)
        cur=ibis[i:i+cfg.confirmation_intervals]
        pred=[a+m*mids[j] for j in range(i,i+cfg.confirmation_intervals)]
        rel=[abs(c-p)/max(p,1e-9) for c,p in zip(cur,pred)]
        signs=[1 if c>p else -1 for c,p in zip(cur,pred)]
        cv=_std(cur)/max(_mean(cur),1e-9)
        confirmed=(all(r>=cfg.relative_prediction_error for r in rel) and len(set(signs))==1 and cv<=cfg.new_regime_cv_max)
        if confirmed:
            out.append({
                "t":on[i],
                "history_bpm":60.0/ys[-1],
                "new_regime_bpm":60.0/_mean(cur),
                "relative_prediction_errors":rel,
                "history_ibi_slope_per_s":m,
                "confirmation_intervals":cfg.confirmation_intervals,
            })
            segment_start=i
            i=segment_start+cfg.history_intervals
        else:
            i+=1
    return {"ctl_version":"0.5-event-phase","config":asdict(cfg),"discontinuities":out,"summary":{"onsets":len(on),"discontinuity_count":len(out)}}
