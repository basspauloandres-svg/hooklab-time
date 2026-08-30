#!/usr/bin/env python3
"""Fast Analyzer v1 replay from already validated derived evidence.

Purpose: validate feature assembly, fingerprint construction and strict readiness
without re-running audio acquisition, Basic Pitch, Beat This or ASR.

This module never upgrades the evidentiary status of the source run. It reuses only
persisted derived evidence and fails closed when the evidence snapshot lacks fields
required by the current Analyzer contract.
"""
import argparse,json,subprocess,sys,tempfile
from pathlib import Path

CORE_PATHS={
    'M.event_count':('M','event_count'),
    'M.median_midi':('M','median_midi'),
    'M.range_semitones':('M','range_semitones'),
    'T.tempo_bpm':('T','tempo_bpm'),
    'T.tactus_count':('T','tactus_count'),
    'T.mean_near_tactus_share':('T','mean_near_tactus_share'),
    'TEXT.line_count':('TEXT','line_count'),
    'TMT.mean_M_events_per_token':('TMT','mean_M_events_per_token'),
}

def load(p): return json.loads(Path(p).read_text())
def run(cmd): subprocess.run(cmd,check=True)
def get(d,path):
    for k in path:
        if not isinstance(d,dict) or k not in d:return None
        d=d[k]
    return d

def find(root,*candidates):
    for rel in candidates:
        p=root/rel
        if p.exists():return p
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--evidence',required=True,help='Extracted E2E artifact root')
    ap.add_argument('--output',required=True)
    a=ap.parse_args(); root=Path(a.evidence); out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    ac=find(root,'acoustic/sensor_regression.json','real_e2e/acoustic/sensor_regression.json')
    tx=find(root,'text_performed.json','real_e2e/text_performed.json')
    if not ac or not tx: raise SystemExit('Replay evidence missing acoustic sensor_regression.json or text_performed.json')
    acoustic=load(ac);text=load(tx)
    evidence_gates={
        'coverage_full':acoustic.get('coverage')=='FULL',
        'audio_not_persisted':acoustic.get('audio_persistence')=='NONE',
        'M_events_available':bool(acoustic.get('M_events')),
        'T_tactus_available':bool(acoustic.get('T_tactus_times')),
        'T_valid':acoustic.get('T_status') in {'VALID','VALID_BEAT_THIS','BEAT_THIS_VALID'},
        'text_aligned':text.get('alignment_status')=='ALIGNED' and float(text.get('alignment_coverage',0))>=0.95,
    }
    if not all(evidence_gates.values()):
        missing=[k for k,v in evidence_gates.items() if not v]
        report={'schema':'ANALYZER_V1_REPLAY_RESULT','status':'EVIDENCE_SNAPSHOT_INSUFFICIENT','gates':evidence_gates,'missing':missing,
                'rule':'Replay never fabricates evidence absent from the source artifact.'}
        (out/'replay_result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));raise SystemExit(2)
    feat=out/'tmt_features.json'
    run([sys.executable,str(Path(__file__).with_name('assemble_tmt_features.py')),'--acoustic',str(ac),'--text',str(tx),'--output',str(feat)])
    fp=out/'structural_fingerprint.json'
    run([sys.executable,str(Path(__file__).with_name('build_structural_fingerprint.py')),str(feat),str(fp)])
    fpd=load(fp);missing_core=[name for name,path in CORE_PATHS.items() if get(fpd,path) is None]
    applicability=load(feat).get('applicability',{})
    recurrence_ok=(fpd.get('TEXT',{}).get('repetition_group_count',0)>0 or applicability.get('recurrence')=='NOT_APPLICABLE_NO_REPETITION')
    gates=dict(evidence_gates)
    gates.update({'core_fingerprint_complete':not missing_core,'recurrence_resolved':recurrence_ok,
                  'data_first_guard':fpd.get('epistemic_guard',{}).get('policy')=='DATA_FIRST'})
    status='STRICT_REPLAY_PASS' if all(gates.values()) else 'STRICT_REPLAY_FAIL'
    report={'schema':'ANALYZER_V1_REPLAY_RESULT','status':status,'gates':gates,'missing_core':missing_core,
            'applicability':applicability,'outputs':{'features':str(feat),'fingerprint':str(fp)},
            'rule':'Derived-evidence replay validates current analytic logic without re-running acoustic or ASR sensors.'}
    (out/'replay_result.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report))
    if status!='STRICT_REPLAY_PASS':raise SystemExit(3)
if __name__=='__main__':main()
