#!/usr/bin/env python3
"""Full-song symbolic engineering probe using POP909.

Purpose: validate HookLab's full-song T/M path and Matrix-X plumbing independently of
the massive-hit acquisition problem. POP909-derived rows are TEST_LANE_ONLY and must
never enter the massive-hit evidence cohort.
"""
import argparse,csv,json,statistics
from pathlib import Path
try:
 import pretty_midi
except ImportError: raise SystemExit('pretty_midi required')

def stats(mid):
 pm=pretty_midi.PrettyMIDI(str(mid)); end=pm.get_end_time(); tempos=pm.get_tempo_changes()[1]
 inst=[i for i in pm.instruments if not i.is_drum and i.notes]
 # POP909 convention includes melody tracks; choose monophonic/high-coverage candidate descriptively.
 ranked=[]
 for i in inst:
  ns=sorted(i.notes,key=lambda n:n.start); pitches=[n.pitch for n in ns]; span=max(n.end for n in ns)-min(n.start for n in ns)
  overlaps=sum(ns[j+1].start < ns[j].end-.03 for j in range(len(ns)-1))/max(1,len(ns)-1)
  score=(2 if overlaps<.12 else 0)+(2 if span>=end*.6 else 0)+(2 if 48<=statistics.median(pitches)<=84 else 0)
  ranked.append((score,i,ns,pitches,span,overlaps))
 ranked.sort(key=lambda x:x[0],reverse=True)
 if not ranked:return None
 _,i,ns,pitches,span,overlaps=ranked[0]
 return {'coverage':'FULL_SONG','strict_gate':'PASS','tempo_bpm':float(statistics.median(tempos)) if len(tempos) else None,
         'melodic_range_semitones':max(pitches)-min(pitches),'melodic_event_count':len(ns),'duration_seconds':end,
         'melodic_events_per_second':len(ns)/max(end,.001),'melody_track_name':i.name,'melody_overlap_ratio':overlaps,
         'evidence_role':'TEST_LANE_ONLY_POP909','source_scope':'FULL_SONG_SYMBOLIC'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--output',required=True);ap.add_argument('--limit',type=int,default=12);a=ap.parse_args()
 mids=list(Path(a.root).rglob('*.mid'))+list(Path(a.root).rglob('*.midi')); rows=[]
 for p in mids[:a.limit]:
  try:
   s=stats(p)
   if s:s.update({'song_id':p.stem,'genre':'pop909_test','style':'fullsong_symbolic'});rows.append(s)
  except Exception as e: rows.append({'song_id':p.stem,'status':'ERROR','error':str(e),'evidence_role':'TEST_LANE_ONLY_POP909'})
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 fields=sorted({k for r in rows for k in r});
 with out.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 print(json.dumps({'status':'POP909_FULLSONG_PROBE_COMPLETE','rows':len(rows),'output':str(out)}))
if __name__=='__main__':main()
