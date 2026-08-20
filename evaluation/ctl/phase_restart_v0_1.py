#!/usr/bin/env python3
"""Phase restart evidence v0.1.
Uses only event timing relative to the pre-gap clock; no condition labels.
A long active-audio gap can be called CLOCK_STOP_RESTART only when the first
post-gap events establish a stable same-tempo clock with phase incompatible with
continuation of the pre-gap clock. Silence is handled separately by audio activity.
"""
from dataclasses import dataclass
from math import floor
from statistics import median

@dataclass
class Config:
    phase_tol_cycles:float=.16
    tempo_tol:float=.12
    post_intervals:int=3

def circular_distance_cycles(x):
    x=x%1.0
    return min(x,1.0-x)

def phase_restart_evidence(last_pre, post_events, expected_ibi, audio_active, cfg=Config()):
    if not audio_active:
        return {'phase_restart':False,'reason':'silence'}
    if len(post_events)<cfg.post_intervals+1:
        return {'phase_restart':False,'reason':'insufficient_post_events'}
    ints=[post_events[i]-post_events[i-1] for i in range(1,cfg.post_intervals+1)]
    post_ibi=median(ints)
    tempo_ok=abs(post_ibi-expected_ibi)/expected_ibi<=cfg.tempo_tol
    cycles=(post_events[0]-last_pre)/expected_ibi
    phase_error=circular_distance_cycles(cycles)
    phase_incompatible=phase_error>cfg.phase_tol_cycles
    return {'phase_restart':bool(tempo_ok and phase_incompatible),'tempo_ok':tempo_ok,'post_ibi':post_ibi,'expected_ibi':expected_ibi,'phase_error_cycles':phase_error,'reason':'same_tempo_new_phase' if tempo_ok and phase_incompatible else 'continuation_compatible'}
