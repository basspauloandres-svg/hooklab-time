#!/usr/bin/env python3
"""Assemble Analyzer v1 empirical TMT features from derived M/T events and performed text.

No musical desirability is inferred. Features that are structurally inapplicable
(e.g. recurrence when the document has no repeated groups) are marked NOT_APPLICABLE
rather than treated as missing/failure.
"""
import argparse,json,math,statistics
from pathlib import Path

def nearest_share(events, beats, tol=0.18):
    if not events or not beats:return None
    n=0
    for e in events:
        t=float(e['start_s'])
        if min(abs(t-b) for b in beats)<=tol:n+=1
    return n/len(events)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--acoustic',required=True);ap.add_argument('--text',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    ac=json.loads(Path(a.acoustic).read_text()); tx=json.loads(Path(a.text).read_text())
    ev=ac.get('M_events',[]); beats=ac.get('T_tactus_times',[]); units=tx.get('units',[])
    midis=[int(x['midi']) for x in ev]
    line_counts=[]; ratios=[]
    for u in units:
        if 'start_s' not in u or 'end_s' not in u: continue
        es=[x for x in ev if float(x['start_s']) < float(u['end_s']) and float(x['end_s']) > float(u['start_s'])]
        tokens=max(int(u.get('token_count',0)),1)
        line_counts.append(len(es));ratios.append(len(es)/tokens)
    reps=tx.get('repetition_groups',[])
    applicability={'recurrence':'APPLICABLE' if reps else 'NOT_APPLICABLE_NO_REPETITION',
                   'salience':'PENDING_CORPUS_OPERATIONALIZATION','internal_recurrence':'APPLICABLE' if reps else 'NOT_APPLICABLE_NO_REPETITION'}
    feat={'schema':'TMT_FEATURE_VECTOR_v1.0','song_id':ac.get('song_id'),'coverage':ac.get('coverage'),
          'global':{'M_event_count':len(ev),'M_median_midi':statistics.median(midis) if midis else None,
                    'M_range_semitones':max(midis)-min(midis) if midis else None,
                    'T_tempo_bpm':ac.get('T_tempo_bpm_median'),'T_tactus_count':len(beats),
                    'mean_near_tactus_share_by_line':nearest_share(ev,beats),
                    'text_line_count':len(units),'text_repetition_group_count':len(reps),
                    'mean_M_events_per_text_token':statistics.mean(ratios) if ratios else None},
          'recurrence':{},'salience':{},'internal_recurrence':{},'applicability':applicability,
          'quality':{'M_events_available':bool(ev),'T_tactus_available':bool(beats),'aligned_text_units':sum('start_s' in u and 'end_s' in u for u in units),
                     'aligned_text_ratio':(sum('start_s' in u and 'end_s' in u for u in units)/len(units)) if units else 0.0}}
    Path(a.output).write_text(json.dumps(feat,indent=2,ensure_ascii=False));print(json.dumps(feat))
if __name__=='__main__':main()
