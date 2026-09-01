#!/usr/bin/env python3
"""Generate three traceable structural TMT candidates from cohort constraints.

Unlike the v1 audible generator, this module explicitly uses the Text dimension.
It emits phrase/token/event scaffolds for inspection without reproducing source lyrics
or source melodies. All numeric controls come from cohort-level descriptive constraints.
"""
import argparse,json,math,random,time
from pathlib import Path

def target(c,key,default):
    v=c.get(key,{})
    x=v.get('target') if isinstance(v,dict) else None
    return float(default if x is None else x)

def variant(name,c,seed):
    rng=random.Random(seed)
    bpm=max(55,min(190,target(c,'tempo_bpm',105))); beat=60/bpm
    reg=round(target(c,'melodic_register_midi',64)); span=max(3,min(24,round(target(c,'melodic_range_semitones',8))))
    ept=max(.4,min(3,target(c,'melodic_events_per_token',1.0))); near=max(.1,min(.99,target(c,'near_tactus_share',.55)))
    lines=max(2,min(16,round(target(c,'text_line_count',6))))
    token_target=max(3,round(8/ept)); scale=[0,2,4,5,7,9,11]
    offset={'thetic':0,'anacrustic':-.5*beat,'syncopated':.5*beat}[name]
    phrases=[]; global_t=max(0,offset); prev=reg
    for li in range(lines):
        tokens=max(3,token_target+rng.choice([-1,0,0,1])); events=max(tokens,round(tokens*ept)); ev=[]
        step=beat if near>=.55 else beat/2
        for j in range(events):
            onset=global_t+j*step
            if name=='syncopated' and j%2: onset+=beat/2
            lo,hi=reg-span//2,reg+span//2
            pcs=[60+s+12*o for o in (-2,-1,0,1,2) for s in scale if lo<=60+s+12*o<=hi]
            ranked=sorted(pcs or list(range(lo,hi+1)),key=lambda m:abs(m-prev))[:5]
            m=rng.choice(ranked); prev=m
            ev.append({'onset_s':round(onset,3),'midi':int(m),'token_slot':min(tokens-1,math.floor(j/max(.001,ept)))})
        dur=(events-1)*step+beat
        phrases.append({'line_index':li+1,'token_slots':[f'T{li+1}_{k+1}' for k in range(tokens)],'events':ev,'phrase_duration_s':round(dur,3)})
        global_t+=dur+beat
    return {'variant':name,'tempo_bpm':bpm,'text_line_count':lines,'register_target_midi':reg,'range_target_semitones':span,'events_per_token_target':ept,'near_tactus_target':near,'phrases':phrases}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--constraints',required=True);ap.add_argument('--output',required=True);ap.add_argument('--seed',type=int,default=1701);a=ap.parse_args()
    t0=time.perf_counter(); obj=json.loads(Path(a.constraints).read_text()); c=obj.get('constraints',{})
    required=['tempo_bpm','melodic_register_midi','melodic_range_semitones','melodic_events_per_token','near_tactus_share','text_line_count']
    missing=[k for k in required if k not in c]
    if missing: raise SystemExit('missing FULL_TMT cohort constraints: '+','.join(missing))
    vv=[variant(n,c,a.seed+i) for i,n in enumerate(('thetic','anacrustic','syncopated'))]
    out={'schema':'HOOKLAB_TMT_STRUCTURAL_GENERATION_v2.0','status':'THREE_FULL_TMT_STRUCTURAL_CANDIDATES_READY','cohort_key':obj.get('cohort_key'),'semantics':'COHORT_CONDITIONED_STRUCTURAL_SCAFFOLD_NO_SOURCE_COPY','variants':vv,'traceability':obj.get('traceability',{}),'latency':{'T_generation_seconds':time.perf_counter()-t0,'T_online_search_seconds':0,'online_corpus_reanalysis':False},'text_policy':'TOKEN_SLOTS_ONLY; no source lyrics copied'}
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':out['status'],'variants':3,'elapsed_s':out['latency']['T_generation_seconds']}))
if __name__=='__main__':main()
