#!/usr/bin/env python3
"""Fail-closed admissibility gate for external symbolic sources used in T1/T2 robust build.

A source may be discovered without being scientifically usable. PASS requires explicit
computational-processing authorization plus a full-length auditable symbolic artifact.
Playback/download availability alone is insufficient.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

REQUIRED_TRUE=("identity_resolved","version_resolved","full_length","provenance_available","computational_processing_authorized")

def evaluate(row):
    reasons=[]
    for k in REQUIRED_TRUE:
        if row.get(k) is not True:
            reasons.append(f"{k.upper()}_NOT_CONFIRMED")
    if row.get("access_mode") not in {"PUBLIC_DOWNLOAD","AUTHORIZED_DOWNLOAD","API_AUTHORIZED","DATASET_AUTHORIZED","PURCHASED_WITH_PROCESSING_RIGHTS"}:
        reasons.append("ACCESS_MODE_NOT_ADMISSIBLE")
    if row.get("source_kind") in {"PREVIEW","DEMO_FRAGMENT","STREAM_ONLY"}:
        reasons.append("NON_FULL_SYMBOLIC_SOURCE")
    status="PASS" if not reasons else "AUDIT"
    return {**row,"symbolic_source_gate":status,"admissibility_reasons":reasons,"scientific_use_ready":status=="PASS"}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    payload=json.loads(Path(a.input).read_text(encoding='utf-8'))
    rows=[evaluate(x) for x in payload.get('sources',[])]
    out={"schema":"HOOKLAB_SYMBOLIC_SOURCE_ADMISSIBILITY_v1.0","sources":rows,"pass_n":sum(x['symbolic_source_gate']=='PASS' for x in rows),"audit_n":sum(x['symbolic_source_gate']=='AUDIT' for x in rows),"invariant":"discoverable symbolic source != scientifically admissible symbolic source"}
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps({"pass":out['pass_n'],"audit":out['audit_n']}))
if __name__=='__main__':main()
