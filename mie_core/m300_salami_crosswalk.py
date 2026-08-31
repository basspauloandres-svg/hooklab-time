#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re,unicodedata
from pathlib import Path

def norm(s):
 s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower();return ' '.join(re.sub(r'[^a-z0-9]+',' ',s).split())
def toks(s):return {x for x in norm(s).split() if x not in {'the','and','with','feat','featuring','ft','x'}}
def overlap(a,b):
 A=toks(a);B=toks(b);return len(A&B)/max(1,min(len(A),len(B)))
def salami_rows(repo):
 p=Path(repo)/'metadata'/'metadata.csv';out=[]
 with p.open(encoding='utf-8-sig',errors='replace') as f:
  for r in csv.DictReader(f):
   sid=str(r.get('SONG_ID') or '').strip();title=r.get('SONG_TITLE') or '';artist=r.get('ARTIST') or ''
   if not sid or not title:continue
   discarded=str(r.get('SONG_WAS_DISCARDED_FLAG') or '').strip().upper() in {'TRUE','1','YES'}
   ann=Path(repo)/'annotations'/sid
   has_annotation=ann.exists() and any(ann.glob('textfile*.txt'))
   out.append({'salami_id':sid,'title':title,'artist':artist,'duration_s':r.get('SONG_DURATION'),'class':r.get('CLASS'),'genre':r.get('GENRE'),'discarded':discarded,'annotation_available':has_annotation})
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--m300',required=True);ap.add_argument('--salami-repo',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 m=json.loads(Path(a.m300).read_text());S=salami_rows(a.salami_repo);by={}
 for r in S:by.setdefault(norm(r['title']),[]).append(r)
 matches=[];audits=[];unavailable=[]
 for c in m['candidates']:
  hits=by.get(norm(c['title']),[]);scored=sorted([(overlap(c['artist'],h['artist']),h) for h in hits],key=lambda z:z[0],reverse=True)
  strong=[(s,h) for s,h in scored if s>=.5 and h['annotation_available'] and not h['discarded']]
  if len(strong)==1:
   s,h=strong[0];matches.append({'candidate_id':c['candidate_id'],'chart_year':c['chart_year'],'m300_rank':c['rank'],'title':c['title'],'artist':c['artist'],'salami_id':h['salami_id'],'salami_title':h['title'],'salami_artist':h['artist'],'artist_overlap':round(s,3),'duration_s':h['duration_s'],'class':h['class'],'genre':h['genre'],'license':'CC0 annotations/metadata','evidence_status':'LICENSED_STRUCTURAL_ANNOTATION_AVAILABLE','scientific_promotion':False})
  elif strong:
   audits.append({'candidate_id':c['candidate_id'],'title':c['title'],'artist':c['artist'],'reason':'MULTIPLE_STRONG_SALAMI_IDENTITIES','candidates':[h['salami_id'] for _,h in strong]})
  elif hits:
   audits.append({'candidate_id':c['candidate_id'],'title':c['title'],'artist':c['artist'],'reason':'TITLE_MATCH_IDENTITY_OR_ANNOTATION_AUDIT','candidates':[{'salami_id':h['salami_id'],'artist':h['artist'],'overlap':round(s,3),'annotation_available':h['annotation_available'],'discarded':h['discarded']} for s,h in scored]})
  else:unavailable.append({'candidate_id':c['candidate_id'],'status':'REFERENCE_UNAVAILABLE'})
 out={'schema':'HOOKLAB_M300_SALAMI_CROSSWALK_v1.0','provider':'SALAMI structural annotations','license':'CC0','m300_count':len(m['candidates']),'salami_metadata_rows':len(S),'match_count':len(matches),'audit_count':len(audits),'reference_unavailable_count':len(unavailable),'coverage_rate':len(matches)/max(1,len(m['candidates'])),'matches':matches,'audits':audits,'unavailable':unavailable,'invariants':['annotation availability != audio authorization','SALAMI YouTube pairing routes are excluded from Gate A','licensed structural annotation availability != scientific promotion','identity ambiguity remains AUDIT and is never auto-promoted']}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'matches':len(matches),'audits':len(audits),'unavailable':len(unavailable),'coverage_rate':out['coverage_rate']}))
if __name__=='__main__':main()
