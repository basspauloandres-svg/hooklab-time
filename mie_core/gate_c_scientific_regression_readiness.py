#!/usr/bin/env python3
"""Gate C fail-closed scientific regression readiness guard.

This module does not rerun or redesign existing technical pipelines. It evaluates
whether the scientific prerequisites needed to launch the final integral regression
are present: observed Gate A evidence, observed Gate B evidence, and technical
regression availability/provenance.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

SCHEMA="HOOKLAB_GATE_C_SCIENTIFIC_REGRESSION_READINESS_v1.0"

def evaluate(payload: dict) -> dict:
    a=payload.get("gate_a",{})
    b=payload.get("gate_b",{})
    tech=payload.get("technical_regression",{})
    docs=payload.get("documentation",{})

    gate_a_observed=bool(a.get("observed_external_validation")) and a.get("state") in {"PASS","AUDIT","FAIL","SEED_EXTERNALLY_CALIBRATED"}
    gate_b_observed=int(b.get("valid_human_trial_n",0))>=1 and bool(b.get("raw_artifacts_retained"))
    technical_ready=bool(tech.get("existing_e2e_available")) and bool(tech.get("existing_replay_available"))
    provenance_ready=bool(docs.get("provenance_manifest_ready")) and bool(docs.get("checkpoint_chain_ready"))

    checks={
        "gate_a_observed_external_evidence":gate_a_observed,
        "gate_b_observed_human_baseline":gate_b_observed,
        "existing_technical_regression_available":technical_ready,
        "provenance_and_checkpoint_chain_ready":provenance_ready,
    }
    ready=all(checks.values())
    return {
        "schema":SCHEMA,
        "checks":checks,
        "state":"SCIENTIFIC_REGRESSION_READY" if ready else "SCIENTIFIC_REGRESSION_BLOCKED",
        "blocked_by":[k for k,v in checks.items() if not v],
        "scientific_completion_claim_allowed":False,
        "invariant":"Gate C cannot convert REFERENCE_UNAVAILABLE, missing human observations, or implementation-only states into scientific PASS.",
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--input",required=True);ap.add_argument("--output",required=True);a=ap.parse_args()
    out=evaluate(json.loads(Path(a.input).read_text(encoding="utf-8")))
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({"state":out["state"],"blocked_by":out["blocked_by"]}))

if __name__=="__main__": main()
