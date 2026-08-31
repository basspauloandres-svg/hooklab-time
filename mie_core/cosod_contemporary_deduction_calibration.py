#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,zipfile,tempfile,re
from pathlib import Path
from scipy.stats import spearmanr

def intish(x):
 try:return int(float(str(x).strip()))
 except:return None

def rows_from_zip(zpath):
 out=[]
 with zipfile.ZipFile(zpath) as z:
  for name in z.namelist():
   if not name.lower().endswith('.csv'): continue
   text=z.read(name).decode('utf-8-sig','replace').splitlines()
   for row in csv.reader(text):
    if row and any(str(c).strip() for c in row): out.append((name,row))
 return out

def metadata(meta_zip):
 out={}
 for name,row in rows_from_zip(meta_zip):
  idx=intish(row[0] if row else None)
  if idx is None or idx<1 or idx>331: continue
  # documented positional contract: index, year, chart position, title, artists, ...
  if len(row)>=5 and intish(row[1]) and intish(row[2]):
   out[idx]={'index':idx,'year':intish(row[1]),'chart_position':intish(row[2]),'title':row[3].strip(),'artist':row[4].strip(),'source_file':name}
 return out

def analysis(analysis_zip):
 by={}
 for name,row in rows_from_zip(analysis_zip):
  idx=intish(row[0] if row else None)
  if idx is None or idx<1 or idx>331 or len(row)<3: continue
  try:t=float(row[1])
  except:continue
  sec=str(row[2]).strip().lower()
  rec=by.setdefault(idx,{'times':[],'chorus':[],'verse':[],'pitch_values':[],'analysis_files':set()});rec['times'].append(t);rec['analysis_files'].add(name)
  if 'chorus' in sec or 'refrain' in sec or sec=='hook': rec['chorus'].append(t)
  if 'verse' in sec: rec['verse'].append(t)
  # README documents pitch fields after vocal-delivery columns in section rows; collect plausible positive Hz cells.
  for c in row[6:]:
   try:v=float(c)
   except:continue
   if 40<=v<=2500: rec['pitch_values'].append(v)
 out={}
 for idx,r in by.items():
  duration=max(r['times']) if r['times'] else None; fc=min(r['chorus']) if r['chorus'] else None
  out[idx]={'section_events':len(r['times']),'duration_proxy_s':duration,'first_chorus_s':fc,'first_chorus_ratio':(fc/duration if fc is not None and duration and duration>0 else None),'pitch_span_hz':(max(r['pitch_values'])-min(r['pitch_values']) if len(r['pitch_values'])>=2 else None),'analysis_file_count':len(r['analysis_files'])}
 return out

def bh(ps):
 m=len(ps);order=sorted(range(m),key=lambda i:ps[i]);q=[1.]*m;prev=1.
 for rank,i in reversed(list(enumerate(order,1))):prev=min(prev,ps[i]*m/rank);q[i]=prev
 return q

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();root=Path(a.repo)
 md=metadata(root/'Metadata.zip');an=analysis(root/'Analysis.zip');joined=[]
 for idx,m in md.items():
  if idx in an: joined.append({**m,**an[idx],'peak_strength':101-m['chart_position']})
 feats=['first_chorus_s','first_chorus_ratio','section_events','duration_proxy_s','pitch_span_hz'];tests=[]
 for feat in feats:
  pairs=[(r.get(feat),r['peak_strength']) for r in joined if r.get(feat) is not None]
  if len(pairs)<30:continue
  rho,p=spearmanr([x for x,_ in pairs],[y for _,y in pairs]);tests.append({'feature':feat,'outcome':'year_end_peak_strength','n':len(pairs),'rho':round(float(rho),4),'p':float(p)})
 qs=bh([x['p'] for x in tests]) if tests else []
 for x,q in zip(tests,qs):x['q_bh']=q;x['exploratory_supported']=bool(x['n']>=100 and abs(x['rho'])>=.15 and q<.05)
 out={'schema':'HOOKLAB_COSOD_CONTEMPORARY_DEDUCTION_CALIBRATION_v1.0','provider':'CoSoD / CC0','population_scope':'multi-artist Billboard Hot 100 Year-End collaborations, 2010-2019','documented_song_count':331,'metadata_rows_resolved':len(md),'analysis_rows_resolved':len(an),'joined_eligible_rows':len(joined),'tests':tests,'supported_exploratory_associations':[x for x in tests if x['exploratory_supported']],'scientific_promotion':False,'boundary':'Contemporary calibration subpopulation only. Year-end chart position is an observed outcome, not a pure measure of musical quality; exposure, artist history, genre/style and other confounds remain separate.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'metadata':len(md),'analysis':len(an),'joined':len(joined),'supported':len(out['supported_exploratory_associations'])}))
if __name__=='__main__':main()
