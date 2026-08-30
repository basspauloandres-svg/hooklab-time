#!/usr/bin/env python3
"""Fetch full-track AcousticBrainz descriptors without acquiring audio.

AcousticBrainz data are indexed by MusicBrainz recording MBID and licensed CC0.
This adapter is intended to populate/corroborate the full-song T layer and tonal
aggregates. It must never be treated as a substitute for full-song vocal melody.
"""
import argparse,json,urllib.request
from pathlib import Path

UA={'User-Agent':'HookLabPrototype/1.0 (research; no audio acquisition)'}

def get_json(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.load(r)

def dig(d,*keys):
    for k in keys:
        if not isinstance(d,dict): return None
        d=d.get(k)
    return d

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--mbid',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    base=f'https://acousticbrainz.org/{a.mbid}'
    low=get_json(base+'/low-level')
    meta=low.get('metadata',{})
    rhythm=low.get('rhythm',{})
    tonal=low.get('tonal',{})
    out={
      'schema':'HOOKLAB_ACOUSTICBRAINZ_FULLSONG_v1.0',
      'mbid':a.mbid,
      'source':'AcousticBrainz',
      'license':'CC0',
      'coverage':'FULL_SONG_AGGREGATE',
      'audio_acquired_by_hooklab':False,
      'dimension_coverage':{'M':'NONE','T':'FULL_AGGREGATE','Text':'NONE'},
      'features':{
        'duration_seconds':dig(meta,'audio_properties','length'),
        'bpm':rhythm.get('bpm'),
        'beat_count':len(rhythm.get('beats_position',[]) or []),
        'danceability':rhythm.get('danceability'),
        'onset_rate':rhythm.get('onset_rate'),
        'key_key':tonal.get('key_key'),
        'key_scale':tonal.get('key_scale'),
        'chords_key':tonal.get('chords_key'),
        'chords_scale':tonal.get('chords_scale')
      },
      'provenance':{'low_level_url':base+'/low-level'},
      'epistemic_note':'Full-track rhythmic/tonal evidence only. Vocal melody must come from an independent full-song source.'
    }
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__': main()
