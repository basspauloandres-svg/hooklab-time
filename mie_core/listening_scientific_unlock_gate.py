#!/usr/bin/env python3
"""Fail-closed unlock for confirmatory H/D/H+D listening."""
from __future__ import annotations
import argparse,json
from pathlib import Path
REQ=('representation_calibrated','deduction_eligible','midi_manifest_valid','audio_standardized','provenance_complete','condition_blinding_ready','evaluation_schema_ready')
def evaluate(x):
 reasons=[f'MISSING_{k.upper()}' for k in REQ if x.get(k) is not True]
 if x.get('stimulus_class')!='SCIENTIFIC_D': reasons.append('D0_EXPLORATORY_CANNOT_UNLOCK_CONFIRMATORY_TEST')
 return {'schema':'HOOKLAB_LISTENING_SCIENTIFIC_UNLOCK_v1.0','status':'CONFIRMATORY_LISTENING_UNLOCKED' if not reasons else 'CONFIRMATORY_LISTENING_BLOCKED','blocking_reasons':reasons,'exploratory_listening_allowed':True}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();out=evaluate(json.loads(Path(a.input).read_text()));Path(a.output).write_text(json.dumps(out,indent=2));print(json.dumps(out));raise SystemExit(0 if not out['blocking_reasons'] else 4)
if __name__=='__main__':main()
