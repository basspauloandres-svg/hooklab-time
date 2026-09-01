#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,re,unicodedata,gzip,pickle
from pathlib import Path

def norm(s):
 s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower();return ' '.join(re.sub(r'[^a-z0-9]+',' ',s).split())
def toks(s):return {x for x in norm(s).split() if x not in {'the','and','with','feat','featuring','ft','x'}}
def overlap(a,b):
 A=toks(a);B=toks(b);return len(A&B)/max(1,min(len(A),len(B)))

def fail_closed(reason,m300_count=300):
 return {'schema':'HOOKLAB_DALI_OPTIONAL_PROVIDER_v1.0','provider':'DALI','license':'CC BY-NC-SA 4.0 / non-commercial research','state':'REFERENCE_UNAVAILABLE','reason':reason,'m300_count':m300_count,'match_count':0,'audit_count':0,'reference_unavailable_count':m300_count,'computational_processing_authorized_for_research':True,'automatic_access_available':False,'network_audio_attempted':False,'video_link_attempted':False,'scientific_promotion':False,'invariants':['restricted provider files require legitimate provisioning','no YouTube/video retrieval','no preview substitution','no scraping','REFERENCE_UNAVAILABLE != FAIL']}

def extract_info(root:Path):
 # DALI releases expose an info/DALI_DATA_INFO.gz object. We intentionally do not
 # infer undocumented layouts. This loader accepts JSON or pickle-like mappings only.
 p=root/'info'/'DALI_DATA_INFO.gz'
 if not p.exists():return None,'DALI_INFO_MISSING'
 try:
  raw=gzip.open(p,'rb').read()
 except Exception:return None,'DALI_INFO_UNREADABLE'
 try:
  obj=json.loads(raw.decode('utf-8'))
  return obj,None
 except Exception:pass
 try:
  obj=pickle.loads(raw)
  return obj,None
 except Exception:return None,'DALI_INFO_FORMAT_UNSUPPORTED_FAIL_CLOSED'

def iter_metadata(info):
 if isinstance(info,dict):
  for k,v in info.items():
   if not isinstance(v,dict):continue
   title=v.get('title') or v.get('song') or v.get('name')
   artist=v.get('artist') or v.get('musician') or v.get('singer')
   if title and artist:yield str(k),str(title),str(artist),v

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--m300',required=True);ap.add_argument('--output',required=True);ap.add_argument('--dali-root',default=os.environ.get('DALI_DATA_ROOT'));a=ap.parse_args();m=json.loads(Path(a.m300).read_text());n=len(m.get('candidates',[]))
 if not a.dali_root:
  out=fail_closed('DALI_DATA_ROOT_NOT_PROVISIONED',n);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'state':out['state'],'reason':out['reason']}));return
 root=Path(a.dali_root)
 if not root.exists():
  out=fail_closed('DALI_DATA_ROOT_NOT_FOUND',n);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'state':out['state'],'reason':out['reason']}));return
 info,err=extract_info(root)
 if err:
  out=fail_closed(err,n);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'state':out['state'],'reason':out['reason']}));return
 D={}
 for did,title,artist,meta in iter_metadata(info):D.setdefault(norm(title),[]).append((did,title,artist,meta))
 matches=[];audits=[];unavailable=[]
 for c in m.get('candidates',[]):
  hits=D.get(norm(c.get('title')),[]);sc=sorted([(overlap(c.get('artist'),h[2]),h) for h in hits],key=lambda z:z[0],reverse=True);strong=[x for x in sc if x[0]>=.5]
  if len(strong)==1:
   s,(did,title,artist,meta)=strong[0];matches.append({'candidate_id':c['candidate_id'],'dali_id':did,'title':c['title'],'artist':c['artist'],'dali_title':title,'dali_artist':artist,'artist_overlap':round(s,3),'evidence_status':'LICENSED_VOCAL_MELODY_LYRICS_METADATA_AVAILABLE','version_identity':'AUDIT_REQUIRED_BEFORE_PROMOTION','scientific_promotion':False})
  elif strong:audits.append({'candidate_id':c['candidate_id'],'reason':'MULTIPLE_STRONG_DALI_IDENTITIES','dali_ids':[h[1][0] for h in strong]})
  elif hits:audits.append({'candidate_id':c['candidate_id'],'reason':'DALI_TITLE_MATCH_IDENTITY_AUDIT'})
  else:unavailable.append({'candidate_id':c['candidate_id'],'status':'REFERENCE_UNAVAILABLE'})
 out={'schema':'HOOKLAB_DALI_OPTIONAL_PROVIDER_v1.0','provider':'DALI','license':'CC BY-NC-SA 4.0 / non-commercial research','state':'PROVISIONED_DISCOVERY_COMPLETE','m300_count':n,'match_count':len(matches),'audit_count':len(audits),'reference_unavailable_count':len(unavailable),'computational_processing_authorized_for_research':True,'automatic_access_available':True,'network_audio_attempted':False,'video_link_attempted':False,'matches':matches,'audits':audits,'unavailable':unavailable,'scientific_promotion':False,'invariants':['metadata discovery != version validation','DALI vocal-note/lyric evidence is not audio Gate A PASS','no YouTube/video retrieval','version identity required before feature promotion']}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'state':out['state'],'matches':len(matches),'audits':len(audits),'unavailable':len(unavailable)}))
if __name__=='__main__':main()
