#!/usr/bin/env python3
"""Cache-first HookLab online preproduction router.

The online path is deliberately unable to search or rebuild the corpus. It resolves
only precomputed cohort references. A cache miss is explicit and must be handled by
the offline build process, keeping TTFP independent from corpus acquisition latency.
"""
import argparse,json,time
from pathlib import Path

def norm(x): return '_'.join(str(x).strip().lower().replace('-',' ').split())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cache',required=True);ap.add_argument('--genre',required=True);ap.add_argument('--style',required=True);ap.add_argument('--purpose',default='');ap.add_argument('--output',required=True);a=ap.parse_args()
 t0=time.perf_counter();cache=json.loads(Path(a.cache).read_text());key=f'{norm(a.genre)}::{norm(a.style)}'
 cohorts=cache.get('cohorts',{});ref=cohorts.get(key)
 if ref is None:
  status='CACHE_MISS_OFFLINE_BUILD_REQUIRED'; payload=None
 else:
  status='CACHE_HIT_READY_FOR_GENERATION';payload={'cohort_key':key,'reference':ref,'purpose':a.purpose}
 elapsed=time.perf_counter()-t0
 out={'schema':'HOOKLAB_PREPRODUCTION_ROUTER_v1.0','status':status,'request':{'genre':a.genre,'style':a.style,'purpose':a.purpose},
      'payload':payload,'latency':{'T_router_seconds':elapsed,'T_online_search_seconds':0,'online_corpus_reanalysis':False},
      'invariant':'ONLINE_PATH_CANNOT_SEARCH_OR_REANALYZE_CORPUS'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
 if ref is None: raise SystemExit(3)
if __name__=='__main__':main()
