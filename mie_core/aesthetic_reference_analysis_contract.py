#!/usr/bin/env python3
"""HookLab AESTHETIC_REFERENCE analyzer bridge contract v0.1.
Validates and normalizes derived sensor output for Producer Interface consumption.
It never promotes aesthetic-reference data into M300/Gate A/scientific evidence.
"""
import argparse, json
from pathlib import Path

SCHEMA='HOOKLAB_AESTHETIC_REFERENCE_ANALYSIS_v0.1'

def normalize(sensor, session_id, expected_sha256=None):
    sha=sensor.get('ephemeral_sha256')
    reasons=[]
    if expected_sha256 and sha!=expected_sha256:
        reasons.append('SHA256_SESSION_MISMATCH')
    if sensor.get('audio_persistence')!='NONE':
        reasons.append('SOURCE_AUDIO_PERSISTENCE_NOT_NONE')
    if sensor.get('T_status')!='VALID':
        reasons.append('BEAT_SENSOR_NOT_VALID')
    if sensor.get('coverage')!='FULL':
        reasons.append('AUDIO_COVERAGE_NOT_FULL')
    result={
      'schema':SCHEMA,
      'status':'PASS' if not reasons else 'FAIL',
      'reasons':reasons,
      'session_id':session_id,
      'role':'AESTHETIC_REFERENCE_ANALYSIS',
      'semantics':'DESCRIPTIVE_SESSION_REFERENCE_ONLY',
      'scientific_ingestion':False,
      'gate_a_ingestion':False,
      'm300_ingestion':False,
      'success_evidence_ingestion':False,
      'source_audio_persistence':'NONE',
      'reference_sha256':sha,
      'duration_s':sensor.get('duration_s'),
      'tempo_bpm_median':sensor.get('T_tempo_bpm_median'),
      'beat_count':sensor.get('T_tactus_count'),
      'beat_times_s':sensor.get('T_tactus_times',[]),
      'beat_sensor':sensor.get('T_sensor'),
      'beat_status':sensor.get('T_status'),
      'melody_event_count':sensor.get('M_post_ornament_count'),
      'melody_range_raw':sensor.get('M_range_raw'),
      'sensor_version':sensor.get('version'),
      'beat_model_sha256':sensor.get('T_model_sha256'),
      'mel_model_sha256':sensor.get('T_mel_model_sha256'),
      'contract':'AESTHETIC_REFERENCE != M300_EVIDENCE != SUCCESS_EVIDENCE != GATE_A_ACQUISITION'
    }
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--sensor',required=True)
    ap.add_argument('--session-id',required=True)
    ap.add_argument('--expected-sha256')
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    sensor=json.loads(Path(a.sensor).read_text())
    out=normalize(sensor,a.session_id,a.expected_sha256)
    Path(a.output).write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
    raise SystemExit(0 if out['status']=='PASS' else 2)

if __name__=='__main__': main()
