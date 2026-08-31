#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re,unicodedata
from pathlib import Path

def norm(s):
 s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower();s=re.sub(r'\([^)]*\)|\[[^]]*\]',' ',s);return ' '.join(re.sub(r'[^a-z0-9]+',' ',s).split())
def toks(s):return {x for x in norm(s).split() if x not in {'the','and','with','feat','featuring','ft','x'}}
def overlap(a,b):
 A=toks(a);B=toks(b);return len(A&B)/max(1,min(len(A),len(B)))
def rows(repo):
 p=Path(repo)/'dataset'/'metadata.csv';out=[]
 with p.open(encoding='utf-8-sig',errors='replace') as f:
  for r in csv.DictReader(f):
   file=(r.get('File') or '').strip();title=(r.get('Title') or '').strip();artist=(r.get('Artist') or '').strip()
   if not file or not title:continue
   seg=Path(repo)/'dataset'/'segments'/(file+'.txt');beat=Path(repo)/'dataset'/'beats_and_downbeats'/(file+'.txt')
   out.append({'harmonix_file':file,'title':title,'artist':artist,'release':r.get('Release'),'duration_s':r.get('Duration'),'bpm':r.get('BPM'),'time_signature':r.get('Time Signature'),'genre':r.get('Genre'),'musicbrainz_id':r.get('MusicBrainz Id'),'acoustid_id':r.get('Acoustid Id'),'segments_available':seg.exists(),'beats_available':beat.exists()})
 return out

def version_gate(candidate,h):
 try:target=float(candidate.get('duration_ms'))/1000.0;provider=float(h.get('duration_s'))
 except:return {'state':'AUDIT_VERSION_DURATION_UNAVAILABLE'}
 delta=abs(target-provider);rel=delta/max(target,1e-9);tol=max(5.0,0.03*target)
 return {'state':'VERSION_COMPATIBLE' if delta<=tol else 'AUDIT_VERSION_MISMATCH','target_duration_s':round(target,3),'provider_duration_s':round(provider,3),'duration_delta_s':round(delta,3),'duration_relative_delta':round(rel,4),'tolerance_s':round(tol,3)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--m300',required=True);ap.add_argument('--harmonix-repo',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();m=json.loads(Path(a.m300).read_text());H=rows(a.harmonix_repo);by={}
 for h in H:by.setdefault(norm(h['title']),[]).append(h)
 matches=[];audits=[];unavailable=[];identity_resolved=0
 for c in m['candidates']:
  hits=by.get(norm(c['title']),[]);scored=sorted([(overlap(c['artist'],h['artist']),h) for h in hits],key=lambda z:z[0],reverse=True)
  strong=[(s,h) for s,h in scored if s>=.5 and h['segments_available']]
  if len(strong)==1:
   identity_resolved+=1;s,h=strong[0];vg=version_gate(c,h)
   base={'candidate_id':c['candidate_id'],'chart_year':c['chart_year'],'m300_rank':c['rank'],'title':c['title'],'artist':c['artist'],'harmonix_file':h['harmonix_file'],'harmonix_title':h['title'],'harmonix_artist':h['artist'],'artist_overlap':round(s,3),'release':h['release'],'duration_s':h['duration_s'],'bpm':h['bpm'],'time_signature':h['time_signature'],'genre':h['genre'],'musicbrainz_id':h['musicbrainz_id'],'acoustid_id':h['acoustid_id'],'segments_available':h['segments_available'],'beats_available':h['beats_available'],'license':'MIT repository annotations/metadata','version_identity':vg,'scientific_promotion':False}
   if vg['state']=='VERSION_COMPATIBLE':matches.append({**base,'evidence_status':'LICENSED_STRUCTURAL_RHYTHMIC_ANNOTATION_VERSION_COMPATIBLE'})
   else:audits.append({**base,'reason':vg['state']})
  elif strong:audits.append({'candidate_id':c['candidate_id'],'title':c['title'],'artist':c['artist'],'reason':'MULTIPLE_STRONG_HARMONIX_IDENTITIES','candidates':[h['harmonix_file'] for _,h in strong]})
  elif hits:audits.append({'candidate_id':c['candidate_id'],'title':c['title'],'artist':c['artist'],'reason':'TITLE_MATCH_IDENTITY_OR_ANNOTATION_AUDIT','candidates':[{'file':h['harmonix_file'],'artist':h['artist'],'overlap':round(s,3),'segments_available':h['segments_available']} for s,h in scored]})
  else:unavailable.append({'candidate_id':c['candidate_id'],'status':'REFERENCE_UNAVAILABLE'})
 out={'schema':'HOOKLAB_M300_HARMONIX_CROSSWALK_v1.1','provider':'Harmonix Set','license':'MIT repository annotations/metadata','m300_count':len(m['candidates']),'harmonix_rows':len(H),'track_identity_resolved_count':identity_resolved,'match_count':len(matches),'audit_count':len(audits),'reference_unavailable_count':len(unavailable),'coverage_rate':len(matches)/max(1,len(m['candidates'])),'version_gate':{'comparison':'M300 Spotify duration metadata vs Harmonix duration metadata','compatible_if':'absolute duration difference <= max(5 seconds, 3% of M300 duration)','purpose':'fail-closed version identity evidence; metadata comparison does not authorize audio processing'},'matches':matches,'audits':audits,'unavailable':unavailable,'invariants':['TRACK_IDENTITY != VERSION_IDENTITY','YouTube URLs are excluded from Gate A','annotation availability != authorized audio access','licensed structural/rhythmic annotation availability != scientific promotion','version mismatch remains AUDIT and is never auto-promoted']}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'track_identity_resolved':identity_resolved,'version_compatible_matches':len(matches),'audits':len(audits),'unavailable':len(unavailable),'coverage_rate':out['coverage_rate']}))
if __name__=='__main__':main()
