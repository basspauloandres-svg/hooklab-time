#!/usr/bin/env python3
"""MIE Relational Analyzer v0.1.

Builds auditable M<->H<->T relations from already-observed musical evidence.
This module does not infer tonal function, cadence, scale degree, expressive
intention, or named non-chord-tone function. AMBIGUOUS harmony propagates.
"""
import statistics

PC_NAMES=('C','C#','D','D#','E','F','F#','G','G#','A','A#','B')


def analyze_relations(m_events, harmony_units, beats):
    events=sorted([dict(e) for e in m_events if e.get('state','LOCK')=='LOCK'],
                  key=lambda e:(float(e['start_s']),float(e['end_s'])))
    beats=[float(x) for x in beats]
    period=(statistics.median([beats[i]-beats[i-1] for i in range(1,len(beats))])
            if len(beats)>1 else None)
    rows=[]
    for i,e in enumerate(events):
        t=float(e['start_s']); midi=int(e['midi']); pc=midi%12
        if beats:
            bj=min(range(len(beats)),key=lambda j:abs(beats[j]-t))
            delta=t-beats[bj]
            tactus={'beat_index':bj,'beat_time_s':beats[bj],'delta_s':delta,
                    'delta_fraction':delta/period if period else None,
                    'proximity_class':('NEAR_TACTUS' if period and abs(delta)<=0.10*period
                                       else 'OFFSET_FROM_TACTUS')}
        else:
            tactus={'state':'UNRESOLVED'}
        active=[(j,h) for j,h in enumerate(harmony_units)
                if float(h['start_s'])<=t<float(h['end_s'])]
        if active:
            hj,h=active[0]
            hstate=h.get('state','AMBIGUOUS')
            chord_pcs={(int(h['root_pc'])+int(iv))%12 for iv in h.get('intervals',[])}
            if hstate=='LOCK':
                pitch_relation='CHORD_TONE' if pc in chord_pcs else 'NON_CHORD_PC'
                root_distance=(pc-int(h['root_pc']))%12
            else:
                pitch_relation='AMBIGUOUS_HARMONY'; root_distance=None
            harmony={'unit_index':hj,
                     'label':f"{PC_NAMES[int(h['root_pc'])]}:{h.get('quality','?')}",
                     'state':hstate,'evidence':h.get('evidence'),'margin':h.get('margin'),
                     'pitch_relation':pitch_relation,
                     'semitones_above_root_mod12':root_distance}
        else:
            harmony={'state':'UNRESOLVED','pitch_relation':'UNRESOLVED'}
        rows.append({'event_index':i,'candidate_id':e.get('id'),'start_s':t,
                     'end_s':float(e['end_s']),'midi':midi,'pitch_class':PC_NAMES[pc],
                     'interval_from_previous':None if i==0 else midi-int(events[i-1]['midi']),
                     'tactus':tactus,'harmony':harmony,
                     'trace':{'M_state':e.get('state'),
                              'M_salience':e.get('plane_acoustic_salience_norm')}})
    locked=[r for r in rows if r['harmony'].get('state')=='LOCK']
    return {'version':'MIE Relational Analyzer v0.1','status':'DESCRIPTIVE_RELATIONAL',
            'summary':{'M_events':len(rows),'H_LOCK_context_events':len(locked),
                       'H_AMBIGUOUS_context_events':sum(r['harmony'].get('state')=='AMBIGUOUS' for r in rows),
                       'chord_tone_events_in_LOCK_H':sum(r['harmony'].get('pitch_relation')=='CHORD_TONE' for r in locked),
                       'non_chord_pc_events_in_LOCK_H':sum(r['harmony'].get('pitch_relation')=='NON_CHORD_PC' for r in locked),
                       'events_near_tactus_10pct':sum(r['tactus'].get('proximity_class')=='NEAR_TACTUS' for r in rows),
                       'tactus_period_s':period,'tempo_bpm':60/period if period else None},
            'events':rows,
            'inference_policy':{'allowed':['temporal concurrence M-H','nearest tactus relation',
                                           'pitch-class membership in LOCK chord'],
                                'not_yet_allowed':['passing tone','appoggiatura','suspension',
                                                   'anticipation as musical function','scale degree',
                                                   'tonal function','cadence','metrical accent hierarchy']}}
