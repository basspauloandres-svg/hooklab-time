#!/usr/bin/env python3
"""Evaluate M structural candidates without conflating musical leaps with errors.

Input: one or more MIE_STRUCTURAL_PROBE_v0_3/v0_4 JSON reports.
Output: compact gate report. This gate does not judge perceptual quality and does
not promote a baseline by itself.
"""
import argparse, json
from pathlib import Path


def summarize(path):
    d=json.loads(Path(path).read_text(encoding='utf-8'))
    pr=d.get('plane_resolution',{})
    events=pr.get('events',[])
    decisions=pr.get('decisions',[])
    ambiguous=[x for x in decisions if x.get('state')=='AMBIGUOUS']
    large=[]
    for i in range(1,len(events)):
        a,b=events[i-1],events[i]
        jump=abs(int(b['midi'])-int(a['midi']))
        if jump>=10:
            large.append({
                'from_id':a.get('id'),'to_id':b.get('id'),'jump_semitones':jump,
                'gap_s':float(b['start_s'])-float(a['end_s']),
                'from_margin':a.get('plane_acoustic_margin_norm'),
                'to_margin':b.get('plane_acoustic_margin_norm'),
            })
    # Large leaps are REVIEW, not automatic failures, when both events are LOCK.
    return {
        'file':str(path),
        'probe_version':d.get('version'),
        'plane_resolver':d.get('plane_resolver'),
        'raw_sensor_count':d.get('raw_sensor_count'),
        'render_count':d.get('render_count'),
        'render_to_raw_ratio':d.get('render_to_raw_ratio'),
        'ambiguous_count':len(ambiguous),
        'ambiguous_ratio_vs_plane_input':len(ambiguous)/max(1,int(pr.get('input_count',0))),
        'large_locked_leaps':large,
        'large_locked_leap_count':len(large),
        'max_locked_leap_semitones':max([x['jump_semitones'] for x in large],default=0),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('reports',nargs='+')
    args=ap.parse_args()
    rows=[summarize(p) for p in args.reports]
    # Structural readiness is intentionally conservative. A large LOCKed leap is
    # flagged for evidence review rather than suppressed. Ambiguity is allowed.
    out={
        'gate':'M STRUCTURAL PRE-AUDITION GATE',
        'status':'REVIEW_REQUIRED' if any(r['large_locked_leap_count'] for r in rows) else 'STRUCTURALLY_CLEAN',
        'baseline_promoted':False,
        'rules':[
            'AMBIGUOUS regions must not be rendered.',
            'Large melodic leaps are not errors by definition.',
            'Any LOCKed leap >=10 semitones requires acoustic/context evidence review.',
            'No parameter may be changed from one song alone.',
            'Auditory promotion still requires the golden perceptual gate.'
        ],
        'cases':rows,
    }
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
