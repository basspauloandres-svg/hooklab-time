#!/usr/bin/env python3
import argparse, json, subprocess
from pathlib import Path
import numpy as np
import librosa, soundfile as sf


def find_vocals(stems):
    hits=list(Path(stems).rglob('vocals.wav'))
    if not hits: raise FileNotFoundError('Demucs vocals.wav not found')
    return hits[0]

def basic_pitch_melody(vocal_path, outdir):
    from basic_pitch.inference import predict
    model_output, midi_data, note_events = predict(str(vocal_path))
    midi_path=outdir/'melody_basic_pitch.mid'
    midi_data.write(str(midi_path))
    notes=[]
    for ev in note_events:
        # Basic Pitch event tuple: start, end, pitch, amplitude, pitch_bends(optional)
        notes.append({'start_s':float(ev[0]),'end_s':float(ev[1]),'midi':int(ev[2]),'confidence':float(ev[3])})
    return notes, midi_path

def beat_sensor(audio):
    # Temporary server-side beat observation. Beat This remains target T sensor.
    y,sr=librosa.load(audio,sr=22050,mono=True)
    tempo,frames=librosa.beat.beat_track(y=y,sr=sr,hop_length=512)
    return float(np.asarray(tempo).reshape(-1)[0]), librosa.frames_to_time(frames,sr=sr,hop_length=512).tolist()

def harmony_sensor(audio, beats):
    y,sr=librosa.load(audio,sr=22050,mono=True)
    yh=librosa.effects.harmonic(y)
    chroma=librosa.feature.chroma_cqt(y=yh,sr=sr,hop_length=512)
    ft=librosa.frames_to_time(np.arange(chroma.shape[1]),sr=sr,hop_length=512)
    bounds=[0.0]+beats+[len(y)/sr]
    templates=[]
    for root in range(12):
        for qual,ints in [('maj',[0,4,7]),('min',[0,3,7])]:
            q=np.zeros(12); q[[(root+i)%12 for i in ints]]=1; q/=np.linalg.norm(q)
            templates.append((root,qual,q))
    out=[]
    for a,b in zip(bounds[:-1],bounds[1:]):
        mask=(ft>=a)&(ft<b)
        if not mask.any(): continue
        v=chroma[:,mask].mean(1); nv=np.linalg.norm(v)
        if nv<1e-9: continue
        vn=v/nv; ranked=sorted([(float(vn@q),r,ql) for r,ql,q in templates],reverse=True)
        s1,r,ql=ranked[0]; margin=s1-ranked[1][0]
        out.append({'start_s':a,'end_s':b,'root_pc':r,'quality':ql,'evidence':s1,'margin':margin,'state':'LOCK' if margin>=0.05 else 'AMBIGUOUS'})
    return out

def synth(notes,chords,beats,duration,outwav,sr=44100):
    z=np.zeros(int(duration*sr)+1,np.float32)
    for n in notes:
        a=max(0,int(n['start_s']*sr)); b=min(len(z),int(n['end_s']*sr));
        if b<=a: continue
        t=np.arange(b-a)/sr; f=librosa.midi_to_hz(n['midi']); amp=.12*max(.2,min(1,n['confidence']))
        env=np.minimum(1,t/.01)*np.minimum(1,np.maximum(0,(n['end_s']-n['start_s']-t)/.03))
        z[a:b]+=amp*env*np.sin(2*np.pi*f*t)
    for c in chords:
        if c['state']!='LOCK': continue
        a=int(c['start_s']*sr); b=min(len(z),int(c['end_s']*sr));
        if b<=a: continue
        t=np.arange(b-a)/sr; ints=[0,4,7] if c['quality']=='maj' else [0,3,7]
        env=np.minimum(1,t/.02)*np.minimum(1,np.maximum(0,(c['end_s']-c['start_s']-t)/.04))
        for iv in ints: z[a:b]+=.035*env*np.sin(2*np.pi*librosa.midi_to_hz(48+c['root_pc']+iv)*t)
    for bt in beats:
        a=int(bt*sr); b=min(len(z),a+int(.04*sr)); t=np.arange(b-a)/sr
        z[a:b]+=.14*np.exp(-t/.012)*np.sin(2*np.pi*900*t)
    mx=np.max(np.abs(z));
    if mx>0: z=.9*z/mx
    sf.write(outwav,z,sr)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--audio',required=True); ap.add_argument('--stems',required=True); ap.add_argument('--output',required=True); args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    vocal=find_vocals(args.stems)
    notes,midi=basic_pitch_melody(vocal,out)
    tempo,beats=beat_sensor(args.audio)
    chords=harmony_sensor(args.audio,beats)
    y,sr=librosa.load(args.audio,sr=None,mono=True); duration=len(y)/sr
    synth(notes,chords,beats,duration,out/'MIE_CORE_MHT_v0_1.wav')
    report={'version':'MIE Core v0.1','architecture':'trained sensors -> MIE fusion -> M+H+T','source_separation':'HTDemucs vocals','M':'Basic Pitch on separated vocals','H':'beat-synchronous harmonic evidence + LOCK/AMBIGUOUS','T':'temporary server beat observation; replace with Beat This before promotion','tempo_bpm':tempo,'notes':notes,'harmony':chords,'beats_s':beats,'baseline_promoted':False,'promotion_gate':'Beat This T + blind generic-song listening'}
    (out/'MIE_CORE_MHT_v0_1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if __name__=='__main__': main()
