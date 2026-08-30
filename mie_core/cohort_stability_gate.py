#!/usr/bin/env python3
"""Evaluate whether a ROBUST genre::style cohort has stabilized across N checkpoints.

N alone never establishes representativeness. The gate requires local convergence across
consecutive nested snapshots AND rejects persistent directional drift across the evaluated
checkpoint sequence. Tolerances are engineering criteria to be calibrated empirically.
"""
import argparse,csv,json,statistics
from pathlib import Path
FEATURES={'tempo_bpm':{'rel_tol':.05},'melodic_range_semitones':{'rel_tol':.10},'melodic_events_per_token':{'rel_tol':.12},'near_tactus_share':{'abs_tol':.08},'text_line_count':{'rel_tol':.15}}
def fnum(x):
 try:return float(x)
 except:return None
def summarize(rows):
 out={}
 for k in FEATURES:
  z=[fnum(r.get(k)) for r in rows];z=[x for x in z if x is not None]
  if z:out[k]={'median':statistics.median(z),'q25':statistics.quantiles(z,n=4,method='inclusive')[0] if len(z)>1 else z[0],'q75':statistics.quantiles(z,n=4,method='inclusive')[2] if len(z)>1 else z[0]}
 return out
def delta(x,y,rule):return abs(y-x) if 'abs_tol' in rule else abs(y-x)/max(abs(x),1e-9)
def tol(rule):return rule.get('abs_tol',rule.get('rel_tol'))
def transition(a,b,k):
 rule=FEATURES[k];ch={s:delta(a[k][s],b[k][s],rule) for s in ('median','q25','q75')};return all(v<=tol(rule) for v in ch.values()),ch
def directional_drift(snaps,k):
 rule=FEATURES[k];med=[s['summary'][k]['median'] for s in snaps if k in s['summary']]
 if len(med)<3:return False,0
 dif=[b-a for a,b in zip(med,med[1:])];nz=[d for d in dif if abs(d)>1e-12];same=bool(nz) and (all(d>0 for d in nz) or all(d<0 for d in nz));cumulative=delta(med[0],med[-1],rule)
 return same and cumulative>1.5*tol(rule),cumulative
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--matrix',required=True);ap.add_argument('--checkpoints',default='30,50,75,100,125');ap.add_argument('--consecutive',type=int,default=2);ap.add_argument('--output',required=True);a=ap.parse_args()
 rows=list(csv.DictReader(Path(a.matrix).open(encoding='utf-8')));cps=[int(x) for x in a.checkpoints.split(',') if int(x)<=len(rows)];snaps=[{'n':n,'summary':summarize(rows[:n])} for n in cps];trs=[]
 for x,y in zip(snaps,snaps[1:]):
  common=sorted(set(x['summary'])&set(y['summary']));feat={};ok=bool(common)
  for k in common:
   z,ch=transition(x['summary'],y['summary'],k);feat[k]={'stable':z,'change':ch};ok=ok and z
  trs.append({'from_n':x['n'],'to_n':y['n'],'stable':ok,'features':feat})
 tail=0
 for t in reversed(trs):
  if t['stable']:tail+=1
  else:break
 drift={};any_drift=False
 for k in FEATURES:
  if all(k in s['summary'] for s in snaps):
   d,c=directional_drift(snaps,k);drift[k]={'persistent_directional_drift':d,'cumulative_change':c};any_drift=any_drift or d
 status='STABLE_REFERENCE_READY' if len(rows)>=50 and tail>=a.consecutive and not any_drift else 'MORE_ROBUST_DATA_REQUIRED'
 rule='N alone does not establish representativeness; freeze only with sufficient N, consecutive local stability, and absence of persistent directional drift.'
 out={'schema':'HOOKLAB_COHORT_STABILITY_GATE_v1.1.1','status':status,'rows':len(rows),'checkpoints_evaluated':cps,'required_consecutive_stable_transitions':a.consecutive,'stable_tail_transitions':tail,'persistent_drift_detected':any_drift,'drift_audit':drift,'feature_rules':FEATURES,'transitions':trs,'rule':rule}
 Path(a.output).write_text(json.dumps(out,indent=2));print(json.dumps({'status':status,'rows':len(rows),'stable_tail':tail,'drift':any_drift}));raise SystemExit(0 if status=='STABLE_REFERENCE_READY' else 4)
if __name__=='__main__':main()
