#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def load(p):return json.loads(Path(p).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cosod',required=True);ap.add_argument('--salami',required=True);ap.add_argument('--harmonix',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 C=load(a.cosod);S=load(a.salami);H=load(a.harmonix)
 sets={
  'COSOD':{x['candidate_id'] for x in C.get('matches',[])},
  'SALAMI':{x['candidate_id'] for x in S.get('matches',[])},
  'HARMONIX':{x['candidate_id'] for x in H.get('matches',[])}
 }
 union=set().union(*sets.values());all_ids=sets['COSOD']&sets['HARMONIX']&sets['SALAMI']
 pair={
  'COSOD_HARMONIX':sorted(sets['COSOD']&sets['HARMONIX']),
  'COSOD_SALAMI':sorted(sets['COSOD']&sets['SALAMI']),
  'HARMONIX_SALAMI':sorted(sets['HARMONIX']&sets['SALAMI'])
 }
 rows=[]
 for cid in sorted(union):rows.append({'candidate_id':cid,'providers':[k for k,v in sets.items() if cid in v]})
 out={'schema':'HOOKLAB_M300_MULTI_PROVIDER_COVERAGE_v1.0','m300_count':300,'providers':{k:{'pass_count':len(v),'coverage_rate':len(v)/300} for k,v in sets.items()},'union_unique_count':len(union),'union_coverage_rate':len(union)/300,'incremental_harmonix_beyond_cosod':len(sets['HARMONIX']-sets['COSOD']),'incremental_cosod_beyond_harmonix':len(sets['COSOD']-sets['HARMONIX']),'pairwise_intersections':{k:{'count':len(v),'candidate_ids':v} for k,v in pair.items()},'all_three_intersection_count':len(all_ids),'rows':rows,'invariants':['provider PASS means licensed annotation evidence available, not audio Gate A PASS','provider ontologies are not pooled until semantic harmonization passes','REFERENCE_UNAVAILABLE is not FAIL','scientific promotion remains false until feature-level gates pass'],'scientific_promotion':False}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'union_unique_count':len(union),'union_coverage_rate':out['union_coverage_rate'],'cosod_harmonix_overlap':len(pair['COSOD_HARMONIX'])}))
if __name__=='__main__':main()
