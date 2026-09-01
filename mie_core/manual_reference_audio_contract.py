#!/usr/bin/env python3
"""Contract/guard for manually supplied commercial reference audio.

This layer is creative reference evidence, never corpus-population evidence.
Raw copyrighted audio must not be committed or promoted into Matrix X by this path.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ALLOWED_PURPOSES={'PRIVATE_RESEARCH_PREPRODUCTION','PRIVATE_STYLE_REFERENCE_ANALYSIS'}

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def build(meta,audio_path=None):
 reasons=[]
 if meta.get('purpose') not in ALLOWED_PURPOSES: reasons.append('PURPOSE_NOT_ALLOWED')
 if meta.get('user_supplied') is not True: reasons.append('NOT_USER_SUPPLIED')
 if meta.get('publish_or_redistribute') is not False: reasons.append('REDISTRIBUTION_NOT_DISABLED')
 if meta.get('corpus_population_evidence') is not False: reasons.append('CORPUS_CONTAMINATION_RISK')
 if meta.get('raw_audio_repository_retention') is not False: reasons.append('RAW_AUDIO_RETENTION_NOT_DISABLED')
 digest=sha256(audio_path) if audio_path else meta.get('sha256')
 if not digest: reasons.append('MISSING_FILE_HASH')
 ok=not reasons
 return {'schema':'HOOKLAB_MANUAL_REFERENCE_AUDIO_CONTRACT_v1.0','status':'REFERENCE_ANALYSIS_ADMISSIBLE' if ok else 'REFERENCE_ANALYSIS_BLOCKED','reference_id':meta.get('reference_id'),'identity':meta.get('identity',{}),'purpose':meta.get('purpose'),'sha256':digest,'evidence_class':'MANUAL_REFERENCE_AUDIO','corpus_population_evidence':False,'matrix_x_eligible':False,'raw_audio_retention':'EPHEMERAL_DELETE_AFTER_ANALYSIS','persist_allowed':['derived_features','analysis_config','method_versions','confidence','section_profile','sha256','identity_metadata','provenance'],'blocking_reasons':reasons,'interpretation_boundary':'Reference-derived features guide local style/preproduction decisions and do not represent corpus statistics.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--metadata',required=True);ap.add_argument('--audio');ap.add_argument('--output',required=True);a=ap.parse_args();out=build(json.loads(Path(a.metadata).read_text()),a.audio);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':out['status'],'reference_id':out['reference_id']}));raise SystemExit(0 if out['status']=='REFERENCE_ANALYSIS_ADMISSIBLE' else 4)
if __name__=='__main__':main()
