#!/usr/bin/env python3
"""Readiness guard for the Dance-Pop robust cohort required by Gate B2.

This does not discover songs or fabricate a matrix. It audits whether observed outputs
from the existing TSDQP -> FULL_TMT -> Matrix X -> stability path are sufficient to
unlock statistical-rule promotion.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

def evaluate(payload):
    reasons=[]
    matrix=payload.get('matrix',{})
    stability=payload.get('stability',{})
    qualification=payload.get('qualification',{})
    n=int(matrix.get('qualified_rows',0) or 0)
    if qualification.get('scientific_population_defined') is not True: reasons.append('SCIENTIFIC_POPULATION_NOT_CONFIRMED')
    if qualification.get('candidate_discovery_separate_from_promotion') is not True: reasons.append('DISCOVERY_PROMOTION_BOUNDARY_NOT_CONFIRMED')
    if qualification.get('identity_version_full_song_provenance_gates') is not True: reasons.append('QUALIFICATION_GATES_NOT_CONFIRMED')
    if matrix.get('full_tmt_complete') is not True: reasons.append('FULL_TMT_NOT_COMPLETE')
    if n < 50: reasons.append('ANALYTICAL_N_LT_50')
    if stability.get('status')!='STABLE_REFERENCE_READY': reasons.append('STABILITY_GATE_NOT_PASSED')
    if stability.get('persistent_drift_detected') is True: reasons.append('PERSISTENT_DRIFT')
    ready=not reasons
    return {'schema':'HOOKLAB_GATE_B2_ROBUST_COHORT_READINESS_v1.0','cohort':payload.get('cohort'),'qualified_rows':n,'status':'ROBUST_COHORT_APPROVED_FOR_PROMOTION_LAYER' if ready else 'ROBUST_COHORT_NOT_READY','downstream_eligible':ready,'blocking_reasons':reasons,'required_next_action':None if ready else 'Continue existing offline TSDQP/FULL_TMT/Matrix-X robust build; rerun stability gate on observed qualified matrix.','invariants':['scientific target population != songs available in Lakh/LMD','candidate discovery != scientific promotion','N alone does not establish representativeness']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();out=evaluate(json.loads(Path(a.input).read_text()));Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':out['status'],'n':out['qualified_rows'],'blocking_reasons':out['blocking_reasons']}));raise SystemExit(0 if out['downstream_eligible'] else 4)
if __name__=='__main__':main()
