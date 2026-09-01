#!/usr/bin/env python3
import argparse, hashlib, json, os, subprocess
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--url',required=True)
    ap.add_argument('--song-id',required=True)
    ap.add_argument('--license',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    ram=Path('/dev/shm')/f'{args.song_id}.audio'
    try:
        subprocess.run(['curl','-L','--fail','--silent','--show-error',args.url,'-o',str(ram)],check=True)
        sha=hashlib.sha256(ram.read_bytes()).hexdigest()
        p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size,format_name','-of','json',str(ram)],capture_output=True,text=True,check=True)
        info=json.loads(p.stdout)['format']
        manifest={
          'version':'Full Track Ephemeral Acquisition Probe v0.1',
          'song_id':args.song_id,
          'source_url':args.url,
          'license':args.license,
          'audio_access_mode':'RAM_EPHEMERAL',
          'audio_persistence':'NONE',
          'coverage':'FULL',
          'duration_s':float(info['duration']),
          'source_bytes':int(info['size']),
          'source_format':info.get('format_name'),
          'ephemeral_sha256':sha,
          'rule':'Only derived metadata may persist. Audio lives in /dev/shm and is deleted in finally.'
        }
        (out/'fulltrack_manifest.json').write_text(json.dumps(manifest,indent=2))
        print(json.dumps(manifest))
    finally:
        try: ram.unlink(missing_ok=True)
        except Exception: pass

if __name__=='__main__': main()
