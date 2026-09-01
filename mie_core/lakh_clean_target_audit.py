#!/usr/bin/env python3
"""Stream the clean Lakh archive and audit only target songs.

This avoids expanding the entire dataset. Target matching is filename-only discovery;
extracted MIDIs must still pass the structural audit and later vocal-melody validation.
"""
import argparse,json,re,tarfile,urllib.request,subprocess,sys,tempfile
from pathlib import Path

ARCHIVE='http://hog.ee.columbia.edu/craffel/lmd/clean_midi.tar.gz'

def norm(x): return re.sub(r'[^a-z0-9]+',' ',str(x or '').lower()).strip()

def hit(name,t):
 n=norm(name); return norm(t['title']) in n and norm(t['artist']) in n

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--targets',required=True);ap.add_argument('--output',required=True);ap.add_argument('--archive-url',default=ARCHIVE);a=ap.parse_args()
 targets=json.loads(Path(a.targets).read_text()); targets=targets.get('targets',targets.get('songs',targets))
 out=Path(a.output);out.mkdir(parents=True,exist_ok=True);found=[]
 req=urllib.request.Request(a.archive_url,headers={'User-Agent':'HookLabPrototype/1.0'})
 with urllib.request.urlopen(req,timeout=120) as resp, tarfile.open(fileobj=resp,mode='r|gz') as tar:
  for m in tar:
   if not m.isfile() or not m.name.lower().endswith(('.mid','.midi','.kar')): continue
   matched=[t for t in targets if hit(m.name,t)]
   if not matched: continue
   raw=tar.extractfile(m).read()
   for t in matched:
    slug=re.sub(r'[^a-z0-9]+','_',norm(t['artist']+' '+t['title'])).strip('_'); d=out/slug;d.mkdir(exist_ok=True)
    midi=d/'candidate.mid';midi.write_bytes(raw);audit=d/'audit.json'
    cmd=[sys.executable,str(Path(__file__).with_name('lakh_midi_structural_audit.py')),'--midi',str(midi),'--output',str(audit)]
    if t.get('duration_seconds'):cmd+=['--expected-duration',str(t['duration_seconds'])]
    p=subprocess.run(cmd); found.append({'target':t,'archive_member':m.name,'audit_path':str(audit),'audit_exit':p.returncode})
 (out/'summary.json').write_text(json.dumps({'schema':'HOOKLAB_LAKH_CLEAN_TARGET_AUDIT_v1.0','archive':a.archive_url,'found':found},indent=2,ensure_ascii=False))
 print(json.dumps({'status':'TARGET_AUDIT_COMPLETE','targets':len(targets),'found':len(found)}))
if __name__=='__main__':main()
