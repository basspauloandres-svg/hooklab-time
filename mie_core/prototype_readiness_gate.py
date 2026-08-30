#!/usr/bin/env python3
"""Evaluate when HookLab has enough full-song cohort evidence to generate a prototype.

This is an engineering gate for the prototype stage, not a statistical adequacy test.
Short previews may validate extraction engineering but can never activate generation.
Generation becomes eligible only when a coherent genre/style cohort contains at least
three STRICT_PASS full-song rows with non-null coverage for the required TMT fields.
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
FULL_COVERAGE_VALUES = {"FULL", "FULL_SONG", "COMPLETE", "STRUCTURALLY_COMPLETE"}


def norm(x):
    return "_".join(str(x or "").strip().lower().replace("-", " ").split())


def ok(v):
    return v is not None and str(v).strip() not in {"", "NA", "NaN", "nan", "null", "None"}


def full_song(r):
    coverage = str(r.get("coverage", r.get("audio_coverage", r.get("analysis_coverage", "")))).upper().strip()
    scope = str(r.get("audio_scope", r.get("source_scope", ""))).upper()
    role = str(r.get("evidence_role", r.get("role", ""))).upper()
    if "PREVIEW" in coverage or "PREVIEW" in scope or "SHORT" in scope or "ENGINEERING_PROBE" in role:
        return False
    return coverage in FULL_COVERAGE_VALUES


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--min-n", type=int, default=3)
    args = ap.parse_args()

    rows = list(csv.DictReader(Path(args.matrix).open(encoding="utf-8")))
    cohorts = defaultdict(list)
    excluded_short = []
    for r in rows:
        strict = str(r.get("strict_gate", r.get("status", ""))).upper()
        if "PASS" not in strict:
            continue
        if not full_song(r):
            excluded_short.append({"song_id": r.get("song_id"), "genre": r.get("genre"), "style": r.get("style"),
                                   "coverage": r.get("coverage", r.get("audio_coverage", r.get("analysis_coverage")))})
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
            "strict_pass_full_song_n": len(rs),
            "complete_full_song_tmt_n": len(complete),
            "required_fields": REQUIRED,
            "coverage_requirement": "FULL_SONG_ONLY",
            "ready": len(complete) >= args.min_n,
        })

    ready = [x for x in report if x["ready"]]
    out = {
        "schema": "HOOKLAB_PROTOTYPE_READINESS_GATE_v1.1",
        "status": "READY_FOR_DATA_CONDITIONED_GENERATION" if ready else "BUILD_MORE_FULL_SONG_COHORT_EVIDENCE",
        "min_complete_strict_pass_per_cohort": args.min_n,
        "coverage_gate": "FULL_SONG_ONLY",
        "short_preview_policy": "ENGINEERING_PROBE_ONLY; excluded from Matrix-X generation readiness and cohort-conditioned rules",
        "excluded_non_full_song_count": len(excluded_short),
        "excluded_non_full_song": excluded_short,
        "ready_cohorts": ready,
        "all_cohorts": report,
        "epistemic_note": "min_n is a prototype engineering trigger, not an inferential sufficiency claim; full-song coverage prevents fragment-selection bias from entering generation readiness."
    }
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))
    raise SystemExit(0 if ready else 4)


if __name__ == "__main__":
    main()
