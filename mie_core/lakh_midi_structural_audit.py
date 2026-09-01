#!/usr/bin/env python3
"""Audit a candidate Lakh MIDI before it can represent a full song in HookLab.

This gate does not assume that any MIDI track is the vocal melody. It measures global
coverage, tempo/meter availability, track note density, polyphony and pitch range, and
returns ranked melody-track candidates for later identity/audio-reference validation.
"""
import argparse,json,statistics
from pathlib import Path
try:
 import pretty_midi
except ImportError:
 raise SystemExit('pretty_midi required')

def track_stats(inst):
 notes=sorted(inst.notes,key=lambda n:n.start)
 if not notes:return None
 pitches=[n.pitch for n in notes];dur=max(n.end for n in notes)-min(n.start for n in notes)
 overlaps=0
 for i,n in enumerate(notes[:-1]):
  if notes[i+1].start < n.end-0.03: overlaps+=1
 return {'name':inst.name,'program':inst.program,'is_drum':inst.is_drum,'notes':len(notes),'start':min(n.start for n in notes),'end':max(n.end for n in notes),
         'active_span_seconds':dur,'median_pitch':statistics.median(pitches),'pitch_range':max(pitches)-min(pitches),
         'overlap_ratio':overlaps/max(1,len(notes)-1),'notes_per_second':len(notes)/max(dur,.001)}

def melody_score(s,total):
 if s['is_drum']:return -999
 score=0
 score+=2 if s['overlap_ratio']<=.12 else 0
 score+=2 if 48<=s['median_pitch']<=84 else 0
 score+=2 if 5<=s['pitch_range']<=36 else 0
 score+=2 if .4<=s['notes_per_second']<=6 else 0
 score+=2 if s['active_span_seconds']>=total*.55 else 0
 return score

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--midi',required=True);ap.add_argument('--output',required=True);ap.add_argument('--expected-duration',type=float);a=ap.parse_args()
 pm=pretty_midi.PrettyMIDI(a.midi);end=pm.get_end_time();tempi=pm.get_tempo_changes();ts=pm.time_signature_changes
 tracks=[x for x in (track_stats(i) for i in pm.instruments) if x]
 for x in tracks:x['melody_candidate_score']=melody_score(x,end)
 tracks.sort(key=lambda x:x['melody_candidate_score'],reverse=True)
 dur_delta=abs(end-a.expected_duration) if a.expected_duration else None
 coverage_ok=end>=90 and (dur_delta is None or dur_delta<=15)
 candidates=[x for x in tracks if x['melody_candidate_score']>=6][:5]
 status='FULLSONG_SYMBOLIC_AUDIT_PASS' if coverage_ok and candidates else 'SYMBOLIC_AUDIT_REQUIRED'
 out={'schema':'HOOKLAB_LAKH_MIDI_STRUCTURAL_AUDIT_v1.0','status':status,'midi_end_seconds':end,'expected_duration_seconds':a.expected_duration,
      'duration_delta_seconds':dur_delta,'coverage_ok':coverage_ok,'tempo_event_count':len(tempi[0]),'time_signature_count':len(ts),
      'melody_track_candidates':candidates,'all_tracks':tracks,
      'rule':'A ranked track is only a vocal-melody candidate; it must still pass recording identity and melodic plausibility/reference validation before M_FULL.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':status,'duration':end,'tracks':len(tracks),'melody_candidates':len(candidates)}))
 raise SystemExit(0 if status.endswith('PASS') else 4)
if __name__=='__main__':main()
