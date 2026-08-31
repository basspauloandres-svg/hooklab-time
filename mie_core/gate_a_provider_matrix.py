#!/usr/bin/env python3
"""Gate A provider-exhaustion matrix and rate calculator.

This module does not acquire audio. It records provider observations and enforces
Gate A semantics: reference unavailability is AUDIT, never an algorithmic FAIL.
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FINAL_STATES={"PASS","FAIL","AUDIT","REFERENCE_UNAVAILABLE"}


def summarize(rows):
    songs=sorted({r["song_id"] for r in rows})
    n=len(songs)
    by={s:[r for r in rows if r["song_id"]==s] for s in songs}
    resolved=[]; validated=[]; audits=[]; failures=[]
    song_states={}
    for s, rr in by.items():
        # A reference is resolver-covered only when a concrete route is both
        # processable and authorized for this project/track, not merely conditionally available.
        has_ref=any(str(r.get("authorized_computational_access","")).lower()=="true" and r.get("result")=="AUTHORIZED_REFERENCE_READY" for r in rr)
        vals=[r for r in rr if r.get("validation_state") in {"PASS","FAIL"}]
        if has_ref: resolved.append(s)
        if vals: validated.append(s)
        if any(r.get("validation_state")=="FAIL" for r in vals): failures.append(s); state="FAIL"
        elif any(r.get("validation_state")=="PASS" for r in vals): state="PASS"
        else: audits.append(s); state="AUDIT"
        song_states[s]=state
    pct=lambda x: round(100.0*len(x)/n,2) if n else 0.0
    return {
      "schema":"HOOKLAB_GATE_A_PROVIDER_MATRIX_SUMMARY_v1.0",
      "song_n":n,
      "resolver_coverage_rate":{"n":len(resolved),"denominator":n,"percent":pct(resolved)},
      "automatic_validation_rate":{"n":len(validated),"denominator":n,"percent":pct(validated)},
      "audit_rate":{"n":len(audits),"denominator":n,"percent":pct(audits)},
      "true_validation_failure_rate":{"n":len(failures),"denominator":n,"percent":pct(failures)},
      "song_states":song_states,
      "invariant":"REFERENCE_UNAVAILABLE_IS_AUDIT_NOT_ALGORITHMIC_FAIL"
    }


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--matrix",required=True); ap.add_argument("--output",required=True); a=ap.parse_args()
    rows=list(csv.DictReader(Path(a.matrix).open(encoding="utf-8")))
    out=summarize(rows)
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(out))
if __name__=="__main__": main()
