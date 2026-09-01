#!/usr/bin/env python3
"""Build the 300-song mass-success discovery frame for HookLab.

Frame: Billboard Year-End Hot 100, chart years 2006-2025, ranks 1-15.
This is discovery/qualification input only. It does not assert Dance-Pop style,
YouTube threshold passage, symbolic-source availability, or scientific promotion.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def build(rows):
    selected=[]
    for r in rows:
        try: year=int(r['chart_year']); rank=int(r['rank'])
        except (KeyError,ValueError,TypeError): continue
        if 2006 <= year <= 2025 and 1 <= rank <= 15:
            selected.append({
                'candidate_id':f'M300::{year}::{rank:02d}',
                'chart_year':year,'rank':rank,'title':r.get('title'),'artist':r.get('artist'),
                'spotify_playcount_observed':int(r['playcount']) if str(r.get('playcount','')).isdigit() else None,
                'spotify_uri':r.get('spotify_uri'),'duration_ms':int(r['duration_ms']) if str(r.get('duration_ms','')).isdigit() else None,
                'discovery_status':'MASS_SUCCESS_FRAME_CANDIDATE',
                'genre_style':'PENDING','youtube_success':'PENDING','identity':'PENDING','version':'PENDING',
                'symbolic_source':'PENDING','full_song':'PENDING','provenance':'PENDING','full_tmt':'PENDING',
                'scientific_promotion':False})
    selected.sort(key=lambda x:(x['chart_year'],x['rank']))
    years={y:0 for y in range(2006,2026)}
    for r in selected: years[r['chart_year']]+=1
    complete=len(selected)==300 and all(v==15 for v in years.values())
    return {'schema':'HOOKLAB_MILESTONE_300_DISCOVERY_FRAME_v1.0','source_frame':'Billboard Year-End Hot 100 matched to Spotify metadata','years':'2006-2025','rank_band':'1-15','candidate_count':len(selected),'year_counts':years,'frame_complete':complete,'status':'FRAME_300_READY_FOR_QUALIFICATION' if complete else 'FRAME_INCOMPLETE','candidates':selected,'invariants':['discovery frame != Dance-Pop stratum','Billboard rank != active dual-platform success qualification','candidate discovery != scientific promotion']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--csv',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    with open(a.csv,encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    out=build(rows);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'status':out['status'],'candidate_count':out['candidate_count']}));raise SystemExit(0 if out['frame_complete'] else 4)
if __name__=='__main__':main()
