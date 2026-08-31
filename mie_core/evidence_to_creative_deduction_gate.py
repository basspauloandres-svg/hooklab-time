#!/usr/bin/env python3
"""Fail-closed gate from observed evidence to a creative deduction.

HookLab does not promote popularity prediction claims. A creative deduction is eligible
only when its provenance, observed pattern, statistical support, interpretation,
alternative explanations and musical realization are explicit.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
REQUIRED=(
 'evidence_id','population_scope','observed_pattern','association_evidence',
 'interpretation','alternative_explanations','theory_support','deduction',
 'musical_realization','provenance'
)
FORBIDDEN_PURPOSES={'HIT_PREDICTION','SUCCESS_GUARANTEE','UNIVERSAL_HIT_FORMULA'}

def evaluate(x):
 reasons=[]
 for k in REQUIRED:
  if not x.get(k): reasons.append(f'MISSING_{k.upper()}')
 if x.get('purpose') in FORBIDDEN_PURPOSES: reasons.append('PREDICTIVE_PURPOSE_FORBIDDEN')
 if x.get('claim_level') not in {'DESCRIPTIVE','ASSOCIATIVE','EXPERIMENTALLY_SUPPORTED'}:
  reasons.append('INVALID_CLAIM_LEVEL')
 if x.get('claim_level')=='EXPERIMENTALLY_SUPPORTED' and not x.get('experimental_support'):
  reasons.append('EXPERIMENTAL_SUPPORT_REQUIRED')
 if x.get('genre_style_role') not in {'STRATIFICATION','AESTHETIC_CONTEXT','CONTROL_VARIABLE','NOT_USED'}:
  reasons.append('GENRE_STYLE_MUST_NOT_BE_UNIVERSAL_SUCCESS_GATE')
 if x.get('source_type')=='INDUSTRY_CLAIM' and not x.get('independent_empirical_support'):
  reasons.append('INDUSTRY_CLAIM_NOT_EMPIRICALLY_CORROBORATED')
 if x.get('association_evidence',{}).get('causal_language') is True and x.get('claim_level')!='EXPERIMENTALLY_SUPPORTED':
  reasons.append('CAUSAL_LANGUAGE_WITHOUT_EXPERIMENTAL_SUPPORT')
 ready=not reasons
 return {
  'schema':'HOOKLAB_EVIDENCE_TO_CREATIVE_DEDUCTION_GATE_v1.0',
  'status':'DEDUCTION_ELIGIBLE_FOR_PROTOTYPE' if ready else 'DEDUCTION_NOT_ELIGIBLE',
  'eligible':ready,'blocking_reasons':reasons,
  'epistemic_chain':['OBSERVATION','ASSOCIATION','INTERPRETATION','HYPOTHESIS','CONDITIONED_DEDUCTION','MUSICAL_REALIZATION','HUMAN_EVALUATION'],
  'invariants':['prediction != deduction','association != causation','industry claim != scientific evidence','genre/style is an analytical/aesthetic layer, not a universal success gate','every deduction retains provenance and scope']
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();x=json.loads(Path(a.input).read_text());out=evaluate(x);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':out['status'],'blocking_reasons':out['blocking_reasons']}));raise SystemExit(0 if out['eligible'] else 4)
if __name__=='__main__':main()
