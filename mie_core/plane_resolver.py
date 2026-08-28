#!/usr/bin/env python3
"""MIE Competitive Plane Resolver reconstruction v0.4.

Generic reconstruction of the documented plane-resolver architecture:
Viterbi over octave alternatives using acoustic harmonic salience, continuity,
octave-shift persistence and short-gap plane memory.

This is NOT recovered historical code. The historical checkpoint documents the
architecture and a 13/14 regression baseline, but not an exact executable.
No fixed singer-specific MIDI range is used here.

v0.4 fixes a confidence defect in isolated phrase segments: per-event salience
normalization makes the strongest octave candidate equal to 1.0 by definition,
so a singleton could be falsely LOCKed even when the second alternative is
nearly equivalent. Singleton LOCK now requires an explicit acoustic margin.
"""
from pathlib import Path
import math
import numpy as np
import librosa

OCTAVE_SHIFTS=(-24,-12,0,12,24)
HISTORICAL_SHORT_GAP_MEMORY_S=0.13931972789115645

DEFAULTS={
    'midi_min':24,
    'midi_max':96,
    'continuity_weight':0.20,
    'octave_shift_change_penalty':0.85,
    'short_gap_shift_change_penalty':1.25,
    'acoustic_weight':2.2,
    'phrase_gap_min_s':0.50,
    'phrase_gap_duration_multiplier':4.0,
    'lock_salience_min':0.55,
    # Experimental generic confidence margin. Not recovered from Luis Miguel/P30.
    'singleton_acoustic_margin_min':0.12,
}


def _event_duration(e):
    return max(0.0,float(e['end_s'])-float(e['start_s']))


def _candidate_midis(midi,cfg):
    out=[]
    for sh in OCTAVE_SHIFTS:
        m=int(midi)+sh
        if cfg['midi_min'] <= m <= cfg['midi_max']:
            out.append((m,sh))
    return out


def _harmonic_salience(y,sr,start_s,end_s,midi):
    a=max(0,int(start_s*sr)); b=min(len(y),int(end_s*sr))
    if b-a < 128:
        return 0.0
    x=np.asarray(y[a:b],dtype=np.float64)
    x=x-np.mean(x)
    if not np.any(x):
        return 0.0
    w=np.hanning(len(x)); x=x*w
    t=np.arange(len(x),dtype=np.float64)/sr
    f=float(librosa.midi_to_hz(midi))
    total=0.0
    for h,weight in ((1,1.0),(2,0.55),(3,0.32),(4,0.20)):
        fh=f*h
        if fh>=sr/2:
            break
        ang=2*np.pi*fh*t
        re=float(np.dot(x,np.cos(ang)))
        im=float(np.dot(x,np.sin(ang)))
        total += weight*math.hypot(re,im)
    return total/max(np.sum(w),1e-12)


def _segments(events,cfg):
    if not events:
        return []
    durs=[_event_duration(e) for e in events if _event_duration(e)>0]
    med=float(np.median(durs)) if durs else 0.2
    phrase_gap=max(cfg['phrase_gap_min_s'],cfg['phrase_gap_duration_multiplier']*med)
    segs=[]; cur=[events[0]]
    for e in events[1:]:
        gap=float(e['start_s'])-float(cur[-1]['end_s'])
        if gap>phrase_gap:
            segs.append(cur); cur=[e]
        else:
            cur.append(e)
    if cur:
        segs.append(cur)
    return segs


def _selected_local_margin(state, selected_index):
    """Normalized acoustic separation of selected candidate from best rival.

    Positive values mean the selected candidate is acoustically stronger.
    A negative value means Viterbi selected it despite a stronger local acoustic
    alternative, which is acceptable in multi-event context but insufficient for
    an isolated singleton LOCK.
    """
    if not state:
        return 0.0
    selected=float(state[selected_index][2])
    rivals=[float(q[2]) for j,q in enumerate(state) if j!=selected_index]
    return selected-(max(rivals) if rivals else 0.0)


def _lock_state(ac, local_margin, segment_length, cfg):
    if ac < cfg['lock_salience_min']:
        return 'AMBIGUOUS'
    if segment_length == 1 and local_margin < cfg['singleton_acoustic_margin_min']:
        return 'AMBIGUOUS'
    return 'LOCK'


def resolve_planes(events,vocal_path,config=None):
    cfg=dict(DEFAULTS)
    if config:
        cfg.update(config)
    src=[dict(e) for e in events]
    if not src:
        return {'version':'MIE Competitive Plane Resolver reconstruction v0.4','events':[],
                'decisions':[],'input_count':0,'output_count':0,'historical_code_exact':False}
    y,sr=librosa.load(Path(vocal_path),sr=22050,mono=True)
    salience_cache={}
    def sal(e,m):
        key=(e['id'],m)
        if key not in salience_cache:
            salience_cache[key]=_harmonic_salience(y,sr,e['start_s'],e['end_s'],m)
        return salience_cache[key]

    resolved=[]; decisions=[]
    for seg_i,seg in enumerate(_segments(src,cfg)):
        states=[]
        for e in seg:
            cand=_candidate_midis(e['midi'],cfg)
            vals=[sal(e,m) for m,_ in cand]
            vmax=max(vals) if vals else 1.0
            states.append([(m,sh,(v/max(vmax,1e-12)),v) for (m,sh),v in zip(cand,vals)])
        if not states or any(not s for s in states):
            continue
        prev=[]; back=[]
        for m,sh,ac,raw_ac in states[0]:
            score=cfg['acoustic_weight']*math.log(0.03+ac)
            prev.append(score)
        back.append([-1]*len(states[0]))
        for i in range(1,len(seg)):
            cur_scores=[]; cur_back=[]
            gap=float(seg[i]['start_s'])-float(seg[i-1]['end_s'])
            for j,(m,sh,ac,raw_ac) in enumerate(states[i]):
                best=-1e99; arg=-1
                acoustic=cfg['acoustic_weight']*math.log(0.03+ac)
                for k,(pm,psh,pac,praw) in enumerate(states[i-1]):
                    trans=-cfg['continuity_weight']*min(abs(m-pm),12)
                    if sh!=psh:
                        trans-=cfg['octave_shift_change_penalty']
                        if gap<=HISTORICAL_SHORT_GAP_MEMORY_S:
                            trans-=cfg['short_gap_shift_change_penalty']
                    score=prev[k]+trans+acoustic
                    if score>best:
                        best=score; arg=k
                cur_scores.append(best); cur_back.append(arg)
            prev=cur_scores; back.append(cur_back)
        j=int(np.argmax(prev)); path=[j]
        for i in range(len(seg)-1,0,-1):
            j=back[i][j]; path.append(j)
        path=path[::-1]
        for i,(e,idx) in enumerate(zip(seg,path)):
            m,sh,ac,raw_ac=states[i][idx]
            margin=_selected_local_margin(states[i],idx)
            ne=dict(e); ne['midi_input']=int(e['midi']); ne['midi']=int(m)
            ne['plane_shift_semitones']=int(sh); ne['plane_acoustic_salience_norm']=float(ac)
            ne['plane_acoustic_margin_norm']=float(margin)
            ne['state']=_lock_state(ac,margin,len(seg),cfg)
            if ne['state']=='LOCK':
                resolved.append(ne)
            decisions.append({
                'candidate_id':e['id'],
                'action':'PLANE_LOCK' if ne['state']=='LOCK' else 'PLANE_HOLD',
                'state':ne['state'],
                'reason':'VITERBI_HARMONIC_SALIENCE_CONTINUITY',
                'evidence':{
                    'segment_index':seg_i,
                    'segment_length':len(seg),
                    'input_midi':int(e['midi']),
                    'output_midi':int(m),
                    'octave_shift_semitones':int(sh),
                    'normalized_harmonic_salience':float(ac),
                    'normalized_acoustic_margin':float(margin),
                    'candidate_count':len(states[i]),
                    'singleton_margin_threshold_experimental':cfg['singleton_acoustic_margin_min'],
                }
            })
    resolved.sort(key=lambda e:(e['start_s'],e['end_s']))
    return {
        'version':'MIE Competitive Plane Resolver reconstruction v0.4',
        'historical_code_exact':False,
        'historical_architecture_recovered':True,
        'fixed_reference_singer_range_used':False,
        'config_status':'EXPERIMENTAL_GENERIC_RECONSTRUCTION',
        'config':cfg,
        'input_count':len(src),
        'output_count':len(resolved),
        'ambiguous_count':sum(1 for d in decisions if d['state']=='AMBIGUOUS'),
        'events':resolved,
        'decisions':decisions,
    }
