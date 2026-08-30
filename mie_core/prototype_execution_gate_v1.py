#!/usr/bin/env python3
"""Execute first audible prototype only from a real readiness-approved cohort.

This orchestration gate refuses synthetic/fabricated cohort statistics. It consumes a
readiness report, router output and compiled constraints already produced by the real
pipeline, then delegates audio generation to tmt_candidate_generator.py.
"""
import argparse,json,subprocess,sys,time
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--readiness',required=True)
    ap.add_argument('--router-output',required=True)
    ap.add_argument('--constraints',required=True)
    ap.add_argument('--output-dir',required=True)
    ap.add_argument('--seed',type=int,default=1701)
    ap.add_argument('--metrics-output',required=True)
    a=ap.parse_args()
    t0=time.perf_counter()
    ready=json.loads(Path(a.readiness).read_text())
    status=ready.get('status','')
    if status!='READY_FOR_DATA_CONDITIONED_GENERATION':
        raise SystemExit('readiness gate has not approved a real cohort')
    router=json.loads(Path(a.router_output).read_text())
    if router.get('status')!='CACHE_HIT_READY_FOR_GENERATION':
        raise SystemExit('router did not resolve a precomputed cohort')
    constraints=json.loads(Path(a.constraints).read_text())
    if constraints.get('cohort_key')!=router.get('payload',{}).get('cohort_key'):
        raise SystemExit('cohort trace mismatch between router and constraints')
    cmd=[sys.executable,str(Path(__file__).with_name('tmt_candidate_generator.py')),
         '--constraints',a.constraints,'--output-dir',a.output_dir,'--seed',str(a.seed)]
    tg=time.perf_counter(); subprocess.run(cmd,check=True); generation=time.perf_counter()-tg
    total=time.perf_counter()-t0
    metrics={'schema':'HOOKLAB_FIRST_AUDIBLE_EXECUTION_v1.0','status':'FIRST_DATA_CONDITIONED_AUDIO_WITH_TRACE_AND_TTFP',
             'cohort_key':constraints.get('cohort_key'),
             'TTFP_seconds':total,'T_online_total_seconds':total,
             'T_generation_seconds':generation,'T_online_search_seconds':0,
             'online_corpus_reanalysis':False,
             'evidence_boundary':'REAL_READINESS_APPROVED_COHORT_ONLY'}
    Path(a.metrics_output).write_text(json.dumps(metrics,indent=2,ensure_ascii=False))
    print(json.dumps(metrics))
if __name__=='__main__': main()
