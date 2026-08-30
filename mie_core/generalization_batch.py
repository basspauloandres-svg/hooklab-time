#!/usr/bin/env python3
"""Analyzer v1 generalization batch controller.

Builds a reproducible validation plan for heterogeneous real songs. Parameters are
frozen globally: no per-song threshold tuning. Each item records genre/style only
as cohort-routing metadata, never as a success rule.
"""
import argparse,json
from pathlib import Path

REQUIRED=('song_id','title','audio_source','text_source','genre','style')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--registry',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 reg=json.loads(Path(a.registry).read_text())
 songs=reg.get('songs',reg if isinstance(reg,list) else [])
 errors=[];seen=set();out=[]
 for i,s in enumerate(songs):
  miss=[k for k in REQUIRED if not s.get(k)]
  if miss: errors.append({'index':i,'missing':miss});continue
  if s['song_id'] in seen: errors.append({'index':i,'duplicate_song_id':s['song_id']});continue
  seen.add(s['song_id'])
  out.append({**s,'parameter_policy':'GLOBAL_FROZEN','analysis_status':'PENDING_REAL_E2E','corpus_eligibility':'PENDING_GATE'})
 plan={'schema':'ANALYZER_GENERALIZATION_PLAN_v1.0','n':len(out),'songs':out,'errors':errors,
       'rules':['No per-song threshold tuning.','Failed songs remain evidence of generalization limits.','Only strict-gate PASS items enter the comparable empirical matrix.','Genre/style route cohorts; they do not determine desirability.']}
 Path(a.output).write_text(json.dumps(plan,indent=2,ensure_ascii=False))
 print(json.dumps({'n':len(out),'errors':len(errors)}))
 if errors: raise SystemExit(2)
if __name__=='__main__':main()
