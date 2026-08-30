#!/usr/bin/env python3
"""Hard gate separating target engineering candidates from scientific evidence.

Scientific promotion requires every row used in a target cohort to pass:
- structural FULL_TMT
- high-confidence identity/version
- genre/style cohort assignment
- YouTube + Spotify reach floors
- social-network reach evidence
- melodic-reference validation

Missing evidence is represented as PENDING/FAIL and can never be silently coerced to PASS.
"""
import argparse,csv,json
from pathlib import Path

def truth(v): return str(v).strip().upper() in {'TRUE','PASS','PASSED','VERIFIED','1'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--matrix',required=True);ap.add_argument('--output',required=True);ap.add_argument('--min-n',type=int,default=3);a=ap.parse_args()
 rows=list(csv.DictReader(Path(a.matrix).open(encoding='utf-8'))); evaluated=[]
 for r in rows:
  gates={
   'target_candidate':r.get('target_candidate_status')=='TARGET_COHORT_CANDIDATE',
   'identity':truth(r.get('identity_high_confidence')),
   'youtube':truth(r.get('youtube_reach_gate')),
   'spotify':truth(r.get('spotify_reach_gate')),
   'crossplatform_streaming':truth(r.get('crossplatform_streaming_gate')),
   'social_network':truth(r.get('social_network_reach_gate')),
   'melodic_reference':truth(r.get('melodic_reference_gate')),
  }
  evaluated.append({'title':r.get('title'),'artist':r.get('artist'),'cohort_key':r.get('cohort_key'),'gates':gates,'scientific_pass':all(gates.values())})
 passing=[x for x in evaluated if x['scientific_pass']];cohorts={x['cohort_key'] for x in passing};ready=len(passing)>=a.min_n and len(cohorts)==1
 out={'schema':'HOOKLAB_TARGET_SCIENTIFIC_PROMOTION_GATE_v1.0','status':'SCIENTIFIC_COHORT_READY' if ready else 'SCIENTIFIC_PROMOTION_BLOCKED','min_n':a.min_n,'scientific_pass_n':len(passing),'evaluated_n':len(evaluated),'cohorts':sorted(cohorts),'rows':evaluated,'hard_rule':'PENDING_OR_MISSING_EVIDENCE_IS_NOT_PASS','scientific_promotion':ready}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':out['status'],'scientific_pass_n':len(passing),'evaluated_n':len(evaluated)}));raise SystemExit(0 if ready else 4)
if __name__=='__main__':main()
