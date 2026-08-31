#!/usr/bin/env python3
"""Optional DALI adapter for licensed non-commercial research annotations.

No dataset provisioning -> deterministic REFERENCE_UNAVAILABLE.
This adapter never resolves or downloads commercial audio/video. DALI annotations
are a melody/lyrics evidence layer only; released-recording Gate A remains separate.
"""
from __future__ import annotations
import argparse,json,os
from pathlib import Path

def resolve(root: str|None):
 if not root:
  return {'provider':'DALI','status':'REFERENCE_UNAVAILABLE','reason':'DALI_DATASET_NOT_PROVISIONED','authorized_annotation_access':False,'audio_access_attempted':False,'scientific_promotion':False}
 p=Path(root)
 if not p.exists() or not p.is_dir():
  return {'provider':'DALI','status':'REFERENCE_UNAVAILABLE','reason':'DALI_DATASET_PATH_UNAVAILABLE','authorized_annotation_access':False,'audio_access_attempted':False,'scientific_promotion':False}
 # Fail closed: provisioning existence is not sufficient to infer file schema/version.
 return {'provider':'DALI','status':'AUDIT_PROVISIONED','reason':'DATASET_PRESENT_SCHEMA_AND_VERSION_IDENTITY_REQUIRE_VALIDATION','authorized_annotation_access':True,'audio_access_attempted':False,'scientific_promotion':False,'dataset_root':str(p)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--dataset-root',default=os.getenv('DALI_DATASET_ROOT'));ap.add_argument('--output',required=True);a=ap.parse_args();out=resolve(a.dataset_root);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
if __name__=='__main__':main()
