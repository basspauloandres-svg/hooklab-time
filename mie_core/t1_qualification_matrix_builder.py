#!/usr/bin/env python3
"""Build the T1 Dance-Pop qualification matrix across mandatory scientific gates.

This layer is fail-closed. Discovery metadata never counts as qualification evidence.
Each gate must be explicitly PASS before a row can become QUALIFIED_FOR_MATRIX_X.
AUDIT, FAIL and PENDING remain distinct and are preserved in provenance.
"""
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path

GATES=[
 'mass_success','identity','genre_style','version','symbolic_source',
 'full_song','provenance','full_tmt'
]
ALLOWED={'PASS','AUDIT','FAIL','PENDING'}

def norm(s): return re.sub(r'[^a-z0-9]+',' ',str(s or '').lower()).strip()
def key(title,artist): return norm(title)+'::'+norm(artist)

def classify(gates):
 vals=[gates[g]['status'] for g in GATES]
 if 'FAIL' in vals: return 'REJECTED'
 if all(v=='PASS' for v in vals): return 'QUALIFIED_FOR_MATRIX_X'
 if 'AUDIT' in vals: return 'AUDIT'
 return 'PENDING'

def build(queue,evidence):
 evidence_map={key(x.get('title'),x.get('artist')):x for x in evidence.get('records',[])}
 rows=[]
 for c in queue.get('candidates',[]):
  ev=evidence_map.get(key(c.get('title'),c.get('artist')),{})
  gates={}
  for g in GATES:
   ge=(ev.get('gates') or {}).get(g,{})
   st=ge.get('status','PENDING')
   if st not in ALLOWED: st='PENDING'
   gates[g]={'status':st,'evidence':ge.get('evidence'), 'provenance':ge.get('provenance')}
  rows.append({
   'title':c.get('title'),'artist':c.get('artist'),'discovery_basis':c.get('discovery_basis'),
   'gates':gates,'qualification_status':classify(gates),
   'scientific_promotion':'NOT_EVALUATED_HERE'
  })
 counts={s:sum(r['qualification_status']==s for r in rows) for s in ('QUALIFIED_FOR_MATRIX_X','AUDIT','REJECTED','PENDING')}
 return {'schema':'HOOKLAB_DANCE_POP_T1_QUALIFICATION_MATRIX_v1.0','cohort_key':queue.get('cohort_key'),'target_checkpoint':queue.get('target_checkpoint',30),'existing_qualified_t0':queue.get('existing_qualified_t0',0),'new_rows':rows,'counts':counts,'t0_plus_new_qualified':queue.get('existing_qualified_t0',0)+counts['QUALIFIED_FOR_MATRIX_X'],'t1_reached':queue.get('existing_qualified_t0',0)+counts['QUALIFIED_FOR_MATRIX_X']>=queue.get('target_checkpoint',30),'invariants':['candidate discovery != scientific promotion','PASS requires observed evidence','AUDIT != FAIL','preview/fragment != FULL_SONG']}

def write_csv(out_json,path):
 fields=['title','artist','qualification_status']+[f'{g}_status' for g in GATES]
 with Path(path).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in out_json['new_rows']:
   row={'title':r['title'],'artist':r['artist'],'qualification_status':r['qualification_status']}
   row.update({f'{g}_status':r['gates'][g]['status'] for g in GATES});w.writerow(row)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--queue',required=True);ap.add_argument('--evidence',required=True);ap.add_argument('--output-json',required=True);ap.add_argument('--output-csv',required=True);a=ap.parse_args()
 out=build(json.loads(Path(a.queue).read_text(encoding='utf-8')),json.loads(Path(a.evidence).read_text(encoding='utf-8')))
 Path(a.output_json).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8');write_csv(out,a.output_csv);print(json.dumps({'counts':out['counts'],'t0_plus_new_qualified':out['t0_plus_new_qualified'],'t1_reached':out['t1_reached']}))
if __name__=='__main__':main()
