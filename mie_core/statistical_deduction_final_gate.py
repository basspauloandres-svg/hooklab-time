#!/usr/bin/env python3
"""Final fail-closed promotion gate for the statistical-deduction registry."""
import argparse,json
from pathlib import Path

ALLOWED_DECISIONS={'PROMOTE_TO_CONDITIONED_DEDUCTION','HOLD_FOR_REPLICATION','NO_PROMOTION','AUDIT'}
PROMOTE_REQUIRED=('POPULATION_SCOPE','OUTCOME','N_ELIGIBLE','FEATURE_DOMAIN','FEATURE','ANALYSIS_PHASE','EFFECT_SIZE_AND_UNCERTAINTY','MULTIPLICITY_CONTROL','ROBUSTNESS_SENSITIVITY','REPLICATION_STATUS','THEORY_SUPPORT','CLAIM_LEVEL','CALIBRATION_STATUS')


def promotable(r):
    reasons=[]
    for k in PROMOTE_REQUIRED:
        if r.get(k) in (None,'','NOT_REPORTED_IN_SOURCE'): reasons.append(f'MISSING_OR_UNRESOLVED_{k}')
    eff=r.get('EFFECT_SIZE_AND_UNCERTAINTY') or {}
    if not eff.get('effect'): reasons.append('MISSING_EFFECT_SIZE')
    if eff.get('uncertainty') in (None,'','NOT_REPORTED_IN_SOURCE','NOT_ESTIMABLE_WITHOUT_POPULATION_DATA'): reasons.append('MISSING_EFFECT_UNCERTAINTY')
    if r.get('ANALYSIS_PHASE') in {'EXPLORATORY','EXPLORATORY_CALIBRATION','POST_HOC','PRE_REGISTERED_PENDING_EXTERNAL_PROVISIONING'}: reasons.append('NON_CONFIRMATORY_PHASE')
    if r.get('FEATURE_DOMAIN')=='MUSIC_MELODY' and not str(r.get('CALIBRATION_STATUS','')).startswith('REPRESENTATION_CALIBRATED'):
        reasons.append('MELODY_REPRESENTATION_NOT_CALIBRATED')
    if r.get('CLAIM_LEVEL') not in {'ASSOCIATIVE','EXPERIMENTAL'}: reasons.append('CLAIM_LEVEL_NOT_PROMOTION_ELIGIBLE')
    return not reasons,reasons

def evaluate(reg):
    audit=[]; promoted=[]
    for r in reg.get('rows',[]):
        if r.get('DECISION') not in ALLOWED_DECISIONS:
            audit.append({'ANALYSIS_ID':r.get('ANALYSIS_ID'),'reasons':['INVALID_DECISION']}); continue
        if r.get('DECISION')=='PROMOTE_TO_CONDITIONED_DEDUCTION':
            ok,reasons=promotable(r)
            if ok: promoted.append(r['ANALYSIS_ID'])
            else: audit.append({'ANALYSIS_ID':r.get('ANALYSIS_ID'),'reasons':reasons})
    if audit:
        status='AUDIT_BLOCKED'
    elif promoted:
        status='CONDITIONED_DEDUCTION_AVAILABLE'
    else:
        status='VALID_NULL_NON_PROMOTION_COMPLETION'
    return {
      'schema':'HOOKLAB_STATISTICAL_DEDUCTION_FINAL_GATE_v1.0','status':status,
      'promoted_analysis_ids':promoted,'audit':audit,
      'scientific_d_state':'ELIGIBILITY_REVIEW_REQUIRED' if promoted else 'BLOCKED_NO_POSITIVE_ELIGIBLE_DEDUCTION',
      'null_result_is_scientifically_valid':True,
      'invariants':['deduction != prediction','association != causation','p-value alone cannot promote','melodic promotion requires representation calibration','exploratory/post-hoc result cannot directly promote','missing uncertainty blocks positive promotion','D0_EXPLORATORY != SCIENTIFIC_D']
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--registry',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    out=evaluate(json.loads(Path(a.registry).read_text()));Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':out['status'],'promoted':out['promoted_analysis_ids'],'audit':len(out['audit'])}))
    raise SystemExit(0 if out['status']!='AUDIT_BLOCKED' else 4)
if __name__=='__main__':main()
