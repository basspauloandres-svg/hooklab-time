#!/usr/bin/env python3
"""Audit known LMD-full MD5 targets, reusing a persistent local MIDI cache when present.

The expensive archive scan is acquisition-only. Once exact target MIDI files have been
resolved, future methodological refinements re-audit those cached symbolic files and do
not stream LMD-full again. This implements HookLab's offline/cache-first speed invariant.
"""
import argparse,csv,io,json,math,re,statistics,tarfile,urllib.request
from pathlib import Path
import mido,pretty_midi
ARCHIVE='http://hog.ee.columbia.edu/craffel/lmd/lmd_full.tar.gz'

def lyric_events(raw):
    mf=mido.MidiFile(file=io.BytesIO(raw)); merged=mido.merge_tracks(mf.tracks); tempo=500000;t=0.;out=[]
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
        ns=sorted(inst.notes,key=lambda n:n.start);p=[n.pitch for n in ns];span=max(n.end for n in ns)-min(n.start for n in ns);cov=span/max(end,.001)
        ov=sum(ns[i+1].start<ns[i].end-.03 for i in range(len(ns)-1))/max(1,len(ns)-1);med=float(statistics.median(p));pr=max(p)-min(p);ept=len(ns)/max(1,token_count)
        score=0.
        if token_count>=20:
            if .45<=ept<=1.8:
                denom=max(abs(math.log(.45)),abs(math.log(1.8)));score+=4.*(1.-abs(math.log(ept))/denom)
            elif .25<=ept<=2.5:score+=1.
        score += 3 if ov<=.08 else 2 if ov<=.15 else 1 if ov<=.25 else 0
        score += 2 if cov>=.75 else 1 if cov>=.55 else 0
        score += 1 if 48<=med<=84 else 0
        score += 1 if 5<=pr<=36 else 0
        ranked.append((score,inst,ns,p,ov,ept,cov,pr,med))
    ranked.sort(key=lambda x:x[0],reverse=True);return ranked[0] if ranked else None

def near_tactus(pm,notes):
    beats=pm.get_beats()
    if len(beats)<2 or not notes:return None
    return sum(min(abs(float(b)-n.start) for b in beats)<=.08 for n in notes)/len(notes)

def melodic_fingerprint(notes,pm):
    """Compact transposition-invariant contour/rhythm fingerprint for cross-arrangement comparison."""
    if len(notes)<3:return {'interval_histogram':'','rhythm_ratio_histogram':''}
    ints=[]
    for a,b in zip(notes,notes[1:]):
        d=max(-12,min(12,int(b.pitch-a.pitch)));ints.append(d)
    ih=[ints.count(i) for i in range(-12,13)];s=sum(ih) or 1;ih=[round(x/s,6) for x in ih]
    beats=pm.get_beats();beat=float(statistics.median([b-a for a,b in zip(beats,beats[1:])])) if len(beats)>2 else .5
    bins=[0,0,0,0,0]
    for a,b in zip(notes,notes[1:]):
        r=(b.start-a.start)/max(beat,.001)
        j=0 if r<.375 else 1 if r<.75 else 2 if r<1.5 else 3 if r<3 else 4;bins[j]+=1
    rs=sum(bins) or 1;rh=[round(x/rs,6) for x in bins]
    return {'interval_histogram':';'.join(map(str,ih)),'rhythm_ratio_histogram':';'.join(map(str,rh))}

def analyze(raw,target,member):
    pm=pretty_midi.PrettyMIDI(io.BytesIO(raw));dur=pm.get_end_time();le=lyric_events(raw);text=' '.join(x[1] for x in le);tokens=re.findall(r"[A-Za-zÀ-ÿ0-9']+",text);cand=candidate_track(pm,len(tokens))
    base={'title':target['title'],'artist':target['artist'],'year':target.get('year'),'md5':target['md5'],'primary_md5':target.get('primary_md5',''),'archive_member':member,'duration_seconds':dur,'lyric_event_count':len(le),'text_token_count':len(tokens),'coverage':'FULL_SONG' if dur>=90 else 'INSUFFICIENT','evidence_role':target.get('evidence_role','TARGET_CANDIDATE_PENDING_IDENTITY_AUDIT')}
    if not cand:return base|{'structural_status':'NO_MELODY_CANDIDATE','full_tmt_candidate':False}
    score,inst,notes,pitches,ov,ept,cov,pr,med=cand;tempi=pm.get_tempo_changes()[1];density_ok=.35<=ept<=2.;melody_ok=score>=7 and ov<=.25 and cov>=.55 and 5<=pr<=36 and 48<=med<=84 and density_ok;text_ok=len(tokens)>=20 and len(le)>=20;tmt=dur>=90 and melody_ok and text_ok;fp=melodic_fingerprint(notes,pm)
    return base|{'structural_status':'FULLSONG_SYMBOLIC_AUDIT_PASS' if dur>=90 and melody_ok else 'SYMBOLIC_AUDIT_REQUIRED','full_tmt_candidate':tmt,'tempo_bpm':float(statistics.median(tempi)) if len(tempi) else None,'melodic_register_midi':med,'melodic_range_semitones':pr,'melodic_events_per_token':ept,'near_tactus_share':near_tactus(pm,notes),'text_line_count':1+sum(1 for a,b in zip(le,le[1:]) if b[0]-a[0]>=1.4) if le else 0,'melody_event_count':len(notes),'melody_track_name':inst.name,'melody_program':int(inst.program),'melody_overlap_ratio':ov,'melody_track_coverage':cov,'melody_candidate_score':score,'melody_density_gate':density_ok,'text_alignment':'MIDI_META_EVENT_TIMED' if le else 'NONE','selection_semantics':'TEXT_CONDITIONED_STRUCTURAL_HEURISTIC_NOT_VOCAL_IDENTITY_PROOF',**fp}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--targets',required=True);ap.add_argument('--output-dir',required=True);ap.add_argument('--midi-cache-dir',default='');ap.add_argument('--archive-url',default=ARCHIVE);a=ap.parse_args()
    obj=json.loads(Path(a.targets).read_text());targets=obj.get('high_priority_identity_audit',obj.get('targets',obj));by={x['md5'].lower():x for x in targets};out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True);cache=Path(a.midi_cache_dir) if a.midi_cache_dir else out/'midi_cache';cache.mkdir(parents=True,exist_ok=True)
    remaining={md5 for md5 in by if not (cache/f'{md5}.mid').exists()};archive_scanned=False;members=0
    if remaining:
        archive_scanned=True;req=urllib.request.Request(a.archive_url,headers={'User-Agent':'HookLabPrototype/1.5'})
        with urllib.request.urlopen(req,timeout=300) as resp,tarfile.open(fileobj=resp,mode='r|gz') as tar:
            for m in tar:
                if not remaining:break
                if not m.isfile() or not m.name.lower().endswith(('.mid','.midi','.kar')):continue
                members+=1;stem=Path(m.name).stem.lower()
                if stem not in remaining:continue
                (cache/f'{stem}.mid').write_bytes(tar.extractfile(m).read());remaining.remove(stem)
    rows=[]
    for md5,t in by.items():
        p=cache/f'{md5}.mid'
        if not p.exists():continue
        rows.append(analyze(p.read_bytes(),t,p.name))
    if rows:
        fields=sorted({k for r in rows for k in r})
        with (out/'target_audit.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    summary={'schema':'HOOKLAB_LMD_FULL_MD5_TARGET_AUDIT_v1.3','archive':a.archive_url,'targets':len(by),'found':len(rows),'missing_md5':sorted(remaining),'full_tmt_candidates':sum(bool(r.get('full_tmt_candidate')) for r in rows),'archive_scanned_this_run':archive_scanned,'members_scanned_this_run':members,'cache_dir':str(cache),'melodic_fingerprint':'TRANSPOSTION_INVARIANT_INTERVAL_PLUS_NORMALIZED_RHYTHM','promotion_rule':'No row becomes massive-hit evidence until identity/version, melodic-reference, genre/style and success-evidence gates pass.'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps(summary));raise SystemExit(0 if rows else 4)
if __name__=='__main__':main()
