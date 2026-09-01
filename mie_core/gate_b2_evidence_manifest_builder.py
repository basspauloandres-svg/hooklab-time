#!/usr/bin/env python3
"""Gate B2 evidence manifest builder.

Fail-closed bridge between validated cohort statistics and creative generation.
It does not invent statistics or promote descriptive/candidate evidence.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
ALLOWED_PROMOTION={"PROMOTED","VALIDATED","ELIGIBLE"}
DIMENSIONS={"FORM","TEMPO_METER","HARMONY","MELODY","RHYTHM","PRODUCTION"}

def build(payload):
    accepted=[]; rejected=[]
    for i,e in enumerate(payload.get("evidence",[])):
        reasons=[]
        if e.get("promotion_state") not in ALLOWED_PROMOTION: reasons.append("NOT_SCIENTIFICALLY_ELIGIBLE")
        if not e.get("evidence_id"): reasons.append("MISSING_EVIDENCE_ID")
        if not e.get("cohort_version"): reasons.append("MISSING_COHORT_VERSION")
        if not e.get("statistical_statement"): reasons.append("MISSING_STATISTICAL_STATEMENT")
        if e.get("musical_dimension") not in DIMENSIONS: reasons.append("INVALID_MUSICAL_DIMENSION")
        if e.get("source_kind") in {"CANDIDATE_DISCOVERY","SINGLE_SONG_UNPROMOTED"}: reasons.append("DISALLOWED_SOURCE_KIND")
        row={**e,"manifest_index":i}
        (rejected if reasons else accepted).append({**row,"rejection_reasons":reasons} if reasons else row)
    return {"schema":"HOOKLAB_GATE_B2_EVIDENCE_MANIFEST_v1.0","experiment_id":payload.get("experiment_id"),"cohort":payload.get("cohort"),"accepted_evidence":accepted,"rejected_evidence":rejected,"generation_eligible":bool(accepted) and not rejected,"decision":"READY_FOR_D_GENERATION" if accepted and not rejected else "BLOCKED_EVIDENCE_AUDIT","invariant":"candidate discovery != scientific promotion"}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--input",required=True);ap.add_argument("--output",required=True);a=ap.parse_args();out=build(json.loads(Path(a.input).read_text(encoding="utf-8")));Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8");print(json.dumps({"decision":out["decision"],"accepted":len(out["accepted_evidence"]),"rejected":len(out["rejected_evidence"])}))
if __name__=="__main__":main()
