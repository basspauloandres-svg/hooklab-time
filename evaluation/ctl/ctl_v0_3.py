#!/usr/bin/env python3
"""CTL v0.3 — continuous drift + adjacent-regime change-point evidence.
Phase A only. No meter, tactus-octave, silence or fermata semantics.
"""
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Observation:
    t: float; bpm: float; confidence: float=1.0; source: str='unknown'

@dataclass
class Config:
    history_n:int=5
    new_regime_n:int=2
    min_confidence:float=.35
    stable_slope:float=.30
    min_shift_bpm:float=12.0
    min_relative_shift:float=.10
    # New regime must be substantially more self-consistent than continuation.
    regime_advantage:float=.55

class CTLv03:
    def __init__(self,cfg:Optional[Config]=None): self.cfg=cfg or Config()
    @staticmethod
    def line(rows):
        xs=[r.t for r in rows]; ys=[r.bpm for r in rows]
        if len(rows)<2:return ys[-1],0.0
        xm=sum(xs)/len(xs); ym=sum(ys)/len(ys); den=sum((x-xm)**2 for x in xs)
        m=sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/den if den else 0.0
        return ym-m*xm,m
    @staticmethod
    def mae(vals,center): return sum(abs(v-center) for v in vals)/max(1,len(vals))

    def run(self,observations):
        obs=sorted([o for o in observations if o.bpm>0 and o.confidence>=self.cfg.min_confidence],key=lambda o:o.t)
        curve=[]; discs=[]; seg=[]; pending=[]
        for o in obs:
            hist=seg[-self.cfg.history_n:]
            if len(hist)<3:
                seg.append(o); curve.append({'t':o.t,'bpm':o.bpm,'state':'SEARCH','source':o.source}); continue
            a,m=self.line(hist); pred=a+m*o.t; shift=o.bpm-pred
            rel=abs(shift)/max(pred,1e-9)
            if abs(shift)>=self.cfg.min_shift_bpm and rel>=self.cfg.min_relative_shift:
                pending.append(o)
            else:
                pending=[]
            change=False; evidence=None
            if len(pending)>=self.cfg.new_regime_n:
                new=pending[-self.cfg.new_regime_n:]
                # Compare continuation errors with compactness of proposed new regime.
                cont_err=sum(abs(x.bpm-(a+m*x.t)) for x in new)/len(new)
                center=sum(x.bpm for x in new)/len(new)
                regime_err=self.mae([x.bpm for x in new],center)
                advantage=(cont_err-regime_err)/max(cont_err,1e-9)
                same_dir=len({1 if x.bpm>(a+m*x.t) else -1 for x in new})==1
                # Stable histories get faster change-point permission. Drifting histories
                # require stronger evidence, preventing accelerando/ritardando fragmentation.
                required=self.cfg.regime_advantage if abs(m)<=self.cfg.stable_slope else min(.90,self.cfg.regime_advantage+.25)
                change=same_dir and advantage>=required
                evidence={'continuation_mae':cont_err,'new_regime_mae':regime_err,'advantage':advantage,'history_slope':m,'required_advantage':required}
            if change:
                first=pending[-self.cfg.new_regime_n]
                discs.append({'t':first.t,'predicted_bpm':a+m*first.t,'observed_bpm':first.bpm,**evidence})
                seg=pending[-self.cfg.new_regime_n:]; pending=[]; state='DISCONTINUITY'
            else:
                seg.append(o)
                state='STABLE' if abs(m)<=self.cfg.stable_slope else ('DRIFT_UP' if m>0 else 'DRIFT_DOWN')
            curve.append({'t':o.t,'bpm':o.bpm,'predicted_bpm':pred,'history_slope':m,'relative_shift':rel,'state':state,'change_evidence':evidence,'source':o.source})
        return {'ctl_version':'0.3','config':asdict(self.cfg),'curve':curve,'discontinuities':discs,'summary':{'observations':len(obs),'discontinuity_count':len(discs)}}
