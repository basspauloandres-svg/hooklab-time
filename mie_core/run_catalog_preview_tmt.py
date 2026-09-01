#!/usr/bin/env python3
"""Catalog preview acquisition layer v0.1.

Consumes an authorized remote preview URL ephemerally, computes a lightweight
TMT sensor regression payload, and deletes the audio bytes before exit.
This runner never persists a permanent commercial-audio corpus.

Full TMT Song Objects require FULL coverage; PREVIEW outputs are sensor/generalization
checks only and are never silently mixed with FULL corpus rows.
"""
import argparse, hashlib, json, os, subprocess, tempfile
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--url',required=True)
    ap.add_argument('--song-id',required=True)
    ap.add_argument('--isrc',default=None)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='tmt_preview_') as td:
        src=Path(td)/'preview.m4a'; wav=Path(td)/'preview.wav'
        subprocess.run(['curl','-L','--fail','--silent','--show-error',args.url,'-o',str(src)],check=True)
        sha=hashlib.sha256(src.read_bytes()).hexdigest()
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-ar','22050','-ac','1',str(wav)],check=True)
        probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(wav)],capture_output=True,text=True,check=True)
        duration=float(json.loads(probe.stdout)['format']['duration'])
        manifest={'version':'Catalog Preview Acquisition v0.1','song_id':args.song_id,'isrc':args.isrc,
                  'audio_access_mode':'EPHEMERAL_CACHE','audio_persistence':'NONE','coverage':'PREVIEW',
                  'coverage_duration_s':duration,'ephemeral_sha256':sha,
                  'promotion_rule':'PREVIEW may test sensors/generalization but cannot populate FULL structural TMT corpus fields.'}
        (out/'preview_manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(manifest))

if __name__=='__main__': main()
