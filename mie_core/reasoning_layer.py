#!/usr/bin/env python3
"""MIE Reasoning Layer v0.1.

Turns relational M-H-T evidence into explicitly scoped analytical claims.
Claims are either DESCRIPTIVE (directly computed) or CANDIDATE_PATTERN.
No tonal-function labels are assigned at this stage.
"""
import statistics


def build_claims(relational):
    ev=relational.get('events',[])
    claims=[]
    def add(kind,statement,indices,metrics,confidence='DESCRIPTIVE'):
        claims.append({'claim_id':f'CLM-{len(claims)+1:03d}','type':kind,
                       'statement':statement,'evidence_event_indices':indices,
                       'metrics':metrics,'confidence_class':confidence})
    ivs=[e.get('interval_from_previous') for e in ev if e.get('interval_from_previous') is not None]
    step=[i for i,e in enumerate(ev) if e.get('interval_from_previous') is not None and abs(e['interval_from_previous'])<=2]
    leaps=[i for i,e in enumerate(ev) if e.get('interval_from_previous') is not None and abs(e['interval_from_previous'])>=5]
    add('MELODIC_MOTION',
        'Predominio de movimiento por unísono, semitono o tono frente a saltos de cinco o más semitonos.',
        step,{'stepwise_count':len(step),'large_leap_count':len(leaps),
              'stepwise_share':len(step)/len(ivs) if ivs else None})
    if ev:
        midis=[int(e['midi']) for e in ev]
        add('REGISTER','Tesitura observada de los eventos melódicos LOCK.',list(range(len(ev))),
            {'lowest_midi':min(midis),'highest_midi':max(midis),
             'range_semitones':max(midis)-min(midis),'median_midi':statistics.median(midis)})
    near=[i for i,e in enumerate(ev) if e.get('tactus',{}).get('proximity_class')=='NEAR_TACTUS']
    add('TACTUS_RELATION','Distribución de ataques respecto al tactus más próximo.',list(range(len(ev))),
        {'near_tactus_count':len(near),'total_events':len(ev),
         'near_share':len(near)/len(ev) if ev else None})
    locked=[(i,e) for i,e in enumerate(ev) if e.get('harmony',{}).get('state')=='LOCK']
    ambiguous=[i for i,e in enumerate(ev) if e.get('harmony',{}).get('state')=='AMBIGUOUS']
    add('HARMONIC_CERTAINTY','Las inferencias nota-acorde se restringen a contextos armónicos LOCK.',
        list(range(len(ev))),{'lock_context_events':len(locked),'ambiguous_context_events':len(ambiguous)})
    chord=[i for i,e in locked if e['harmony'].get('pitch_relation')=='CHORD_TONE']
    non=[i for i,e in locked if e['harmony'].get('pitch_relation')=='NON_CHORD_PC']
    add('M_H_RELATION','En contextos H LOCK coexisten alturas del acorde y alturas externas al conjunto observado.',
        [i for i,_ in locked],{'chord_tone_count':len(chord),'non_chord_pc_count':len(non)})
    contextual=[]
    for i in non:
        if i==0 or i==len(ev)-1: continue
        inc=int(ev[i]['midi'])-int(ev[i-1]['midi'])
        out=int(ev[i+1]['midi'])-int(ev[i]['midi'])
        contextual.append({'event_index':i,'interval_in':inc,'interval_out':out,
                           'stepwise_in':abs(inc)<=2,'stepwise_out':abs(out)<=2,
                           'harmony_label':ev[i]['harmony'].get('label')})
    both=[x for x in contextual if x['stepwise_in'] and x['stepwise_out']]
    add('NON_CHORD_CONTEXT',
        'Parte de las alturas externas al acorde LOCK aparece entre movimientos conjuntos; se registra como patrón candidato sin asignar función tonal.',
        [x['event_index'] for x in both],
        {'non_chord_context_events':len(contextual),'stepwise_on_both_sides':len(both)},
        'CANDIDATE_PATTERN')
    return {'version':'MIE Reasoning Layer v0.1','claims':claims,
            'non_chord_context_evidence':contextual,
            'epistemic_policy':{'DESCRIPTIVE':'directly computed from observed/LOCK evidence',
                                'CANDIDATE_PATTERN':'relational pattern detected; musical function not assigned',
                                'PROHIBITED_WITH_CURRENT_EVIDENCE':['tonal center','scale degree','passing tone',
                                    'appoggiatura','suspension','cadence','metrical accent hierarchy',
                                    'expressive intention']}}
