#!/usr/bin/env python3
"""MIE melody-only structural probe v0.1.

Runs the trained melody sensor and MIE Structural Reduction without H/T synthesis.
This is an engineering probe, not a promoted musical baseline.
"""
import argparse, json
from pathlib import Path
from structural_reduction import reduce_candidates


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


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--vocal', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--duration', type=float, default=None)
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)

    raw,midi_path=basic_pitch_candidates(Path(args.vocal),out)
    reduction=reduce_candidates(raw)
    duration=args.duration
    if duration is None:
        duration=max((n['end_s'] for n in raw),default=0.0)

    render=reduction['render_events']
    hypotheses=reduction['events']
    removed=max(0,len(raw)-len(hypotheses))
    report={
        'version':'MIE melody structural probe v0.1',
        'status':'ENGINEERING_PROBE_NOT_BASELINE',
        'sensor':'Basic Pitch',
        'reducer':reduction['version'],
        'historical_p30_equivalence_claimed':False,
        'duration_s':duration,
        'raw_sensor_count':len(raw),
        'hypothesis_count':len(hypotheses),
        'render_count':len(render),
        'ambiguous_count':reduction['ambiguous_count'],
        'raw_density_events_per_s':density(raw,duration),
        'render_density_events_per_s':density(render,duration),
        'render_to_raw_ratio':len(render)/len(raw) if raw else 0.0,
        'hypothesis_to_raw_ratio':len(hypotheses)/len(raw) if raw else 0.0,
        'sensor_midi':str(midi_path),
        'reduction':reduction,
        'promotion_gate':'Do not audition. Compare structural density, ambiguity, timing preservation and generic-song stability first.',
    }
    path=out/'MIE_STRUCTURAL_PROBE_v0_1.json'
    path.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in [
        'raw_sensor_count','hypothesis_count','render_count','ambiguous_count',
        'raw_density_events_per_s','render_density_events_per_s','render_to_raw_ratio'
    ]},indent=2))


if __name__=='__main__':
    main()
