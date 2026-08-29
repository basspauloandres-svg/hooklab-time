#!/usr/bin/env python3
"""Conservative melody-sensor fusion for MIE.

Basic Pitch remains the primary event sensor. pYIN is secondary continuous
pitch/voicing evidence and may add candidates only where the primary sensor does
not already provide adequate same-pitch coverage. Added candidates must also
pass a recording-relative vocal-energy floor derived from Basic Pitch events.

A secondary-only candidate is held when it forms an isolated large excursion
between two nearby, mutually coherent primary events. This is a conservative
uncertainty rule: secondary evidence may fill gaps, but cannot override a stable
primary local contour without independent resolution downstream.

This is experimental fusion, not historical P30 code and not a final melody
representation. Fused candidates still pass through Structural Reduction,
Ornament Reduction and Plane Resolver before rendering.
"""
from pathlib import Path
import numpy as np
import librosa

DEFAULTS={
    'pyin_sr':22050,
    'pyin_hop_length':256,   # 11.609977 ms at 22050 Hz
    'pyin_frame_length':2048,
    'voiced_prob_min':0.35,
    'stable_frames_min':3,
    'same_pitch_coverage_max':0.30,
    'any_overlap_max':0.50,
    'overlap_exception_frames_min':4,
    'overlap_exception_voiced_prob_min':0.50,
    'primary_energy_percentile':5.0,
    'secondary_confidence_scale':0.85,
    # Reuses the project's generic continuity concepts rather than singer range.
    'local_primary_neighbor_max_gap_s':0.50,
    'primary_neighbor_coherence_max_semitones':7,
    'secondary_large_excursion_min_semitones':10,
}


def _overlap(a,b,c,d):
    return max(0.0,min(b,d)-max(a,c))


def _segment_rms(y,sr,a,b):
    A=max(0,int(float(a)*sr)); B=min(len(y),int(float(b)*sr))
    if B<=A:
        return 0.0
    return float(np.sqrt(np.mean(np.asarray(y[A:B],dtype=np.float64)**2)))


def _nearest_primary_neighbors(primary,a,b,max_gap):
    before=[e for e in primary if float(e['end_s'])<=a and a-float(e['end_s'])<=max_gap]
    after=[e for e in primary if float(e['start_s'])>=b and float(e['start_s'])-b<=max_gap]
    prev=max(before,key=lambda e:float(e['end_s'])) if before else None
    nxt=min(after,key=lambda e:float(e['start_s'])) if after else None
    return prev,nxt


def fuse_basic_pitch_with_pyin(primary_events,vocal_path,config=None):
    cfg=dict(DEFAULTS)
    if config:
        cfg.update(config)
    primary=[dict(e) for e in primary_events]
    primary.sort(key=lambda e:(float(e['start_s']),float(e['end_s']),int(e['midi'])))

    y,sr=librosa.load(Path(vocal_path),sr=int(cfg['pyin_sr']),mono=True)
    primary_rms=[_segment_rms(y,sr,e['start_s'],e['end_s']) for e in primary]
    primary_rms=[x for x in primary_rms if np.isfinite(x) and x>0]
    energy_floor=(float(np.percentile(primary_rms,float(cfg['primary_energy_percentile'])))
                  if primary_rms else 0.0)

    f0,voiced_flag,voiced_prob=librosa.pyin(
        y,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7'),
        sr=sr,
        frame_length=int(cfg['pyin_frame_length']),
        hop_length=int(cfg['pyin_hop_length']))
    times=librosa.times_like(f0,sr=sr,hop_length=int(cfg['pyin_hop_length']))
    midi=librosa.hz_to_midi(f0)
    valid=np.isfinite(midi) & np.isfinite(voiced_prob) & (voiced_prob>=float(cfg['voiced_prob_min']))
    quant=np.where(valid,np.rint(midi),np.nan)

    runs=[]; i=0
    while i<len(quant):
        if not np.isfinite(quant[i]):
            i+=1; continue
        pitch=int(quant[i]); j=i+1
        while j<len(quant) and np.isfinite(quant[j]) and int(quant[j])==pitch:
            j+=1
        if j-i>=int(cfg['stable_frames_min']):
            half=float(cfg['pyin_hop_length'])/(2.0*sr)
            a=max(0.0,float(times[i]-half))
            b=min(len(y)/sr,float(times[j-1]+half))
            runs.append((a,b,pitch,float(np.nanmedian(voiced_prob[i:j])),j-i))
        i=j

    additions=[]; decisions=[]
    for k,(a,b,pitch,vprob,frames) in enumerate(runs):
        dur=b-a
        if dur<=0:
            continue
        rms=_segment_rms(y,sr,a,b)
        if rms<energy_floor:
            decisions.append({'run_index':k,'action':'HOLD','reason':'SECONDARY_BELOW_PRIMARY_RELATIVE_ENERGY_FLOOR',
                              'midi':pitch,'start_s':a,'end_s':b,'run_rms':rms,'energy_floor':energy_floor})
            continue
        overlaps=[e for e in primary if _overlap(a,b,float(e['start_s']),float(e['end_s']))>0]
        same=sum(_overlap(a,b,float(e['start_s']),float(e['end_s'])) for e in overlaps
                 if abs(int(e['midi'])-pitch)<=1)
        same_ratio=same/dur
        if same_ratio>=float(cfg['same_pitch_coverage_max']):
            decisions.append({'run_index':k,'action':'HOLD','reason':'PRIMARY_ALREADY_COVERS_SECONDARY_PITCH',
                              'midi':pitch,'same_pitch_coverage':same_ratio})
            continue
        any_overlap=sum(_overlap(a,b,float(e['start_s']),float(e['end_s'])) for e in overlaps)/dur
        overlap_exception=(frames>=int(cfg['overlap_exception_frames_min']) and
                           vprob>=float(cfg['overlap_exception_voiced_prob_min']))
        if any_overlap>float(cfg['any_overlap_max']) and not overlap_exception:
            decisions.append({'run_index':k,'action':'HOLD','reason':'PRIMARY_OVERLAP_WITHOUT_STRONG_SECONDARY_EXCEPTION',
                              'midi':pitch,'any_primary_overlap':any_overlap})
            continue

        prev,nxt=_nearest_primary_neighbors(primary,a,b,float(cfg['local_primary_neighbor_max_gap_s']))
        if prev is not None and nxt is not None:
            prev_m=int(prev['midi']); next_m=int(nxt['midi'])
            coherent=abs(prev_m-next_m)<=int(cfg['primary_neighbor_coherence_max_semitones'])
            large_prev=abs(pitch-prev_m)>=int(cfg['secondary_large_excursion_min_semitones'])
            large_next=abs(pitch-next_m)>=int(cfg['secondary_large_excursion_min_semitones'])
            if coherent and large_prev and large_next:
                decisions.append({
                    'run_index':k,'action':'HOLD','reason':'SECONDARY_ISOLATED_LARGE_EXCURSION_BETWEEN_COHERENT_PRIMARY_NEIGHBORS',
                    'midi':pitch,'start_s':a,'end_s':b,'previous_primary_midi':prev_m,
                    'next_primary_midi':next_m,'previous_gap_s':a-float(prev['end_s']),
                    'next_gap_s':float(nxt['start_s'])-b,'voiced_prob':vprob,'frames':frames})
                continue

        event={
            'id':f'py_{k:05d}','start_s':a,'end_s':b,'midi':pitch,
            'confidence':min(0.95,vprob*float(cfg['secondary_confidence_scale'])),
            'sensor':'pyin_secondary','voiced_prob':vprob,'frames':frames,
            'run_rms':rms,'relative_energy_floor':energy_floor,
        }
        additions.append(event)
        decisions.append({'run_index':k,'action':'ADD','reason':'SECONDARY_PERSISTENT_UNDERCOVERED_REGION',
                          'candidate_id':event['id'],'midi':pitch,'start_s':a,'end_s':b,
                          'voiced_prob':vprob,'frames':frames,'run_rms':rms,
                          'energy_floor':energy_floor,'same_pitch_coverage':same_ratio,
                          'any_primary_overlap':any_overlap})

    combined=primary+additions
    combined.sort(key=lambda e:(float(e['start_s']),float(e['end_s']),-float(e.get('confidence',0.0))))
    return {
        'version':'MIE Sensor Fusion BP+pYIN v0.2',
        'historical_code_exact':False,
        'config_status':'EXPERIMENTAL_GENERIC_RECONSTRUCTION_REQUIRES_BLIND_VALIDATION',
        'config':cfg,
        'primary_count':len(primary),
        'secondary_stable_run_count':len(runs),
        'secondary_added_count':len(additions),
        'primary_energy_floor':energy_floor,
        'combined_count':len(combined),
        'events':combined,
        'secondary_events':additions,
        'decisions':decisions,
    }
