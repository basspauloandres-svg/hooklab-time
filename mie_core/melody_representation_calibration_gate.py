#!/usr/bin/env python3
"""Fail-closed calibration gate for vocal melody representations.

Purpose: prevent F0-derived or provider-note features from entering creative deduction
unless representation stability has been observed on an independent calibration corpus.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

CORE=('pitch_range_st','median_pitch_st','median_interval_st','stepwise_motion_share','pitch_repetition_share')

def evaluate(x):
 reasons=[]
 n=int(x.get('paired_items',0) or 0)
 if n < int(x.get('minimum_paired_items',30)): reasons.append('INSUFFICIENT_PAIRED_CALIBRATION_ITEMS')
 if x.get('independent_reference') is not True: reasons.append('NO_INDEPENDENT_REFERENCE')
 if x.get('same_performance_or_aligned_identity') is not True: reasons.append('PERFORMANCE_IDENTITY_NOT_ESTABLISHED')
 metrics=x.get('feature_agreement',{})
 stable=[]
 for f in CORE:
  m=metrics.get(f,{})
  if m.get('n',0)>=30 and m.get('spearman_rho',0)>=0.80 and abs(m.get('median_abs_error',999))<=m.get('max_allowed_median_abs_error',1.0): stable.append(f)
 if not stable: reasons.append('NO_CORE_FEATURE_REPRESENTATION_STABLE')
 return {'schema':'HOOKLAB_MELODY_REPRESENTATION_CALIBRATION_GATE_v1.0','status':'REPRESENTATION_CALIBRATED' if not reasons else 'REPRESENTATION_CALIBRATION_PENDING','stable_features':stable,'blocking_reasons':reasons,'invariants':['F0 != discrete notes','provider annotation != ground truth by default','representation stability precedes population association','unstable features cannot become creative deductions']}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();out=evaluate(json.loads(Path(a.input).read_text()));Path(a.output).write_text(json.dumps(out,indent=2));print(json.dumps(out));raise SystemExit(0 if out['status']=='REPRESENTATION_CALIBRATED' else 4)
if __name__=='__main__':main()
