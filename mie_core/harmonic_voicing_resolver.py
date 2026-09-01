#!/usr/bin/env python3
"""Generic Harmonic Register/Voicing Resolver v0.1.

Harmonic LOCK operates primarily in pitch-class space. This resolver maps only
LOCK pitch classes to octave/register candidates using octave-resolved acoustic
salience plus bass evidence and continuity. It never treats pitch class as a
voicing instruction and may return AMBIGUOUS.
"""


def resolve_voicing(lock_unit, octave_candidates, previous_notes=None, min_margin=0.08):
    """Rank supplied octave-resolved candidates; do not invent pitches.

    octave_candidates: iterable of dicts with midi, salience, bass_support.
    Only MIDI notes whose pc belongs to lock_unit selected_pcs (or bass_pc for
    explicit bass candidates) are eligible.
    """
    pcs=set(int(x)%12 for x in lock_unit.get('selected_pcs',[]))
    bass_pc=lock_unit.get('bass_pc')
    prev=list(previous_notes or [])
    rows=[]
    for c in octave_candidates:
        m=int(c['midi']); pc=m%12
        role='BASS' if bass_pc is not None and pc==int(bass_pc)%12 and c.get('bass_candidate') else 'HARMONY'
        if role=='HARMONY' and pc not in pcs: continue
        sal=float(c.get('salience',0)); bs=float(c.get('bass_support',0))
        continuity=0.0 if not prev else min(abs(m-p) for p in prev)
        score=.62*sal+.23*bs-.15*min(continuity/12.0,1.5)
        rows.append({'midi':m,'pc':pc,'role':role,'salience':sal,'bass_support':bs,
                     'continuity_distance':continuity,'score':score})
    rows.sort(key=lambda r:r['score'],reverse=True)
    # select at most one bass realization and one realization per selected pc
    chosen=[]; used=set(); bass_used=False
    for r in rows:
        if r['role']=='BASS':
            if bass_used: continue
            bass_used=True; chosen.append(r); continue
        if r['pc'] in used: continue
        used.add(r['pc']); chosen.append(r)
    top=rows[0]['score'] if rows else 0; second=rows[1]['score'] if len(rows)>1 else 0
    margin=top-second
    covered=pcs.issubset({r['pc'] for r in chosen if r['role']=='HARMONY'})
    state='LOCK' if rows and covered and margin>=min_margin else 'AMBIGUOUS'
    return {'version':'Harmonic Voicing Resolver v0.1','state':state,'margin':margin,
            'notes':[r['midi'] for r in chosen] if state=='LOCK' else [],'ranked':rows,
            'rule':'Pitch-class LOCK does not imply octave/voicing LOCK. Register is emitted only with octave-resolved evidence.'}
