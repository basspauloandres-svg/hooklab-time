#!/usr/bin/env python3
"""Generate three deterministic TMT prototype variants from cohort constraints.

This is an engineering prototype generator. It never searches the corpus and it never
copies source melodies. Every numeric generation parameter is derived from the cached
cohort constraint object or from explicit neutral engineering defaults recorded in the
manifest. Output audio is a simple synthesized melody plus click, intended for rapid
preproduction listening and TTFP measurement rather than finished production.
"""
import argparse, json, math, time, wave, struct, random
from pathlib import Path

SR=44100

def target(c,key,default):
    v=c.get(key,{})
    x=v.get('target') if isinstance(v,dict) else None
    return float(default if x is None else x)

def midi_hz(m): return 440.0*(2.0**((m-69.0)/12.0))

def tone(freq,dur,amp=.24):
    n=max(1,int(dur*SR)); out=[]
    a=min(int(.01*SR),n//4); r=min(int(.04*SR),n//3)
    for i in range(n):
        env=1.0
        if a and i<a: env=i/a
        if r and i>n-r: env=max(0.0,(n-i)/r)
        t=i/SR
        s=(math.sin(2*math.pi*freq*t)+0.25*math.sin(4*math.pi*freq*t))*amp*env
        out.append(s)
    return out

def click(dur=.035,amp=.18):
    n=max(1,int(dur*SR)); return [amp*(1-i/n)*math.sin(2*math.pi*1800*(i/SR)) for i in range(n)]

def mix(buf,start_s,data):
    p=int(start_s*SR)
    need=p+len(data)
    if need>len(buf): buf.extend([0.0]*(need-len(buf)))
    for i,x in enumerate(data): buf[p+i]+=x

def write_wav(path,buf):
    mx=max(1.0,max(abs(x) for x in buf) if buf else 1.0)
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        frames=b''.join(struct.pack('<h',int(max(-1,min(1,x/mx))*32767)) for x in buf)
        w.writeframes(frames)

def make_variant(name,c,seed,outdir):
    rng=random.Random(seed)
    bpm=max(55,min(190,target(c,'tempo_bpm',105)))
    beat=60.0/bpm
    reg=round(target(c,'melodic_register_midi',64))
    span=max(3,min(18,round(target(c,'melodic_range_semitones',8))))
    near=max(.15,min(.95,target(c,'near_tactus_share',.55)))
    ept=max(.4,min(3.0,target(c,'melodic_events_per_token',1.0)))
    # 8 bars, 4/4. Event density is shaped jointly by near-tactus share and events/token.
    bars=8; total=bars*4*beat
    buf=[0.0]*int((total+beat)*SR)
    for b in range(bars*4): mix(buf,b*beat,click())
    if name=='thetic': offset=0.0
    elif name=='anacrustic': offset=-0.5*beat
    else: offset=0.5*beat
    # More events/token yields shorter spacing, constrained to musically inspectable values.
    base_step=beat/max(.5,min(2.0,ept))
    steps=[]; t=max(0.0,offset)
    scale=[0,2,4,5,7,9,11]
    prev=reg
    while t<total-0.1:
        if name=='syncopated':
            dur=0.75*beat if rng.random()<near else 0.5*beat
            onset=t+(0.5*beat if rng.random()>.45 else 0.0)
        else:
            dur=beat if rng.random()<near else 0.5*beat
            onset=t
        lo=reg-span//2; hi=reg+span//2
        candidates=[]
        for octv in (-12,0,12):
            for s in scale:
                m=60+s+octv
                if lo<=m<=hi: candidates.append(m)
        if not candidates: candidates=list(range(lo,hi+1))
        # continuity-biased random walk; still generative, not source-copying.
        ranked=sorted(candidates,key=lambda m:abs(m-prev))[:max(3,min(7,len(candidates)))]
        m=rng.choice(ranked); prev=m
        mix(buf,onset,tone(midi_hz(m),max(.08,dur*.86)))
        steps.append({'onset_s':round(onset,4),'duration_s':round(dur,4),'midi':int(m)})
        t+=base_step
    wav=outdir/f'{name}.wav'; write_wav(wav,buf)
    return {'variant':name,'audio':wav.name,'tempo_bpm':bpm,'events':steps,
            'derived':{'register_target_midi':reg,'range_target_semitones':span,'near_tactus_target':near,'events_per_token_target':ept}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--constraints',required=True); ap.add_argument('--output-dir',required=True); ap.add_argument('--seed',type=int,default=1701); a=ap.parse_args()
    t0=time.perf_counter(); obj=json.loads(Path(a.constraints).read_text()); c=obj.get('constraints',{})
    required=['tempo_bpm','melodic_register_midi','melodic_range_semitones','melodic_events_per_token','near_tactus_share']
    missing=[k for k in required if k not in c]
    if missing: raise SystemExit('missing cohort-derived constraints: '+','.join(missing))
    outdir=Path(a.output_dir); outdir.mkdir(parents=True,exist_ok=True)
    variants=[make_variant(n,c,a.seed+i,outdir) for i,n in enumerate(('thetic','anacrustic','syncopated'))]
    elapsed=time.perf_counter()-t0
    manifest={'schema':'HOOKLAB_TMT_GENERATION_MANIFEST_v1.0','cohort_key':obj.get('cohort_key'),'semantics':'DATA_CONDITIONED_ENGINEERING_PROTOTYPE',
              'constraints_trace':obj.get('traceability',{}),'variants':variants,
              'latency':{'T_generation_and_render_seconds':elapsed,'T_online_search_seconds':0,'online_corpus_reanalysis':False},
              'copying_policy':'NO_SOURCE_MELODY_INPUT; generation uses cohort-level descriptive bounds only'}
    (outdir/'generation_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
    print(json.dumps({'status':'THREE_AUDIBLE_VARIANTS_READY','output_dir':str(outdir),'elapsed_s':elapsed}))
if __name__=='__main__': main()
