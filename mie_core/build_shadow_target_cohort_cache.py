#!/usr/bin/env python3
"""Build a cacheable cohort reference from TARGET_COHORT_CANDIDATE rows.

This is a SHADOW engineering lane: it allows the online preproduction path to be tested
with real massive-hit candidate data before the remaining scientific promotion gates
(social-network evidence and melodic-reference validation) are complete. Outputs are
therefore forbidden from being labeled scientific evidence.
"""
import argparse,csv,json,statistics
from pathlib import Path
FIELDS={
 'T_tempo_bpm':'tempo_bpm','M_median_midi':'melodic_register_midi','M_range_semitones':'melodic_range_semitones',
 'M_events_per_token':'melodic_events_per_token','T_near_tactus_share':'near_tactus_share','text_line_count':'text_line_count'}
def q(a,p):
 a=sorted(a);x=(len(a)-1)*p;l=int(x);h=min(l+1,len(a)-1);f=x-l;return a[l]*(1-f)+a[h]*f
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--matrix',required=True);ap.add_argument('--output',required=True);ap.add_argument('--min-n',type=int,default=3);a=ap.parse_args()
 rows=[r for r in csv.DictReader(Path(a.matrix).open(encoding='utf-8')) if r.get('target_candidate_status')=='TARGET_COHORT_CANDIDATE']
 if len(rows)<a.min_n:raise SystemExit(f'need >={a.min_n} target candidate rows; found {len(rows)}')
 keys={r['cohort_key'] for r in rows}
 if len(keys)!=1:raise SystemExit('shadow rows must share one genre::style cohort')
 ref={}
 for outk,ink in FIELDS.items():
  vals=[float(r[ink]) for r in rows if r.get(ink) not in ('',None)]
  if len(vals)!=len(rows):raise SystemExit('missing field '+ink)
  ref[outk]={'min':min(vals),'q25':q(vals,.25),'median':statistics.median(vals),'q75':q(vals,.75),'max':max(vals),'n':len(vals)}
 key=next(iter(keys));obj={'schema':'HOOKLAB_SHADOW_TARGET_COHORT_CACHE_v1.0','status':'TARGET_SHADOW_READY_FOR_ENGINEERING','scientific_promotion':False,'remaining_gates':['social_network_reach','melodic_reference_validation'],'cohorts':{key:ref},'cohort_n':len(rows),'semantics':'REAL_TARGET_CANDIDATES_ENGINEERING_ONLY_NOT_FINAL_SCIENTIFIC_EVIDENCE'}
 Path(a.output).write_text(json.dumps(obj,indent=2,ensure_ascii=False));print(json.dumps({'status':obj['status'],'cohort_key':key,'n':len(rows)}))
if __name__=='__main__':main()
