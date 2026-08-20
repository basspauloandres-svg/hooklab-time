#!/usr/bin/env python3
"""Clock/evidence state resolver v0.1 for MB05-MB07.
Separates acoustic evidence availability from musical-clock state.
This layer consumes event evidence plus explicit audio-activity evidence; it does not
solve tactus octave, meter or accent.
"""
from dataclasses import dataclass

@dataclass
class Config:
    expected_ibi_tolerance: float=.18
    missing_beats_for_gap: float=2.5
    active_audio_floor: float=.15
    reacquire_intervals: int=2

def classify_gap(last_t,next_t,expected_ibi,audio_activity,phase_restart=False,cfg=Config()):
    gap=next_t-last_t
    missing=max(0.0,gap/expected_ibi-1.0)
    if missing < cfg.missing_beats_for_gap:
        return {'state':'CONTINUOUS_CLOCK','gap_s':gap,'missing_beats':missing}
    if audio_activity < cfg.active_audio_floor:
        return {'state':'SILENCE_EVIDENCE_GAP','clock_action':'SUSPEND_INFERENCE','gap_s':gap,'missing_beats':missing}
    if phase_restart:
        return {'state':'CLOCK_STOP_RESTART','clock_action':'STOP_AND_RELOCK_PHASE','gap_s':gap,'missing_beats':missing}
    return {'state':'LOW_EVIDENCE_CLOCK_CONTINUES','clock_action':'PREDICT_THROUGH_GAP','gap_s':gap,'missing_beats':missing}

def reacquisition(intervals,expected_ibi,cfg=Config()):
    good=[abs(x-expected_ibi)/expected_ibi <= cfg.expected_ibi_tolerance for x in intervals[:cfg.reacquire_intervals]]
    return {'same_clock_reacquired':len(good)==cfg.reacquire_intervals and all(good),'intervals_checked':len(good)}
