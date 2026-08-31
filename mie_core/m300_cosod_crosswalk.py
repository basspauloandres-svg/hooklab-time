#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re,unicodedata,zipfile
from pathlib import Path

def norm(s):
 s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower();s=re.sub(r'\([^)]*\)|\[[^]]*\]',' ',s);return ' '.join(re.sub(r'[^a-z0-9]+',' ',s).split())
def artist_tokens(s):
 stop={'the','and','with','feat','featuring','ft','x'};return {x for x in norm(s).split() if x not in stop}
def overlap(a,b):
 A=artist_tokens(a);B=artist_tokens(b);return len(A&B)/max(1,min(len(A),len(B)))
def metadata(zpath):
 out=[]
 with zipfile.ZipFile(zpath) as z:
  for name in z.namelist():
   if '__MACOSX/' in name or not name.lower().endswith('.csv'):continue
   for row in csv.reader(z.read(name).decode('utf-8-sig','replace').splitlines()):
    if len(row)!=9:continue
    try:idx=int(row[0]);year=int(row[1]);pos=int(row[2])
    except:continue
    out.append({'cosod_index':idx,'year':year,'year_end_position':pos,'title':row[3].strip(),'artist':row[4].strip(),'musicbrainz_url':row[8].strip()})
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--m300',required=True);ap.add_argument('--cosod-metadata',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();m=json.loads(Path(a.m300).read_text());cm=metadata(a.cosod_metadata);idx={}
 for r in cm:idx.setdefault((r['year'],norm(r['title'])),[]).append(r)
 matches=[];audits=[]
 for x in m['candidates']:
  hits=idx.get((int(x['chart_year']),norm(x['title'])),[])
  scored=sorted([(overlap(x['artist'],h['artist']),h) for h in hits],key=lambda z:z[0],reverse=True)
  if scored and scored[0][0]>=.5:
   s,h=scored[0];matches.append({'candidate_id':x['candidate_id'],'chart_year':x['chart_year'],'m300_rank':x['rank'],'title':x['title'],'artist':x['artist'],'cosod_index':h['cosod_index'],'cosod_year_end_position':h['year_end_position'],'cosod_artist':h['artist'],'artist_overlap':round(s,3),'musicbrainz_url':h['musicbrainz_url'],'evidence_status':'LICENSED_MUSICAL_EVIDENCE_AVAILABLE','scientific_promotion':False})
  elif hits:audits.append({'candidate_id':x['candidate_id'],'title':x['title'],'artist':x['artist'],'reason':'TITLE_YEAR_MATCH_ARTIST_AUDIT','candidates':hits})
 out={'schema':'HOOKLAB_M300_COSOD_CROSSWALK_v1.0','m300_count':len(m['candidates']),'cosod_documented_count':331,'match_count':len(matches),'coverage_rate':len(matches)/max(1,len(m['candidates'])),'matches':matches,'audits':audits,'invariant':'Licensed evidence availability != scientific promotion. CoSoD coverage is collaboration-specific and supplies structural/vocal evidence only for exact resolved intersections.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'matches':len(matches),'audits':len(audits),'coverage_rate':out['coverage_rate']}))
if __name__=='__main__':main()
