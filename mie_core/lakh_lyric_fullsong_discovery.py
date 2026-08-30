#!/usr/bin/env python3
"""Discover lyric-bearing full-song MIDI files from clean Lakh for the TMT test lane.

This is an engineering-only bridge to obtain synchronized Text events together with
full-song symbolic M/T. It is not massive-hit evidence and must remain isolated from
the scientific target cohort.
"""
import argparse,csv,io,json,math,re,statistics,tarfile,urllib.request
from pathlib import Path
import mido, pretty_midi

ARCHIVE='http://hog.ee.columbia.edu/craffel/lmd/clean_midi.tar.gz'

def lyric_events(raw):
    mf=mido.MidiFile(file=io.BytesIO(raw))
    merged=mido.merge_tracks(mf.tracks)
    tempo=500000; t=0.0; out=[]
    for msg in merged:
        t += mido.tick2second(msg.time,mf.ticks_per_beat,tempo)
        if msg.type=='set_tempo': tempo=msg.tempo
        if msg.type in ('lyrics','text'):
            txt=str(getattr(msg,'text','')).strip()
            if txt and not txt.startswith('@') and len(txt)<=120: out.append((t,txt,msg.type))
    return out

def track_candidate(pm):
    end=pm.get_end_time(); ranked=[]
    for inst in pm.instruments:
        if inst.is_drum or not inst.notes: continue
        ns=sorted(inst.notes,key=lambda n:n.start); pitches=[n.pitch for n in ns]
        span=max(n.end for n in ns)-min(n.start for n in ns)
        ov=sum(ns[i+1].start < ns[i].end-.03 for i in range(len(ns)-1))/max(1,len(ns)-1)
        med=statistics.median(pitches); score=(2 if ov<.12 else 0)+(2 if span>=end*.55 else 0)+(2 if 48<=med<=84 else 0)+(1 if 5<=max(pitches)-min(pitches)<=36 else 0)
        ranked.append((score,inst,ns,pitches,ov))
    ranked.sort(key=lambda x:x[0],reverse=True)
    return ranked[0] if ranked else None

def line_count(events):
    explicit=sum(1 for _,t,_ in events if '\n' in t or '/' in t or '\\' in t)
    if explicit: return max(1,explicit)
    times=[t for t,_,_ in events]
    return 1+sum(1 for a,b in zip(times,times[1:]) if b-a>=1.4)

def near_tactus_share(pm, notes):
    beats=pm.get_beats()
    if len(beats)<2 or not notes:return None
    tol=.08; hit=0
    for n in notes:
        if min(abs(float(b)-n.start) for b in beats) <= tol: hit+=1
    return hit/len(notes)

def row_from(raw,name):
    le=lyric_events(raw)
    if len(le)<24:return None
    pm=pretty_midi.PrettyMIDI(io.BytesIO(raw)); dur=pm.get_end_time()
    if dur<90:return None
    cand=track_candidate(pm)
    if not cand:return None
    score,inst,notes,pitches,ov=cand
    if score<5:return None
    text=' '.join(x[1] for x in le)
    tokens=re.findall(r"[A-Za-zÀ-ÿ0-9']+",text)
    if len(tokens)<20:return None
    tempi=pm.get_tempo_changes()[1]
    nts=near_tactus_share(pm,notes)
    return {
      'song_id':re.sub(r'[^a-zA-Z0-9]+','_',Path(name).stem)[:80],
      'genre':'lakh_lyric_test','style':'full_tmt_symbolic','coverage':'FULL_SONG','strict_gate':'PASS',
      'tempo_bpm':float(statistics.median(tempi)) if len(tempi) else None,
      'melodic_register_midi':float(statistics.median(pitches)),
      'melodic_range_semitones':max(pitches)-min(pitches),
      'melodic_events_per_token':len(notes)/len(tokens),
      'near_tactus_share':nts,'text_line_count':line_count(le),
      'duration_seconds':dur,'lyric_event_count':len(le),'text_token_count':len(tokens),
      'melody_event_count':len(notes),'melody_track_name':inst.name,'melody_overlap_ratio':ov,
      'evidence_role':'TEST_LANE_ONLY_LAKH_LYRIC_MIDI','source_scope':'FULL_SONG_SYMBOLIC_WITH_EMBEDDED_TEXT',
      'text_alignment':'MIDI_META_EVENT_TIMED','archive_member':name
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);ap.add_argument('--target-n',type=int,default=5);ap.add_argument('--scan-max',type=int,default=2500);ap.add_argument('--archive-url',default=ARCHIVE);a=ap.parse_args()
    out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True);rows=[];scanned=0
    req=urllib.request.Request(a.archive_url,headers={'User-Agent':'HookLabPrototype/1.0'})
    with urllib.request.urlopen(req,timeout=180) as resp, tarfile.open(fileobj=resp,mode='r|gz') as tar:
      for m in tar:
        if scanned>=a.scan_max or len(rows)>=a.target_n:break
        if not m.isfile() or not m.name.lower().endswith(('.mid','.midi','.kar')):continue
        scanned+=1
        try:
          raw=tar.extractfile(m).read(); r=row_from(raw,m.name)
          if r:
            rows.append(r); (out/f"{len(rows):02d}_{r['song_id']}.mid").write_bytes(raw)
        except Exception: pass
    if rows:
      fields=sorted({k for r in rows for k in r})
      with (out/'matrix_x_full_tmt_test.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    summary={'schema':'HOOKLAB_LYRIC_FULLSONG_DISCOVERY_v1.0','status':'FULL_TMT_TEST_ROWS_FOUND' if len(rows)>=3 else 'INSUFFICIENT_FULL_TMT_TEST_ROWS','scanned':scanned,'found':len(rows),'target_n':a.target_n,'evidence_boundary':'TEST_LANE_ONLY; NOT MASSIVE_HIT_EVIDENCE'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
    raise SystemExit(0 if len(rows)>=3 else 4)
if __name__=='__main__':main()
