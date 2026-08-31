#!/usr/bin/env python3
"""Coordinate HookLab robust-cohort growth without redefining scientific promotion.

This controller consumes an observed ledger produced by the existing TSDQP/FULL_TMT/
Matrix-X path. It never discovers songs, downloads media, relaxes gates, or converts
preview/prototype evidence into scientific rows.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
CHECKPOINTS=(5,30,50,75,100,125)
FORBIDDEN_SCOPES={'PUBLIC_SHORT_PREVIEW','PROTOTYPE_EVIDENCE_NOT_FINAL_SAMPLE','FRAGMENT','EXCERPT'}

def truthy(v): return str(v).strip().lower() in {'1','true','yes','y'}

def classify(r):
    reasons=[]
    scope=str(r.get('audio_scope') or r.get('evidence_scope') or '').upper()
    role=str(r.get('role') or '').upper()
    if scope in FORBIDDEN_SCOPES or role in FORBIDDEN_SCOPES: reasons.append('NON_FINAL_OR_FRAGMENTARY_EVIDENCE')
    for field,label in [
        ('identity_pass','IDENTITY'),('version_pass','VERSION'),('full_song_pass','FULL_SONG'),
        ('provenance_pass','PROVENANCE'),('full_tmt_pass','FULL_TMT'),('mass_success_pass','MASS_SUCCESS'),
        ('genre_style_pass','GENRE_STYLE')]:
        if not truthy(r.get(field)): reasons.append(label+'_GATE_NOT_PASSED')
    candidate=not reasons
    promotion=truthy(r.get('scientific_promotion'))
    if promotion and not candidate: reasons.append('INVALID_PROMOTION_WITH_FAILED_UPSTREAM_GATE')
    return candidate,promotion,reasons

def evaluate(rows):
    audited=[]; candidate_n=0; promoted_n=0
    for r in rows:
        cand,prom,reasons=classify(r)
        candidate_n+=int(cand); promoted_n+=int(cand and prom)
        audited.append({**r,'robust_candidate_eligible':cand,'robust_scientifically_promoted':bool(cand and prom),'controller_reasons':reasons})
    reached=max((n for n in CHECKPOINTS if candidate_n>=n),default=0)
    next_cp=next((n for n in CHECKPOINTS if candidate_n<n),None)
    return {
      'schema':'HOOKLAB_ROBUST_COHORT_BATCH_CONTROLLER_v1.0',
      'observed_rows':len(rows),'qualified_candidate_n':candidate_n,'scientifically_promoted_n':promoted_n,
      'reached_checkpoint':reached,'next_checkpoint':next_cp,
      'rows_needed_for_next_checkpoint':0 if next_cp is None else next_cp-candidate_n,
      'candidate_stage':'T0_VALIDATION_SEED' if candidate_n<30 else 'T1_PILOT' if candidate_n<50 else 'T2_ANALYTICAL_OR_HIGHER',
      'scientific_promotion_complete':promoted_n==candidate_n and candidate_n>=50,
      'audited_rows':audited,
      'invariants':['scientific target population != songs available in Lakh/LMD','candidate discovery != scientific promotion','preview/prototype evidence != robust scientific row','N alone does not establish representativeness']
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ledger',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    p=Path(a.ledger); rows=list(csv.DictReader(p.open(encoding='utf-8'))) if p.suffix.lower()=='.csv' else json.loads(p.read_text()).get('rows',[])
    out=evaluate(rows);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({k:out[k] for k in ('qualified_candidate_n','scientifically_promoted_n','reached_checkpoint','next_checkpoint','rows_needed_for_next_checkpoint')}))
if __name__=='__main__': main()
