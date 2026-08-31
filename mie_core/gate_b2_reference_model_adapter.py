#!/usr/bin/env python3
"""Convert a cohort Corpus Reference Model into Gate-B2 descriptive evidence candidates.

Important: CRM distributions are empirical standardization evidence, not automatically
promoted generative rules. Output is CANDIDATE_EVIDENCE_PENDING_PROMOTION unless an
external promotion registry explicitly authorizes a feature/statistic pair.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

def dimension(feature):
    f=feature.lower()
    if any(x in f for x in ('tempo','bpm','meter','tactus')): return 'TEMPO_METER'
    if any(x in f for x in ('pitch','melod','interval','range')): return 'MELODY'
    if any(x in f for x in ('rhythm','onset','duration','syncop','ioi')): return 'RHYTHM'
    if any(x in f for x in ('section','form','position','recurrence')): return 'FORM'
    if any(x in f for x in ('harmon','chord','tonal','key')): return 'HARMONY'
    return None

def adapt(crm, cohort, promotions=None):
    promotions=promotions or {}; out=[]; skipped=[]
    for feature,stats in sorted(crm.get('features',{}).items()):
        dim=dimension(feature)
        if not dim:
            skipped.append({"feature":feature,"reason":"NO_GENERATIVE_DIMENSION_MAPPING"}); continue
        for stat in ('median','q1','q3','iqr','mean','std','min','max'):
            if stat not in stats: continue
            key=f'{feature}::{stat}'; promo=promotions.get(key)
            state='PROMOTED' if promo and promo.get('authorized') else 'CANDIDATE_EVIDENCE_PENDING_PROMOTION'
            out.append({"evidence_id":f'CRM::{cohort.get("id","UNKNOWN")}::{key}',"source_kind":"CORPUS_REFERENCE_MODEL","origin":"CORPUS_EMPIRICAL","cohort_version":cohort.get('version'),"feature":feature,"statistic":stat,"value":stats[stat],"n":stats.get('n'),"musical_dimension":dim,"statistical_statement":f'{feature} {stat}={stats[stat]} (n={stats.get("n")})',"promotion_state":state,"promotion_record":promo})
    return {"schema":"HOOKLAB_GATE_B2_CRM_ADAPTER_v1.0","cohort":cohort,"candidate_evidence":out,"skipped":skipped,"generation_ready_n":sum(x['promotion_state']=='PROMOTED' for x in out),"invariant":"Empirical distribution != promoted generative rule."}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--crm',required=True);ap.add_argument('--cohort',required=True);ap.add_argument('--promotions');ap.add_argument('--output',required=True);a=ap.parse_args();crm=json.loads(Path(a.crm).read_text());cohort=json.loads(Path(a.cohort).read_text());prom=json.loads(Path(a.promotions).read_text()) if a.promotions else {};out=adapt(crm,cohort,prom);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({"candidates":len(out['candidate_evidence']),"generation_ready_n":out['generation_ready_n']}))
if __name__=='__main__':main()
