#!/usr/bin/env python3
from __future__ import annotations
import json, math, wave
from pathlib import Path
import numpy as np

SR=44100
OUT=Path(__file__).parent/'generated'
OUT.mkdir(parents=True,exist_ok=True)

def write_wav(path,y):
    y=np.clip(y,-1,1); pcm=(y*32767).astype('<i2')
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def click(y,t,amp=.8,f=1200,d=.035):
    i=int(t*SR); n=int(d*SR)
    if i<0 or i>=len(y): return
    k=min(n,len(y)-i); x=np.arange(k)/SR
    env=np.exp(-x*45); y[i:i+k]+=amp*np.sin(2*np.pi*f*x)*env

def tonebed(dur):
    t=np.arange(int(dur*SR))/SR
    return .05*(np.sin(2*np.pi*220*t)+.5*np.sin(2*np.pi*330*t))

def constant_beats(bpm,dur,start=.25):
    p=60/bpm; return np.arange(start,dur-.05,p).tolist()

def linear_tempo_beats(b0,b1,dur,start=.25):
    beats=[]; t=start; phase=0.0; dt=1/SR; target=1.0
    while t<dur:
        bpm=b0+(b1-b0)*(t/dur); phase+=bpm/60*dt; t+=dt
        if phase>=target: beats.append(t); target+=1
    return beats

def render(beats,dur,subdiv=None,silent=None,drop_attacks=None,secondary_every=None):
    y=tonebed(dur)
    for j,t in enumerate(beats):
        amp=.9 if secondary_every and j%secondary_every==0 else .7
        click(y,t,amp=amp,f=900)
    if subdiv:
        for t in subdiv: click(y,t,amp=.26,f=1700,d=.02)
    if drop_attacks:
        a,b=drop_attacks
        y2=tonebed(dur)
        # regenerate only attacks outside dropout
        for j,t in enumerate(beats):
            if not (a<=t<b): click(y2,t,amp=.7,f=900)
        if subdiv:
            for t in subdiv:
                if not (a<=t<b): click(y2,t,amp=.26,f=1700,d=.02)
        y=y2
    if silent:
        a,b=silent; y[int(a*SR):int(b*SR)]=0
    return y

def save_case(cid,dur,beats,**meta):
    np.savetxt(OUT/f'{cid}.beats',np.array(beats),fmt='%.6f')
    return {'id':cid,'duration_s':dur,'reference_beats_s':len(beats),**meta}

manifest={'schema':'HookLab-TIME-microbenchmark-v0.1','sample_rate_hz':SR,'cases':[]}
# MB01
cid='MB01'; dur=32; beats=constant_beats(120,dur); write_wav(OUT/f'{cid}.wav',render(beats,dur)); manifest['cases'].append(save_case(cid,dur,beats,condition='constant_120'))
# MB02
cid='MB02'; dur=40; beats=linear_tempo_beats(80,140,dur); write_wav(OUT/f'{cid}.wav',render(beats,dur)); manifest['cases'].append(save_case(cid,dur,beats,condition='linear_accelerando',bpm_start=80,bpm_end=140))
# MB03
cid='MB03'; dur=40; beats=linear_tempo_beats(140,70,dur); write_wav(OUT/f'{cid}.wav',render(beats,dur)); manifest['cases'].append(save_case(cid,dur,beats,condition='linear_ritardando',bpm_start=140,bpm_end=70))
# MB04
cid='MB04'; dur=40; b1=[x for x in constant_beats(120,20,start=.25) if x<20]; start2=20.25; b2=np.arange(start2,dur-.05,60/80).tolist(); beats=b1+b2; write_wav(OUT/f'{cid}.wav',render(beats,dur)); manifest['cases'].append(save_case(cid,dur,beats,condition='abrupt_120_to_80',transition_s=20))
# MB05
cid='MB05'; dur=36; beats=constant_beats(120,dur); write_wav(OUT/f'{cid}.wav',render(beats,dur,silent=(12,18))); mask={'exclude_intervals_s':[[12,18]],'reacquisition_anchor_s':18}; (OUT/f'{cid}.mask.json').write_text(json.dumps(mask,indent=2)); manifest['cases'].append(save_case(cid,dur,beats,condition='silence_reentry',mask=mask))
# MB06
cid='MB06'; dur=36; pre=[x for x in constant_beats(100,12,start=.25) if x<12]; post=np.arange(15.25,dur-.05,60/100).tolist(); beats=pre+post; write_wav(OUT/f'{cid}.wav',render(beats,dur)); mask={'fermata_interval_s':[12,15],'reacquisition_anchor_s':15}; (OUT/f'{cid}.mask.json').write_text(json.dumps(mask,indent=2)); manifest['cases'].append(save_case(cid,dur,beats,condition='fermata_clock_stop',mask=mask))
# MB07
cid='MB07'; dur=36; beats=constant_beats(105,dur); write_wav(OUT/f'{cid}.wav',render(beats,dur,drop_attacks=(12,20))); mask={'attack_dropout_interval_s':[12,20]}; (OUT/f'{cid}.mask.json').write_text(json.dumps(mask,indent=2)); manifest['cases'].append(save_case(cid,dur,beats,condition='attack_dropout_continuous_tactus',mask=mask))
# MB08
cid='MB08'; dur=36; beats=constant_beats(90,dur); subdiv=constant_beats(180,dur,start=.25); write_wav(OUT/f'{cid}.wav',render(beats,dur,subdiv=subdiv,secondary_every=2)); manifest['cases'].append(save_case(cid,dur,beats,condition='half_double_ambiguity',reference_tactus_bpm=90,subdivision_bpm=180))
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'generated':len(manifest['cases']),'out':str(OUT)},indent=2))
