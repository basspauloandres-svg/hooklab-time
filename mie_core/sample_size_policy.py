#!/usr/bin/env python3
"""Adaptive sample-size policy for the first HookLab/TIME empirical sample.

There is deliberately no arbitrary fixed maximum. Growth is bounded by evidence
quality, cohort coverage and stabilization of descriptive estimates. The policy
never claims inferential adequacy from N alone.
"""
import argparse,json,math
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 d=json.loads(Path(a.report).read_text())
 n=int(d.get('n_pass',0)); genres=int(d.get('n_genres',0)); styles=int(d.get('n_styles',0)); fail=int(d.get('n_fail',0))
 # Operational bands are collection targets, not statistical power claims.
 if n < 30: target=30; phase='PILOT_DIVERSIFICATION'
 elif n < 60: target=60; phase='COHORT_DENSIFICATION'
 elif n < 100: target=100; phase='REFERENCE_STABILIZATION'
 else: target=None; phase='ADAPTIVE_STOPPING_REVIEW'
 out={'schema':'FIRST_SAMPLE_SIZE_POLICY_v1.0','current_strict_pass_n':n,'fail_n':fail,'genres':genres,'styles':styles,
      'next_operational_target':target,'phase':phase,
      'hard_maximum':None,
      'stopping_rule':'After N>=100, continue collection while key cohort distributions or feature estimates materially change; stop the first sample only after stability diagnostics and cohort sufficiency are documented.',
      'minimum_diversity_targets':{'genres':5,'styles':10,'strict_pass_per_primary_cohort':10},
      'epistemic_note':'30/60/100 are engineering checkpoints for staged collection, not claims of statistical power or representativeness.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
if __name__=='__main__':main()
