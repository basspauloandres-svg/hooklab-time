#!/usr/bin/env python3
"""Gate A validator: released-recording vocal reference vs symbolic vocal candidate.

This module operates only after the released-recording annotation has been frozen.
It does not acquire songs, discover MIDI/KAR candidates, or modify the TSDQP.

Input JSON schema (minimal):
{
  "song_id": "...",
  "excerpts": [
    {
      "excerpt_id": "...",
      "reference_notes": [{"start_s":0.0,"end_s":0.5,"midi_pitch":60}, ...],
      "symbolic_notes":  [{"start_s":0.01,"end_s":0.49,"midi_pitch":60}, ...]
    }
  ]
}

Times must already be expressed in a common locally aligned coordinate system.
Original note events must be retained upstream; alignment transforms are metadata,
not silent mutations of source evidence.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from scipy.optimize import linear_sum_assignment

ONSET_TOLERANCE_S = 0.050
PITCH_TOLERANCE_CENTS = 50.0
OFFSET_MIN_TOLERANCE_S = 0.050
OFFSET_REL_TOLERANCE = 0.20


@dataclass(frozen=True)
class Note:
    start_s: float
    end_s: float
    midi_pitch: float

    @property
    def duration_s(self) -> float:
        return max(0.0, self.end_s - self.start_s)


def _notes(rows: Iterable[dict]) -> list[Note]:
    out = []
    for r in rows:
        n = Note(float(r["start_s"]), float(r["end_s"]), float(r["midi_pitch"]))
        if n.end_s < n.start_s:
            raise ValueError("note end_s precedes start_s")
        out.append(n)
    return sorted(out, key=lambda x: (x.start_s, x.end_s, x.midi_pitch))


def _pitch_cents(a: Note, b: Note) -> float:
    return abs(a.midi_pitch - b.midi_pitch) * 100.0


def _offset_ok(ref: Note, est: Note) -> bool:
    tol = max(OFFSET_MIN_TOLERANCE_S, OFFSET_REL_TOLERANCE * ref.duration_s)
    return abs(ref.end_s - est.end_s) <= tol


def _eligible(ref: Note, est: Note, with_offset: bool) -> bool:
    if abs(ref.start_s - est.start_s) > ONSET_TOLERANCE_S:
        return False
    if _pitch_cents(ref, est) > PITCH_TOLERANCE_CENTS:
        return False
    return (not with_offset) or _offset_ok(ref, est)


def _match(refs: list[Note], ests: list[Note], with_offset: bool) -> list[tuple[int, int]]:
    if not refs or not ests:
        return []
    # Assignment cost privileges eligible pairs and, among them, minimal onset/pitch error.
    BIG = 1e6
    cost = []
    for r in refs:
        row = []
        for e in ests:
            if not _eligible(r, e, with_offset):
                row.append(BIG)
            else:
                row.append(abs(r.start_s - e.start_s) + (_pitch_cents(r, e) / 10000.0))
        cost.append(row)
    ri, ci = linear_sum_assignment(cost)
    return [(int(i), int(j)) for i, j in zip(ri, ci) if cost[int(i)][int(j)] < BIG]


def _overlap_ratio(a: Note, b: Note) -> float:
    inter = max(0.0, min(a.end_s, b.end_s) - max(a.start_s, b.start_s))
    union = max(a.end_s, b.end_s) - min(a.start_s, b.start_s)
    return inter / union if union > 0 else 0.0


def transcription_metrics(refs: list[Note], ests: list[Note], with_offset: bool) -> dict:
    pairs = _match(refs, ests, with_offset)
    tp = len(pairs)
    precision = tp / len(ests) if ests else (1.0 if not refs else 0.0)
    recall = tp / len(refs) if refs else (1.0 if not ests else 0.0)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    overlaps = [_overlap_ratio(refs[i], ests[j]) for i, j in pairs]
    return {
        "matched_notes": tp,
        "reference_notes": len(refs),
        "symbolic_notes": len(ests),
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
        "average_overlap": round(sum(overlaps) / len(overlaps), 6) if overlaps else 0.0,
        "matched_pairs": pairs,
    }


def _intervals(notes: list[Note]) -> list[int]:
    return [int(round(notes[i].midi_pitch - notes[i - 1].midi_pitch)) for i in range(1, len(notes))]


def _directions(intervals: list[int]) -> list[int]:
    return [1 if x > 0 else -1 if x < 0 else 0 for x in intervals]


def _pitch_class_contour(notes: list[Note]) -> list[int]:
    # Relative pitch-class motion, transposition invariant after first note normalization.
    if not notes:
        return []
    base = int(round(notes[0].midi_pitch)) % 12
    return [((int(round(n.midi_pitch)) % 12) - base) % 12 for n in notes]


def _lcs_ratio(a: list[int], b: list[int]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, start=1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1] / max(len(a), len(b))


def tolerant_identity_metrics(refs: list[Note], ests: list[Note]) -> dict:
    r_int, e_int = _intervals(refs), _intervals(ests)
    return {
        "interval_sequence_agreement": round(_lcs_ratio(r_int, e_int), 6),
        "pitch_class_contour_agreement": round(_lcs_ratio(_pitch_class_contour(refs), _pitch_class_contour(ests)), 6),
        "direction_sequence_agreement": round(_lcs_ratio(_directions(r_int), _directions(e_int)), 6),
    }


def classify_excerpt(metrics: dict) -> str:
    # Conservative operational rule for the T0 calibration seed.
    # Strong evidence requires both note-level agreement and structural identity.
    f1 = metrics["absolute_no_offset"]["f1"]
    interval = metrics["tolerant_identity"]["interval_sequence_agreement"]
    direction = metrics["tolerant_identity"]["direction_sequence_agreement"]
    if f1 >= 0.80 and interval >= 0.80 and direction >= 0.85:
        return "AUDIO_REFERENCE_PASS"
    if f1 >= 0.60 and interval >= 0.60 and direction >= 0.70:
        return "AUDIO_REFERENCE_AUDIT"
    return "AUDIO_REFERENCE_FAIL"


def validate_excerpt(excerpt: dict) -> dict:
    refs = _notes(excerpt.get("reference_notes", []))
    ests = _notes(excerpt.get("symbolic_notes", []))
    metrics = {
        "absolute_no_offset": transcription_metrics(refs, ests, with_offset=False),
        "absolute_with_offset": transcription_metrics(refs, ests, with_offset=True),
        "tolerant_identity": tolerant_identity_metrics(refs, ests),
    }
    return {
        "excerpt_id": excerpt.get("excerpt_id"),
        "reference_note_n": len(refs),
        "symbolic_note_n": len(ests),
        "metrics": metrics,
        "excerpt_decision": classify_excerpt(metrics),
        "alignment_transform": excerpt.get("alignment_transform"),
        "audit_notes": excerpt.get("audit_notes", ""),
    }


def song_decision(rows: list[dict]) -> str:
    if not rows:
        return "AUDIO_REFERENCE_AUDIT"
    states = [r["excerpt_decision"] for r in rows]
    if all(x == "AUDIO_REFERENCE_PASS" for x in states):
        return "AUDIO_REFERENCE_PASS"
    if any(x == "AUDIO_REFERENCE_FAIL" for x in states):
        return "AUDIO_REFERENCE_FAIL"
    return "AUDIO_REFERENCE_AUDIT"


def validate(payload: dict) -> dict:
    rows = [validate_excerpt(x) for x in payload.get("excerpts", [])]
    return {
        "schema": "HOOKLAB_EXTERNAL_VOCAL_IDENTITY_VALIDATION_RESULT_v1.0",
        "gate": "A",
        "song_id": payload.get("song_id"),
        "release_reference": payload.get("release_reference"),
        "reference_annotation_frozen": bool(payload.get("reference_annotation_frozen", False)),
        "independence_attested": bool(payload.get("independence_attested", False)),
        "thresholds": {
            "onset_tolerance_s": ONSET_TOLERANCE_S,
            "pitch_tolerance_cents": PITCH_TOLERANCE_CENTS,
            "offset_min_tolerance_s": OFFSET_MIN_TOLERANCE_S,
            "offset_relative_tolerance": OFFSET_REL_TOLERANCE,
        },
        "excerpts": rows,
        "song_decision": song_decision(rows),
        "scientific_eligibility": bool(rows)
        and bool(payload.get("reference_annotation_frozen", False))
        and bool(payload.get("independence_attested", False)),
        "interpretation_boundary": "This result validates released-recording vocal identity for the evaluated excerpts only; it does not establish population-level sensitivity/specificity or target-population representativeness.",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    out = validate(payload)
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"song_id": out["song_id"], "song_decision": out["song_decision"], "scientific_eligibility": out["scientific_eligibility"]}))


if __name__ == "__main__":
    main()
