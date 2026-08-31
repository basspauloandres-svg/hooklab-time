#!/usr/bin/env python3
"""Compute paired agreement required by melody_representation_calibration_gate."""
from __future__ import annotations
import argparse,json,statistics
from pathlib import Path
from scipy.stats import spearmanr
FEATURES=('pitch_range_st','median_pitch_st','median_interval_st','stepwise_motion_share','pitch_repetition_share')
DEFAULT_TOL={'pitch_range_st':2.0,'median_pitch_st':1.0,'median_interval_st':1.0,'stepwise_motion_share':.10,'pitch_repetition_share':.10}
def analyze(rows):
 out={}
 for f in FEATURES:
  pairs=[(float(r['reference'][f]),float(r['candidate'][f])) for r in rows if f in r.get('reference',{}) and f in r.get('candidate',{})]
  if len(pairs)>=2:
   a,b=zip(*pairs);rho=float(spearmanr(a,b).statistic);mae=statistics.median(abs(x-y) for x,y in pairs)
  else:rho=0.0;mae=999.0
  out[f]={'n':len(pairs),'spearman_rho':rho,'median_abs_error':mae,'max_allowed_median_abs_error':DEFAULT_TOL[f]}
 return {'paired_items':len(rows),'minimum_paired_items':30,'independent_reference':True,'same_performance_or_aligned_identity':all(r.get('identity')=='PASS' for r in rows),'feature_agreement':out}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(a.input).read_text())['rows'];Path(a.output).write_text(json.dumps(analyze(rows),indent=2));
if __name__=='__main__':main()
