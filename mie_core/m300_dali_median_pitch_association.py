#!/usr/bin/env python3
"""Fail-closed M300 association runner for the single calibrated melody feature.

Consumes HookLab-parsed DALI annotation evidence plus an explicit released-recording
identity manifest. It tests only median_pitch_st (= DALI pitch_median_midi), the sole
feature currently representation-stable against both Vocadito human note references.
It does not promote a creative deduction automatically.
"""
from __future__ import annotations
import argparse,json,math,re,unicodedata
from pathlib import Path
from scipy.stats import spearmanr

FEATURE='median_pitch_st'
MIN_N=30
MIN_ABS_RHO=.20
ALPHA=.05

def norm(s):
 s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower()
 s=re.sub(r'\([^)]*\)|\[[^]]*\]',' ',s)
 return ' '.join(re.sub(r'[^a-z0-9]+',' ',s).split())

def toks(s): return {x for x in norm(s).split() if x not in {'the','and','with','feat','featuring','ft','x'}}
def artist_overlap(a,b):
 A,B=toks(a),toks(b)
 return len(A&B)/max(1,min(len(A),len(B)))

def bh(ps):
 m=len(ps)
 if not m:return []
 order=sorted(range(m),key=lambda i:ps[i]);q=[1.]*m;prev=1.
 for rank,i in reversed(list(enumerate(order,1))):
  prev=min(prev,ps[i]*m/rank);q[i]=prev
 return q

def load_evidence(root):
 out=[]
 for p in sorted(Path(root).glob('*.json')):
  try:d=json.loads(p.read_text())
  except Exception:continue
  if d.get('schema')!='HOOKLAB_DALI_ANNOTATION_EVIDENCE_v1.0':continue
  if d.get('status')!='PASS_ANNOTATION_PARSE':continue
  med=(d.get('melody_summary') or {}).get('pitch_median_midi')
  if not isinstance(med,(int,float)):continue
  out.append(d)
 return out

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--m300',required=True)
 ap.add_argument('--dali-evidence-dir',required=True)
 ap.add_argument('--identity-manifest',required=True)
 ap.add_argument('--allowlist',default='config/representation_stable_features_v1.json')
 ap.add_argument('--output',required=True)
 a=ap.parse_args()
 allow=json.loads(Path(a.allowlist).read_text())
 stable=allow.get('stable_features') or allow.get('allowed_features') or []
 if FEATURE not in stable:
  raise SystemExit('median_pitch_st is not representation-calibrated/allowlisted')
 m=json.loads(Path(a.m300).read_text()); evidence=load_evidence(a.dali_evidence_dir)
 ident=json.loads(Path(a.identity_manifest).read_text())
 passes={str(x.get('dali_id')):x for x in ident.get('rows',[]) if x.get('released_recording_identity')=='PASS'}
 rows=[];audit=[]
 for c in m.get('candidates',[]):
  cand=[]
  for d in evidence:
   if norm(c.get('title'))!=norm(d.get('title')):continue
   ov=artist_overlap(c.get('artist'),d.get('artist'))
   if ov>=.5:cand.append((ov,d))
  if not cand:continue
  ov,d=max(cand,key=lambda z:z[0]);did=str(d.get('dali_id'))
  if did not in passes:
   audit.append({'candidate_id':c.get('candidate_id'),'dali_id':did,'reason':'RELEASED_RECORDING_IDENTITY_NOT_PASS'})
   continue
  pitch=float(d['melody_summary']['pitch_median_midi'])
  rows.append({
   'candidate_id':c.get('candidate_id'),'chart_year':c.get('chart_year'),'rank':c.get('rank'),
   'title':c.get('title'),'artist':c.get('artist'),'dali_id':did,'artist_overlap':ov,
   FEATURE:pitch,'m300_rank_strength':16-int(c['rank']),
   'log10_spotify_playcount':math.log10(max(1,int(c.get('spotify_playcount_observed') or 0))),
   'dali_quality_tier':d.get('quality_tier'),'dali_ncc':d.get('ncc'),
   'released_recording_identity':'PASS'})
 tests=[]
 for outcome in ('m300_rank_strength','log10_spotify_playcount'):
  pairs=[(r[FEATURE],r[outcome]) for r in rows if r.get(FEATURE) is not None and r.get(outcome) is not None]
  if len(pairs)>=MIN_N:
   rho,p=spearmanr([x for x,_ in pairs],[y for _,y in pairs])
   tests.append({'feature':FEATURE,'outcome':outcome,'n':len(pairs),'rho':round(float(rho),4),'p':float(p)})
 qs=bh([x['p'] for x in tests])
 for x,q in zip(tests,qs):
  x['q_bh']=float(q)
  x['supported_for_interpretation']=bool(x['n']>=MIN_N and abs(x['rho'])>=MIN_ABS_RHO and q<ALPHA)
 supported=[x for x in tests if x['supported_for_interpretation']]
 reasons=[]
 if len(rows)<MIN_N:reasons.append('INSUFFICIENT_VERSION_ALIGNED_DALI_M300_ROWS')
 if not tests:reasons.append('NO_ASSOCIATION_TEST_REACHED_MIN_N')
 if tests and not supported:reasons.append('NO_ASSOCIATION_SURVIVED_FROZEN_GATE')
 out={
  'schema':'HOOKLAB_M300_DALI_MEDIAN_PITCH_ASSOCIATION_v1.0',
  'feature':FEATURE,'representation_calibration':'VOCADITO_DUAL_REFERENCE_PASS',
  'population_scope':'M300 songs with authorized DALI note-level annotations and explicit released-recording identity PASS',
  'eligible_rows':len(rows),'audit_rows':len(audit),'tests':tests,'supported_for_interpretation':supported,
  'decision':'TARGET_SUBCOHORT_ASSOCIATION_AVAILABLE' if supported else 'ASSOCIATION_PENDING_OR_NOT_SUPPORTED',
  'blocking_reasons':reasons,'scientific_promotion':False,'creative_rule_promotion':False,
  'frozen_gate':{'min_n':MIN_N,'min_abs_spearman_rho':MIN_ABS_RHO,'bh_q_lt':ALPHA,'outcomes':['m300_rank_strength','log10_spotify_playcount']},
  'boundary':'Association is descriptive/associative evidence only. It does not establish causality, hit prediction, or creative deduction eligibility.',
  'rows':rows,'audit':audit}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False))
 print(json.dumps({'eligible_rows':len(rows),'decision':out['decision'],'supported':supported,'blocking_reasons':reasons}))

if __name__=='__main__':main()
