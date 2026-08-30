#!/usr/bin/env python3
"""Merge Sample 1 verified massive-hit batches into one deduplicated registry.

Only songs already carrying CROSS_PLATFORM_GATE_PASS status are merged. View counts
remain time-indexed provenance fields and are never converted into model weights.
"""
import argparse,json
from pathlib import Path

def load_songs(path):
 d=json.loads(Path(path).read_text())
 if 'dual_verified_seed' in d:
  return d['dual_verified_seed']
 return d.get('songs',[])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('inputs',nargs='+');ap.add_argument('--output',required=True);a=ap.parse_args()
 merged={};conflicts=[]
 for p in a.inputs:
  for s in load_songs(p):
   sid=s.get('song_id')
   status=s.get('sample_status','')
   if not sid or not status.startswith('CROSS_PLATFORM_GATE_PASS'):
    continue
   if sid in merged and merged[sid] != s:
    conflicts.append({'song_id':sid,'source':p})
    continue
   merged[sid]=s
 out={
  'schema':'SAMPLE1_VERIFIED_REGISTRY_v1.0',
  'n_verified':len(merged),
  'songs':list(merged.values()),
  'conflicts':conflicts,
  'policy':'VERIFIED_CROSS_PLATFORM_ONLY_NO_VIEW_WEIGHTING'
 }
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False))
 print(json.dumps({'n_verified':len(merged),'conflicts':len(conflicts)}))
 if conflicts: raise SystemExit(2)
if __name__=='__main__':main()
