#!/usr/bin/env python3
"""Full-track autonomous M/T regression v0.1.

Acquires a documented FULL remote stream into RAM (/dev/shm), runs Basic Pitch
as the melody sensor plus the existing structural reduction, estimates a temporal
sensor diagnostic, and persists derived JSON only. The source audio is deleted in
finally. This is a generalization gate, not a final Song Object and does not tune
parameters per song.
"""
import argparse, hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--url',required=True); ap.add_argument('--song-id',required=True)
    ap.add_argument('--source-license',required=True); ap.add_argument('--output',required=True)
    args=ap.parse_args(); out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    ram=Path('/dev/shm') if Path('/dev/shm').exists() else Path(tempfile.gettempdir())
    src=ram/f'tmt_{os.getpid()}.mp3'; wav=ram/f'tmt_{os.getpid()}.wav'
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
        # T diagnostic only here. Beat This remains authoritative once its ONNX assets are attached to this runner.
        import librosa, numpy as np
        y,sr=librosa.load(str(wav),sr=22050,mono=True)
        tempo,bt=librosa.beat.beat_track(y=y,sr=sr,units='time')
        tempo=float(np.asarray(tempo).reshape(-1)[0])
        result={'version':'FULL M/T Sensor Regression v0.1','song_id':args.song_id,'coverage':'FULL',
                'audio_persistence':'NONE','source_license':args.source_license,'ephemeral_sha256':sha,
                'duration_s':len(y)/sr,'M_raw_count':len(raw),'M_structural_count':len(red['render_events']),
                'M_post_ornament_count':len(orn['render_events']),'M_range_raw':[min([e['midi'] for e in raw],default=None),max([e['midi'] for e in raw],default=None)],
                'T_diagnostic_bpm':tempo,'T_diagnostic_count':len(bt),
                'T_status':'DIAGNOSTIC_LIBROSA_NOT_BEAT_THIS','promotion':'NOT_SONG_OBJECT_UNTIL_TEXT_AND_BEAT_THIS'}
        (out/'sensor_regression.json').write_text(json.dumps(result,indent=2))
        print(json.dumps(result))
    finally:
        for p in (src,wav):
            try:p.unlink()
            except FileNotFoundError:pass

if __name__=='__main__':main()
