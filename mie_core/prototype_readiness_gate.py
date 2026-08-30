#!/usr/bin/env python3
"""Evaluate when HookLab has enough real cohort evidence to generate a prototype.

This is an engineering gate for the prototype stage, not a statistical adequacy test.
Generation becomes eligible when a coherent genre/style cohort contains at least three
STRICT_PASS rows with non-null coverage for the required TMT fields.
"""
import argparse, csv, json
from collections import defaultdict
from pathlib import Path

REQUIRED = [
    "tempo_bpm",
    "melodic_range_semitones",
    "melodic_events_per_token",
    "near_tactus_share",
    "text_line_count",
]


def norm(x):
    return "_".join(str(x or "").strip().lower().replace("-", " ").split())


def ok(v):
    return v is not None and str(v).strip() not in {"", "NA", "NaN", "nan", "null", "None"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--min-n", type=int, default=3)
    args = ap.parse_args()

    rows = list(csv.DictReader(Path(args.matrix).open(encoding="utf-8")))
    cohorts = defaultdict(list)
    for r in rows:
        strict = str(r.get("strict_gate", r.get("status", ""))).upper()
        if "PASS" not in strict:
            continue
        key = f"{norm(r.get('genre'))}::{norm(r.get('style'))}"
        if key == "::":
            continue
        cohorts[key].append(r)

    report = []
    for key, rs in sorted(cohorts.items()):
        complete = [r for r in rs if all(ok(r.get(f)) for f in REQUIRED)]
        report.append({
            "cohort_key": key,
            "strict_pass_n": len(rs),
            "complete_tmt_n": len(complete),
            "required_fields": REQUIRED,
            "ready": len(complete) >= args.min_n,
        })

    ready = [x for x in report if x["ready"]]
    out = {
        "schema": "HOOKLAB_PROTOTYPE_READINESS_GATE_v1.0",
        "status": "READY_FOR_DATA_CONDITIONED_GENERATION" if ready else "BUILD_MORE_COHORT_EVIDENCE",
        "min_complete_strict_pass_per_cohort": args.min_n,
        "ready_cohorts": ready,
        "all_cohorts": report,
        "epistemic_note": "min_n is a prototype engineering trigger, not an inferential sufficiency claim."
    }
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))
    raise SystemExit(0 if ready else 4)


if __name__ == "__main__":
    main()
