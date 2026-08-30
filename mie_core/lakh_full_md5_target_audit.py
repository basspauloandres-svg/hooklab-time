#!/usr/bin/env python3
"""Stream LMD-full once and audit only known MD5 targets from massive-hit metadata matches.

This bypasses the clean-subset coverage problem. Matching is by exact MD5 filename stem,
then the extracted MIDI is audited for full-song structural plausibility and embedded
lyric/text events. Results remain TARGET_CANDIDATE_PENDING_IDENTITY_AUDIT until recording
identity and version are independently confirmed.
"""
import argparse,csv,io,json,re,statistics,tarfile,urllib.request
from pathlib import Path
import mido,pretty_midi

ARCHIVE='http://hog.ee.columbia.edu/craffel/lmd/lmd_full.tar.gz'

def lyric_events(raw):
    mf=mido.MidiFile(file=io.BytesIO(raw)); merged=mido.merge_tracks(mf.tracks)
    tempo=500000;t=0.;out=[]
    for msg in merged:
        t+=mido.tick2second(msg.time,mf.ticks_per_beat,tempo)
        if msg.type=='set_tempo':tempo=msg.tempo
        if msg.type in ('lyrics','text'):
            txt=str(getattr(msg,'text','')).strip()
            if txt and not txt.startswith('@') and len(txt)<=160:out.append((t,txt,msg.type))
    return out

def candidate_track(pm):
    end=pm.get_end_time(); ranked=[]
    for inst in pm.instruments:
        if inst.is_drum or not inst.notes:continue
        ns=sorted(inst.notes,key=lambda n:n.start); pitches=[n.pitch for n in ns]
        span=max(n.end for n in ns)-min(n.start for n in ns)
        ov=sum(ns[i+1].start<ns[i].end-.03 for i in range(len(ns)-1))/max(1,len(ns)-1)
        med=statistics.median(pitches)
        score=(2 if ov<=.12 else 0)+(2 if span>=end*.55 else 0)+(2 if 48<=med<=84 else 0)+(2 if 5<=max(pitches)-min(pitches)<=36 else 0)
        ranked.append((score,inst,ns,pitches,ov))
    ranked.sort(key=lambda x:x[0],reverse=True);return ranked[0] if ranked else None

def near_tactus(pm,notes):
    beats=pm.get_beats()
    if len(beats)<2 or not notes:return None
    return sum(min(abs(float(b)-n.start) for b in beats)<=.08 for n in notes)/len(notes)

def analyze(raw,target,member):
    pm=pretty_midi.PrettyMIDI(io.BytesIO(raw));dur=pm.get_end_time();le=lyric_events(raw);cand=candidate_track(pm)
    base={'title':target['title'],'artist':target['artist'],'year':target.get('year'),'md5':target['md5'],'archive_member':member,
          'duration_seconds':dur,'lyric_event_count':len(le),'coverage':'FULL_SONG' if dur>=90 else 'INSUFFICIENT','evidence_role':'TARGET_CANDIDATE_PENDING_IDENTITY_AUDIT'}
    if not cand:return base|{'structural_status':'NO_MELODY_CANDIDATE','full_tmt_candidate':False}
    score,inst,notes,pitches,ov=cand; text=' '.join(x[1] for x in le);tokens=re.findall(r"[A-Za-zÀ-ÿ0-9']+",text)
    tempi=pm.get_tempo_changes()[1]
    tmt=dur>=90 and score>=6 and len(tokens)>=20 and len(le)>=20
    return base|{'structural_status':'FULLSONG_SYMBOLIC_AUDIT_PASS' if dur>=90 and score>=6 else 'SYMBOLIC_AUDIT_REQUIRED',
      'full_tmt_candidate':tmt,'tempo_bpm':float(statistics.median(tempi)) if len(tempi) else None,
      'melodic_register_midi':float(statistics.median(pitches)),'melodic_range_semitones':max(pitches)-min(pitches),
      'melodic_events_per_token':len(notes)/len(tokens) if tokens else None,'near_tactus_share':near_tactus(pm,notes),
      'text_token_count':len(tokens),'text_line_count':1+sum(1 for a,b in zip(le,le[1:]) if b[0]-a[0]>=1.4) if le else 0,
      'melody_event_count':len(notes),'melody_track_name':inst.name,'melody_overlap_ratio':ov,'melody_candidate_score':score,
      'text_alignment':'MIDI_META_EVENT_TIMED' if le else 'NONE'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--targets',required=True);ap.add_argument('--output-dir',required=True);ap.add_argument('--archive-url',default=ARCHIVE);a=ap.parse_args()
    obj=json.loads(Path(a.targets).read_text());targets=obj.get('high_priority_identity_audit',obj.get('targets',obj));by={x['md5'].lower():x for x in targets}
    remaining=set(by);out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True);rows=[];members=0
    req=urllib.request.Request(a.archive_url,headers={'User-Agent':'HookLabPrototype/1.0'})
    with urllib.request.urlopen(req,timeout=300) as resp,tarfile.open(fileobj=resp,mode='r|gz') as tar:
      for m in tar:
        if not remaining:break
        if not m.isfile() or not m.name.lower().endswith(('.mid','.midi','.kar')):continue
        members+=1;stem=Path(m.name).stem.lower()
        if stem not in remaining:continue
        raw=tar.extractfile(m).read();r=analyze(raw,by[stem],m.name);rows.append(r);(out/f'{stem}.mid').write_bytes(raw);remaining.remove(stem)
    if rows:
      fields=sorted({k for r in rows for k in r})
      with (out/'target_audit.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    summary={'schema':'HOOKLAB_LMD_FULL_MD5_TARGET_AUDIT_v1.0','archive':a.archive_url,'targets':len(by),'found':len(rows),'missing_md5':sorted(remaining),
      'full_tmt_candidates':sum(bool(r.get('full_tmt_candidate')) for r in rows),'members_scanned':members,
      'promotion_rule':'No row becomes massive-hit evidence until identity/version and success-evidence gates pass.'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps(summary))
    raise SystemExit(0 if rows else 4)
if __name__=='__main__':main()
