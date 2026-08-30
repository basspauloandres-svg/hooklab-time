#!/usr/bin/env python3
"""Massive-hit eligibility guard for HookLab/TIME Sample 1.

Selection is external to the musical analysis. A candidate enters Sample 1 only
when the recording/release is contemporary and has independently verified massive
reach on YouTube AND at least one social platform. Social evidence must identify
the song/audio explicitly; artist popularity alone is insufficient.
"""
import argparse,json,datetime
from pathlib import Path

CUTOFF_YEARS=20
YT_MIN=100_000_000
SOCIAL_MIN=50_000_000


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 d=json.loads(Path(a.input).read_text())
 year=int(d.get('release_year',0) or 0);current=datetime.date.today().year
 youtube=int(d.get('youtube_views',0) or 0)
 social=d.get('social_evidence',[]) or []
 verified_social=[x for x in social if x.get('song_match_verified') is True and int(x.get('views',0) or 0)>=SOCIAL_MIN]
 official=bool(d.get('official_release'))
 contemporary=(current-CUTOFF_YEARS)<=year<=current
 yt_gate=youtube>=YT_MIN
 social_gate=bool(verified_social)
 eligible=official and contemporary and yt_gate and social_gate
 out={**d,'sample1_massive_hit_eligibility':{
   'official_release':official,'within_last_20_years':contemporary,
   'youtube_100m_gate':yt_gate,'verified_social_50m_gate':social_gate,
   'verified_social_items':len(verified_social),'eligible':eligible,
   'policy':'SELECTION_ONLY_NOT_PREDICTOR',
   'note':'YouTube/social metrics select the massive-success population only. Artist-level reach, unrelated viral posts, and inferred song matches cannot satisfy the social gate.'}}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out['sample1_massive_hit_eligibility']))
if __name__=='__main__':main()
