#!/usr/bin/env python3
"""Observed melody-representation calibration on Vocadito using two independent human note references.

Design:
- candidate = Basic Pitch note events estimated from Vocadito audio;
- reference A1 = human note annotator 1;
- reference A2 = human note annotator 2;
- frozen HookLab feature extractor and agreement thresholds are reused unchanged;
- a feature is dual-reference stable only if it passes the frozen gate against BOTH A1 and A2.

Vocadito calibration never changes M300 N and never creates a creative rule.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

from representation_calibration_feature_extractor import features
from paired_representation_agreement import analyze
from melody_representation_calibration_gate import evaluate


def note_events(note_data):
    if note_data is None:
        return []
    rows=[]
    for (start,end), hz in zip(note_data.intervals, note_data.pitches):
        rows.append({'start':float(start),'end':float(end),'freq_hz':float(hz)})
    return rows


def basic_pitch_events(audio_path):
    # Runtime-only decision: force the packaged ONNX serialization so Linux does
    # not silently select TFLite. Scientific features/thresholds remain unchanged.
    from basic_pitch.inference import predict
    from basic_pitch import build_icassp_2022_model_path, FilenameSuffix
    model_path = build_icassp_2022_model_path(FilenameSuffix.onnx)
    _, _, notes = predict(str(audio_path), model_or_model_path=model_path)
    out=[]
    for row in notes:
        # basic-pitch note event: start, end, midi_pitch, amplitude, pitch_bend(optional)
        if len(row) >= 3:
            out.append({'start':float(row[0]),'end':float(row[1]),'pitch_midi':float(row[2])})
    return out


def row(track_id, ref_events, cand_events, annotator):
    return {
      'pair_id':f'vocadito:{track_id}:{annotator}',
      'dataset':'vocadito',
      'track_id':track_id,
      'reference_annotator':annotator,
      'independent_reference':True,
      'identity':'PASS',
      'same_performance':True,
      'reference':features(ref_events),
      'candidate':features(cand_events),
      'candidate_system':'basic_pitch_onnx',
      'calibration_only':True,
      'm300_ingestion':False,
    }


def run(data_home):
    import mirdata
    ds=mirdata.initialize('vocadito', data_home=str(data_home))
    tracks=ds.load_tracks()
    rows_a1=[]; rows_a2=[]; failures=[]
    for tid, tr in sorted(tracks.items()):
        try:
            cand=basic_pitch_events(tr.audio_path)
            rows_a1.append(row(tid,note_events(tr.notes_a1),cand,'A1'))
            rows_a2.append(row(tid,note_events(tr.notes_a2),cand,'A2'))
        except Exception as e:
            failures.append({'track_id':tid,'error':type(e).__name__+': '+str(e)})
    ag1=analyze(rows_a1); ag2=analyze(rows_a2)
    g1=evaluate(ag1); g2=evaluate(ag2)
    stable_both=sorted(set(g1['stable_features']) & set(g2['stable_features']))
    status='REPRESENTATION_CALIBRATED_DUAL_REFERENCE' if stable_both and g1['status']=='REPRESENTATION_CALIBRATED' and g2['status']=='REPRESENTATION_CALIBRATED' else 'REPRESENTATION_CALIBRATION_PENDING'
    return {
      'schema':'HOOKLAB_VOCADITO_DUAL_REFERENCE_CALIBRATION_v0.2',
      'status':status,
      'dataset':'vocadito',
      'candidate_system':'basic_pitch_onnx',
      'runtime_decision':'FORCE_ONNX_SERIALIZATION_ONLY__SCIENTIFIC_THRESHOLDS_UNCHANGED',
      'observed_tracks_a1':len(rows_a1),
      'observed_tracks_a2':len(rows_a2),
      'failed_tracks':failures,
      'agreement_A1':ag1,
      'agreement_A2':ag2,
      'gate_A1':g1,
      'gate_A2':g2,
      'dual_reference_stable_features':stable_both,
      'scientific_semantics':'REPRESENTATION_VALIDATION_ONLY',
      'm300_ingestion':False,
      'creative_rule_promotion':False,
      'invariant':'A feature is promoted as representation-stable here only when frozen HookLab thresholds pass against both human note references.'
    }


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--data-home',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    out=run(Path(a.data_home)); Path(a.output).write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
    raise SystemExit(0 if out['status']=='REPRESENTATION_CALIBRATED_DUAL_REFERENCE' else 4)

if __name__=='__main__': main()
