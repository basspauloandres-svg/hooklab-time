#!/usr/bin/env python3
"""Generate three audible MT-only test-lane variants from full-song symbolic cohort stats.

This is an engineering demonstrator, not HookLab model evidence. It intentionally uses
no text-derived constraints and therefore must never be labeled FULL_TMT or enter the
massive-hit evidence cohort. Purpose: validate cache/reference -> constraints -> render
-> latency plumbing while full-song text acquisition remains unresolved.
"""
import argparse,csv,json,math,random,statistics,struct,time,wave
from pathlib import Path

def median(rows,key):
 vals=[float(r[key]) for r in rows if r.get(key) not in (None,'')]
 return statistics.median(vals) if vals else None

def render(path,bpm,span,density,mode,seed=1701,seconds=12,sr=22050):
 random.seed(seed); beat=60.0/bpm; step=max(beat/2,1.0/max(density,.25)); n=int(seconds/step)
 starts={'thetic':0.0,'anacrustic':max(0,beat-step),'syncopated':beat/2}; offset=starts[mode]
 scale=[0,2,4,7,9]; notes=[]
 for i in range(n):
  t=offset+i*step
  if t>=seconds:break
  deg=scale[(i+(1 if mode=='syncopated' else 0))%len(scale)]
  octave=(i//len(scale))%2
  semitone=min(span,deg+12*octave)
  midi=60+semitone; notes.append((t,min(step*.82,.45),midi))
 frames=[0.0]*int(seconds*sr)
 for t,d,m in notes:
  f=440.0*(2**((m-69)/12)); a=int(t*sr); b=min(len(frames),int((t+d)*sr))
  for j in range(a,b):
   env=min(1,(j-a)/(sr*.02+1))*max(0,1-(j-a)/max(1,b-a))
   frames[j]+=0.22*env*math.sin(2*math.pi*f*(j/sr))
 with wave.open(str(path),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
  w.writeframes(b''.join(struct.pack('<h',max(-32767,min(32767,int(x*32767)))) for x in frames))
 return notes

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--matrix',required=True);ap.add_argument('--output-dir',required=True);a=ap.parse_args();t0=time.perf_counter()
 rows=[r for r in csv.DictReader(Path(a.matrix).open()) if r.get('coverage')=='FULL_SONG' and r.get('strict_gate')=='PASS']
 bpm=median(rows,'tempo_bpm');span=round(median(rows,'melodic_range_semitones'));density=median(rows,'melodic_events_per_second')
 out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True); variants={}
 for k in ['thetic','anacrustic','syncopated']:
  p=out/f'{k}.wav';notes=render(p,bpm,span,density,k);variants[k]={'audio':str(p),'note_count':len(notes)}
 elapsed=time.perf_counter()-t0
 manifest={'schema':'HOOKLAB_TESTLANE_MT_AUDIO_DEMO_v1.0','status':'TECHNICAL_AUDIO_SMOKE_TEST','evidence_role':'TEST_LANE_ONLY_POP909',
  'full_tmt':False,'text_dimension':'ABSENT_BY_DESIGN','cohort_n':len(rows),'descriptive_reference':{'tempo_bpm_median':bpm,'melodic_range_semitones_median':span,'melodic_events_per_second_median':density},
  'variants':variants,'TTFP_seconds':elapsed,'T_online_search_seconds':0,'online_corpus_reanalysis':False,
  'boundary':'Validates MT full-song data-to-audio plumbing only; cannot support musical-effectiveness or massive-hit claims.'}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False));print(json.dumps(manifest))
if __name__=='__main__':main()
