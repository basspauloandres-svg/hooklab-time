#!/usr/bin/env python3
"""Fail-closed admissibility gate for BiMMuDa as a scientific symbolic provider.

The gate separates repository accessibility, dataset-content suitability, population
intersection and licensing/authorization. Public availability alone is never treated
as authorization for scientific corpus ingestion.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

def evaluate(payload):
    reasons=[]
    if payload.get('repository_public') is not True: reasons.append('REPOSITORY_NOT_PUBLIC')
    if payload.get('full_main_melody_midi') is not True: reasons.append('NO_FULL_MAIN_MELODY_MIDI')
    if payload.get('section_midis') is not True: reasons.append('NO_SECTION_MIDIS')
    if payload.get('metadata_available') is not True: reasons.append('NO_METADATA')
    if payload.get('manual_transcription_quality_control') is not True: reasons.append('QUALITY_CONTROL_NOT_CONFIRMED')
    if payload.get('target_population_intersection_observed') is not True: reasons.append('NO_TARGET_POPULATION_INTERSECTION')
    license_status=payload.get('dataset_license_status')
    if license_status not in {'EXPLICIT_DATASET_LICENSE','EXPLICIT_RESEARCH_PERMISSION'}:
        reasons.append('DATASET_FILE_LICENSE_OR_RESEARCH_PERMISSION_NOT_EXPLICIT')
    if payload.get('computational_processing_authorized') is not True:
        reasons.append('COMPUTATIONAL_PROCESSING_AUTHORIZATION_NOT_EXPLICIT')
    status='PROVIDER_ADMISSIBLE' if not reasons else 'PROVIDER_AUDIT_REQUIRED'
    return {
        'schema':'HOOKLAB_BIMMUDA_PROVIDER_ADMISSIBILITY_v1.0',
        'provider':'BiMMuDa',
        'status':status,
        'downstream_eligible':status=='PROVIDER_ADMISSIBLE',
        'blocking_reasons':reasons,
        'invariant':'public repository != explicit dataset-file processing authorization'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    out=evaluate(json.loads(Path(a.input).read_text()))
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False))
    print(json.dumps({'status':out['status'],'blocking_reasons':out['blocking_reasons']}))
    raise SystemExit(0 if out['downstream_eligible'] else 4)
if __name__=='__main__':main()
