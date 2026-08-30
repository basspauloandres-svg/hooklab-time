#!/usr/bin/env python3
"""Compute transparent project-stage completion from current HookLab evidence.

The script refuses to report 100% unless every definitive HookLab criterion is evidenced.
Social-network propagation is excluded by project decision and deferred to a future
release-analytics development. Percentages are engineering progress indicators, never
statistical confidence estimates.
"""
import argparse,csv,json
from pathlib import Path

def truth(v): return str(v).strip().lower() in {'true','1','yes','pass','ready'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--matrix',required=True);ap.add_argument('--checkpoint',required=True);ap.add_argument('--output',required=True);ap.add_argument('--ttfp-baseline',default='PENDING');ap.add_argument('--docs-final',default='PENDING');a=ap.parse_args()
 rows=list(csv.DictReader(Path(a.matrix).open(encoding='utf-8')));cp=json.loads(Path(a.checkpoint).read_text())
 candidates=[r for r in rows if r.get('target_candidate_status')=='TARGET_COHORT_CANDIDATE']
 n=max(1,len(candidates))
 fullsong=sum(r.get('coverage')=='FULL_SONG' for r in candidates)/n
 identity=sum(truth(r.get('identity_high_confidence')) for r in candidates)/n
 full_tmt=sum(truth(r.get('full_tmt_candidate')) for r in candidates)/n
 reach=sum(truth(r.get('crossplatform_streaming_gate')) for r in candidates)/n
 melody=sum(truth(r.get('melodic_reference_gate')) for r in candidates)/n
 e2e=1.0 if cp.get('status')=='TARGET_SHADOW_E2E_PASS' else 0.0
 cache=1.0 if cp.get('router')=='CACHE_HIT_READY_FOR_GENERATION' and cp.get('T_online_search_seconds')==0 and cp.get('online_corpus_reanalysis') is False else 0.0
 generation=1.0 if cp.get('generation')=='THREE_FULL_TMT_STRUCTURAL_CANDIDATES_READY' else 0.0
 stages=[
  ('architecture_contracts',1.0),('offline_online_cache',cache),('full_song_coverage',fullsong),('identity_version',identity),('analyzer_full_tmt',full_tmt),('matrix_and_cohort',1.0 if candidates else 0.0),('readiness_router_constraints',e2e),('structural_generation',generation),('massive_hit_same_style_cohort',min(1.0,len(candidates)/3)),('youtube_spotify_reach',reach),('melodic_reference_validation',melody),('ttfp_vs_traditional',1.0 if a.ttfp_baseline=='PASS' else 0.0),('final_validation_documentation',1.0 if a.docs_final=='PASS' else 0.0)]
 pct={k:round(v*100,1) for k,v in stages};overall=round(sum(v for _,v in stages)/len(stages)*100,1)
 definitive=all(v==1.0 for _,v in stages)
 out={'schema':'HOOKLAB_DEFINITIVE_COMPLETION_GATE_v1.1','status':'DEFINITIVE_100_PERCENT' if definitive else 'DEVELOPMENT_IN_PROGRESS','overall_percent':100.0 if definitive else overall,'stage_percent':pct,'target_candidates':len(candidates),'scientific_minimum_n_reached':len(candidates)>=3,'excluded_scope':{'social_network_reach':'DEFERRED_TO_FUTURE_RELEASE_ANALYTICS_MODULE'},'rule':'100% is emitted only when every current HookLab stage criterion is evidenced; deferred scopes are not counted in the denominator.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
 raise SystemExit(0 if definitive else 4)
if __name__=='__main__':main()
