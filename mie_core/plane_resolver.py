#!/usr/bin/env python3
"""MIE Competitive Plane Resolver reconstruction v0.7.

Generic reconstruction of the documented plane-resolver architecture:
Viterbi over octave alternatives using acoustic harmonic salience, continuity,
octave-shift persistence and plane memory.

This is NOT recovered historical code. The checkpoint documents the architecture
and a 13/14 historical regression baseline, but not an exact executable.
No fixed singer-specific MIDI range is used here.

v0.5 added cross-segment plane memory. v0.6 adds an evidence veto: Viterbi
continuity may propose an octave correction, but a nonzero shift cannot be LOCKed
when another local octave candidate has greater acoustic salience. In that case,
the resolver falls back to the sensor plane (shift=0) only when that plane is
locally dominant and sufficiently salient; otherwise the event is AMBIGUOUS.
This prevents continuity from overriding contradictory acoustic evidence.
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
    'singleton_acoustic_margin_min':0.12,
    # Generic conservative priors; experimental, not recovered P30 constants.
    'zero_shift_prior_weight':0.42,
    'cross_segment_memory_weight':1.10,
    'cross_segment_memory_decay_s':2.0,
    'nonzero_singleton_margin_min':0.18,
    'octave_excursion_alt_salience_min':0.60,
    'octave_excursion_continuity_gain_min':12.0,
    'octave_excursion_neighbor_max':7.0,
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
    if not state:
        return 0.0
    selected=float(state[selected_index][2])
    rivals=[float(q[2]) for j,q in enumerate(state) if j!=selected_index]
    return selected-(max(rivals) if rivals else 0.0)


def _memory_strength(gap_s,cfg):
    tau=max(float(cfg['cross_segment_memory_decay_s']),1e-6)
    return float(cfg['cross_segment_memory_weight'])*math.exp(-max(0.0,float(gap_s))/tau)


def _segment_start_prior(shift, previous_shift, gap_s, cfg):
    # Sensor plane is the default hypothesis; octave movement requires evidence.
    score=-float(cfg['zero_shift_prior_weight'])*(abs(int(shift))/12.0)
    memory=0.0
    if previous_shift is not None:
        strength=_memory_strength(gap_s,cfg)
        memory=-strength*(abs(int(shift)-int(previous_shift))/12.0)
        score+=memory
    return score,memory


def _lock_state(ac,local_margin,segment_length,shift,cfg):
    if ac < cfg['lock_salience_min']:
        return 'AMBIGUOUS'
    if segment_length == 1:
        needed=float(cfg['singleton_acoustic_margin_min'])
        if int(shift)!=0:
            needed=max(needed,float(cfg['nonzero_singleton_margin_min']))
        if local_margin < needed:
            return 'AMBIGUOUS'
    return 'LOCK'


def _octave_excursion_override(states, path, i, cfg):
    """Return an alternate state index for an isolated octave excursion, else None.

    The rule is relative and generic: an octave-related alternative must retain
    substantial local acoustic salience, reduce continuity cost by at least one
    octave in aggregate, and land near both selected neighbors. It never uses
    reference-song notes or a fixed singer range.
    """
    if i <= 0 or i >= len(path)-1:
        return None
    cur_idx=path[i]
    cur_m,cur_sh,cur_ac,_=states[i][cur_idx]
    prev_m=states[i-1][path[i-1]][0]
    next_m=states[i+1][path[i+1]][0]
    cur_cost=abs(cur_m-prev_m)+abs(next_m-cur_m)
    best=None
    for j,(m,sh,ac,raw) in enumerate(states[i]):
        if j==cur_idx or abs(int(m)-int(cur_m))!=12:
            continue
        if float(ac) < float(cfg['octave_excursion_alt_salience_min']):
            continue
        alt_cost=abs(m-prev_m)+abs(next_m-m)
        gain=cur_cost-alt_cost
        if gain < float(cfg['octave_excursion_continuity_gain_min']):
            continue
        if max(abs(m-prev_m),abs(next_m-m)) > float(cfg['octave_excursion_neighbor_max']):
            continue
        key=(gain,float(ac),-alt_cost)
        if best is None or key>best[0]:
            best=(key,j)
    return None if best is None else best[1]


def resolve_planes(events,vocal_path,config=None):
    cfg=dict(DEFAULTS)
    if config:
        cfg.update(config)
    src=[dict(e) for e in events]
    if not src:
        return {'version':'MIE Competitive Plane Resolver reconstruction v0.7','events':[],
                'decisions':[],'input_count':0,'output_count':0,'historical_code_exact':False}
    y,sr=librosa.load(Path(vocal_path),sr=22050,mono=True)
    salience_cache={}
    def sal(e,m):
        key=(e['id'],m)
        if key not in salience_cache:
            salience_cache[key]=_harmonic_salience(y,sr,e['start_s'],e['end_s'],m)
        return salience_cache[key]

    resolved=[]; decisions=[]
    previous_locked_shift=None
    previous_segment_end=None

    for seg_i,seg in enumerate(_segments(src,cfg)):
        states=[]
        for e in seg:
            cand=_candidate_midis(e['midi'],cfg)
            vals=[sal(e,m) for m,_ in cand]
            vmax=max(vals) if vals else 1.0
            states.append([(m,sh,(v/max(vmax,1e-12)),v) for (m,sh),v in zip(cand,vals)])
        if not states or any(not s for s in states):
            continue

        segment_gap=(float(seg[0]['start_s'])-float(previous_segment_end)
                     if previous_segment_end is not None else None)
        prev=[]; back=[]; start_priors=[]
        for m,sh,ac,raw_ac in states[0]:
            prior,memory=_segment_start_prior(
                sh,previous_locked_shift,segment_gap if segment_gap is not None else 1e9,cfg)
            acoustic=cfg['acoustic_weight']*math.log(0.03+ac)
            prev.append(acoustic+prior)
            start_priors.append((prior,memory))
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

        # Generic v0.7 octave-excursion correction. This operates only on the
        # competitive state set already observed acoustically; it cannot invent
        # a pitch outside the sensor's octave-related hypotheses. Iterate once
        # from left to right so corrections remain local and auditable.
        excursion_overrides={}
        for ii in range(1,len(path)-1):
            alt_idx=_octave_excursion_override(states,path,ii,cfg)
            if alt_idx is not None:
                excursion_overrides[ii]=(path[ii],alt_idx)
                path[ii]=alt_idx

        segment_locked=[]
        for i,(e,idx) in enumerate(zip(seg,path)):
            m,sh,ac,raw_ac=states[i][idx]
            margin=_selected_local_margin(states[i],idx)
            evidence_veto=False
            fallback_to_sensor=False
            excursion_override=i in excursion_overrides
            # A nonzero octave correction requires local acoustic support.
            # If Viterbi selected a shifted plane that is locally weaker than a
            # rival, continuity alone cannot authorize the correction. Prefer
            # the sensor plane only when shift=0 is itself the local acoustic
            # winner and satisfies the normal salience lock threshold.
            if int(sh)!=0 and margin < 0.0:
                evidence_veto=True
                zero_idx=next((jj for jj,q in enumerate(states[i]) if int(q[1])==0),None)
                if zero_idx is not None:
                    zm,zsh,zac,zraw=states[i][zero_idx]
                    zmargin=_selected_local_margin(states[i],zero_idx)
                    if zmargin >= 0.0 and zac >= cfg['lock_salience_min']:
                        m,sh,ac,raw_ac,margin=zm,zsh,zac,zraw,zmargin
                        fallback_to_sensor=True
            ne=dict(e); ne['midi_input']=int(e['midi']); ne['midi']=int(m)
            ne['plane_shift_semitones']=int(sh); ne['plane_acoustic_salience_norm']=float(ac)
            ne['plane_acoustic_margin_norm']=float(margin)
            ne['plane_evidence_veto']=bool(evidence_veto)
            ne['plane_fallback_to_sensor']=bool(fallback_to_sensor)
            ne['plane_octave_excursion_override']=bool(excursion_override)
            ne['state']=_lock_state(ac,margin,len(seg),sh,cfg)
            if evidence_veto and not fallback_to_sensor:
                ne['state']='AMBIGUOUS'
            if ne['state']=='LOCK':
                resolved.append(ne); segment_locked.append(ne)
            start_prior,start_memory=start_priors[idx] if i==0 else (0.0,0.0)
            decisions.append({
                'candidate_id':e['id'],
                'action':'PLANE_LOCK' if ne['state']=='LOCK' else 'PLANE_HOLD',
                'state':ne['state'],
                'reason':'VITERBI_HARMONIC_SALIENCE_CONTINUITY_WITH_SEGMENT_MEMORY',
                'evidence':{
                    'segment_index':seg_i,
                    'segment_length':len(seg),
                    'segment_gap_s':segment_gap if i==0 else None,
                    'previous_locked_shift_semitones':previous_locked_shift if i==0 else None,
                    'input_midi':int(e['midi']),
                    'output_midi':int(m),
                    'octave_shift_semitones':int(sh),
                    'normalized_harmonic_salience':float(ac),
                    'normalized_acoustic_margin':float(margin),
                    'candidate_count':len(states[i]),
                    'segment_start_prior_score':float(start_prior),
                    'cross_segment_memory_score':float(start_memory),
                    'evidence_veto_nonzero_shift':bool(evidence_veto),
                    'fallback_to_sensor_plane':bool(fallback_to_sensor),
                    'octave_excursion_override':bool(excursion_override),
                }
            })

        # Carry only a resolved plane forward. Ambiguity cannot create memory.
        if segment_locked:
            previous_locked_shift=int(segment_locked[-1]['plane_shift_semitones'])
        previous_segment_end=float(seg[-1]['end_s'])

    resolved.sort(key=lambda e:(e['start_s'],e['end_s']))
    return {
        'version':'MIE Competitive Plane Resolver reconstruction v0.7',
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
