#!/usr/bin/env python3
"""HookLab preproduction latency gate.

Separates offline knowledge-building cost from online creative inference. The online
path must never trigger corpus search/reanalysis. Thresholds are engineering targets
subject to empirical calibration against measured traditional preproduction baselines.
"""
import argparse,json,time
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--metrics',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 m=json.loads(Path(a.metrics).read_text())
 online=float(m.get('T_online_total_seconds',m.get('T_total_seconds',1e18)))
 search=float(m.get('T_online_search_seconds',0))
 reanalysis=bool(m.get('online_corpus_reanalysis',False))
 first_audio=float(m.get('TTFP_seconds',online))
 # Initial engineering gates; calibration requires empirical traditional-workflow baseline.
 gates={
   'NO_ONLINE_CORPUS_SEARCH': search == 0,
   'NO_ONLINE_CORPUS_REANALYSIS': not reanalysis,
   'TTFP_RECORDED': first_audio < 1e18,
   'ONLINE_LATENCY_RECORDED': online < 1e18
 }
 status='LATENCY_ARCHITECTURE_PASS' if all(gates.values()) else 'LATENCY_ARCHITECTURE_FAIL'
 out={'schema':'HOOKLAB_PREPRODUCTION_LATENCY_GATE_v1.0','status':status,'gates':gates,
      'metrics':m,
      'architecture':{'offline':'sources->validation->Analyzer->MatrixX->cohorts->reference_models->cache',
                      'online':'genre/style/purpose->router->cached_reference->constraints->generation->audible_prototype'},
      'primary_metric':'TTFP_seconds',
      'comparison_requirement':'Calibrate acceptable TTFP against measured traditional preproduction baseline; do not claim acceleration from an arbitrary threshold.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
 if status.endswith('FAIL'): raise SystemExit(2)
if __name__=='__main__':main()
