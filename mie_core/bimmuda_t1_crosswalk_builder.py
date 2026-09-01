#!/usr/bin/env python3
"""Build a reproducible crosswalk between HookLab T1 discovery candidates and BiMMuDa metadata.

This layer is coverage-only. Presence in BiMMuDa never implies license permission,
scientific qualification, or Matrix X promotion.
"""
from __future__ import annotations
import argparse,csv,json,re
from pathlib import Path

def norm(x):
    return re.sub(r'[^a-z0-9]+',' ',str(x or '').lower()).strip()

def build(queue, metadata_rows, license_status='AUDIT_REQUIRED'):
    by_title={}
    for r in metadata_rows:
        by_title.setdefault(norm(r.get('Title')),[]).append(r)
    rows=[]
    for c in queue.get('candidates',[]):
        title=c.get('title'); artist=c.get('artist')
        matches=by_title.get(norm(title),[])
        best=None
        for m in matches:
            if norm(artist).split(' feat ')[0] in norm(m.get('Artist')) or norm(m.get('Artist')).split(' feat ')[0] in norm(artist):
                best=m;break
        if best is None and len(matches)==1: best=matches[0]
        present=best is not None
        year=best.get('Year') if best else None
        pos=best.get('Position') if best else None
        dataset_id=f"{year}_{str(pos).zfill(2)}" if present and str(pos).isdigit() else None
        rows.append({
            'title':title,'artist':artist,'present_in_bimmuda':present,
            'bimmuda_year':year,'bimmuda_position':pos,'bimmuda_id':dataset_id,
            'full_midi_expected':present,'section_midis_expected':present,'lyrics_expected':present,
            'license_processing_status':license_status,
            'scientific_eligibility':'BLOCKED_LICENSE_AUDIT' if present and license_status!='AUTHORIZED' else ('PENDING_OTHER_GATES' if present else 'NOT_COVERED'),
            'note':'Coverage only; dataset presence != scientific promotion.'
        })
    covered=sum(r['present_in_bimmuda'] for r in rows)
    return {'schema':'HOOKLAB_BIMMUDA_T1_CROSSWALK_v1.0','rows':rows,'counts':{'t1_candidates':len(rows),'covered_by_bimmuda':covered,'coverage_rate':covered/len(rows) if rows else 0.0,'scientifically_promoted_rows':0},'invariants':['dataset available != scientific target population','dataset presence != license authorization','candidate discovery != scientific promotion']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--queue',required=True);ap.add_argument('--metadata',required=True);ap.add_argument('--output',required=True);ap.add_argument('--license-status',default='AUDIT_REQUIRED');a=ap.parse_args()
    q=json.loads(Path(a.queue).read_text(encoding='utf-8'))
    with Path(a.metadata).open(encoding='utf-8-sig',newline='') as f: meta=list(csv.DictReader(f))
    out=build(q,meta,a.license_status)
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(out['counts']))
if __name__=='__main__':main()
