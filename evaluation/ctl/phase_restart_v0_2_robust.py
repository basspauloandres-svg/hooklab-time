#!/usr/bin/env python3
"""Robust phase-restart detector v0.2.
Uses consensus over several post-gap events and interval median/MAD so one noisy or
missing event cannot alone create a CLOCK_STOP_RESTART decision.
"""
from dataclasses import dataclass
from statistics import median

@dataclass
class Config:
    phase_tol_cycles:float=.18
    tempo_tol:float=.14
    post_events:int=5
    min_phase_votes:int=3

def circ(x):
    x=x%1.0; return min(x,1.0-x)

def robust_phase_restart(last_pre,post,ibi,audio_active,cfg=Config()):
    if not audio_active:return {'phase_restart':False,'reason':'silence'}
    if len(post)<cfg.post_events:return {'phase_restart':False,'reason':'insufficient'}
    p=post[:cfg.post_events]
    ints=[p[i]-p[i-1] for i in range(1,len(p))]
    med=median(ints)
    # tolerate one doubled interval from a missed event by folding near integer multiples
    folded=[]
    for x in ints:
        k=max(1,round(x/ibi)); folded.append(x/k)
    post_ibi=median(folded)
    tempo_ok=abs(post_ibi-ibi)/ibi<=cfg.tempo_tol
    # Each post event votes on incompatibility with the extrapolated pre-gap phase.
    votes=[]
    for t in p:
        e=circ((t-last_pre)/ibi)
        votes.append(e>cfg.phase_tol_cycles)
    restart=tempo_ok and sum(votes)>=cfg.min_phase_votes
    return {'phase_restart':restart,'tempo_ok':tempo_ok,'post_ibi':post_ibi,'phase_votes':sum(votes),'events_checked':len(votes),'reason':'consensus_new_phase' if restart else 'continuation_or_uncertain'}
