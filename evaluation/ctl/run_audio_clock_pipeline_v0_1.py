#!/usr/bin/env python3
"""Audio -> evidence -> clock-state pipeline v0.1.
No benchmark condition label is used for the decision itself.
"""
from statistics import median
from audio_evidence_v0_1 import extract
from phase_restart_v0_3_uncertain import resolve

def active_fraction_in(ev,a,b):
    ts=ev['frame_times_s']; ac=ev['active']; vals=[v for t,v in zip(ts,ac) if a<=t<b]
    return sum(vals)/len(vals) if vals else 0.0

def run(wav,gap_start,gap_end,pre_ibi):
    ev=extract(wav); on=ev['onsets_s']
    pre=[t for t in on if t<gap_start]; post=[t for t in on if t>=gap_end]
    if not pre:return {'state':'UNCERTAIN','reason':'no_pre_events','evidence':{'onset_count':len(on)}}
    af=active_fraction_in(ev,gap_start,gap_end)
    # Very low activity is a directly observed silence state.
    if af<.08:return {'state':'SILENCE','confidence':'high','gap_active_fraction':af,'onset_count':len(on)}
    out=resolve(pre[-1],post,pre_ibi,True)
    out['gap_active_fraction']=af; out['onset_count']=len(on); out['last_pre_onset']=pre[-1]; out['post_onsets_used']=post[:5]
    return out

if __name__=='__main__':
 import argparse,json
 p=argparse.ArgumentParser(); p.add_argument('wav'); p.add_argument('gap_start',type=float); p.add_argument('gap_end',type=float); p.add_argument('pre_ibi',type=float)
 a=p.parse_args(); print(json.dumps(run(a.wav,a.gap_start,a.gap_end,a.pre_ibi),indent=2))
