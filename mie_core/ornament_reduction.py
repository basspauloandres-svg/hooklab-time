#!/usr/bin/env python3
"""Context-relative micro-ornament suppression for MIE Structural Reduction.

Experimental engineering module. It does not claim historical P30 equivalence.
A candidate is suppressed only when it is locally brief, forms a real small
pitch excursion, and the surrounding pitches return to the same local plane.
Physical timing of all surviving events is left untouched.
"""
from statistics import median

DEFAULTS={
    'duration_ratio_max':0.55,
    'return_tolerance_semitones':1,
    'excursion_min_semitones':1,
    'excursion_max_semitones':3,
    'local_radius':2,
}


def _dur(e):
    return max(0.0,float(e['end_s'])-float(e['start_s']))


def suppress_microornaments(events, config=None):
    cfg=dict(DEFAULTS)
    if config:
        cfg.update(config)
    src=[dict(e) for e in events]
    drop=set()
    decisions=[]
    radius=int(cfg['local_radius'])
    for i in range(1,len(src)-1):
        p,q,n=src[i-1],src[i],src[i+1]
        if q.get('state')=='AMBIGUOUS':
            continue
        lo=max(0,i-radius); hi=min(len(src),i+radius+1)
        local=[_dur(x) for j,x in enumerate(src[lo:hi],start=lo) if j!=i and _dur(x)>0]
        if not local:
            continue
        local_med=median(local)
        ratio=_dur(q)/local_med if local_med>0 else 1.0
        return_distance=abs(int(p['midi'])-int(n['midi']))
        excursion=max(abs(int(q['midi'])-int(p['midi'])),abs(int(q['midi'])-int(n['midi'])))
        if (ratio < cfg['duration_ratio_max'] and
            return_distance <= cfg['return_tolerance_semitones'] and
            cfg['excursion_min_semitones'] <= excursion <= cfg['excursion_max_semitones']):
            drop.add(q['id'])
            decisions.append({
                'candidate_id':q['id'],
                'action':'SUPPRESS_FROM_RENDER',
                'reason':'LOCAL_MICROORNAMENT_RETURN_CONTOUR',
                'state':'PROVISIONAL',
                'evidence':{
                    'duration_s':_dur(q),
                    'local_median_duration_s':local_med,
                    'duration_ratio':ratio,
                    'prev_midi':int(p['midi']),
                    'midi':int(q['midi']),
                    'next_midi':int(n['midi']),
                    'return_distance_semitones':return_distance,
                    'excursion_semitones':excursion,
                    'thresholds_experimental':dict(cfg),
                },
            })
    render=[e for e in src if e['id'] not in drop]
    return {
        'version':'MIE micro-ornament reduction v0.2',
        'historical_code_exact':False,
        'config_status':'EXPERIMENTAL_CONTEXT_RELATIVE_NOT_TUNED_TO_REFERENCE_SONG',
        'config':cfg,
        'input_count':len(src),
        'suppressed_count':len(drop),
        'render_count':len(render),
        'render_events':render,
        'decisions':decisions,
    }
