#!/usr/bin/env python3
"""CTL v0.2 — persistent model-mismatch discontinuity detector.

Phase A only (MB01-MB04). Adds a second model: continuation of a locally fitted
linear tempo trajectory. A discontinuity is proposed when recent observations
show a coherent level shift that is poorly explained by that trajectory.
No tactus octave, meter, silence or fermata logic is included.
"""
from dataclasses import dataclass, asdict
from typing import Optional
import statistics

@dataclass
class Observation:
    t: float; bpm: float; confidence: float=1.0; source: str='unknown'

@dataclass
class Config:
    history_n: int=5
    mismatch_n: int=2
    min_confidence: float=.35
    relative_mismatch: float=.12
    slope_change_factor: float=2.5
    min_level_shift_bpm: float=12.0

class CTLv02:
    def __init__(self,cfg:Optional[Config]=None): self.cfg=cfg or Config()

    @staticmethod
    def fit_line(rows):
        if len(rows)<2: return rows[-1].bpm,0.0
        xs=[r.t for r in rows]; ys=[r.bpm for r in rows]
        xm=sum(xs)/len(xs); ym=sum(ys)/len(ys)
        den=sum((x-xm)**2 for x in xs)
        slope=sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/den if den else 0.0
        intercept=ym-slope*xm
        return intercept,slope

    def run(self,observations):
        obs=[o for o in observations if o.bpm>0 and o.confidence>=self.cfg.min_confidence]
        obs.sort(key=lambda o:o.t)
        if not obs:return {'ctl_version':'0.2','curve':[],'discontinuities':[]}
        curve=[]; discs=[]; segment=[]; mismatch=[]
        for o in obs:
            hist=segment[-self.cfg.history_n:]
            if len(hist)>=3:
                a,slope=self.fit_line(hist)
                pred=a+slope*o.t
                rel=abs(o.bpm-pred)/max(pred,1e-9)
                level_shift=abs(o.bpm-pred)
                mismatch.append((o,rel,level_shift,pred,slope))
                if len(mismatch)>self.cfg.mismatch_n:mismatch=mismatch[-self.cfg.mismatch_n:]
                coherent=(len(mismatch)==self.cfg.mismatch_n and all(x[1]>=self.cfg.relative_mismatch and x[2]>=self.cfg.min_level_shift_bpm for x in mismatch))
                # Require mismatch direction to agree across persistence window.
                same_dir=coherent and len({1 if x[0].bpm>x[3] else -1 for x in mismatch})==1
                if same_dir:
                    first=mismatch[0]
                    discs.append({'t':first[0].t,'predicted_bpm':first[3],'observed_bpm':first[0].bpm,'relative_mismatch':first[1],'history_slope_bpm_s':first[4]})
                    segment=[x[0] for x in mismatch]
                    mismatch=[]
                    state='DISCONTINUITY'
                    curve.append({'t':o.t,'bpm':o.bpm,'state':state,'source':o.source})
                    continue
                # If observation is compatible, clear stale mismatch evidence.
                if rel<self.cfg.relative_mismatch: mismatch=[]
                state='STABLE' if abs(slope)<.18 else ('DRIFT_UP' if slope>0 else 'DRIFT_DOWN')
            else:
                pred=o.bpm; rel=0.0; slope=0.0; state='SEARCH'
            segment.append(o)
            curve.append({'t':o.t,'bpm':o.bpm,'predicted_bpm':pred,'relative_mismatch':rel,'history_slope_bpm_s':slope,'state':state,'source':o.source})
        return {'ctl_version':'0.2','config':asdict(self.cfg),'curve':curve,'discontinuities':discs,'summary':{'observations':len(obs),'discontinuity_count':len(discs)}}
