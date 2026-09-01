#!/usr/bin/env python3
import argparse, json
from pathlib import Path

from basic_pitch.inference import predict
from sensor_fusion import fuse_basic_pitch_with_pyin
from structural_reduction import reduce_candidates
from ornament_reduction import suppress_microornaments
from plane_resolver import resolve_planes


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--vocal',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    vocal=Path(args.vocal)
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)

    _,midi_data,note_events=predict(str(vocal))
    midi_data.write(str(out/'melody_basic_pitch_sensor.mid'))
    primary=[]
    for i,ev in enumerate(note_events):
        primary.append({
            'id':f'bp_{i:05d}','start_s':float(ev[0]),'end_s':float(ev[1]),
            'midi':int(ev[2]),'confidence':float(ev[3]),'sensor':'basic_pitch'})
    primary.sort(key=lambda e:(e['start_s'],e['end_s'],e['midi']))

    fusion=fuse_basic_pitch_with_pyin(primary,vocal)
    reduction=reduce_candidates(fusion['events'])
    ornament=suppress_microornaments(reduction['render_events'])
    plane=resolve_planes(ornament['render_events'],vocal)

    final=plane['events']
    jumps=[abs(int(b['midi'])-int(a['midi'])) for a,b in zip(final,final[1:])]
    pre={e['id']:e for e in ornament['render_events']}
    introduced=0; worsened=0
    for a,b in zip(final,final[1:]):
        if a['id'] not in pre or b['id'] not in pre:
            continue
        before=abs(int(pre[b['id']]['midi'])-int(pre[a['id']]['midi']))
        after=abs(int(b['midi'])-int(a['midi']))
        if after>=10 and before<10:
            introduced+=1
        if after-before>=12:
            worsened+=1

    metrics={
        'raw_primary_count':len(primary),
        'secondary_added_count':fusion['secondary_added_count'],
        'combined_count':fusion['combined_count'],
        'structural_render_count':reduction['render_count'],
        'ornament_suppressed_count':ornament['suppressed_count'],
        'final_render_count':len(final),
        'plane_ambiguous_count':plane['ambiguous_count'],
        'max_jump_semitones':max(jumps) if jumps else 0,
        'jumps_ge_10':sum(1 for x in jumps if x>=10),
        'resolver_introduced_large_jumps':introduced,
        'resolver_worsened_by_octave_or_more':worsened,
    }
    report={
        'version':'MIE Fused Melody Probe v0.1',
        'status':'EXPERIMENTAL_NOT_PROMOTED',
        'primary_sensor':'Basic Pitch',
        'secondary_sensor':'pYIN continuous evidence only',
        'fusion':fusion,
        'reduction':reduction,
        'microornament_reduction':ornament,
        'plane_resolution':plane,
        'metrics':metrics,
        'final_render_events':final,
    }
    (out/'MIE_FUSED_PROBE_v0_1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(metrics,indent=2))

if __name__=='__main__':
    main()
