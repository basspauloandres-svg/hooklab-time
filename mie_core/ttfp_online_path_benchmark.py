#!/usr/bin/env python3
"""Benchmark HookLab's online preproduction path from cached cohort to structural candidates.

This measures machine-side latency only. It does not claim superiority over traditional
preproduction until a separately observed human baseline is supplied. The benchmark runs
router -> constraints -> generation repeatedly with no network search and no corpus reanalysis.
"""
import argparse,json,subprocess,sys,tempfile,time,statistics
from pathlib import Path

def run(cmd):
 t=time.perf_counter();p=subprocess.run(cmd,check=True,capture_output=True,text=True);return time.perf_counter()-t,p.stdout

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cache',required=True);ap.add_argument('--output',required=True);ap.add_argument('--runs',type=int,default=30);a=ap.parse_args()
 root=Path(__file__).resolve().parent;times=[];parts=[]
 with tempfile.TemporaryDirectory() as td:
  td=Path(td)
  for i in range(a.runs):
   r=td/f'r{i}.json';c=td/f'c{i}.json';g=td/f'g{i}.json'
   t1,_=run([sys.executable,str(root/'preproduction_router.py'),'--cache',a.cache,'--genre','pop_rock','--style','dance_pop','--purpose','TTFP benchmark','--output',str(r)])
   t2,_=run([sys.executable,str(root/'preproduction_constraints_compiler.py'),'--router-output',str(r),'--output',str(c)])
   t3,_=run([sys.executable,str(root/'tmt_structural_candidate_generator_v2.py'),'--constraints',str(c),'--output',str(g)])
   total=t1+t2+t3;times.append(total);parts.append({'router_s':t1,'constraints_s':t2,'generation_s':t3,'total_s':total})
 out={'schema':'HOOKLAB_TTFP_ONLINE_PATH_BENCHMARK_v1.0','runs':a.runs,'median_seconds':statistics.median(times),'mean_seconds':statistics.mean(times),'p95_seconds':sorted(times)[max(0,min(len(times)-1,int(.95*len(times))-1))],'min_seconds':min(times),'max_seconds':max(times),'T_online_search_seconds':0,'online_corpus_reanalysis':False,'path':'cached cohort -> router -> constraints -> 3 structural TMT candidates','human_traditional_baseline_status':'PENDING_OBSERVED_EXPERIMENT','comparative_claim_allowed':False,'run_details':parts}
 Path(a.output).write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['runs','median_seconds','p95_seconds','human_traditional_baseline_status']}))
if __name__=='__main__':main()
