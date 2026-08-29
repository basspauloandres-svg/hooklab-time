#!/usr/bin/env python3
"""MIE Melodic Analyzer v0.1.

Purpose
-------
Transform a stabilized monophonic event representation into an auditable musical
analysis layer. Sensor events remain evidence; analytic claims are derived from
that evidence and retain event-index provenance.

v0.1 is deliberately descriptive/relational. It does not infer tonal center,
scale degree, harmonic function, cadence, expressive intention or validated
motivic identity.
"""
from __future__ import annotations

from collections import Counter
from statistics import mean, median

PITCH_NAMES=("C","C#","D","D#","E","F","F#","G","G#","A","A#","B")


def pitch_name(midi:int)->str:
    m=int(midi)
    return f"{PITCH_NAMES[m%12]}{m//12-1}"


def _phrase_groups(events, multiplier=4.0, floor_s=0.50):
    if not events:
        return [], floor_s
    durs=[max(0.0,float(e['end_s'])-float(e['start_s'])) for e in events]
    threshold=max(float(floor_s),float(multiplier)*median(durs))
    groups=[]; cur=[0]
    for i in range(1,len(events)):
        gap=float(events[i]['start_s'])-float(events[i-1]['end_s'])
        if gap>threshold:
            groups.append(cur); cur=[i]
        else:
            cur.append(i)
    if cur: groups.append(cur)
    return groups,threshold


def _nearest_tactus(t, beats):
    if not beats:
        return None
    j=min(range(len(beats)),key=lambda k:abs(float(beats[k])-float(t)))
    return j,float(t)-float(beats[j])


def analyze_melody(events, beats=None):
    """Analyze LOCKed monophonic events.

    Parameters
    ----------
    events : sequence of dict
        Requires start_s, end_s and midi. id/state/confidence/plane fields are
        passed through when present.
    beats : sequence of float, optional
        Tactus timestamps. v0.1 reports nearest-tactus relation only; it does not
        infer a metrical hierarchy.
    """
    ev=sorted([dict(e) for e in events if e.get('state','LOCK')=='LOCK'],
              key=lambda e:(float(e['start_s']),float(e['end_s'])))
    beats=[float(x) for x in (beats or [])]
    if not ev:
        return {'version':'MIE Melodic Analyzer v0.1','events':[],
                'status':'EMPTY','traceability':{}}

    midis=[int(e['midi']) for e in ev]
    starts=[float(e['start_s']) for e in ev]
    ends=[float(e['end_s']) for e in ev]
    durs=[b-a for a,b in zip(starts,ends)]
    intervals=[midis[i]-midis[i-1] for i in range(1,len(midis))]
    abs_intervals=[abs(x) for x in intervals]

    beat_period=(median([beats[i]-beats[i-1] for i in range(1,len(beats))])
                 if len(beats)>1 else None)
    phrases,phrase_gap=_phrase_groups(ev)

    fragmentation=[]
    for i in range(1,len(ev)):
        gap=starts[i]-ends[i-1]
        if midis[i]==midis[i-1] and gap<=0.08:
            fragmentation.append({
                'left_event':i-1,'right_event':i,'midi':midis[i],
                'pitch':pitch_name(midis[i]),'gap_s':gap,
                'interpretation':'SENSOR_BOUNDARY_CANDIDATE_NOT_MUSICAL_REATTACK'
            })

    rows=[]
    for i,e in enumerate(ev):
        row={
            'event_index':i,'candidate_id':e.get('id'),
            'start_s':starts[i],'end_s':ends[i],'duration_s':durs[i],
            'midi':midis[i],'pitch_name':pitch_name(midis[i]),
            'state':e.get('state'),
            'plane_shift_semitones':e.get('plane_shift_semitones'),
            'plane_acoustic_salience_norm':e.get('plane_acoustic_salience_norm'),
            'plane_acoustic_margin_norm':e.get('plane_acoustic_margin_norm'),
        }
        if i:
            row['interval_from_previous_semitones']=intervals[i-1]
        nt=_nearest_tactus(starts[i],beats)
        if nt:
            j,delta=nt
            row['nearest_tactus']={
                'beat_index':j,'delta_s':delta,
                'delta_fraction_of_tactus':(delta/beat_period if beat_period else None)
            }
        rows.append(row)

    phrase_rows=[]
    for pi,idxs in enumerate(phrases):
        ms=[midis[i] for i in idxs]
        ivs=[ms[j]-ms[j-1] for j in range(1,len(ms))]
        phrase_rows.append({
            'phrase_index':pi,'event_indices':idxs,
            'start_s':starts[idxs[0]],'end_s':ends[idxs[-1]],
            'event_count':len(idxs),
            'lowest_midi':min(ms),'highest_midi':max(ms),
            'range_semitones':max(ms)-min(ms),
            'median_midi':median(ms),
            'opening_midi':ms[0],'closing_midi':ms[-1],
            'net_contour_semitones':ms[-1]-ms[0],
            'ascending_intervals':sum(x>0 for x in ivs),
            'descending_intervals':sum(x<0 for x in ivs),
            'same_pitch_intervals':sum(x==0 for x in ivs),
        })

    motif_candidates=[]
    for n in (3,4,5):
        seq=[tuple(intervals[i:i+n]) for i in range(len(intervals)-n+1)]
        cnt=Counter(seq)
        for pat,c in cnt.items():
            if c>=2:
                motif_candidates.append({
                    'interval_length':n,'pattern':list(pat),'occurrences':c,
                    'positions':[i for i,x in enumerate(seq) if x==pat],
                    'state':'CANDIDATE_NOT_VALIDATED_MOTIF'
                })
    motif_candidates.sort(key=lambda x:(-x['occurrences'],-x['interval_length']))

    return {
        'version':'MIE Melodic Analyzer v0.1',
        'status':'DESCRIPTIVE_RELATIONAL_ANALYSIS',
        'global':{
            'event_count':len(ev),
            'lowest_midi':min(midis),'lowest_pitch':pitch_name(min(midis)),
            'highest_midi':max(midis),'highest_pitch':pitch_name(max(midis)),
            'range_semitones':max(midis)-min(midis),
            'median_midi':median(midis),'mean_midi':mean(midis),
            'median_duration_s':median(durs),'mean_duration_s':mean(durs),
            'event_density_per_s':len(ev)/(max(ends)-min(starts)),
            'ascending_intervals':sum(x>0 for x in intervals),
            'descending_intervals':sum(x<0 for x in intervals),
            'same_pitch_intervals':sum(x==0 for x in intervals),
            'stepwise_intervals_le_2_semitones':sum(x<=2 for x in abs_intervals),
            'leaps_ge_5_semitones':sum(x>=5 for x in abs_intervals),
            'largest_ascending_interval':max([x for x in intervals if x>0],default=0),
            'largest_descending_interval':min([x for x in intervals if x<0],default=0),
            'phrase_count':len(phrases),
            'phrase_gap_threshold_s':phrase_gap,
            'fragmentation_boundaries_same_pitch':len(fragmentation),
            'tactus_period_s':beat_period,
            'tempo_bpm_from_tactus':(60.0/beat_period if beat_period else None),
        },
        'interval_histogram':dict(Counter(intervals)),
        'absolute_interval_histogram':dict(Counter(abs_intervals)),
        'phrase_summaries':phrase_rows,
        'fragmentation_boundaries':fragmentation,
        'motif_candidates_interval_sequences':motif_candidates[:12],
        'events':rows,
        'traceability':{
            'claim_policy':'Every quantitative statement must resolve to event indices and/or tactus timestamps.',
            'sensor_event_is_not_automatically_musical_event':True,
            'not_inferred_in_v0_1':[
                'tonal center','scale degree','harmonic function','cadence',
                'validated motif identity','phrase function','expressive intention',
                'metrical hierarchy beyond nearest tactus'
            ]
        }
    }
