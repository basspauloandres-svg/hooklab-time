#!/usr/bin/env python3
"""Build a candidate scientific Matrix X for a genre/style cohort.

Inputs:
- structural target audit from LMD-full
- external genre/style + duration + observed-reach registry

A row is promoted to TARGET_COHORT_CANDIDATE only when:
1) structural FULL_TMT candidate is true,
2) title/artist/year/duration identity evidence is high-confidence,
3) genre/style exactly matches the requested cohort,
4) observed YouTube reach clears the configured engineering floor.

Cross-platform reach and melodic-reference validation remain explicit pending gates.
"""
import argparse,csv,json,re
from pathlib import Path

def norm(x):return re.sub(r'[^a-z0-9]+',' ',str(x or '').lower()).strip()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--audit',required=True);ap.add_argument('--registry',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 audit=list(csv.DictReader(Path(a.audit).open(encoding='utf-8'))); reg=json.loads(Path(a.registry).read_text()); songs={x['md5'].lower():x for x in reg['songs']}; floor=int(reg['success_rule']['youtube_min_views']); rows=[]
 for r in audit:
  md5=r['md5'].lower(); meta=songs.get(md5)
  if not meta:continue
  dur=float(r.get('duration_seconds') or 0); delta=abs(dur-float(meta['expected_duration_seconds']))
  title_ok=norm(r.get('title'))==norm(meta['title']);artist_ok=norm(r.get('artist'))==norm(meta['artist']);year_ok=str(r.get('year'))==str(meta['year']);duration_ok=delta<=8
  identity_score=(4 if title_ok else 0)+(3 if artist_ok else 0)+(2 if year_ok else 0)+(2 if duration_ok else 0);identity_high=identity_score>=9
  structural=str(r.get('full_tmt_candidate','')).lower()=='true'; reach=int(meta['youtube_views_observed'])>=floor
  cohort=(norm(meta['genre']).replace(' ','_')+'::'+norm(meta['style']).replace(' ','_'))
  status='TARGET_COHORT_CANDIDATE' if structural and identity_high and reach else 'TARGET_AUDIT_REQUIRED'
  rows.append({**r,'genre':meta['genre'],'style':meta['style'],'cohort_key':cohort,'identity_score':identity_score,'identity_high_confidence':identity_high,'duration_delta_seconds':delta,'youtube_views_observed':meta['youtube_views_observed'],'youtube_reach_gate':reach,'style_source':meta['style_source'],'youtube_source':meta['youtube_source'],'target_candidate_status':status,'crossplatform_reach_gate':'PENDING','melodic_reference_gate':'PENDING','scientific_promotion':'PENDING'})
 fields=sorted({k for r in rows for k in r});out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 summary={'schema':'HOOKLAB_TARGET_SCIENTIFIC_CANDIDATE_MATRIX_v1.0','cohort_key':reg['cohort_key'],'rows':len(rows),'target_cohort_candidates':sum(r['target_candidate_status']=='TARGET_COHORT_CANDIDATE' for r in rows),'youtube_floor':floor,'remaining_gates':['crossplatform_reach','melodic_reference_validation'],'scientific_promotion':False}
 out.with_suffix('.summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps(summary))
if __name__=='__main__':main()
