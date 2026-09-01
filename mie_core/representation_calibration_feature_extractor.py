#!/usr/bin/env python3
"""Provider-neutral feature extractor for paired vocal melody representations."""
from __future__ import annotations
import math,statistics

def hz_to_midi(hz): return 69+12*math.log2(float(hz)/440.0) if hz and float(hz)>0 else None

def features(events):
 # event: {start,end,pitch_midi} or {start,end,freq_hz}
 seq=[]
 for e in events:
  p=e.get('pitch_midi');p=float(p) if p is not None else hz_to_midi(e.get('freq_hz'))
  if p is not None: seq.append((float(e['start']),float(e['end']),p))
 if len(seq)<2:return {'n_events':len(seq)}
 pitches=[x[2] for x in seq];ints=[b-a for a,b in zip(pitches,pitches[1:])]
 return {'n_events':len(seq),'pitch_range_st':max(pitches)-min(pitches),'median_pitch_st':statistics.median(pitches),'median_interval_st':statistics.median(abs(x) for x in ints),'stepwise_motion_share':sum(abs(x)<=2 for x in ints)/len(ints),'pitch_repetition_share':sum(abs(x)<.5 for x in ints)/len(ints)}
