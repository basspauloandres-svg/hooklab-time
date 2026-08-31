#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,zipfile
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr,pearsonr,rankdata

def intish(x):
 try:return int(float(str(x).strip()))
 except:return None

def rows_from_zip(zpath):
 out=[]
 with zipfile.ZipFile(zpath) as z:
  for name in z.namelist():
   if '__MACOSX/' in name or not name.lower().endswith('.csv'): continue
   text=z.read(name).decode('utf-8-sig','replace').splitlines()
   for row in csv.reader(text):
    if row and any(str(c).strip() for c in row): out.append((name,row))
 return out

def metadata(meta_zip):
 out={}
 for name,row in rows_from_zip(meta_zip):
  idx=intish(row[0] if row else None)
  if idx is None or idx<1 or idx>331 or len(row)<9: continue
  if intish(row[1]) and intish(row[2]):
   out[idx]={'index':idx,'year':intish(row[1]),'chart_position':intish(row[2]),'title':row[3].strip(),'artist':row[4].strip(),'collaboration_type':row[5].strip(),'artist_gender':row[6].strip(),'collaboration_type_gender':row[7].strip(),'musicbrainz_url':row[8].strip(),'source_file':name}
 return out

def analysis(analysis_zip):
 by={}
 for name,row in rows_from_zip(analysis_zip):
  idx=intish(row[0] if row else None)
  if idx is None or idx<1 or idx>331 or len(row)<15: continue
  try:t=float(row[1])
  except:continue
  sec=str(row[2]).strip().lower();rec=by.setdefault(idx,{'times':[],'chorus':[],'pitch_values':[],'analysis_files':set()});rec['times'].append(t);rec['analysis_files'].add(name)
  if 'chorus' in sec or 'refrain' in sec or sec=='hook': rec['chorus'].append(t)
  # Provider schema explicitly places Pitch min..Pitch max at columns 7..11.
  for c in row[7:12]:
   try:v=float(c)
   except:continue
   if 40<=v<=2500: rec['pitch_values'].append(v)
 out={}
 for idx,r in by.items():
  last_section_start=max(r['times']) if r['times'] else None;fc=min(r['chorus']) if r['chorus'] else None
  out[idx]={'section_events':len(r['times']),'last_section_start_s':last_section_start,'first_chorus_s':fc,'first_chorus_annotated_timeline_ratio':(fc/last_section_start if fc is not None and last_section_start and last_section_start>0 else None),'aggregate_vocal_pitch_span_hz':(max(r['pitch_values'])-min(r['pitch_values']) if len(r['pitch_values'])>=2 else None),'analysis_file_count':len(r['analysis_files'])}
 return out

def bh(ps):
 m=len(ps);order=sorted(range(m),key=lambda i:ps[i]);q=[1.]*m;prev=1.
 for rank,i in reversed(list(enumerate(order,1))):prev=min(prev,ps[i]*m/rank);q[i]=prev
 return q

def design_controls(rows):
 years=sorted(set(r['year'] for r in rows));cats=sorted(set(r['collaboration_type_gender'] for r in rows));cols=[np.ones(len(rows))]
 for y in years[1:]:cols.append(np.array([1. if r['year']==y else 0. for r in rows]))
 for c in cats[1:]:cols.append(np.array([1. if r['collaboration_type_gender']==c else 0. for r in rows]))
 return np.column_stack(cols),{'year_levels':years,'collaboration_type_gender_levels':cats}

def partial_spearman(rows,feature,outcome='peak_strength'):
 use=[r for r in rows if r.get(feature) is not None and r.get(outcome) is not None and r.get('collaboration_type_gender')]
 if len(use)<30:return None
 X,levels=design_controls(use);xf=rankdata([r[feature] for r in use]);yf=rankdata([r[outcome] for r in use]);bx=np.linalg.lstsq(X,xf,rcond=None)[0];by=np.linalg.lstsq(X,yf,rcond=None)[0];rx=xf-X@bx;ry=yf-X@by;rho,p=pearsonr(rx,ry)
 return {'feature':feature,'outcome':outcome,'n':len(use),'partial_spearman_rho':round(float(rho),4),'p':float(p),'controls':['year','collaboration_type_gender'],'control_levels':levels}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();root=Path(a.repo)
 md=metadata(root/'Metadata.zip');an=analysis(root/'Analysis.zip');joined=[]
 for idx,m in md.items():
  if idx in an: joined.append({**m,**an[idx],'peak_strength':101-m['chart_position']})
 feats=['first_chorus_s','first_chorus_annotated_timeline_ratio','section_events','last_section_start_s','aggregate_vocal_pitch_span_hz'];tests=[]
 for feat in feats:
  pairs=[(r.get(feat),r['peak_strength']) for r in joined if r.get(feat) is not None]
  if len(pairs)<30:continue
  rho,p=spearmanr([x for x,_ in pairs],[y for _,y in pairs]);tests.append({'feature':feat,'outcome':'year_end_peak_strength','n':len(pairs),'rho':round(float(rho),4),'p':float(p)})
 qs=bh([x['p'] for x in tests]) if tests else []
 for x,q in zip(tests,qs):x['q_bh']=q;x['exploratory_supported']=bool(x['n']>=100 and abs(x['rho'])>=.15 and q<.05)
 controlled=[partial_spearman(joined,'first_chorus_s'),partial_spearman(joined,'aggregate_vocal_pitch_span_hz')];controlled=[x for x in controlled if x]
 out={'schema':'HOOKLAB_COSOD_CONTEMPORARY_DEDUCTION_CALIBRATION_v1.1','provider':'CoSoD / CC0','population_scope':'multi-artist Billboard Hot 100 Year-End collaborations, 2010-2019','documented_song_count':331,'metadata_rows_resolved':len(md),'analysis_rows_resolved':len(an),'joined_eligible_rows':len(joined),'feature_semantics':{'first_chorus_s':'absolute onset of first chorus/refrain/hook annotation','first_chorus_annotated_timeline_ratio':'first chorus onset divided by last annotated section start; NOT song-duration proportion','aggregate_vocal_pitch_span_hz':'max minus min across provider-reported vocal pitch statistics over all analyzed sections/performers; NOT single-melody range'},'tests':tests,'controlled_tests':controlled,'supported_exploratory_associations':[x for x in tests if x['exploratory_supported']],'scientific_promotion':False,'boundary':'Contemporary collaboration subpopulation only. Year-end chart position is an observed outcome, not musical quality. Controlled tests address year and collaboration-type/gender only; genre/style, exposure, artist history and other confounds remain.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'metadata':len(md),'analysis':len(an),'joined':len(joined),'supported':len(out['supported_exploratory_associations']),'controlled':controlled}))
if __name__=='__main__':main()
