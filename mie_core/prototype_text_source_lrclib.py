#!/usr/bin/env python3
"""Free, keyless lyrics-source adapter for HookLab prototype work.

Retrieves candidate lyrics from LRCLIB and stores only the fields required for
traceability and downstream alignment. This module does NOT claim that full-song
synced lyrics are aligned to an Apple/iTunes preview excerpt; that remains a separate
observable alignment step.
"""
import argparse,json,re,urllib.parse,urllib.request
from pathlib import Path

def norm(s): return re.sub(r'[^a-z0-9]+',' ',str(s or '').lower()).strip()

def get_json(url):
    req=urllib.request.Request(url,headers={'User-Agent':'HookLab-TIME/0.3 (https://github.com/basspauloandres-svg/hooklab-time)'})
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--track',required=True);ap.add_argument('--artist',required=True)
    ap.add_argument('--album');ap.add_argument('--output',required=True);a=ap.parse_args()
    q={'track_name':a.track,'artist_name':a.artist}
    if a.album:q['album_name']=a.album
    url='https://lrclib.net/api/search?'+urllib.parse.urlencode(q)
    rows=get_json(url)
    nt,na=norm(a.track),norm(a.artist); scored=[]
    for x in rows:
        tt,aa=norm(x.get('trackName')),norm(x.get('artistName'))
        score=(4 if tt==nt else 2 if nt in tt or tt in nt else 0)+(3 if na==aa else 2 if na in aa or aa in na else 0)
        if x.get('plainLyrics') or x.get('syncedLyrics'): scored.append((score,x))
    if not scored: raise SystemExit('LRCLIB_NO_MATCH')
    scored.sort(key=lambda z:z[0],reverse=True);score,hit=scored[0]
    if score<5: raise SystemExit('LRCLIB_AMBIGUOUS_MATCH')
    plain=hit.get('plainLyrics') or ''
    synced=hit.get('syncedLyrics') or ''
    lines=[ln for ln in plain.splitlines() if ln.strip()]
    tokens=re.findall(r"\b[\w'’]+\b",plain,flags=re.UNICODE)
    out={'schema':'HOOKLAB_LRCLIB_TEXT_SOURCE_v1.0','status':'FULL_SONG_TEXT_REFERENCE_NOT_PREVIEW_ALIGNED',
         'query':{'track':a.track,'artist':a.artist,'album':a.album},'lrclib_id':hit.get('id'),
         'resolved':{'track':hit.get('trackName'),'artist':hit.get('artistName'),'album':hit.get('albumName'),'duration_s':hit.get('duration')},
         'has_synced_lyrics':bool(synced),'line_count_full_song':len(lines),'token_count_full_song':len(tokens),
         'plainLyrics':plain,'syncedLyrics':synced,
         'evidence_boundary':'Text is a full-song public reference. It must not be mixed with preview-derived M/T metrics until excerpt alignment is independently established.'}
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'status':out['status'],'lrclib_id':out['lrclib_id'],'has_synced_lyrics':out['has_synced_lyrics'],'lines':len(lines),'tokens':len(tokens)}))
if __name__=='__main__':main()
