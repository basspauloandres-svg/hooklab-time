#!/usr/bin/env python3
"""Gate B2 promotion registry builder.

Promotes a corpus statistic into a generative constraint only when the robust cohort
has passed the frozen stability gate and the rule is explicitly declared, bounded,
traceable and non-provisional. This module never invents the transformation rule.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
ALLOWED_ORIGINS={"CORPUS_EMPIRICAL","OUT_OF_SAMPLE_VALIDATED","MEASUREMENT_INVARIANT"}
ALLOWED_DIMS={"FORM","TEMPO_METER","HARMONY","MELODY","RHYTHM","PRODUCTION"}

def build(stability, proposals):
    cohort_ready=stability.get('status')=='STABLE_REFERENCE_READY' and int(stability.get('rows',0))>=50 and not stability.get('persistent_drift_detected',True)
    promoted=[]; rejected=[]
    for r in proposals.get('rules',[]):
        reasons=[]
        for k in ('rule_id','evidence_id','musical_dimension','transformation','validation_scope'):
            if not r.get(k): reasons.append('MISSING_'+k.upper())
        if r.get('origin') not in ALLOWED_ORIGINS: reasons.append('ORIGIN_NOT_ALLOWED')
        if r.get('musical_dimension') not in ALLOWED_DIMS: reasons.append('INVALID_DIMENSION')
        if r.get('provisional',True): reasons.append('PROVISIONAL_RULE')
        if not cohort_ready: reasons.append('COHORT_NOT_STABLE_REFERENCE_READY')
        if r.get('transformation',{}).get('type') not in {'RANGE_CONSTRAINT','QUANTILE_SAMPLING','EMPIRICAL_DISTRIBUTION_SAMPLING','STRUCTURAL_TEMPLATE_DISTRIBUTION'}: reasons.append('UNSUPPORTED_TRANSFORMATION')
        row={**r,'promotion_state':'REJECTED' if reasons else 'PROMOTED','rejection_reasons':reasons}
        (rejected if reasons else promoted).append(row)
    return {'schema':'HOOKLAB_GATE_B2_PROMOTION_REGISTRY_v1.0','cohort_stability_status':stability.get('status'),'cohort_rows':stability.get('rows'),'promoted_rules':promoted,'rejected_rules':rejected,'downstream_eligible':cohort_ready and bool(promoted) and not rejected,'decision':'PROMOTION_READY' if cohort_ready and promoted and not rejected else 'PROMOTION_BLOCKED','invariant':'empirical distribution != promoted generative rule'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stability',required=True);ap.add_argument('--proposals',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();out=build(json.loads(Path(a.stability).read_text()),json.loads(Path(a.proposals).read_text()));Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'decision':out['decision'],'promoted':len(out['promoted_rules']),'rejected':len(out['rejected_rules'])}));raise SystemExit(0 if out['decision']=='PROMOTION_READY' else 4)
if __name__=='__main__':main()
