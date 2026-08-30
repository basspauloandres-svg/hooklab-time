#!/usr/bin/env python3
"""Stream LMD-full once and audit known MD5 targets from massive-hit metadata matches.

v1.1 improves vocal-melody candidate selection by conditioning track ranking on the
observed text-token count. A plausible vocal line should be relatively monophonic,
cover much of the song, lie in a vocal register, and have an event/token ratio in a
reasonable neighborhood of one. This remains a structural heuristic, not proof that
the selected track is the sung melody; recording/version and melodic-reference audits
remain mandatory before scientific promotion.
"""
import argparse,csv,io,json,math,re,statistics,tarfile,urllib.request
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

def candidate_track(pm,token_count):
    end=pm.get_end_time(); ranked=[]
    for inst in pm.instruments:
        if inst.is_drum or not inst.notes:continue
        ns=sorted(inst.notes,key=lambda n:n.start); pitches=[n.pitch for n in ns]
        span=max(n.end for n in ns)-min(n.start for n in ns); coverage=span/max(end,.001)
        ov=sum(ns[i+1].start<ns[i].end-.03 for i in range(len(ns)-1))/max(1,len(ns)-1)
        med=float(statistics.median(pitches)); pr=max(pitches)-min(pitches)
        ept=len(ns)/max(1,token_count)
        score=0.0
        # Text-conditioned density evidence: strongest around one melodic event per token.
        if token_count>=20:
            if .45<=ept<=1.8:
                denom=max(abs(math.log(.45)),abs(math.log(1.8)))
                score+=4.0*(1.0-abs(math.log(ept))/denom)
            elif .25<=ept<=2.5: score+=1.0
        if ov<=.08:score+=3
        elif ov<=.15:score+=2
        elif ov<=.25:score+=1
        if coverage>=.75:score+=2
        elif coverage>=.55:score+=1
        if 48<=med<=84:score+=1
        if 5<=pr<=36:score+=1
        ranked.append((score,inst,ns,pitches,ov,ept,coverage,pr,med))
    ranked.sort(key=lambda x:x[0],reverse=True);return ranked[0] if ranked else None

def near_tactus(pm,notes):
    beats=pm.get_beats()
    if len(beats)<2 or not notes:return None
    return sum(min(abs(float(b)-n.start) for b in beats)<=.08 for n in notes)/len(notes)

def analyze(raw,target,member):
    pm=pretty_midi.PrettyMIDI(io.BytesIO(raw));dur=pm.get_end_time();le=lyric_events(raw)
    text=' '.join(x[1] for x in le);tokens=re.findall(r"[A-Za-zÀ-ÿ0-9']+",text)
    cand=candidate_track(pm,len(tokens))
    base={'title':target['title'],'artist':target['artist'],'year':target.get('year'),'md5':target['md5'],'archive_member':member,
          'duration_seconds':dur,'lyric_event_count':len(le),'text_token_count':len(tokens),
          'coverage':'FULL_SONG' if dur>=90 else 'INSUFFICIENT','evidence_role':'TARGET_CANDIDATE_PENDING_IDENTITY_AUDIT'}
    if not cand:return base|{'structural_status':'NO_MELODY_CANDIDATE','full_tmt_candidate':False}
    score,inst,notes,pitches,ov,ept,track_cov,pr,med=cand; tempi=pm.get_tempo_changes()[1]
    # Engineering eligibility, deliberately stricter than v1.0.
    density_ok=.35<=ept<=2.0
    melody_ok=score>=7 and ov<=.25 and track_cov>=.55 and 5<=pr<=36 and 48<=med<=84 and density_ok
    text_ok=len(tokens)>=20 and len(le)>=20
    tmt=dur>=90 and melody_ok and text_ok
    return base|{'structural_status':'FULLSONG_SYMBOLIC_AUDIT_PASS' if dur>=90 and melody_ok else 'SYMBOLIC_AUDIT_REQUIRED',
      'full_tmt_candidate':tmt,'tempo_bpm':float(statistics.median(tempi)) if len(tempi) else None,
      'melodic_register_midi':med,'melodic_range_semitones':pr,'melodic_events_per_token':ept,
      'near_tactus_share':near_tactus(pm,notes),'text_line_count':1+sum(1 for a,b in zip(le,le[1:]) if b[0]-a[0]>=1.4) if le else 0,
      'melody_event_count':len(notes),'melody_track_name':inst.name,'melody_program':int(inst.program),
      'melody_overlap_ratio':ov,'melody_track_coverage':track_cov,'melody_candidate_score':score,
      'melody_density_gate':density_ok,'text_alignment':'MIDI_META_EVENT_TIMED' if le else 'NONE',
      'selection_semantics':'TEXT_CONDITIONED_STRUCTURAL_HEURISTIC_NOT_VOCAL_IDENTITY_PROOF'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--targets',required=True);ap.add_argument('--output-dir',required=True);ap.add_argument('--archive-url',default=ARCHIVE);a=ap.parse_args()
    obj=json.loads(Path(a.targets).read_text());targets=obj.get('high_priority_identity_audit',obj.get('targets',obj));by={x['md5'].lower():x for x in targets}
    remaining=set(by);out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True);rows=[];members=0
    req=urllib.request.Request(a.archive_url,headers={'User-Agent':'HookLabPrototype/1.1'})
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
    summary={'schema':'HOOKLAB_LMD_FULL_MD5_TARGET_AUDIT_v1.1','archive':a.archive_url,'targets':len(by),'found':len(rows),'missing_md5':sorted(remaining),
      'full_tmt_candidates':sum(bool(r.get('full_tmt_candidate')) for r in rows),'members_scanned':members,
      'promotion_rule':'No row becomes massive-hit evidence until identity/version, melodic-reference, genre/style and success-evidence gates pass.'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps(summary))
    raise SystemExit(0 if rows else 4)
if __name__=='__main__':main()
