#!/usr/bin/env python3
"""Correct MB06 so CLOCK_STOP_RESTART is observable from timing.
Audit finding: v0.1 restarted at 15.25 s after last pre-gap beat 11.65 s with IBI=.6;
3.6 s = exactly 6 cycles, so the alleged 'new phase' was phase-compatible with
continuation. MB06-v0.1 therefore could not test phase restart vs attack dropout.
This patch changes only MB06 post-fermata phase to 15.40 s (0.25 cycle offset).
"""
import json, wave
from pathlib import Path
import numpy as np
SR=44100
OUT=Path(__file__).parent/'generated'
def click(y,t,amp=.7,f=900,d=.035):
 i=int(t*SR); n=min(int(d*SR),len(y)-i)
 if n<=0:return
 x=np.arange(n)/SR; y[i:i+n]+=amp*np.sin(2*np.pi*f*x)*np.exp(-x*45)
def tonebed(d):
 t=np.arange(int(d*SR))/SR; return .05*(np.sin(2*np.pi*220*t)+.5*np.sin(2*np.pi*330*t))
def write(path,y):
 pcm=(np.clip(y,-1,1)*32767).astype('<i2')
 with wave.open(str(path),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
dur=36; ibi=.6
pre=np.arange(.25,12-.05,ibi).tolist(); post=np.arange(15.40,dur-.05,ibi).tolist(); beats=pre+post
y=tonebed(dur)
for t in beats:click(y,t)
write(OUT/'MB06.wav',y); np.savetxt(OUT/'MB06.beats',beats,fmt='%.6f')
mask={'fermata_interval_s':[12,15],'reacquisition_anchor_s':15,'phase_restart_first_beat_s':15.40,'benchmark_revision':'MB06-v0.2'}
(OUT/'MB06.mask.json').write_text(json.dumps(mask,indent=2))
mp=OUT/'manifest.json'
if mp.exists():
 m=json.loads(mp.read_text())
 m['schema']='HookLab-TIME-microbenchmark-v0.2'
 for c in m['cases']:
  if c['id']=='MB06':
   c.update({'reference_beats_s':len(beats),'condition':'fermata_clock_stop_phase_restart','phase_restart_first_beat_s':15.40,'benchmark_revision':'MB06-v0.2','mask':mask})
 mp.write_text(json.dumps(m,indent=2))
print(json.dumps({'MB06':'v0.2','first_post_beat_s':15.40,'phase_offset_cycles':.25,'beats':len(beats)},indent=2))
