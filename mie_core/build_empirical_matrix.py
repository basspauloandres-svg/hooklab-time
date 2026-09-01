#!/usr/bin/env python3
"""Build matrix X from strict-pass Analyzer fingerprints.
No feature weighting, ranking, imputation or success interpretation is performed.
"""
import argparse,csv,json
from pathlib import Path

def flatten(prefix,x,out):
 if isinstance(x,dict):
  for k,v in x.items(): flatten(f'{prefix}.{k}' if prefix else k,v,out)
 elif isinstance(x,(int,float)) and not isinstance(x,bool): out[prefix]=x

def main():
 ap=argparse.ArgumentParser();ap.add_argument('inputs',nargs='+');ap.add_argument('--csv',required=True);ap.add_argument('--manifest',required=True);a=ap.parse_args()
 rows=[];features=set()
 for p in a.inputs:
  d=json.loads(Path(p).read_text());status=d.get('strict_gate_status') or d.get('status')
  if status not in {'STRICT_REPLAY_PASS','FULL_TMT_READY'}: continue
  fp=d.get('fingerprint',d); flat={};flatten('',fp,flat)
  sid=fp.get('song_id') or d.get('song_id') or Path(p).stem
  row={'song_id':sid,**flat};rows.append(row);features.update(flat)
 cols=['song_id']+sorted(features)
 with open(a.csv,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
 manifest={'schema':'EMPIRICAL_MATRIX_X_v1.0','n_songs':len(rows),'n_numeric_features':len(features),'columns':cols,
           'policy':'DESCRIPTIVE_DATA_FIRST_NO_WEIGHTS_NO_IMPUTATION','Y_status':'NOT_ATTACHED'}
 Path(a.manifest).write_text(json.dumps(manifest,indent=2,ensure_ascii=False));print(json.dumps(manifest))
if __name__=='__main__':main()
