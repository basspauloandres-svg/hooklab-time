#!/usr/bin/env python3
"""Dimension-aware distinction between two TMT structural fingerprints.
Uses standardized distances only when corpus reference statistics are supplied;
otherwise reports raw per-feature deltas and refuses an arbitrary global score.
"""
import argparse,json
from pathlib import Path

def flatten(d,p=''):
 out={}
 for k,v in d.items():
  q=f'{p}.{k}' if p else k
  if isinstance(v,dict):out.update(flatten(v,q))
  elif isinstance(v,(int,float)):out[q]=v
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('a');ap.add_argument('b');ap.add_argument('output');x=ap.parse_args()
 A=json.loads(Path(x.a).read_text());B=json.loads(Path(x.b).read_text());fa,fb=flatten(A),flatten(B)
 keys=sorted(set(fa)&set(fb));dims={}
 for k in keys:
  top=k.split('.')[0]
  dims.setdefault(top,[]).append({'feature':k,'a':fa[k],'b':fb[k],'delta':fb[k]-fa[k],'absolute_delta':abs(fb[k]-fa[k])})
 out={'schema':'TMT_FINGERPRINT_COMPARISON_v1.0','a':A.get('song_id'),'b':B.get('song_id'),'dimensions':dims,
      'global_similarity':None,'reason':'A corpus reference distribution is required before heterogeneous features can be standardized and combined.',
      'inference_status':'DESCRIPTIVE_DISTINCTION_ONLY'}
 Path(x.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
if __name__=='__main__':main()
