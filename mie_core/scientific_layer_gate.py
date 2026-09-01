#!/usr/bin/env python3
"""Fail-closed approval gate for HookLab/TIME scientific layers."""
from __future__ import annotations
import argparse,json
from pathlib import Path
REQUIRED=("scientific_basis","decision_record","implementation","provenance","checkpoint")
VALIDATED_STATES={"VALIDATED","APPROVED","DOWNSTREAM_ELIGIBLE"}

def evaluate(layer):
    missing=[k for k in REQUIRED if not layer.get(k)]
    validation=layer.get("tests_or_validation")
    if validation is None: missing.append("tests_or_validation")
    state=layer.get("state","PROPOSED")
    approved=(not missing and state in {"APPROVED","DOWNSTREAM_ELIGIBLE"} and bool(layer.get("approval_decision")))
    return {"schema":"HOOKLAB_SCIENTIFIC_LAYER_GATE_v1.0","layer_id":layer.get("layer_id"),"input_state":state,"missing_requirements":missing,"approved":approved,"downstream_eligible":approved,"decision":"PASS" if approved else "BLOCKED","invariant":"No downstream scientific layer may consume an unapproved upstream layer."}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();out=evaluate(json.loads(Path(a.input).read_text(encoding='utf-8')));Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps({"decision":out["decision"],"layer_id":out["layer_id"]}))
if __name__=='__main__':main()
