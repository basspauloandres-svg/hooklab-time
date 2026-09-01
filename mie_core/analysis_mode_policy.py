#!/usr/bin/env python3
"""Validated policy contract for HookLab robust vs light analysis modes.

ROBUST builds/refreshes the master genre::style reference offline.
LIGHT never substitutes for ROBUST: it retrieves the master reference and adds a small
contextual comparison cohort for a particular preproduction request.
"""
import argparse,json
from pathlib import Path

POLICY={
 'schema':'HOOKLAB_ANALYSIS_MODE_POLICY_v1.0',
 'ROBUST':{
   'validation_seed_n':5,'pilot_n':30,'minimum_analytic_n':50,'standard_target_n':100,
   'heterogeneous_extension_n':[150,200],
   'stability_checkpoints_n':[30,50,75,100,125],
   'purpose':'MASTER_GENRE_STYLE_REFERENCE_OFFLINE',
   'requires_full_song':True,'requires_full_tmt':True,'cache_publish':True
 },
 'LIGHT':{
   'contextual_cohort_min_n':10,'contextual_cohort_max_n':20,
   'purpose':'PARTICULAR_PREPRODUCTION_CONTEXTUALIZATION',
   'requires_robust_reference':True,'rebuild_master_corpus':False,
   'online_corpus_reanalysis':False,'cache_first':True
 },
 'hard_rules':[
   'LIGHT_NEVER_REPLACES_ROBUST',
   'LIGHT_MUST_USE_A_CACHED_ROBUST_REFERENCE',
   'ROBUST_N_IS_A_TARGET_PLUS_STABILITY_TEST_NOT_A_CLAIM_OF_AUTOMATIC_REPRESENTATIVENESS',
   'FULL_SONG_AND_PROVENANCE_GATES_REMAIN_ACTIVE_IN_BOTH_MODES'
 ]
}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['ROBUST','LIGHT'],required=True);ap.add_argument('--n',type=int,required=True);ap.add_argument('--robust-cache-ready',action='store_true');ap.add_argument('--output',required=True);a=ap.parse_args()
 p=POLICY[a.mode]
 if a.mode=='ROBUST':
  status='PASS' if a.n>=p['minimum_analytic_n'] else 'PILOT_ONLY' if a.n>=p['pilot_n'] else 'VALIDATION_ONLY'
  note='N>=50 permits analytic use; N=100 is the standard target. Stability checkpoints remain mandatory before freezing a master reference.'
 else:
  size_ok=p['contextual_cohort_min_n']<=a.n<=p['contextual_cohort_max_n'];status='PASS' if size_ok and a.robust_cache_ready else 'BLOCKED'
  note='LIGHT requires 10-20 contextual comparators plus an existing ROBUST cached reference; it never rebuilds the master corpus online.'
 out={'schema':'HOOKLAB_ANALYSIS_MODE_POLICY_GATE_v1.0','mode':a.mode,'n':a.n,'status':status,'policy':p,'robust_cache_ready':a.robust_cache_ready,'note':note,'hard_rules':POLICY['hard_rules']}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
 raise SystemExit(0 if status=='PASS' else 4)
if __name__=='__main__':main()
