#!/usr/bin/env python3
"""Automatic melodic-confidence triage for large HookLab batches.

This is a scalable confidence gate, not independent proof of vocal identity. It combines
observable structural evidence already produced by the Analyzer and sends ambiguous rows
to audit instead of blocking the whole corpus.
"""
import argparse,csv,json,math
from pathlib import Path

def f(r,k,default=0.):
 try:return float(r.get(k,default))
 except:return default

def score(r):
 overlap=f(r,'melody_overlap_ratio',1);coverage=f(r,'melody_track_coverage');rng=f(r,'melodic_range_semitones');reg=f(r,'melodic_register_midi');ept=f(r,'melodic_events_per_token');base=f(r,'melody_candidate_score');tokens=f(r,'text_token_count')
 s=0.;parts={}
 parts['monophony']=max(0.,1-min(1.,overlap/.25));s+=parts['monophony']*.20
 parts['coverage']=max(0.,min(1.,(coverage-.45)/.45));s+=parts['coverage']*.18
 parts['range']=1. if 7<=rng<=30 else .6 if 5<=rng<=36 else 0.;s+=parts['range']*.12
 parts['register']=1. if 50<=reg<=82 else .5 if 45<=reg<=88 else 0.;s+=parts['register']*.10
 parts['text_density']=1. if .45<=ept<=1.8 else .5 if .25<=ept<=2.5 else 0.;s+=parts['text_density']*.20
 parts['analyzer_score']=max(0.,min(1.,base/11));s+=parts['analyzer_score']*.12
 parts['text_support']=max(0.,min(1.,tokens/100));s+=parts['text_support']*.08
 return round(s,4),parts

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);ap.add_argument('--high',type=float,default=.78);ap.add_argument('--low',type=float,default=.58);a=ap.parse_args()
 rows=list(csv.DictReader(Path(a.input).open(encoding='utf-8')));out=[]
 for r in rows:
  s,p=score(r);decision='AUTO_HIGH_CONFIDENCE' if s>=a.high else 'HUMAN_AUDIT' if s>=a.low else 'REJECT_OR_REANALYZE'
  out.append({**r,'melodic_confidence_score':s,'melodic_confidence_decision':decision,'melodic_confidence_components':json.dumps(p,separators=(',',':'))})
 fields=sorted({k for r in out for k in r});op=Path(a.output);op.parent.mkdir(parents=True,exist_ok=True)
 with op.open('w',newline='',encoding='utf-8') as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(out)
 counts={x:sum(r['melodic_confidence_decision']==x for r in out) for x in ['AUTO_HIGH_CONFIDENCE','HUMAN_AUDIT','REJECT_OR_REANALYZE']}
 summary={'schema':'HOOKLAB_MELODIC_CONFIDENCE_GATE_v1.0','rows':len(out),'thresholds':{'high':a.high,'low':a.low},'counts':counts,'semantics':'TRIAGE_ONLY_NOT_INDEPENDENT_VOCAL_IDENTITY_PROOF','batch_rule':'AMBIGUOUS_ROWS_ARE_QUARANTINED; THEY_DO_NOT_BLOCK_OTHER_SONGS'}
 op.with_suffix('.summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
if __name__=='__main__':main()
