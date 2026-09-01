#!/usr/bin/env python3
"""Aggregate Gate A released-recording validation results for the five-song T0 seed.

This gate does not discover songs or symbolic representations. It consumes only
completed per-song outputs from external_vocal_identity_validator.py and preserves
the TSDQP distinction between candidate discovery and scientific promotion.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_SONGS = {
    "poker_face_lady_gaga",
    "bad_romance_lady_gaga",
    "tik_tok_kesha",
    "firework_katy_perry",
    "dynamite_taio_cruz",
}


def evaluate(results: list[dict]) -> dict:
    by_id = {r.get("song_id"): r for r in results if r.get("song_id")}
    missing = sorted(EXPECTED_SONGS - set(by_id))
    unexpected = sorted(set(by_id) - EXPECTED_SONGS)
    rows = []
    for sid in sorted(EXPECTED_SONGS):
        r = by_id.get(sid)
        if r is None:
            rows.append({"song_id": sid, "decision": "MISSING", "scientific_eligibility": False})
            continue
        rows.append({
            "song_id": sid,
            "decision": r.get("song_decision"),
            "scientific_eligibility": bool(r.get("scientific_eligibility", False)),
        })

    eligible_pass = [x for x in rows if x["scientific_eligibility"] and x["decision"] == "AUDIO_REFERENCE_PASS"]
    audits = [x for x in rows if x["decision"] == "AUDIO_REFERENCE_AUDIT"]
    fails = [x for x in rows if x["decision"] == "AUDIO_REFERENCE_FAIL"]

    pass_n = len(eligible_pass)
    if not missing and not unexpected and pass_n == 5:
        status = "SEED_EXTERNALLY_CALIBRATED"
        promotion = True
    elif not missing and pass_n == 4 and len(fails) + len(audits) == 1:
        status = "AUDIT_DISCREPANT_CASE_BEFORE_PROMOTION"
        promotion = False
    else:
        status = "SCIENTIFIC_PROMOTION_BLOCKED"
        promotion = False

    return {
        "schema": "HOOKLAB_EXTERNAL_VOCAL_IDENTITY_SEED_GATE_v1.0",
        "gate": "A",
        "expected_seed_n": 5,
        "evaluated_n": len(results),
        "eligible_audio_reference_pass_n": pass_n,
        "missing_song_ids": missing,
        "unexpected_song_ids": unexpected,
        "rows": rows,
        "status": status,
        "scientific_promotion": promotion,
        "population_claim": "NONE_T0_CALIBRATION_SEED_ONLY",
        "invariants": [
            "scientific target population != songs available in Lakh/LMD",
            "candidate discovery != scientific promotion",
            "symbolic binding != released-recording vocal identity"
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", nargs="+", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    results = [json.loads(Path(p).read_text(encoding="utf-8")) for p in args.inputs]
    out = evaluate(results)
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": out["status"], "pass_n": out["eligible_audio_reference_pass_n"], "scientific_promotion": out["scientific_promotion"]}))
    raise SystemExit(0 if out["scientific_promotion"] else 4)


if __name__ == "__main__":
    main()
