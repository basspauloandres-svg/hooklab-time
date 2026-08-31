#!/usr/bin/env python3
"""Observed dual-platform qualification for the frozen 300-song discovery frame."""
from __future__ import annotations
import argparse,csv,json,re,unicodedata
from difflib import SequenceMatcher
from pathlib import Path
THRESHOLD=100_000_000

def norm(s):
 s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower();s=re.sub(r'\([^)]*\)|\[[^]]*\]',' ',s);s=re.sub(r'feat\.?|featuring|ft\.?',' ',s);return ' '.join(re.sub(r'[^a-z0-9]+',' ',s).split())
def artist_overlap(a,b):
 A=set(norm(a).split());B=set(norm(b).split());return len(A&B)/max(1,min(len(A),len(B)))
def qualify(frame, yt_rows):
 idx={}
 for r in yt_rows:
  key=norm(r.get('Track'))
  if key: idx.setdefault(key,[]).append(r)
 out=[]
 for x in frame['candidates']:
  cand=[];k=norm(x['title'])
  for kk,rows in idx.items():
   ts=SequenceMatcher(None,k,kk).ratio()
   if ts>=.88:
    for r in rows:
     ao=artist_overlap(x['artist'],r.get('Artist'))
     if ao>=.5: cand.append((ts,ao,r))
  cand.sort(key=lambda z:(z[0],z[1],float(z[2].get('Views') or 0)),reverse=True);best=cand[0] if cand else None
  spotify=(x.get('spotify_playcount_observed') or 0)>=THRESHOLD
  if best:
   r=best[2]
   try: views=float(r.get('Views') or 0)
   except: views=0
   youtube=views>=THRESHOLD;identity='PASS' if best[0]>=.94 and best[1]>=.5 else 'AUDIT';dual='PASS' if spotify and youtube and identity=='PASS' else ('FAIL' if (not spotify or not youtube) and identity=='PASS' else 'AUDIT')
   out.append({**x,'youtube_views_observed':int(views),'youtube_match_title':r.get('Track'),'youtube_match_artist':r.get('Artist'),'youtube_title_similarity':round(best[0],4),'youtube_artist_overlap':round(best[1],4),'identity':identity,'spotify_success':'PASS' if spotify else 'FAIL','youtube_success':'PASS' if youtube else 'FAIL','mass_success_dual_platform':dual})
  else: out.append({**x,'youtube_views_observed':None,'identity':'AUDIT','spotify_success':'PASS' if spotify else 'FAIL','youtube_success':'AUDIT','mass_success_dual_platform':'AUDIT'})
 from collections import Counter
 return {'schema':'HOOKLAB_MILESTONE_300_DUAL_PLATFORM_v1.0','threshold_each_platform':THRESHOLD,'candidate_count':len(out),'mass_success_counts':dict(Counter(x['mass_success_dual_platform'] for x in out)),'identity_counts':dict(Counter(x['identity'] for x in out)),'rows':out,'boundary':'AUDIT is not FAIL; this snapshot supports mass-success qualification only and does not establish genre/style or symbolic eligibility.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--frame',required=True);ap.add_argument('--youtube-csv',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();frame=json.load(open(a.frame));
 with open(a.youtube_csv,encoding='utf-8-sig',errors='replace',newline='') as f: yt=list(csv.DictReader(f))
 out=qualify(frame,yt);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out['mass_success_counts']))
if __name__=='__main__':main()
