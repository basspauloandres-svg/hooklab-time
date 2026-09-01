#!/usr/bin/env python3
"""Resolve song identity before accepting a symbolic full-song representation.

Metadata is evidence for identity, not evidence for musical content. The resolver
scores title/artist/version/year/duration/ISRC/MBID consistency and refuses automatic
acceptance when version identity is ambiguous. Designed to sit before Lakh/MIDI audit.
"""
import argparse,json,re
from pathlib import Path

def norm(x):
 return re.sub(r'[^a-z0-9]+',' ',str(x or '').lower()).strip()

def eq(a,b): return bool(a and b and norm(a)==norm(b))
def contains(a,b):
 a,b=norm(a),norm(b); return bool(a and b and (a in b or b in a))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--target',required=True);ap.add_argument('--candidate',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 t=json.loads(Path(a.target).read_text()); c=json.loads(Path(a.candidate).read_text())
 evidence={}
 evidence['title_exact']=eq(t.get('title'),c.get('title'))
 evidence['title_close']=contains(t.get('title'),c.get('title'))
 evidence['artist_close']=contains(t.get('artist'),c.get('artist'))
 evidence['isrc_exact']=eq(t.get('isrc'),c.get('isrc')) if t.get('isrc') and c.get('isrc') else None
 evidence['mbid_exact']=eq(t.get('mbid'),c.get('mbid')) if t.get('mbid') and c.get('mbid') else None
 evidence['year_match']=(str(t.get('year'))==str(c.get('year'))) if t.get('year') and c.get('year') else None
 td,cd=t.get('duration_seconds'),c.get('duration_seconds')
 evidence['duration_delta_seconds']=abs(float(td)-float(cd)) if td is not None and cd is not None else None
 evidence['duration_close']=evidence['duration_delta_seconds']<=8 if evidence['duration_delta_seconds'] is not None else None
 tv,cv=norm(t.get('version','original')),norm(c.get('version','original'))
 version_conflict=bool(tv and cv and tv!=cv and any(x in tv+' '+cv for x in ['remix','live','acoustic','edit','instrumental','karaoke']))
 score=0
 score+=4 if evidence['title_exact'] else 2 if evidence['title_close'] else 0
 score+=3 if evidence['artist_close'] else 0
 score+=5 if evidence['isrc_exact'] is True else 0
 score+=4 if evidence['mbid_exact'] is True else 0
 score+=2 if evidence['year_match'] is True else 0
 score+=2 if evidence['duration_close'] is True else 0
 hard_id=(evidence['isrc_exact'] is True or evidence['mbid_exact'] is True)
 status='IDENTITY_HIGH_CONFIDENCE' if (not version_conflict and evidence['title_close'] and evidence['artist_close'] and (hard_id or score>=9)) else 'IDENTITY_AUDIT_REQUIRED'
 out={'schema':'HOOKLAB_METADATA_IDENTITY_RESOLVER_v1.0','status':status,'score':score,'version_conflict':version_conflict,'evidence':evidence,
      'target':t,'candidate':c,'rule':'Metadata resolves recording/version identity only; symbolic musical content remains separately auditable.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
 raise SystemExit(0 if status=='IDENTITY_HIGH_CONFIDENCE' else 4)
if __name__=='__main__':main()
