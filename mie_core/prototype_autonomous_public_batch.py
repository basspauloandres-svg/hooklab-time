#!/usr/bin/env python3
"""Autonomous free-preview batch for HookLab prototype evidence.

Resolves public iTunes/Apple preview URLs without API keys, downloads only the short
preview needed by the offline Analyzer path, separates vocals, runs the frozen
structural probe, and records provenance. Intended for prototype engineering only.
"""
import argparse,json,re,subprocess,sys,urllib.parse,urllib.request
from pathlib import Path

DEFAULT_CANDIDATES=[
 {"id":"despacito","track":"Despacito","artist":"Luis Fonsi","genre":"latin_urban_pop","style":"reggaeton_pop","release":"2017-01-12","apple_song_id":"1447401620"},
 {"id":"mi_gente","track":"Mi Gente","artist":"J Balvin","genre":"latin_urban_pop","style":"reggaeton_crossover","release":"2017-06-29","apple_song_id":"1368816792"},
 {"id":"taki_taki","track":"Taki Taki","artist":"DJ Snake","genre":"latin_urban_pop","style":"reggaeton_crossover","release":"2018-09-28","apple_song_id":"1460306646"},
 {"id":"con_calma","track":"Con Calma","artist":"Daddy Yankee","genre":"latin_urban_pop","style":"reggaeton_crossover","release":"2019-01-24","apple_song_id":1450718725}
]

def norm(s): return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()

def resolve_preview(track,artist):
 term=urllib.parse.quote(f'{track} {artist}')
 url=f'https://itunes.apple.com/search?term={term}&entity=song&limit=25'
 req=urllib.request.Request(url,headers={'User-Agent':'HookLabPrototype/1.1'})
 with urllib.request.urlopen(req,timeout=30) as r: data=json.load(r)
 nt,na=norm(track),norm(artist); scored=[]
 for x in data.get('results',[]):
  tt,aa=norm(x.get('trackName','')),norm(x.get('artistName',''))
  score=(3 if tt==nt else 2 if nt in tt or tt in nt else 0)+(2 if na in aa or aa in na else 0)
  if x.get('previewUrl'): scored.append((score,x))
 if not scored: raise RuntimeError(f'no preview for {track} / {artist}')
 scored.sort(key=lambda z:z[0],reverse=True)
 if scored[0][0] < 4: raise RuntimeError(f'ambiguous preview resolution for {track} / {artist}')
 return scored[0][1],url

def run(cmd): subprocess.run(cmd,check=True)

def structural_metrics(obj):
 keys=['duration_s','raw_sensor_count','hypothesis_count','render_count','structural_ambiguous_count',
       'raw_density_events_per_s','render_density_events_per_s','render_to_raw_ratio','hypothesis_to_raw_ratio',
       'max_jump_semitones','jumps_ge_10','plane_ambiguous_count','resolver_introduced_large_jumps','resolver_worsened_by_octave_or_more']
 return {k:obj.get(k) for k in keys}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); ap.add_argument('--limit',type=int,default=len(DEFAULT_CANDIDATES)); a=ap.parse_args()
 root=Path(a.output); root.mkdir(parents=True,exist_ok=True); summary=[]
 for c in DEFAULT_CANDIDATES[:a.limit]:
  d=root/c['id']; (d/'input').mkdir(parents=True,exist_ok=True); (d/'output').mkdir(exist_ok=True)
  hit,query_url=resolve_preview(c['track'],c['artist']); preview=hit['previewUrl']
  src=d/'input'/'preview.m4a'; wav=d/'input'/'preview.wav'
  urllib.request.urlretrieve(preview,src)
  run(['ffmpeg','-y','-i',str(src),'-ar','44100','-ac','2',str(wav)])
  stems=d/'stems'; run([sys.executable,'-m','demucs','-n','htdemucs','-o',str(stems),str(wav)])
  vocals=list(stems.rglob('vocals.wav'))
  if not vocals: raise RuntimeError('vocal stem missing')
  out=d/'output'/'structural_probe'; run([sys.executable,str(Path(__file__).with_name('run_structural_probe.py')),'--vocal',str(vocals[0]),'--output',str(out)])
  prov={"schema":"HOOKLAB_FREE_PREVIEW_PROVENANCE_v1.1","candidate":c,"itunes_query":query_url,
        "resolved_track":hit.get('trackName'),"resolved_artist":hit.get('artistName'),"track_id":hit.get('trackId'),
        "preview_url":preview,"collection":hit.get('collectionName'),"primary_genre":hit.get('primaryGenreName'),
        "role":"PROTOTYPE_EVIDENCE_NOT_FINAL_SAMPLE","audio_scope":"public short preview only"}
  (d/'output'/'provenance.json').write_text(json.dumps(prov,indent=2,ensure_ascii=False))
  probe_path=out/'MIE_STRUCTURAL_PROBE_v0_4.json'
  probe=json.loads(probe_path.read_text()) if probe_path.exists() else {}
  summary.append({"candidate":c,"resolved_track_id":hit.get('trackId'),"structural_metrics":structural_metrics(probe),
                  "probe_status":probe.get('status'),"tmt_status":"M_ONLY_PREVIEW; TEXT_AND_TACTUS_PENDING"})
 (root/'batch_summary.json').write_text(json.dumps({"schema":"HOOKLAB_AUTONOMOUS_PUBLIC_BATCH_v1.1","results":summary},indent=2,ensure_ascii=False))
 print(json.dumps({"status":"AUTONOMOUS_PUBLIC_BATCH_COMPLETE","count":len(summary),"output":str(root)}))
if __name__=='__main__': main()
