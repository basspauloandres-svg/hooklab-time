#!/usr/bin/env python3
"""Audit direct lyric-to-note binding evidence inside Standard MIDI/KAR files.

This adds a stronger source-internal validation layer than generic melody heuristics. It
uses track-level lyric/text events, note-on timing, and MIDI Channel Prefix evidence when
present. It does NOT claim external/independent proof of the commercial recording's lead
vocal; it reports direct symbolic binding evidence in the source file.
"""
import argparse,csv,json,re
from pathlib import Path
import mido

def clean_text(msg):
 t=str(getattr(msg,'text','')).strip()
 return bool(t and not t.startswith('@') and len(t)<=160)

def track_name(track):
 for m in track:
  if m.type=='track_name': return str(m.name)
 return ''

def inspect_midi(path):
 mf=mido.MidiFile(path);tpb=mf.ticks_per_beat;tol=max(1,tpb//8);tracks=[];all_lyrics=[]
 for ti,tr in enumerate(mf.tracks):
  tick=0;notes=[];lyrics=[];channels=set();prefixes=[]
  for m in tr:
   tick+=m.time
   if m.type=='note_on' and m.velocity>0:
    notes.append(tick);channels.add(int(m.channel))
   elif m.type in ('lyrics','text') and clean_text(m):lyrics.append(tick)
   elif m.type=='channel_prefix':prefixes.append(int(m.channel))
  all_lyrics.extend(lyrics);tracks.append({'index':ti,'name':track_name(tr),'notes':notes,'lyrics':lyrics,'channels':sorted(channels),'prefixes':prefixes})
 def align(note_ticks):
  if not all_lyrics or not note_ticks:return 0.
  return sum(min(abs(x-y) for y in note_ticks)<=tol for x in all_lyrics)/len(all_lyrics)
 for t in tracks:t['lyric_onset_alignment']=align(t['notes']);t['note_count']=len(t['notes']);t['lyric_count']=len(t['lyrics']);t['same_track_binding']=bool(t['notes'] and t['lyrics']);t['channel_prefix_binding']=bool(set(t['channels']) & set(t['prefixes']))
 ranked=sorted([t for t in tracks if t['note_count']>=10],key=lambda x:(x['channel_prefix_binding'],x['same_track_binding'],x['lyric_onset_alignment'],x['note_count']),reverse=True)
 best=ranked[0] if ranked else None
 if not best:return {'binding_status':'NO_NOTE_TRACK','lyric_event_count':len(all_lyrics)}
 if best['channel_prefix_binding'] and best['lyric_onset_alignment']>=.5:status='DIRECT_CHANNEL_PREFIX_LYRIC_BINDING'
 elif best['same_track_binding'] and best['lyric_onset_alignment']>=.5:status='DIRECT_SAME_TRACK_LYRIC_NOTE_BINDING'
 elif best['lyric_onset_alignment']>=.65:status='STRONG_TEMPORAL_LYRIC_NOTE_BINDING'
 elif best['lyric_onset_alignment']>=.35:status='MODERATE_TEMPORAL_BINDING_AUDIT'
 else:status='WEAK_BINDING_REQUIRES_REFERENCE'
 return {'binding_status':status,'lyric_event_count':len(all_lyrics),'best_track_index':best['index'],'best_track_name':best['name'],'best_track_note_count':best['note_count'],'best_track_lyric_count':best['lyric_count'],'lyric_onset_alignment':round(best['lyric_onset_alignment'],4),'same_track_binding':best['same_track_binding'],'channel_prefix_binding':best['channel_prefix_binding'],'best_track_channels':';'.join(map(str,best['channels']))}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--audit',required=True);ap.add_argument('--midi-dir',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 rows=list(csv.DictReader(Path(a.audit).open(encoding='utf-8')));out=[]
 for r in rows:
  p=Path(a.midi_dir)/(r['md5'].lower()+'.mid')
  ev=inspect_midi(str(p)) if p.exists() else {'binding_status':'MIDI_MISSING'}
  selected=str(r.get('melody_track_name') or '')
  name_match=bool(selected and ev.get('best_track_name') and selected.strip().lower()==str(ev['best_track_name']).strip().lower())
  out.append({'md5':r['md5'],'title':r.get('title',''),'artist':r.get('artist',''),'analyzer_selected_track':selected,'analyzer_selected_vs_binding_track_name_match':name_match,**ev})
 fields=sorted({k for x in out for k in x});op=Path(a.output);op.parent.mkdir(parents=True,exist_ok=True)
 with op.open('w',newline='',encoding='utf-8') as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(out)
 strong={'DIRECT_CHANNEL_PREFIX_LYRIC_BINDING','DIRECT_SAME_TRACK_LYRIC_NOTE_BINDING','STRONG_TEMPORAL_LYRIC_NOTE_BINDING'};nstrong=sum(x.get('binding_status') in strong for x in out)
 summ={'schema':'HOOKLAB_MIDI_VOCAL_BINDING_AUDIT_v1.0','rows':len(out),'strong_symbolic_binding_n':nstrong,'strong_symbolic_binding_rate':nstrong/max(1,len(out)),'status_counts':{s:sum(x.get('binding_status')==s for x in out) for s in sorted({x.get('binding_status') for x in out})},'semantics':'SOURCE_INTERNAL_SYMBOLIC_VOCAL_BINDING_EVIDENCE_NOT_EXTERNAL_RECORDING_PROOF','tolerance_ticks':'ticks_per_beat/8','evidence_basis':'SMF lyric/text timing, same-track note events, and MIDI Channel Prefix when available'}
 op.with_suffix('.summary.json').write_text(json.dumps(summ,indent=2));print(json.dumps(summ))
if __name__=='__main__':main()
