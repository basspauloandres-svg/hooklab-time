#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,math,zipfile
from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.stats import spearmanr,pearsonr,rankdata

def intish(x):
 try:return int(float(str(x).strip()))
 except:return None

def csv_rows(zpath):
 with zipfile.ZipFile(zpath) as z:
  for name in z.namelist():
   if '__MACOSX/' in name or not name.lower().endswith('.csv'):continue
   for row in csv.reader(z.read(name).decode('utf-8-sig','replace').splitlines()):
    if row and any(str(c).strip() for c in row):yield name,row

def metadata(path):
 out={}
 for name,row in csv_rows(path):
  idx=intish(row[0] if row else None)
  if idx is None or not (1<=idx<=331) or len(row)<9:continue
  y=intish(row[1]);pos=intish(row[2])
  if y and pos:out[idx]={'index':idx,'year':y,'chart_position':pos,'peak_strength':101-pos,'collaboration_type_gender':row[7].strip()}
 return out

def analysis(path):
 by=defaultdict(lambda:{'section_spans':[],'performer_sections':defaultdict(list)})
 for _,row in csv_rows(path):
  idx=intish(row[0] if row else None)
  if idx is None or not (1<=idx<=331) or len(row)<15:continue
  artist=row[3].strip() or 'UNKNOWN'
  try:lo=float(row[7]);hi=float(row[11])
  except:continue
  if lo<=0 or hi<=lo:continue
  span=12*math.log2(hi/lo)
  if not (0<span<=60):continue
  by[idx]['section_spans'].append(span);by[idx]['performer_sections'][artist].append(span)
 out={}
 for idx,r in by.items():
  spans=r['section_spans'];performer_medians=[float(np.median(v)) for v in r['performer_sections'].values() if v]
  if not spans:continue
  out[idx]={
   'median_section_vocal_span_st':float(np.median(spans)),
   'q75_section_vocal_span_st':float(np.quantile(spans,.75)),
   'max_section_vocal_span_st':float(max(spans)),
   'median_performer_section_span_st':float(np.median(performer_medians)) if performer_medians else None,
   'performer_count_with_pitch':len(performer_medians),
   'vocal_section_count_with_pitch':len(spans)
  }
 return out

def residual_partial(rows,feature):
 use=[r for r in rows if r.get(feature) is not None and r.get('collaboration_type_gender')]
 years=sorted(set(r['year'] for r in use));cats=sorted(set(r['collaboration_type_gender'] for r in use));X=[np.ones(len(use))]
 for y in years[1:]:X.append(np.array([1. if r['year']==y else 0. for r in use]))
 for c in cats[1:]:X.append(np.array([1. if r['collaboration_type_gender']==c else 0. for r in use]))
 X.append(np.array([float(r['performer_count_with_pitch']) for r in use]));X=np.column_stack(X)
 xf=rankdata([r[feature] for r in use]);yf=rankdata([r['peak_strength'] for r in use]);rx=xf-X@np.linalg.lstsq(X,xf,rcond=None)[0];ry=yf-X@np.linalg.lstsq(X,yf,rcond=None)[0];rho,p=pearsonr(rx,ry)
 return {'feature':feature,'n':len(use),'partial_spearman_rho':round(float(rho),4),'p':float(p),'controls':['year','collaboration_type_gender','performer_count_with_pitch']}

def bh(ps):
 m=len(ps);order=sorted(range(m),key=lambda i:ps[i]);q=[1.]*m;prev=1.
 for rank,i in reversed(list(enumerate(order,1))):prev=min(prev,ps[i]*m/rank);q[i]=prev
 return q

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();root=Path(a.repo);md=metadata(root/'Metadata.zip');an=analysis(root/'Analysis.zip');rows=[{**m,**an[i]} for i,m in md.items() if i in an]
 feats=['median_section_vocal_span_st','q75_section_vocal_span_st','max_section_vocal_span_st','median_performer_section_span_st'];tests=[]
 for f in feats:
  pairs=[(r[f],r['peak_strength']) for r in rows if r.get(f) is not None];rho,p=spearmanr([x for x,_ in pairs],[y for _,y in pairs]);tests.append({'feature':f,'n':len(pairs),'rho':round(float(rho),4),'p':float(p)})
 for t,q in zip(tests,bh([t['p'] for t in tests])):t['q_bh']=q;t['exploratory_supported']=bool(t['n']>=100 and abs(t['rho'])>=.15 and q<.05)
 controlled=[residual_partial(rows,f) for f in feats]
 out={'schema':'HOOKLAB_COSOD_VOCAL_VARIABILITY_ROBUSTNESS_v1.0','population_scope':'CoSoD Billboard Year-End collaborations 2010-2019','joined_rows':len(rows),'feature_definition':'Section vocal span = 12*log2(PitchMax/PitchMin), using provider section-level pitch extrema; song summaries are robust aggregations in semitones.','tests':tests,'controlled_tests':controlled,'decision':'REPLICATION_CANDIDATE' if any(t['exploratory_supported'] and next(c for c in controlled if c['feature']==t['feature'])['p']<.05 for t in tests) else 'DO_NOT_ADVANCE_POSITIVE_HYPOTHESIS','scientific_promotion':False,'boundary':'Association remains observational and collaboration-specific. Controls here include year, collaboration-type/gender and number of performers with pitch data; genre/style, exposure, artist history, key/register and production remain unmodeled.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'rows':len(rows),'decision':out['decision'],'tests':tests,'controlled':controlled}))
if __name__=='__main__':main()
