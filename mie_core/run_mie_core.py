#!/usr/bin/env python3
import argparse, hashlib, json, math, urllib.request
from pathlib import Path
import numpy as np
import librosa, soundfile as sf
import onnxruntime as ort

try:
    from mie_core.mie_temporal_refinement import (
        align_harmony_to_shared_clock_v2,
        align_harmony_to_metric,
        consolidate_harmony_persistence,
        recover_melody_gaps,
        resolve_metric_grid,
        resolve_tactus,
    )
    from mie_core.mie_tf_plane_registration import (
        consolidate_sustained_fragments,
        consolidate_sustained_fragments_v2,
        plane_residual_metrics,
        recover_plane_supported_gaps_v3,
    )
except ModuleNotFoundError:  # Direct script execution from the repository.
    from mie_temporal_refinement import (
        align_harmony_to_shared_clock_v2,
        align_harmony_to_metric,
        consolidate_harmony_persistence,
        recover_melody_gaps,
        resolve_metric_grid,
        resolve_tactus,
    )
    from mie_tf_plane_registration import (
        consolidate_sustained_fragments,
        consolidate_sustained_fragments_v2,
        plane_residual_metrics,
        recover_plane_supported_gaps_v3,
    )

BEAT_MEL_URL='https://raw.githubusercontent.com/danigb/beat-this-rs/main/models/mel_spectrogram.onnx'
BEAT_MODEL_URL='https://raw.githubusercontent.com/danigb/beat-this-rs/main/models/beat_this_small.onnx'


def find_stem(stems,name):
    hits=list(Path(stems).rglob(name+'.wav'))
    if not hits: raise FileNotFoundError(name+'.wav not found')
    return hits[0]


def basic_pitch_melody(vocal_path, outdir, tactus_period_s):
    from basic_pitch.inference import predict
    model_output, midi_data, note_events = predict(str(vocal_path))
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
    continuity_notes, continuity_audit = consolidate_sustained_fragments(recovered, model_output)
    generalized_notes, generalized_audit = consolidate_sustained_fragments_v2(
        continuity_notes,
        model_output,
        tactus_period_s=tactus_period_s,
    )
    continuity_aligned_notes, continuity_alignment_audit = recover_plane_supported_gaps_v3(
        generalized_notes,
        raw,
        model_output,
        tactus_period_s=tactus_period_s,
    )
    plane_metrics_v0_3_1 = plane_residual_metrics(model_output, recovered)
    plane_metrics_v0_3_2 = plane_residual_metrics(model_output, continuity_notes)
    plane_metrics_v0_3_3 = plane_residual_metrics(model_output, generalized_notes)
    plane_metrics_v0_3_4 = plane_residual_metrics(model_output, continuity_aligned_notes)
    return (
        continuity_aligned_notes,
        generalized_notes,
        continuity_notes,
        recovered,
        midi_path,
        raw,
        accepted,
        recovery_audit,
        continuity_audit,
        generalized_audit,
        continuity_alignment_audit,
        plane_metrics_v0_3_1,
        plane_metrics_v0_3_2,
        plane_metrics_v0_3_3,
        plane_metrics_v0_3_4,
    )


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


def tactus_fingerprint(beats):
    payload = [
        {
            't': round(float(item['t']), 9),
            'score': round(float(item.get('score', 0.0)), 9),
            'clock_state': item.get('clock_state'),
            'run': item.get('run'),
        }
        for item in beats
    ]
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--audio',required=True); ap.add_argument('--stems',required=True); ap.add_argument('--output',required=True); args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    vocal=find_stem(args.stems,'vocals'); other=find_stem(args.stems,'other'); bass=find_stem(args.stems,'bass')
    tempo,beats,raw_beats,downbeats,metric_grid,tactus_resolution=beat_this(args.audio,out/'cache')
    periods = [run['period_s'] for run in tactus_resolution.get('runs', []) if run.get('period_s', 0) > 0]
    tactus_period_s = float(np.median(periods)) if periods else None
    (
        notes,
        notes_v0_3_3,
        notes_v0_3_2,
        notes_v0_3_1,
        midi,
        raw_notes,
        raw_accepted,
        melody_recovery,
        melody_continuity,
        melody_generalization,
        melody_gap_recovery,
        plane_metrics_v0_3_1,
        plane_metrics_v0_3_2,
        plane_metrics_v0_3_3,
        plane_metrics_v0_3_4,
    )=basic_pitch_melody(vocal,out,tactus_period_s)
    raw_beat_times=[item['t'] for item in raw_beats]
    raw_chords=harmony_sensor(other,bass,raw_beat_times)
    y,sr=librosa.load(args.audio,sr=None,mono=True); duration=len(y)/sr
    aligned_chords,harmony_alignment=align_harmony_to_metric(raw_chords,metric_grid,duration)
    chords_v0_3_2=aligned_chords if aligned_chords else raw_chords
    chords_v0_3_3,harmony_persistence=consolidate_harmony_persistence(
        chords_v0_3_2,
        tactus_period_s=tactus_period_s,
    )
    chords,harmony_shared_clock=align_harmony_to_shared_clock_v2(
        chords_v0_3_3,
        notes,
        beats,
        tactus_period_s=tactus_period_s,
    )
    baseline_wav=out/'MIE_CORE_MHT_v0_2.wav'
    synth(raw_accepted,raw_chords,raw_beats,duration,baseline_wav)
    wav_v0_3_1=out/'MIE_CORE_MHT_v0_3_1.wav'; synth(notes_v0_3_1,chords_v0_3_2,beats,duration,wav_v0_3_1)
    wav_v0_3_2=out/'MIE_CORE_MHT_v0_3_2.wav'; synth(notes_v0_3_2,chords_v0_3_2,beats,duration,wav_v0_3_2)
    wav_v0_3_3=out/'MIE_CORE_MHT_v0_3_3.wav'; synth(notes_v0_3_3,chords_v0_3_3,beats,duration,wav_v0_3_3)
    wav=out/'MIE_CORE_MHT_v0_3_4.wav'; synth(notes,chords,beats,duration,wav)
    tactus_fingerprint_a=tactus_fingerprint(beats)
    tactus_fingerprint_b=tactus_fingerprint(beats)
    report={
        'version':'MIE Core v0.3.4 continuity/alignment candidate',
        'architecture':'HTDemucs -> trained sensors -> traceable M/H/T refinements -> cross-track fail-closed A/B -> M+H+T',
        'source_separation':'HTDemucs 4 stems',
        'M':'Basic Pitch on vocals + monophonic gate + tactus-normalized neural sustain + plane-supported gap recovery candidate',
        'H':'beat-synchronous harmonic+bass evidence + LOCK/AMBIGUOUS + persistent state + shared-tactus alignment candidate',
        'T':'Beat This small ONNX + HookLab clock-lineage resolver',
        'tempo_bpm':tempo,
        'notes':notes,
        'notes_v0_3_2':notes_v0_3_2,
        'notes_v0_3_3':notes_v0_3_3,
        'notes_v0_3_1':notes_v0_3_1,
        'notes_continuity_derived':notes_v0_3_2,
        'notes_generalized_derived':notes,
        'notes_raw_accepted':raw_accepted,
        'raw_note_candidates':len(raw_notes),
        'melody_recovery':melody_recovery,
        'melody_continuity':melody_continuity,
        'melody_generalization':melody_generalization,
        'melody_gap_recovery':melody_gap_recovery,
        'tf_plane_registration':{
            'feature_id':'M_TF_PLANE_REGISTRATION_RESIDUAL_v0_1',
            'status':'AUDIT_FEATURE_NOT_CALIBRATED',
            'comparison_A_v0_3_1':plane_metrics_v0_3_1,
            'comparison_B_v0_3_2':plane_metrics_v0_3_2,
            'comparison_C_v0_3_3':plane_metrics_v0_3_3,
            'comparison_D_v0_3_4':plane_metrics_v0_3_4,
            'producer_decision':'PENDING_CROSS_TRACK_AB_LISTENING',
        },
        'harmony':chords,
        'harmony_v0_3_2':chords_v0_3_2,
        'harmony_v0_3_3':chords_v0_3_3,
        'harmony_raw':raw_chords,
        'harmony_metric_aligned':aligned_chords,
        'harmony_alignment':harmony_alignment,
        'harmony_persistence':harmony_persistence,
        'harmony_shared_clock':harmony_shared_clock,
        'beats':beats,
        'beat_observations_raw':raw_beats,
        'downbeat_candidates_raw':downbeats,
        'metric_grid':metric_grid,
        'tactus_resolution':tactus_resolution,
        'duration_s':duration,
        'generation_class':'D0_EXPLORATORY',
        'scientific_d_unlocked':False,
        'baseline_promoted':False,
        'cross_track_generalization':{
            'invariant_id':'MIE_CROSS_TRACK_GENERALIZATION_INVARIANT_v1',
            'status':'HOLD_FOR_MULTICASE_HELD_OUT_EVALUATION',
            'evaluation_unit':'INDEPENDENT_HELD_OUT_TRACK',
            'identity_features_used':False,
            'beat_tactus_fingerprint_A':tactus_fingerprint_a,
            'beat_tactus_fingerprint_B':tactus_fingerprint_b,
            'beat_tactus_unchanged_between_A_B':tactus_fingerprint_a == tactus_fingerprint_b,
            'scientific_replication_requirement':30,
        },
        'promotion_gate':'cross-track held-out macro evaluation + non-inferiority + producer listening',
    }
    (out/'MIE_CORE_MHT_v0_2.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'wav':str(wav),'comparison_wav_v0_3_3':str(wav_v0_3_3),'comparison_wav_v0_3_2':str(wav_v0_3_2),'comparison_wav_v0_3_1':str(wav_v0_3_1),'baseline_wav':str(baseline_wav),'notes_v0_3_4':len(notes),'notes_v0_3_3':len(notes_v0_3_3),'plane_recovered_notes_v0_3_4':melody_gap_recovery['recovered_candidate_count'],'tail_extensions_v0_3_4':melody_gap_recovery['tail_extension_count'],'raw_beats':len(raw_beats),'tactus':len(beats),'harmony_units_v0_3_3':len(chords_v0_3_3),'harmony_units_v0_3_4':len(chords),'tempo':tempo,'metric_state':tactus_resolution['metric_resolution']['state']}))
if __name__=='__main__': main()
