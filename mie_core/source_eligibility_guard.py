#!/usr/bin/env python3
"""Source eligibility guard for HookLab/TIME Sample 1.

Determines whether a candidate can enter real analysis based on source provenance.
It does not evaluate musical quality. Audio and text rights/provenance are checked
independently because a usable recording does not imply a usable lyric source.
"""
import argparse,json
from pathlib import Path

ALLOWED_AUDIO={'PUBLIC_DOMAIN','LICENSED_API','USER_AUTHORIZED_CORPUS','RESEARCH_CORPUS'}
ALLOWED_TEXT={'PUBLIC_DOMAIN','LICENSED_API','USER_AUTHORIZED_CORPUS','RESEARCH_CORPUS'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 d=json.loads(Path(a.candidate).read_text())
 audio=d.get('audio',{});text=d.get('text',{})
 checks={
  'song_id':bool(d.get('song_id')),
  'genre':bool(d.get('genre')),
  'style':bool(d.get('style')),
  'audio_source_id':bool(audio.get('source_id')),
  'audio_source_type_allowed':audio.get('source_type') in ALLOWED_AUDIO,
  'audio_locator':bool(audio.get('locator')),
  'text_source_id':bool(text.get('source_id')),
  'text_source_type_allowed':text.get('source_type') in ALLOWED_TEXT,
  'text_locator_or_local_ref':bool(text.get('locator') or text.get('local_ref')),
 }
 status='ELIGIBLE_FOR_REAL_E2E' if all(checks.values()) else 'INELIGIBLE_SOURCE_GAP'
 out={'schema':'SOURCE_ELIGIBILITY_v1.0','song_id':d.get('song_id'),'status':status,'checks':checks,
      'audio_source_type':audio.get('source_type'),'text_source_type':text.get('source_type'),
      'rule':'Eligibility concerns provenance/access only; it is not evidence of analyzer success or musical relevance.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
 if status!='ELIGIBLE_FOR_REAL_E2E':raise SystemExit(2)
if __name__=='__main__':main()
