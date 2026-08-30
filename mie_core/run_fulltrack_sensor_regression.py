#!/usr/bin/env python3
"""Full-track autonomous M/T regression v0.2.
Acquires FULL audio into RAM, derives M, runs authoritative Beat This for T, persists derived JSON only, deletes audio in finally.
"""
import argparse, hashlib, json, os, subprocess, sys, tempfile, statistics
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--url',required=True); ap.add_argument('--song-id',required=True)
    ap.add_argument('--source-license',required=True); ap.add_argument('--output',required=True)
    ap.add_argument('--beat-this-bin',default='beat-this'); ap.add_argument('--beat-model',required=True); ap.add_argument('--mel-model',required=True)
    args=ap.parse_args(); out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    ram=Path('/dev/shm') if Path('/dev/shm').exists() else Path(tempfile.gettempdir())
    src=ram/f'tmt_{os.getpid()}.mp3'; wav=ram/f'tmt_{os.getpid()}.wav'; beats_file=ram/f'tmt_{os.getpid()}.beats'
    try:
        subprocess.run(['curl','-L','--fail','--silent','--show-error',args.url,'-o',str(src)],check=True)
        sha=hashlib.sha256(src.read_bytes()).hexdigest()
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-ar','22050','-ac','1',str(wav)],check=True)
        from basic_pitch.inference import predict
        _,_,notes=predict(str(wav))
        raw=[{'id':f'ev_{i:05d}','start_s':float(e[0]),'end_s':float(e[1]),'midi':int(e[2]),'confidence':float(e[3])} for i,e in enumerate(notes)]
        sys.path.insert(0,str(Path(__file__).parent))
        from structural_reduction import reduce_candidates
        from ornament_reduction import suppress_microornaments
        red=reduce_candidates(raw); orn=suppress_microornaments(red['render_events'])
        subprocess.run([args.beat_this_bin,str(wav),'--model',args.beat_model,'--mel-model',args.mel_model,f'--beats={beats_file}'],check=True)
        beat_times=[]
        for line in beats_file.read_text().splitlines():
            s=line.strip().split()[0] if line.strip() else ''
            try: beat_times.append(float(s))
            except ValueError: pass
        intervals=[beat_times[i]-beat_times[i-1] for i in range(1,len(beat_times)) if beat_times[i]>beat_times[i-1]]
        bpm=60/statistics.median(intervals) if intervals else None
        import librosa
        y,sr=librosa.load(str(wav),sr=22050,mono=True)
        result={'version':'FULL M/T Sensor Regression v0.2','song_id':args.song_id,'coverage':'FULL','audio_persistence':'NONE',
                'source_license':args.source_license,'ephemeral_sha256':sha,'duration_s':len(y)/sr,
                'M_raw_count':len(raw),'M_structural_count':len(red['render_events']),'M_post_ornament_count':len(orn['render_events']),
                'M_range_raw':[min([e['midi'] for e in raw],default=None),max([e['midi'] for e in raw],default=None)],
                'T_sensor':'Beat This','T_status':'VALID','T_tactus_count':len(beat_times),'T_tempo_bpm_median':bpm,
                'T_model_sha256':hashlib.sha256(Path(args.beat_model).read_bytes()).hexdigest(),
                'T_mel_model_sha256':hashlib.sha256(Path(args.mel_model).read_bytes()).hexdigest(),
                'promotion':'M_T_REGRESSION_VALID; TEXT_REQUIRED_FOR_TMT_SONG_OBJECT'}
        (out/'sensor_regression.json').write_text(json.dumps(result,indent=2)); (out/'tactus.json').write_text(json.dumps({'beats':beat_times,'tempo_bpm':bpm},indent=2))
        print(json.dumps(result))
    finally:
        for p in (src,wav,beats_file):
            try:p.unlink()
            except FileNotFoundError:pass

if __name__=='__main__':main()
