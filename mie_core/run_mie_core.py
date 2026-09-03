#!/usr/bin/env python3
import argparse, json, math, urllib.request
from pathlib import Path
import numpy as np
import librosa, soundfile as sf
import onnxruntime as ort

try:
    from mie_core.mie_temporal_refinement import (
        align_harmony_to_metric,
        recover_melody_gaps,
        resolve_metric_grid,
        resolve_tactus,
    )
except ModuleNotFoundError:  # Direct script execution from the repository.
    from mie_temporal_refinement import (
        align_harmony_to_metric,
        recover_melody_gaps,
        resolve_metric_grid,
        resolve_tactus,
    )

BEAT_MEL_URL='https://raw.githubusercontent.com/danigb/beat-this-rs/main/models/mel_spectrogram.onnx'
BEAT_MODEL_URL='https://raw.githubusercontent.com/danigb/beat-this-rs/main/models/beat_this_small.onnx'


def find_stem(stems,name):
    hits=list(Path(stems).rglob(name+'.wav'))
    if not hits: raise FileNotFoundError(name+'.wav not found')
    return hits[0]


def basic_pitch_melody(vocal_path, outdir):
    from basic_pitch.inference import predict
    _, midi_data, note_events = predict(str(vocal_path))
    midi_path=outdir/'melody_basic_pitch.mid'
    midi_data.write(str(midi_path))
    raw=[]
    for ev in note_events:
        raw.append({'start_s':float(ev[0]),'end_s':float(ev[1]),'midi':int(ev[2]),'confidence':float(ev[3])})
    # MIE monophonic fusion gate: confidence + duration + local continuity.
    eligible=[n for n in raw if n['confidence']>=0.28 and n['end_s']-n['start_s']>=0.045]
    eligible.sort(key=lambda n:(n['start_s'],-n['confidence']))
    accepted=[]
    for n in eligible:
        overlaps=[q for q in accepted if min(q['end_s'],n['end_s'])-max(q['start_s'],n['start_s'])>0.025]
        if not overlaps:
            accepted.append(n); continue
        strongest=max(overlaps,key=lambda q:q['confidence'])
        prev=accepted[-1] if accepted else None
        continuity=0 if prev is None else abs(n['midi']-prev['midi'])
        old_cont=0 if prev is None else abs(strongest['midi']-prev['midi'])
        if n['confidence']>strongest['confidence']+0.08 or (continuity+2<old_cont and n['confidence']>=strongest['confidence']-0.04):
            accepted.remove(strongest); accepted.append(n)
    accepted.sort(key=lambda n:n['start_s'])
    recovered,recovery_audit=recover_melody_gaps(raw,accepted)
    return recovered, midi_path, raw, accepted, recovery_audit


def download(url,path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists(): urllib.request.urlretrieve(url,path)
    return path


def beat_this(audio, cache):
    y,sr=librosa.load(audio,sr=22050,mono=True)
    mel_path=download(BEAT_MEL_URL,Path(cache)/'mel_spectrogram.onnx')
    beat_path=download(BEAT_MODEL_URL,Path(cache)/'beat_this_small.onnx')
    providers=['CPUExecutionProvider']
    ms=ort.InferenceSession(str(mel_path),providers=providers)
    bs=ort.InferenceSession(str(beat_path),providers=providers)
    x=y.astype(np.float32)[None,:]
    mo=ms.run(None,{ms.get_inputs()[0].name:x})[0]
    if mo.ndim==3: spec=mo[0]
    elif mo.ndim==2: spec=mo
    else: raise RuntimeError('Unexpected mel output shape '+str(mo.shape))
    frames,bands=spec.shape
    probs=[]; downbeat_probs=[]; chunk=1500; ov=12; step=chunk-2*ov
    for st in range(0,frames,step):
        ar=spec[st:min(frames,st+chunk)].astype(np.float32)[None,:,:]
        outputs=bs.run(None,{bs.get_inputs()[0].name:ar})
        z=np.asarray(outputs[0]).reshape(-1)
        dz=np.asarray(outputs[1]).reshape(-1) if len(outputs)>1 else None
        n=ar.shape[1]; L=ov if st else 0; R=ov if st+n<frames else 0
        for j in range(L,n-R):
            probs.append((st+j,1.0/(1.0+math.exp(-float(z[j])))))
            if dz is not None:
                downbeat_probs.append((st+j,1.0/(1.0+math.exp(-float(dz[j])))))

    def peak_pick(values, threshold, separation):
        peaks=[]
        for i in range(1,len(values)-1):
            fr,v=values[i]
            if v>=threshold and v>=values[i-1][1] and v>values[i+1][1]:
                peaks.append((fr*.02,v))
        peaks=sorted(peaks,key=lambda q:q[1],reverse=True)
        keep=[]
        for t,v in peaks:
            if all(abs(t-k[0])>=separation for k in keep):
                keep.append((t,v))
        keep.sort()
        return [{'t':float(t),'score':float(v)} for t,v in keep]

    raw_beats=peak_pick(probs,.5,.16)
    raw_downbeats=peak_pick(downbeat_probs,.5,.30) if downbeat_probs else []
    tactus,tactus_audit=resolve_tactus(raw_beats,len(y)/sr)
    metric_grid,metric_audit=resolve_metric_grid(tactus,raw_downbeats)
    tactus_audit['metric_resolution']=metric_audit
    return tactus_audit['tempo_bpm'],tactus,raw_beats,raw_downbeats,metric_grid,tactus_audit


def load_mix(paths,sr=22050):
    ys=[]; maxn=0
    for p in paths:
        y,_=librosa.load(p,sr=sr,mono=True); ys.append(y); maxn=max(maxn,len(y))
    z=np.zeros(maxn,np.float32)
    for y in ys: z[:len(y)]+=y
    mx=np.max(np.abs(z));
    if mx>1: z/=mx
    return z,sr


def harmony_sensor(other_path,bass_path,beats):
    y,sr=load_mix([other_path,bass_path],22050)
    yh=librosa.effects.harmonic(y)
    hop=512
    chroma=librosa.feature.chroma_cqt(y=yh,sr=sr,hop_length=hop)
    yb,_=librosa.load(bass_path,sr=sr,mono=True)
    bass_chroma=librosa.feature.chroma_cqt(y=librosa.effects.harmonic(yb),sr=sr,hop_length=hop)
    ft=librosa.frames_to_time(np.arange(chroma.shape[1]),sr=sr,hop_length=hop)
    duration=len(y)/sr
    bounds=sorted(set([0.0]+[b for b in beats if 0<b<duration]+[duration]))
    qualities=[('maj',[0,4,7]),('min',[0,3,7]),('7',[0,4,7,10]),('maj7',[0,4,7,11]),('min7',[0,3,7,10]),('sus4',[0,5,7])]
    templates=[]
    for root in range(12):
        for qual,ints in qualities:
            q=np.zeros(12); q[[(root+i)%12 for i in ints]]=1; q/=np.linalg.norm(q)
            templates.append((root,qual,ints,q))
    out=[]
    for a,b in zip(bounds[:-1],bounds[1:]):
        mask=(ft>=a)&(ft<b)
        if not mask.any(): continue
        v=chroma[:,mask].mean(1); nv=np.linalg.norm(v)
        if nv<1e-8: continue
        vn=v/nv
        bv=bass_chroma[:,mask].mean(1) if bass_chroma.shape[1]>=mask.size else np.zeros(12)
        bass_pc=int(np.argmax(bv)) if np.max(bv)>0 else None
        ranked=[]
        for root,qual,ints,q in templates:
            spectral=float(vn@q)
            bass_bonus=.08 if bass_pc==root else (.025 if bass_pc==(root+7)%12 else 0)
            outside=float(np.mean([vn[i] for i in range(12) if i not in [(root+j)%12 for j in ints]]))
            score=spectral+bass_bonus-.12*outside
            ranked.append((score,root,qual,ints,spectral,bass_bonus))
        ranked.sort(reverse=True)
        s1,r,ql,ints,sp,bb=ranked[0]; s2=ranked[1][0]; margin=s1-s2
        state='LOCK' if margin>=0.035 and sp>=0.45 else 'AMBIGUOUS'
        out.append({'start_s':float(a),'end_s':float(b),'root_pc':int(r),'quality':ql,'intervals':ints,'evidence':float(sp),'bass_bonus':float(bb),'margin':float(margin),'state':state})
    return out


def synth(notes,chords,beats,duration,outwav,sr=44100):
    z=np.zeros(int(duration*sr)+1,np.float32)
    # melody: soft additive lead
    for n in notes:
        a=max(0,int(n['start_s']*sr)); b=min(len(z),int(n['end_s']*sr))
        if b<=a: continue
        t=np.arange(b-a)/sr; f=librosa.midi_to_hz(n['midi']); amp=.13*max(.25,min(1,n['confidence']))
        env=np.clip(np.minimum(1,t/.018)*np.minimum(1,np.maximum(0,(n['end_s']-n['start_s']-t)/.035)),0,1)
        wave=np.sin(2*np.pi*f*t)+.22*np.sin(4*np.pi*f*t)+.08*np.sin(6*np.pi*f*t)
        z[a:b]+=amp*env*wave
    # harmony: warm root-position voicing with bass root
    for c in chords:
        if c['state']!='LOCK': continue
        a=int(c['start_s']*sr); b=min(len(z),int(c['end_s']*sr))
        if b<=a: continue
        t=np.arange(b-a)/sr
        env=np.clip(np.minimum(1,t/.035)*np.minimum(1,np.maximum(0,(c['end_s']-c['start_s']-t)/.07)),0,1)
        root=48+c['root_pc']
        for j,iv in enumerate(c['intervals']):
            f=librosa.midi_to_hz(root+iv); z[a:b]+=(.031 if j else .038)*env*(np.sin(2*np.pi*f*t)+.12*np.sin(4*np.pi*f*t))
        bf=librosa.midi_to_hz(root-12); z[a:b]+=.028*env*np.sin(2*np.pi*bf*t)
    # Beat This clicks
    for item in beats:
        bt=item['t'] if isinstance(item,dict) else item
        strength=item.get('metric_strength') if isinstance(item,dict) else None
        a=int(bt*sr); b=min(len(z),a+int(.055*sr)); t=np.arange(b-a)/sr
        freq=1100 if strength=='DOWNBEAT' else (950 if strength=='STRONG' else 820)
        amp=.16 if strength=='DOWNBEAT' else (.13 if strength=='STRONG' else .11)
        z[a:b]+=amp*np.exp(-t/.014)*np.sin(2*np.pi*freq*t)
    mx=np.max(np.abs(z));
    if mx>0: z=.92*z/mx
    sf.write(outwav,z,sr)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--audio',required=True); ap.add_argument('--stems',required=True); ap.add_argument('--output',required=True); args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    vocal=find_stem(args.stems,'vocals'); other=find_stem(args.stems,'other'); bass=find_stem(args.stems,'bass')
    notes,midi,raw_notes,raw_accepted,melody_recovery=basic_pitch_melody(vocal,out)
    tempo,beats,raw_beats,downbeats,metric_grid,tactus_resolution=beat_this(args.audio,out/'cache')
    raw_beat_times=[item['t'] for item in raw_beats]
    raw_chords=harmony_sensor(other,bass,raw_beat_times)
    y,sr=librosa.load(args.audio,sr=None,mono=True); duration=len(y)/sr
    aligned_chords,harmony_alignment=align_harmony_to_metric(raw_chords,metric_grid,duration)
    chords=aligned_chords if aligned_chords else raw_chords
    baseline_wav=out/'MIE_CORE_MHT_v0_2.wav'
    synth(raw_accepted,raw_chords,raw_beats,duration,baseline_wav)
    wav=out/'MIE_CORE_MHT_v0_3_1.wav'; synth(notes,chords,beats,duration,wav)
    report={
        'version':'MIE Core v0.3.1',
        'architecture':'HTDemucs -> trained sensors -> traceable M/H/T refinements -> M+H+T',
        'source_separation':'HTDemucs 4 stems',
        'M':'Basic Pitch on vocals + MIE monophonic gate + conservative candidate gap recovery',
        'H':'beat-synchronous harmonic+bass evidence + LOCK/AMBIGUOUS + metric-aligned derived layer',
        'T':'Beat This small ONNX + HookLab clock-lineage resolver',
        'tempo_bpm':tempo,
        'notes':notes,
        'notes_raw_accepted':raw_accepted,
        'raw_note_candidates':len(raw_notes),
        'melody_recovery':melody_recovery,
        'harmony':chords,
        'harmony_raw':raw_chords,
        'harmony_metric_aligned':aligned_chords,
        'harmony_alignment':harmony_alignment,
        'beats':beats,
        'beat_observations_raw':raw_beats,
        'downbeat_candidates_raw':downbeats,
        'metric_grid':metric_grid,
        'tactus_resolution':tactus_resolution,
        'duration_s':duration,
        'generation_class':'D0_EXPLORATORY',
        'scientific_d_unlocked':False,
        'baseline_promoted':False,
        'promotion_gate':'auditory recognizability + blind generic-song regression',
    }
    (out/'MIE_CORE_MHT_v0_2.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'wav':str(wav),'baseline_wav':str(baseline_wav),'notes':len(notes),'recovered_notes':melody_recovery['recovered_candidate_count'],'raw_beats':len(raw_beats),'tactus':len(beats),'harmony_units':len(chords),'tempo':tempo,'metric_state':tactus_resolution['metric_resolution']['state']}))
if __name__=='__main__': main()
