#!/usr/bin/env python3
"""Dimension-aware distinction between two TMT structural fingerprints.
Uses standardized distances only when corpus reference statistics are supplied;
otherwise reports raw per-feature deltas and refuses an arbitrary global score.
Data-first guard prevents manual success-weight injection.
"""
import argparse,json,math
from pathlib import Path
from data_first_guard import assert_no_manual_success_weights

def flatten(d,p=''):
 out={}
 for k,v in d.items():
  q=f'{p}.{k}' if p else k
  if isinstance(v,dict):out.update(flatten(v,q))
  elif isinstance(v,(int,float)) and math.isfinite(v):out[q]=v
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('a');ap.add_argument('b');ap.add_argument('output');ap.add_argument('--reference')
 x=ap.parse_args(); A=json.loads(Path(x.a).read_text());B=json.loads(Path(x.b).read_text())
 assert_no_manual_success_weights(A);assert_no_manual_success_weights(B)
 fa,fb=flatten(A),flatten(B);keys=sorted(set(fa)&set(fb));dims={}
 ref=None
 if x.reference:
  ref=json.loads(Path(x.reference).read_text());assert_no_manual_success_weights(ref)
 for k in keys:
  top=k.split('.')[0]; row={'feature':k,'a':fa[k],'b':fb[k],'delta':fb[k]-fa[k],'absolute_delta':abs(fb[k]-fa[k])}
  if ref and k in ref.get('features',{}):
   sd=ref['features'][k].get('std')
   if isinstance(sd,(int,float)) and sd>0: row['standardized_delta']=row['delta']/sd
  dims.setdefault(top,[]).append(row)
 standardized=[abs(r['standardized_delta']) for rows in dims.values() for r in rows if 'standardized_delta' in r]
 out={'schema':'TMT_FINGERPRINT_COMPARISON_v1.1','a':A.get('song_id'),'b':B.get('song_id'),'dimensions':dims,
      'global_standardized_distance':(sum(v*v for v in standardized)**0.5 if standardized else None),
      'global_similarity':None,
      'reason':('Reference-standardized Euclidean distance is reported without converting it to a similarity/success score.' if standardized else 'A corpus reference distribution is required before heterogeneous features can be standardized and combined.'),
      'epistemic_guard':{'policy':'DATA_FIRST','manual_weights':'REJECTED'},'inference_status':'DESCRIPTIVE_DISTINCTION_ONLY'}
 Path(x.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
if __name__=='__main__':main()
