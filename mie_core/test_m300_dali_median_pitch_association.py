#!/usr/bin/env python3
"""Software regression only; synthetic fixtures are never scientific evidence."""
import json,tempfile,subprocess,sys
from pathlib import Path

def write(p,x):p.write_text(json.dumps(x))

def main():
 with tempfile.TemporaryDirectory() as td:
  root=Path(td); ev=root/'ev';ev.mkdir()
  candidates=[];ident=[]
  for i in range(30):
   title=f'Song {i}';artist=f'Artist {i}';did=f'D{i}'
   candidates.append({'candidate_id':f'M300::X::{i}','chart_year':2020,'rank':i%15+1,'title':title,'artist':artist,'spotify_playcount_observed':10**(6+i/10)})
   write(ev/f'{i}.json',{'schema':'HOOKLAB_DALI_ANNOTATION_EVIDENCE_v1.0','status':'PASS_ANNOTATION_PARSE','dali_id':did,'title':title,'artist':artist,'quality_tier':'HIGH_NCC','ncc':.9,'melody_summary':{'pitch_median_midi':50+i}})
   ident.append({'dali_id':did,'released_recording_identity':'PASS'})
  write(root/'m300.json',{'candidates':candidates});write(root/'ident.json',{'rows':ident})
  write(root/'allow.json',{'stable_features':['median_pitch_st']})
  cmd=[sys.executable,'mie_core/m300_dali_median_pitch_association.py','--m300',str(root/'m300.json'),'--dali-evidence-dir',str(ev),'--identity-manifest',str(root/'ident.json'),'--allowlist',str(root/'allow.json'),'--output',str(root/'out.json')]
  subprocess.check_call(cmd);out=json.loads((root/'out.json').read_text())
  assert out['eligible_rows']==30
  assert out['scientific_promotion'] is False and out['creative_rule_promotion'] is False
  assert all(t['n']==30 for t in out['tests'])
  # Remove identity PASS: all rows must fail closed.
  write(root/'ident.json',{'rows':[]});subprocess.check_call(cmd);out=json.loads((root/'out.json').read_text())
  assert out['eligible_rows']==0
  assert 'INSUFFICIENT_VERSION_ALIGNED_DALI_M300_ROWS' in out['blocking_reasons']
  print('PASS: association runner is identity-gated and never auto-promotes synthetic evidence')
if __name__=='__main__':main()
