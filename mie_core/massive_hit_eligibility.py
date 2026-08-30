#!/usr/bin/env python3
"""Massive-hit eligibility guard for HookLab/TIME Sample 1.

Selection is external to the musical analysis. A candidate enters Sample 1 only
when the recording/release is contemporary and has independently verified massive
reach on YouTube AND at least one social platform. Social evidence must identify
the song/audio explicitly; artist popularity alone is insufficient.
"""
import argparse,json,datetime,calendar
from pathlib import Path

CUTOFF_YEARS=20
YT_MIN=100_000_000
SOCIAL_MIN=50_000_000


def rolling_cutoff(today):
    y=today.year-CUTOFF_YEARS
    d=min(today.day,calendar.monthrange(y,today.month)[1])
    return datetime.date(y,today.month,d)


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 d=json.loads(Path(a.input).read_text())
 today=datetime.date.today(); cutoff=rolling_cutoff(today)
 release_date_raw=d.get('release_date')
 release_date=None
 if release_date_raw:
  try: release_date=datetime.date.fromisoformat(release_date_raw)
  except ValueError: release_date=None
 youtube=int(d.get('youtube_views',d.get('youtube_views_observed',0)) or 0)
 social=d.get('social_evidence',[]) or []
 verified_social=[x for x in social if x.get('song_match_verified') is True and int(x.get('views',x.get('views_observed',0)) or 0)>=SOCIAL_MIN]
 official=bool(d.get('official_release'))
 contemporary=(release_date is not None and cutoff<=release_date<=today)
 yt_gate=youtube>=YT_MIN
 social_gate=bool(verified_social)
 eligible=official and contemporary and yt_gate and social_gate
 out={**d,'sample1_massive_hit_eligibility':{
   'official_release':official,'release_date_valid':release_date is not None,
   'rolling_20y_cutoff':cutoff.isoformat(),'within_last_20_years':contemporary,
   'youtube_100m_gate':yt_gate,'verified_social_50m_gate':social_gate,
   'verified_social_items':len(verified_social),'eligible':eligible,
   'policy':'SELECTION_ONLY_NOT_PREDICTOR',
   'note':'Strict eligibility requires an exact ISO release_date. Release year alone is retained as metadata but cannot prove membership in the rolling 20-year window. YouTube/social metrics select the massive-success population only.'}}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out['sample1_massive_hit_eligibility']))
if __name__=='__main__':main()
