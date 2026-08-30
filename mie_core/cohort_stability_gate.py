#!/usr/bin/env python3
"""Evaluate whether a ROBUST genre::style cohort has stabilized across N checkpoints.

This gate does not claim representativeness from N alone. It compares descriptive
reference parameters between nested cohort snapshots and reports convergence only when
changes remain below prespecified engineering tolerances for consecutive checkpoints.
"""
import argparse,csv,json,statistics
from pathlib import Path

FEATURES={
 'tempo_bpm': {'rel_tol':0.05},
 'melodic_range_semitones': {'rel_tol':0.10},
 'melodic_events_per_token': {'rel_tol':0.12},
 'near_tactus_share': {'abs_tol':0.08},
 'text_line_count': {'rel_tol':0.15},
}

def fnum(x):
 try:return float(x)
 except:return None

def summarize(rows):
 out={}
 for k in FEATURES:
  a=[fnum(r.get(k)) for r in rows];a=[x for x in a if x is not None]
  if a:out[k]={'median':statistics.median(a),'q25':statistics.quantiles(a,n=4,method='inclusive')[0] if len(a)>1 else a[0],'q75':statistics.quantiles(a,n=4,method='inclusive')[2] if len(a)>1 else a[0]}
 return out

def stable(a,b,k):
 rule=FEATURES[k]
 changes={}
 ok=True
 for stat in ('median','q25','q75'):
  x,y=a[k][stat],b[k][stat]
  if 'abs_tol' in rule: d=abs(y-x); pass_=d<=rule['abs_tol']
  else:
   d=abs(y-x)/max(abs(x),1e-9);pass_=d<=rule['rel_tol']
  changes[stat]=d;ok=ok and pass_
 return ok,changes

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--matrix',required=True);ap.add_argument('--checkpoints',default='30,50,75,100,125');ap.add_argument('--consecutive',type=int,default=2);ap.add_argument('--output',required=True);a=ap.parse_args()
 rows=list(csv.DictReader(Path(a.matrix).open(encoding='utf-8'))); cps=[int(x) for x in a.checkpoints.split(',') if int(x)<=len(rows)]
 snaps=[]
 for n in cps:snaps.append({'n':n,'summary':summarize(rows[:n])})
 transitions=[]
 for x,y in zip(snaps,snaps[1:]):
  common=sorted(set(x['summary'])&set(y['summary']));feat={};all_ok=bool(common)
  for k in common:
   ok,ch=stable(x['summary'],y['summary'],k);feat[k]={'stable':ok,'change':ch};all_ok=all_ok and ok
  transitions.append({'from_n':x['n'],'to_n':y['n'],'stable':all_ok,'features':feat})
 tail=0
 for t in reversed(transitions):
  if t['stable']:tail+=1
  else:break
 status='STABLE_REFERENCE_READY' if len(rows)>=50 and tail>=a.consecutive else 'MORE_ROBUST_DATA_REQUIRED'
 out={'schema':'HOOKLAB_COHORT_STABILITY_GATE_v1.0','status':status,'rows':len(rows),'checkpoints_evaluated':cps,'required_consecutive_stable_transitions':a.consecutive,'stable_tail_transitions':tail,'feature_rules':FEATURES,'transitions':transitions,'rule':'N alone does not establish representativeness; reference freezing requires sufficient N plus observed incremental stability.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':status,'rows':len(rows),'stable_tail':tail}))
 raise SystemExit(0 if status=='STABLE_REFERENCE_READY' else 4)
if __name__=='__main__':main()
