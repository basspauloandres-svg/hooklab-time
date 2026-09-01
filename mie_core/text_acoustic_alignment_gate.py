#!/usr/bin/env python3
"""Text-Acoustic Alignment Gate v0.1.

Accepts documentary Text Object plus externally produced acoustic line/nucleus
windows. It validates monotonicity/coverage and attaches timing only when evidence
exists. It never reconstructs lyric content from audio and never uses text to set pitch.
"""
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--text',required=True);ap.add_argument('--windows',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 t=json.loads(Path(a.text).read_text());w=json.loads(Path(a.windows).read_text())
 wins=w.get('windows',w if isinstance(w,list) else [])
 valid=[];last=-1.0
 for x in wins:
  s=float(x['start_s']);e=float(x['end_s']);lid=x.get('line_id')
  if e<=s or s<last: continue
  valid.append({'line_id':lid,'start_s':s,'end_s':e,'confidence':x.get('confidence'),'evidence':x.get('evidence','ACOUSTIC')});last=s
 by={x['line_id']:x for x in valid if x.get('line_id')}
 aligned=[]
 for u in t.get('units',[]):
  z=dict(u);x=by.get(u['line_id'])
  if x:z.update({'start_s':x['start_s'],'end_s':x['end_s'],'alignment_confidence':x.get('confidence')})
  aligned.append(z)
 n=sum('start_s' in x for x in aligned);total=len(aligned);ratio=n/total if total else 0
 t['units']=aligned;t['alignment_status']='ALIGNED' if ratio>=.95 else ('PARTIAL' if n else 'UNALIGNED')
 t['alignment_coverage']=ratio;t['alignment_rule']='Timing attaches only from acoustic evidence; lexical content remains documentary.'
 Path(a.output).write_text(json.dumps(t,indent=2,ensure_ascii=False));print(json.dumps({'aligned':n,'total':total,'coverage':ratio,'status':t['alignment_status']}))
if __name__=='__main__':main()
