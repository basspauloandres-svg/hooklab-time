#!/usr/bin/env python3
"""Massive-hit eligibility guard for HookLab/TIME Sample 1.

A candidate enters Sample 1 only if it is a contemporary commercial release and
its success evidence is externally observable. YouTube and social-platform metrics
are selection variables, not musical predictors.
"""
import argparse,json,datetime
from pathlib import Path

CUTOFF_YEARS=20


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 d=json.loads(Path(a.input).read_text())
 year=int(d.get('release_year',0) or 0);current=datetime.date.today().year
 youtube=int(d.get('youtube_views',0) or 0);social=int(d.get('social_peak_views',0) or 0)
 official=bool(d.get('official_release'))
 contemporary=year>=current-CUTOFF_YEARS
 # Operational thresholds for discovery. These do not define success as a theory.
 yt_gate=youtube>=100_000_000
 social_gate=social>=50_000_000
 eligible=official and contemporary and yt_gate and social_gate
 out={**d,'sample1_massive_hit_eligibility':{
   'official_release':official,'within_last_20_years':contemporary,
   'youtube_100m_gate':yt_gate,'social_50m_gate':social_gate,'eligible':eligible,
   'policy':'SELECTION_ONLY_NOT_PREDICTOR',
   'note':'View thresholds are operational inclusion gates for a massive-success sample; they are not weights in the musical model.'}}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out['sample1_massive_hit_eligibility']))
if __name__=='__main__':main()
