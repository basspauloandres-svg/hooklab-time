#!/usr/bin/env python3
"""HookLab TIME Continuous Tempo Layer v0.1.

Offline/auditable prototype for MB01-MB04. It consumes local tempo observations
(e.g. onset/BeatThis evidence) and produces a continuous tempo trajectory.
It intentionally does NOT solve tactus octave selection, meter, downbeat, silence,
fermata, or attack-dropout semantics.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable, Optional
import json, math

@dataclass
class Observation:
    t: float
    bpm: float
    confidence: float = 1.0
    source: str = "unknown"

@dataclass
class CTLPoint:
    t: float
    observed_bpm: float
    tempo_bpm: float
    slope_bpm_s: float
    confidence: float
    mode: str
    tempo_state: str
    source: str
    prediction_error_ratio: float

@dataclass
class CTLConfig:
    # Generic prototype constants; not song-specific.
    alpha_tempo: float = 0.35
    alpha_slope: float = 0.25
    stable_slope_bpm_s: float = 0.18
    discontinuity_ratio: float = 0.22
    discontinuity_persistence: int = 3
    lock_observations: int = 3
    min_confidence: float = 0.35

class ContinuousTempoLayer:
    def __init__(self, config: Optional[CTLConfig]=None):
        self.cfg=config or CTLConfig()

    def run(self, observations: Iterable[Observation]):
        obs=sorted([o for o in observations if o.bpm>0 and o.confidence>=self.cfg.min_confidence], key=lambda x:x.t)
        if not obs:
            return {"ctl_version":"0.1","tempo_curve":[],"discontinuities":[],"config":asdict(self.cfg)}
        points=[]; discontinuities=[]
        tempo=obs[0].bpm; slope=0.0; prev_t=obs[0].t
        mode="SEARCH"; bad=0; lock_count=1
        for i,o in enumerate(obs):
            dt=max(1e-6,o.t-prev_t) if i else 1e-6
            predicted=tempo+slope*dt
            err=abs(o.bpm-predicted)/max(predicted,1e-6)
            if i==0:
                mode="SEARCH"; state="STABLE"
            else:
                if err>self.cfg.discontinuity_ratio:
                    bad+=1; mode="RE_EVALUATE"
                else:
                    bad=0
                    if mode in ("SEARCH","LOCK"):
                        lock_count+=1
                        mode="TRACK" if lock_count>=self.cfg.lock_observations else "LOCK"
                    else: mode="TRACK"
                if bad>=self.cfg.discontinuity_persistence:
                    discontinuities.append({"t":o.t,"from_bpm":tempo,"to_bpm":o.bpm,"error_ratio":err})
                    tempo=o.bpm; slope=0.0; bad=0; lock_count=1; mode="LOCK"; state="DISCONTINUITY"
                else:
                    innovation=o.bpm-predicted
                    new_tempo=predicted+self.cfg.alpha_tempo*o.confidence*innovation
                    inst_slope=(new_tempo-tempo)/dt
                    slope=(1-self.cfg.alpha_slope)*slope+self.cfg.alpha_slope*inst_slope
                    tempo=new_tempo
                    if abs(slope)<=self.cfg.stable_slope_bpm_s: state="STABLE"
                    elif slope>0: state="DRIFT_UP"
                    else: state="DRIFT_DOWN"
            points.append(CTLPoint(o.t,o.bpm,tempo,slope,o.confidence,mode,state,o.source,err if i else 0.0))
            prev_t=o.t
        return {
            "ctl_version":"0.1",
            "config":asdict(self.cfg),
            "tempo_curve":[asdict(p) for p in points],
            "discontinuities":discontinuities,
            "summary":{
                "observations":len(obs),
                "discontinuity_count":len(discontinuities),
                "start_bpm":points[0].tempo_bpm,
                "end_bpm":points[-1].tempo_bpm,
                "states":{s:sum(p.tempo_state==s for p in points) for s in ["STABLE","DRIFT_UP","DRIFT_DOWN","DISCONTINUITY"]}
            }
        }

def observations_from_json(data):
    """Accept a simple list or {'observations': [...]} for reproducible offline tests."""
    rows=data.get("observations",data) if isinstance(data,dict) else data
    return [Observation(float(r["t"]),float(r["bpm"]),float(r.get("confidence",1)),str(r.get("source","unknown"))) for r in rows]

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--output")
    args=ap.parse_args()
    with open(args.input,encoding="utf-8") as f: data=json.load(f)
    result=ContinuousTempoLayer().run(observations_from_json(data))
    text=json.dumps(result,indent=2,ensure_ascii=False)
    if args.output:
        with open(args.output,"w",encoding="utf-8") as f:f.write(text+"\n")
    else: print(text)
