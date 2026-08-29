#!/usr/bin/env python3
"""Generic Metric Phase Resolver v0.1.

Beat This supplies tactus timestamps. This resolver estimates metric phase over
candidate group sizes without assuming that the first detected tactus is beat 1.
Evidence is generic: onset energy, low-frequency energy, harmonic-change evidence,
and optional phrase-onset proximity. If the best phase lacks margin, state remains
AMBIGUOUS. No song-specific offsets are allowed.
"""
import math


def resolve_metric_phase(beats, evidence_at_beat, group_sizes=(4,3), min_margin=0.08):
    """Return ranked (group_size, phase) hypotheses.

    evidence_at_beat[i] may contain onset, bass, harmonic_change, phrase_onset in
    [0,1]. Phase p means beat i is a downbeat candidate when i % group_size == p.
    """
    rows=[]
    for g in group_sizes:
        for p in range(g):
            down=[]; other=[]
            for i,_ in enumerate(beats):
                e=evidence_at_beat[i] if i < len(evidence_at_beat) else {}
                score=(0.34*float(e.get('onset',0))+0.26*float(e.get('bass',0))+
                       0.25*float(e.get('harmonic_change',0))+0.15*float(e.get('phrase_onset',0)))
                (down if i%g==p else other).append(score)
            d=sum(down)/max(1,len(down)); o=sum(other)/max(1,len(other))
            rows.append({'group_size':g,'phase':p,'score':d-o,
                         'downbeat_evidence_mean':d,'other_evidence_mean':o})
    rows.sort(key=lambda r:r['score'],reverse=True)
    margin=rows[0]['score']-rows[1]['score'] if len(rows)>1 else rows[0]['score']
    return {'version':'Metric Phase Resolver v0.1','state':'LOCK' if margin>=min_margin else 'AMBIGUOUS',
            'best':rows[0] if rows else None,'margin':margin,'ranked':rows,
            'rule':'Tactus is not downbeat. Metric phase requires independent evidence and may remain AMBIGUOUS.'}
