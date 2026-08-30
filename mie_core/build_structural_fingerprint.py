#!/usr/bin/env python3
"""Analyzer v1 structural fingerprint.
Builds a comparable descriptive vector from a TMT Song Object/feature payload.
No success, genre, or hook label is inferred. Missing dimensions remain null.
"""
import argparse,json,math,statistics
from pathlib import Path

def num(x): return x if isinstance(x,(int,float)) and math.isfinite(x) else None

def main():
 ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output');a=ap.parse_args()
 d=json.loads(Path(a.input).read_text()); g=d.get('global',d)
 r=d.get('recurrence',{}); s=d.get('salience',{}); ir=d.get('internal_recurrence',{})
 fp={
  'schema':'TMT_STRUCTURAL_FINGERPRINT_v1.0','song_id':d.get('song_object_id',d.get('song_id')),
  'coverage':d.get('coverage','FULL' if d.get('song_object_id') else None),
  'M':{'event_count':num(g.get('M_event_count')),'median_midi':num(g.get('M_median_midi')),'range_semitones':num(g.get('M_range_semitones'))},
  'T':{'tempo_bpm':num(g.get('T_tempo_bpm')),'tactus_count':num(g.get('T_tactus_count')),'mean_near_tactus_share':num(g.get('mean_near_tactus_share_by_line'))},
  'TEXT':{'line_count':num(g.get('text_line_count')),'repetition_group_count':num(g.get('text_repetition_group_count'))},
  'TMT':{'mean_M_events_per_token':num(g.get('mean_M_events_per_text_token')),
         'mean_recurrence_similarity':num(r.get('mean_multimodal_recurrence_similarity')),
         'median_recurrence_similarity':num(r.get('median_multimodal_recurrence_similarity')),
         'stable_region_count':num(ir.get('stable_region_count')),
         'mean_stable_region_stability':num(ir.get('mean_stable_region_stability')),
         'mean_event_salience':num(s.get('mean_event_salience')),
         'max_recurrence_x_salience':num(s.get('max_recurrence_x_salience'))},
  'inference_status':'DESCRIPTIVE_ONLY','success_association':'NOT_TESTED'}
 Path(a.output).write_text(json.dumps(fp,indent=2,ensure_ascii=False));print(json.dumps(fp))
if __name__=='__main__':main()
