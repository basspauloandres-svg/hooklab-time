#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re,unicodedata,zipfile,math
from pathlib import Path
from collections import defaultdict
from scipy.stats import spearmanr

def norm(s):
 s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower();s=re.sub(r'\([^)]*\)|\[[^]]*\]',' ',s);return ' '.join(re.sub(r'[^a-z0-9]+',' ',s).split())
def toks(s):return {x for x in norm(s).split() if x not in {'the','and','with','feat','featuring','ft','x'}}
def ov(a,b):
 A=toks(a);B=toks(b);return len(A&B)/max(1,min(len(A),len(B)))
def csvrows(path):
 with zipfile.ZipFile(path) as z:
  for name in z.namelist():
   if '__MACOSX/' in name or not name.lower().endswith('.csv'):continue
   for row in csv.reader(z.read(name).decode('utf-8-sig','replace').splitlines()):
    if row and any(str(c).strip() for c in row):yield row

def md(path):
 out={}
 for r in csvrows(path):
  if len(r)!=9:continue
  try:i=int(r[0]);y=int(r[1]);pos=int(r[2])
  except:continue
  out[i]={'cosod_index':i,'year':y,'cosod_year_end_position':pos,'title':r[3].strip(),'artist':r[4].strip(),'collaboration_type_gender':r[7].strip(),'musicbrainz_url':r[8].strip()}
 return out

def an(path):
 d=defaultdict(lambda:{'times':[],'chorus':[],'section_spans_st':[]})
 for r in csvrows(path):
  if len(r)!=15:continue
  try:i=int(r[0]);t=float(r[1])
  except:continue
  sec=r[2].strip().lower();d[i]['times'].append(t)
  if 'chorus' in sec or 'refrain' in sec or sec=='hook':d[i]['chorus'].append(t)
  try:lo=float(r[7]);hi=float(r[11])
  except:continue
  if lo>0 and hi>lo:
   st=12*math.log2(hi/lo)
   if 0<st<=60:d[i]['section_spans_st'].append(st)
 out={}
 import statistics
 for i,x in d.items():
  out[i]={'first_chorus_s':min(x['chorus']) if x['chorus'] else None,'section_events':len(x['times']),'median_section_vocal_span_st':statistics.median(x['section_spans_st']) if x['section_spans_st'] else None}
 return out

def bh(ps):
 m=len(ps);o=sorted(range(m),key=lambda i:ps[i]);q=[1.]*m;p=1.
 for rank,i in reversed(list(enumerate(o,1))):p=min(p,ps[i]*m/rank);q[i]=p
 return q

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--m300',required=True);ap.add_argument('--cosod-metadata',required=True);ap.add_argument('--cosod-analysis',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();m=json.loads(Path(a.m300).read_text());M=md(a.cosod_metadata);A=an(a.cosod_analysis);by={}
 for i,r in M.items():by.setdefault((r['year'],norm(r['title'])),[]).append(r)
 rows=[];aud=[]
 for c in m['candidates']:
  h=sorted([(ov(c['artist'],x['artist']),x) for x in by.get((int(c['chart_year']),norm(c['title'])),[])],reverse=True,key=lambda z:z[0])
  if h and h[0][0]>=.5 and h[0][1]['cosod_index'] in A:
   s,r=h[0];rows.append({**c,**r,**A[r['cosod_index']],'artist_overlap':s,'m300_rank_strength':16-int(c['rank']),'log10_spotify_playcount':math.log10(max(1,int(c.get('spotify_playcount_observed') or 0)))})
  elif h:aud.append({'candidate_id':c['candidate_id'],'title':c['title'],'artist':c['artist'],'reason':'IDENTITY_AUDIT'})
 feats=['first_chorus_s','section_events','median_section_vocal_span_st'];outs=['m300_rank_strength','log10_spotify_playcount'];tests=[]
 for f in feats:
  for o in outs:
   pairs=[(r[f],r[o]) for r in rows if r.get(f) is not None and r.get(o) is not None]
   if len(pairs)<30:continue
   rho,p=spearmanr([x for x,_ in pairs],[y for _,y in pairs]);tests.append({'feature':f,'outcome':o,'n':len(pairs),'rho':round(float(rho),4),'p':float(p)})
 qs=bh([x['p'] for x in tests])
 for x,q in zip(tests,qs):x['q_bh']=q;x['supported_for_interpretation']=bool(x['n']>=30 and abs(x['rho'])>=.2 and q<.05)
 out={'schema':'HOOKLAB_M300_COSOD_TARGET_SUBCOHORT_ANALYSIS_v1.0','population_scope':'Exact M300 intersections with licensed CoSoD collaboration annotations, chart years 2010-2019','eligible_rows':len(rows),'audit_rows':len(aud),'tests':tests,'supported_for_interpretation':[x for x in tests if x['supported_for_interpretation']],'decision':'TARGET_SUBCOHORT_ASSOCIATION_AVAILABLE' if any(x['supported_for_interpretation'] for x in tests) else 'NO_TARGET_SUBCOHORT_ASSOCIATION_PASSED_GATE','scientific_promotion':False,'boundary':'This is a top-15 Year-End collaboration subcohort embedded in M300. It cannot represent all 300 songs, all genres/styles, or causal success mechanisms. Spotify playcount is a current cumulative outcome snapshot and M300 rank strength is within-year top-15 ordering.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'eligible_rows':len(rows),'audit_rows':len(aud),'decision':out['decision'],'supported':out['supported_for_interpretation']}))
if __name__=='__main__':main()
