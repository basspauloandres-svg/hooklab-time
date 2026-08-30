#!/usr/bin/env python3
"""Discover alternate Lakh MIDI representations for target recordings.

Purpose: create an independent-arrangement consensus lane for validating the selected
vocal-melody proxy. This is stronger than a single-file heuristic but is still symbolic
cross-representation evidence, not audio-reference ground truth.
"""
import argparse,json,re,urllib.request
from difflib import SequenceMatcher
from pathlib import Path

DEFAULT_INDEX='https://colinraffel.com/projects/lmd/md5_to_paths.json'

def norm(s):
 s=str(s or '').lower();s=re.sub(r'\.(mid|midi|kar)$','',s);return re.sub(r'[^a-z0-9]+',' ',s).strip()
def sim(a,b):return SequenceMatcher(None,norm(a),norm(b)).ratio()
def text(paths):
 if isinstance(paths,str):paths=[paths]
 return ' '.join(str(p).replace('/',' ') for p in (paths or []))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--registry',required=True);ap.add_argument('--output',required=True);ap.add_argument('--index-url',default=DEFAULT_INDEX);ap.add_argument('--top-k',type=int,default=3);ap.add_argument('--min-score',type=float,default=.72);a=ap.parse_args()
 reg=json.loads(Path(a.registry).read_text());songs=reg['songs']
 req=urllib.request.Request(a.index_url,headers={'User-Agent':'HookLabPrototype/1.4'})
 with urllib.request.urlopen(req,timeout=120) as r:idx=json.load(r)
 groups=[];flat=[]
 for s in songs:
  target=f"{s['artist']} {s['title']}";hits=[]
  for md5,paths in idx.items():
   if md5.lower()==s['md5'].lower():continue
   tx=text(paths);score=sim(target,tx);ts=sim(s['title'],tx);ars=sim(s['artist'],tx)
   if score>=a.min_score and ts>=.55 and ars>=.35:
    hits.append((score,ts,ars,md5,paths))
  hits.sort(reverse=True,key=lambda x:(x[0],x[1],x[2]))
  out=[]
  for rank,(score,ts,ars,md5,paths) in enumerate(hits[:a.top_k],1):
   x={'title':s['title'],'artist':s['artist'],'year':s.get('year'),'expected_duration_seconds':s.get('expected_duration_seconds'),'primary_md5':s['md5'],'md5':md5,'rank':rank,'metadata_score':round(score,4),'title_score':round(ts,4),'artist_score':round(ars,4),'paths':paths,'evidence_role':'ALTERNATE_SYMBOLIC_REPRESENTATION_PENDING_AUDIT'}
   out.append(x);flat.append(x)
  groups.append({'title':s['title'],'artist':s['artist'],'primary_md5':s['md5'],'alternate_n':len(out),'alternates':out})
 payload={'schema':'HOOKLAB_ALTERNATE_SYMBOLIC_REPRESENTATION_DISCOVERY_v1.0','source_index':a.index_url,'groups':groups,'high_priority_identity_audit':flat,'automatic_promotion':False,'semantics':'Alternate symbolic arrangements are used for cross-representation melodic consensus. They do not independently prove audio-ground-truth vocal melody.'}
 Path(a.output).write_text(json.dumps(payload,indent=2,ensure_ascii=False));print(json.dumps({'songs':len(groups),'alternate_files':len(flat),'songs_with_alternates':sum(bool(g['alternates']) for g in groups)}))
if __name__=='__main__':main()
