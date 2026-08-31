#!/usr/bin/env python3
"""Merge observed gate evidence into the T1 qualification state without promotion shortcuts."""
from __future__ import annotations
import argparse,json
from pathlib import Path
ALLOWED={'PASS','AUDIT','FAIL','PENDING'}
GATES=('mass_success','identity','genre_style','version','symbolic_source','full_song','provenance','full_tmt')
def merge(base, batch):
    by={(r['title'],r['artist']):r for r in base.get('rows',[])}
    changed=[]
    for obs in batch.get('rows',[]):
        k=(obs['title'],obs['artist'])
        if k not in by: by[k]={'title':k[0],'artist':k[1],'gates':{g:'PENDING' for g in GATES},'evidence':{}}
        row=by[k]
        for g,v in obs.get('gates',{}).items():
            if g not in GATES or v not in ALLOWED: raise ValueError(f'invalid gate state {g}={v}')
            old=row['gates'].get(g,'PENDING')
            if old=='PASS' and v in {'AUDIT','FAIL'}: raise ValueError(f'cannot silently downgrade PASS for {k} {g}; explicit audit revision required')
            row['gates'][g]=v
        row.setdefault('evidence_batches',[]).append(batch.get('batch_id'))
        row.setdefault('evidence',{}).update(obs.get('evidence',{}));changed.append({'title':k[0],'artist':k[1]})
    rows=list(by.values())
    for r in rows:
        vals=[r['gates'].get(g,'PENDING') for g in GATES]
        r['qualification_status']='REJECTED' if 'FAIL' in vals else 'QUALIFIED_FOR_MATRIX_X' if all(v=='PASS' for v in vals) else 'AUDIT_REQUIRED' if 'AUDIT' in vals else 'PENDING'
    return {'schema':'HOOKLAB_T1_QUALIFICATION_STATE_v1.0','rows':rows,'changed':changed,'qualified_n':sum(r['qualification_status']=='QUALIFIED_FOR_MATRIX_X' for r in rows),'audit_n':sum(r['qualification_status']=='AUDIT_REQUIRED' for r in rows),'rejected_n':sum(r['qualification_status']=='REJECTED' for r in rows),'invariant':'candidate discovery != scientific promotion'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True);ap.add_argument('--batch',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();out=merge(json.loads(Path(a.base).read_text()),json.loads(Path(a.batch).read_text()));Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'qualified_n':out['qualified_n'],'audit_n':out['audit_n'],'rejected_n':out['rejected_n']}))
if __name__=='__main__':main()
