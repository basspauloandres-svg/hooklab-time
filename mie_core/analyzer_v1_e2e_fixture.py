#!/usr/bin/env python3
"""Deterministic end-to-end integration fixture for Analyzer v1.
Tests orchestration/gates without pretending synthetic fixture data are empirical song evidence.
"""
import json,tempfile,subprocess,sys
from pathlib import Path

def dump(p,x):p.write_text(json.dumps(x,indent=2))
def main():
 with tempfile.TemporaryDirectory() as td:
  d=Path(td);out=d/'out'
  manifest=d/'manifest.json';ac=d/'acoustic.json';txt=d/'text.json';reg=d/'registry.json'
  dump(manifest,{'song_id':'FIXTURE_001','source':'INTEGRATION_TEST_ONLY'})
  dump(ac,{'coverage':'FULL','audio_persistence':'NONE','M_structural_count':12,'T_status':'VALID_BEAT_THIS',
           'global':{'M_event_count':12,'M_median_midi':62,'M_range_semitones':9,'T_tempo_bpm':100,'T_tactus_count':32,
                     'mean_near_tactus_share_by_line':.6,'text_line_count':4,'text_repetition_group_count':1,'mean_M_events_per_text_token':1.2}})
  dump(txt,{'schema':'TMT_TEXT_OBJECT_v1.0','units':[{'line_id':'TXT_000','text':'fixture'}],'repetition_groups':[]})
  dump(reg,[{'song_id':'REF_001','genres':['pop'],'styles':['ballad'],'fingerprint':'ref1.json'},
            {'song_id':'REF_002','genres':['pop'],'styles':['ballad'],'fingerprint':'ref2.json'},
            {'song_id':'REF_003','genres':['pop'],'styles':['ballad'],'fingerprint':'ref3.json'},
            {'song_id':'REF_004','genres':['pop'],'styles':['ballad'],'fingerprint':'ref4.json'},
            {'song_id':'REF_005','genres':['pop'],'styles':['ballad'],'fingerprint':'ref5.json'}])
  cmd=[sys.executable,str(Path(__file__).with_name('analyzer_v1_orchestrator.py')),'--manifest',str(manifest),'--acoustic',str(ac),'--text',str(txt),'--registry',str(reg),'--genre','pop','--style','ballad','--output',str(out)]
  subprocess.run(cmd,check=True)
  r=json.loads((out/'analyzer_result.json').read_text())
  assert r['status']=='FULL_TMT_READY',r
  assert (out/'song_object.json').exists() and (out/'structural_fingerprint.json').exists()
  print(json.dumps({'integration_fixture':'PASS','status':r['status']}))
if __name__=='__main__':main()
