#!/usr/bin/env python3
"""Compile cached cohort statistics into traceable TMT generation constraints.

This module is strictly online-safe: it consumes only a cached cohort reference and
never searches or reanalyzes the corpus. It emits bounded descriptive constraints,
not claims about causation or guaranteed success.
"""
import argparse,json,time
from pathlib import Path

def pick_interval(ref, key, fallback=None):
    v=ref.get(key)
    if isinstance(v, dict):
        lo=v.get('q25', v.get('p25', v.get('min')))
        hi=v.get('q75', v.get('p75', v.get('max')))
        med=v.get('median', v.get('mean'))
        return {'low':lo,'target':med,'high':hi,'source_feature':key}
    return fallback

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--router-output',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    t0=time.perf_counter();r=json.loads(Path(a.router_output).read_text())
    if r.get('status')!='CACHE_HIT_READY_FOR_GENERATION':
        raise SystemExit('router output is not generation-ready')
    ref=r['payload']['reference']; purpose=r['payload'].get('purpose','')
    constraints={
      'tempo_bpm':pick_interval(ref,'T_tempo_bpm'),
      'melodic_register_midi':pick_interval(ref,'M_median_midi'),
      'melodic_range_semitones':pick_interval(ref,'M_range_semitones'),
      'melodic_events_per_token':pick_interval(ref,'M_events_per_token'),
      'near_tactus_share':pick_interval(ref,'T_near_tactus_share'),
      'text_line_count':pick_interval(ref,'text_line_count')
    }
    constraints={k:v for k,v in constraints.items() if v is not None}
    out={'schema':'HOOKLAB_TMT_CONSTRAINTS_v1.0','cohort_key':r['payload']['cohort_key'],'purpose':purpose,
         'constraints':constraints,
         'semantics':'DESCRIPTIVE_COHORT_BOUNDS_NOT_CAUSAL_RULES',
         'traceability':{'router_schema':r.get('schema'),'reference_fields_used':[v['source_feature'] for v in constraints.values()]},
         'latency':{'T_constraints_seconds':time.perf_counter()-t0,'T_online_search_seconds':0,'online_corpus_reanalysis':False}}
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
if __name__=='__main__': main()
