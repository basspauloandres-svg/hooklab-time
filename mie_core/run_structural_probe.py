#!/usr/bin/env python3
"""MIE melody-only structural probe v0.3.

Pipeline: Basic Pitch sensor -> structural reduction -> micro-ornament reduction
-> competitive plane resolver. No H/T synthesis. Engineering probe only; no
historical P30 equivalence is claimed.
"""
import argparse, json
from pathlib import Path
from structural_reduction import reduce_candidates
from ornament_reduction import suppress_microornaments
from plane_resolver import resolve_planes


def basic_pitch_candidates(vocal_path, outdir):
    from basic_pitch.inference import predict
    _, midi_data, note_events = predict(str(vocal_path))
    midi_path=outdir/'melody_basic_pitch_sensor.mid'
    midi_data.write(str(midi_path))
    raw=[]
    for i,ev in enumerate(note_events):
        raw.append({
            'id':f'bp_{i:05d}',
            'start_s':float(ev[0]),
            'end_s':float(ev[1]),
            'midi':int(ev[2]),
            'confidence':float(ev[3]),
            'sensor':'basic_pitch',
        })
    raw.sort(key=lambda n:(n['start_s'],n['end_s'],-n['confidence'],n['midi']))
    return raw, midi_path


def density(events, duration):
    return len(events)/duration if duration>0 else 0.0


def jump_metrics(events):
    if len(events)<2:
        return {'max_jump_semitones':0,'jumps_ge_10':0}
    jumps=[abs(int(events[i]['midi'])-int(events[i-1]['midi'])) for i in range(1,len(events))]
    return {'max_jump_semitones':max(jumps),'jumps_ge_10':sum(1 for j in jumps if j>=10)}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--vocal', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--duration', type=float, default=None)
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)

    raw,midi_path=basic_pitch_candidates(Path(args.vocal),out)
    reduction=reduce_candidates(raw)
    ornament=suppress_microornaments(reduction['render_events'])
    plane=resolve_planes(ornament['render_events'],Path(args.vocal))
    duration=args.duration
    if duration is None:
        duration=max((n['end_s'] for n in raw),default=0.0)

    render=plane['events']
    hypotheses=reduction['events']
    jm=jump_metrics(render)
    report={
        'version':'MIE melody structural probe v0.3',
        'status':'ENGINEERING_PROBE_NOT_BASELINE',
        'sensor':'Basic Pitch',
        'reducer':reduction['version'],
        'ornament_stage':ornament['version'],
        'plane_resolver':plane['version'],
        'historical_p30_equivalence_claimed':False,
        'duration_s':duration,
        'raw_sensor_count':len(raw),
        'hypothesis_count':len(hypotheses),
        'pre_ornament_render_count':reduction['render_count'],
        'microornament_suppressed_count':ornament['suppressed_count'],
        'pre_plane_count':len(ornament['render_events']),
        'plane_ambiguous_count':plane['ambiguous_count'],
        'render_count':len(render),
        'structural_ambiguous_count':reduction['ambiguous_count'],
        'raw_density_events_per_s':density(raw,duration),
        'render_density_events_per_s':density(render,duration),
        'render_to_raw_ratio':len(render)/len(raw) if raw else 0.0,
        'hypothesis_to_raw_ratio':len(hypotheses)/len(raw) if raw else 0.0,
        'max_jump_semitones':jm['max_jump_semitones'],
        'jumps_ge_10':jm['jumps_ge_10'],
        'sensor_midi':str(midi_path),
        'reduction':reduction,
        'microornament_reduction':ornament,
        'plane_resolution':plane,
        'final_render_events':render,
        'promotion_gate':'Do not audition. Compare density, ambiguity, jump stability, physical timing and generic-song stability first.',
    }
    path=out/'MIE_STRUCTURAL_PROBE_v0_3.json'
    path.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in [
        'raw_sensor_count','hypothesis_count','pre_ornament_render_count',
        'microornament_suppressed_count','pre_plane_count','plane_ambiguous_count',
        'render_count','structural_ambiguous_count','raw_density_events_per_s',
        'render_density_events_per_s','render_to_raw_ratio','max_jump_semitones','jumps_ge_10'
    ]},indent=2))


if __name__=='__main__':
    main()
