#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,zipfile
from collections import Counter
from pathlib import Path

def inspect_zip(path,limit=8):
 samples=[];lens=Counter();files=0;rows=0
 with zipfile.ZipFile(path) as z:
  for name in z.namelist():
   if not name.lower().endswith('.csv'): continue
   files+=1
   text=z.read(name).decode('utf-8-sig','replace').splitlines()
   for row in csv.reader(text):
    if not row or not any(str(c).strip() for c in row): continue
    rows+=1;lens[len(row)]+=1
    if len(samples)<limit:samples.append({'file':name,'len':len(row),'row':row})
 return {'csv_files':files,'nonempty_rows':rows,'row_length_counts':dict(lens),'samples':samples}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();root=Path(a.repo)
 out={'schema':'HOOKLAB_COSOD_SCHEMA_AUDIT_v1.0','metadata':inspect_zip(root/'Metadata.zip'),'analysis':inspect_zip(root/'Analysis.zip')}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'metadata_files':out['metadata']['csv_files'],'analysis_files':out['analysis']['csv_files'],'analysis_lengths':out['analysis']['row_length_counts']}))
if __name__=='__main__':main()
