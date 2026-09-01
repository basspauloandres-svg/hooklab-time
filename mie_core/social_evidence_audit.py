#!/usr/bin/env python3
"""Audit social evidence before Sample 1 inclusion.

Search relevance is discovery evidence only. A social item can satisfy the massive-hit
gate only when the returned metadata explicitly identifies the requested recording/song
(or a subsequently watched item confirms it). Ambiguous results remain pending.
"""
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 d=json.loads(Path(a.input).read_text()); accepted=[]; rejected=[]; pending=[]
 for x in d.get('social_evidence',[]):
  views=int(x.get('views',0) or 0)
  explicit=bool(x.get('song_match_verified')) and bool(x.get('match_basis'))
  if views < 50_000_000: rejected.append({**x,'audit_reason':'BELOW_50M'})
  elif explicit: accepted.append({**x,'audit_status':'EXPLICIT_MATCH_ACCEPTED'})
  else: pending.append({**x,'audit_status':'AMBIGUOUS_REQUIRES_CONFIRMATION'})
 out={**d,'social_evidence_audit':{'accepted':accepted,'pending':pending,'rejected':rejected,
      'gate_pass':bool(accepted),'policy':'SEARCH_RELEVANCE_IS_NOT_SONG_IDENTITY'}}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out['social_evidence_audit']))
if __name__=='__main__': main()
