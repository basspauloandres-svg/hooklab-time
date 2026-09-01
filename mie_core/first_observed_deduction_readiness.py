#!/usr/bin/env python3
"""Gate the first substantive HookLab deduction against actually observed evidence."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def evaluate(x):
 reasons=[]
 n=int(x.get('scientifically_eligible_musical_rows',0) or 0)
 if n < int(x.get('minimum_rows_for_first_association',30)): reasons.append('INSUFFICIENT_ELIGIBLE_MUSICAL_ROWS')
 if x.get('observed_association_available') is not True: reasons.append('NO_OBSERVED_MUSICAL_ASSOCIATION')
 if x.get('provenance_complete') is not True: reasons.append('PROVENANCE_INCOMPLETE')
 if x.get('feature_semantics_defined') is not True: reasons.append('FEATURE_SEMANTICS_NOT_DEFINED')
 if x.get('alternative_explanations_recorded') is not True: reasons.append('ALTERNATIVE_EXPLANATIONS_NOT_RECORDED')
 if x.get('theory_support_matched_to_pattern') is not True: reasons.append('THEORY_NOT_MATCHED_TO_OBSERVED_PATTERN')
 ready=not reasons
 return {'schema':'HOOKLAB_FIRST_OBSERVED_DEDUCTION_READINESS_v1.0','status':'D001_OBSERVED_READY' if ready else 'D001_OBSERVED_BLOCKED','eligible_rows':n,'blocking_reasons':reasons,'next_action':None if ready else 'Continue scientific musical-row qualification; estimate first scoped association only after minimum eligible rows and provenance are present.','invariants':['no placeholder may be promoted','discovery frame != musical evidence matrix','deduction requires observed association','theory follows the actual pattern rather than replacing it']}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();out=evaluate(json.loads(Path(a.input).read_text()));Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out));raise SystemExit(0 if out['status']=='D001_OBSERVED_READY' else 4)
if __name__=='__main__':main()
