#!/usr/bin/env python3
"""Syllable–Melody Resolver v0.1.

Uses externally aligned syllable intervals as independent temporal evidence to
refine structural melody. Text never determines pitch. The resolver classifies
1 syllable↔1 note, melisma, reattack, and likely sensor fragmentation. It merges
only same/near-same pitch fragments inside one syllable when no independent
syllable boundary separates them; otherwise it preserves events.
"""


def overlap(a0,a1,b0,b1):
    return max(0.0,min(a1,b1)-max(a0,b0))


def resolve_syllable_melody(events, syllables, same_pitch_tol=0, max_fragment_gap=.08):
    ev=sorted([dict(e) for e in events],key=lambda x:(float(x['start_s']),float(x['end_s'])))
    syl=sorted([dict(s) for s in syllables],key=lambda x:(float(x['start_s']),float(x['end_s'])))
    assignments=[]; refined=[]; used=set()
    for si,s in enumerate(syl):
        a,b=float(s['start_s']),float(s['end_s'])
        ids=[i for i,e in enumerate(ev) if overlap(a,b,float(e['start_s']),float(e['end_s']))>0]
        group=[ev[i] for i in ids]
        if not group:
            assignments.append({'syllable_index':si,'state':'NO_MELODY_EVENT','event_indices':[]});continue
        pitches=[int(e['midi']) for e in group]
        # same syllable, near-identical pitch, tiny internal gaps => sensor fragmentation candidate
        fragment=(len(group)>1 and max(pitches)-min(pitches)<=same_pitch_tol and
                  all(float(group[j]['start_s'])-float(group[j-1]['end_s'])<=max_fragment_gap for j in range(1,len(group))))
        if fragment:
            q=dict(group[0]);q['start_s']=min(float(e['start_s']) for e in group);q['end_s']=max(float(e['end_s']) for e in group)
            q['syllable_refined']=True;q['merged_event_indices']=ids;refined.append(q);used.update(ids)
            state='SENSOR_FRAGMENTATION_MERGED'
        else:
            state='SYLLABIC' if len(group)==1 else ('MELISMATIC' if len(set(pitches))>1 else 'REATTACK_CANDIDATE')
            for i in ids:
                if i not in used:refined.append(dict(ev[i]));used.add(i)
        assignments.append({'syllable_index':si,'state':state,'event_indices':ids,'pitch_count':len(set(pitches))})
    for i,e in enumerate(ev):
        if i not in used:refined.append(dict(e))
    refined.sort(key=lambda x:(float(x['start_s']),float(x['end_s'])))
    return {'version':'Syllable–Melody Resolver v0.1','events':refined,'assignments':assignments,
            'input_event_count':len(ev),'output_event_count':len(refined),
            'rule':'Syllable timing may refine boundaries/continuity but never supplies or changes pitch.'}
