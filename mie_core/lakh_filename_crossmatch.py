#!/usr/bin/env python3
"""Crossmatch target songs against Lakh MIDI filename metadata without downloading audio.

The Lakh filename index maps MIDI MD5s to original source paths. This resolver performs
metadata-only fuzzy matching first. It does not download MIDI files and it never promotes
a match automatically to HookLab evidence; matched candidates must later pass an identity
and coverage audit on the specific symbolic file.
"""
import argparse,json,re,urllib.request
from pathlib import Path
from difflib import SequenceMatcher

DEFAULT_INDEX='https://colinraffel.com/projects/lmd/md5_to_paths.json'

def norm(s):
 s=str(s or '').lower()
 s=re.sub(r'\.(mid|midi|kar)$','',s)
 s=re.sub(r'\b(feat|ft|featuring|official|video|audio|lyrics|lyric)\b.*',' ',s)
 return re.sub(r'[^a-z0-9]+',' ',s).strip()

def sim(a,b): return SequenceMatcher(None,norm(a),norm(b)).ratio()

def candidate_text(paths):
 if isinstance(paths,str): paths=[paths]
 return ' '.join(str(p).replace('/',' ') for p in (paths or []))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidates',required=True);ap.add_argument('--output',required=True)
 ap.add_argument('--index-url',default=DEFAULT_INDEX);ap.add_argument('--min-score',type=float,default=.74);ap.add_argument('--top-k',type=int,default=5);a=ap.parse_args()
 cand=json.loads(Path(a.candidates).read_text())
 if isinstance(cand,dict): cand=cand.get('priority',cand.get('candidates',cand.get('songs',[])))
 req=urllib.request.Request(a.index_url,headers={'User-Agent':'HookLabPrototype/1.0'})
 with urllib.request.urlopen(req,timeout=120) as r: idx=json.load(r)
 results=[]
 for c in cand:
  title=c.get('title',c.get('track',''));artist=c.get('artist','')
  target=f'{artist} {title}'
  scored=[]
  for md5,paths in idx.items():
   text=candidate_text(paths)
   s=sim(target,text)
   # Require title evidence in addition to global fuzzy score to reduce artist-only collisions.
   ts=sim(title,text)
   if s>=a.min_score and ts>=.55: scored.append((s,ts,md5,paths))
  scored.sort(reverse=True,key=lambda x:(x[0],x[1]))
  hits=[{'score':round(s,4),'title_score':round(ts,4),'md5':m,'paths':p} for s,ts,m,p in scored[:a.top_k]]
  results.append({'candidate':c,'status':'CANDIDATE_MATCH_REQUIRES_IDENTITY_AUDIT' if hits else 'NO_METADATA_MATCH','hits':hits})
 out={'schema':'HOOKLAB_LAKH_FILENAME_CROSSMATCH_v1.0','source_index':a.index_url,
      'source_role':'FULL_SONG_SYMBOLIC_DISCOVERY_METADATA_ONLY','automatic_promotion':False,'results':results,
      'method_note':'Filename metadata can be inaccurate; a MIDI candidate must pass title/artist identity plus structural plausibility before use as evidence.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':'LAKH_CROSSMATCH_COMPLETE','songs':len(results),'with_hits':sum(bool(x['hits']) for x in results)}))
if __name__=='__main__':main()
