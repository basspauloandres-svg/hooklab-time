"""Fail-closed measurement calibration for HookLab lyric, melody and beat lanes.

This module measures agreement or error only.  It cannot perform association
tests, infer success rules, promote compositional deductions, or unlock
scientific generation.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any


ENGINE_VERSION = "hooklab-measurement-calibration-engine-v0.1"


def _quantile(values: list[float], probability: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * probability
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def _average_ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    cursor = 0
    while cursor < len(order):
        end = cursor + 1
        while end < len(order) and values[order[end]] == values[order[cursor]]:
            end += 1
        rank = (cursor + 1 + end) / 2
        for index in order[cursor:end]:
            ranks[index] = rank
        cursor = end
    return ranks


def _pearson(left: list[float], right: list[float]) -> float | None:
    if len(left) < 2 or len(left) != len(right):
        return None
    left_mean, right_mean = statistics.fmean(left), statistics.fmean(right)
    numerator = sum((x - left_mean) * (y - right_mean) for x, y in zip(left, right))
    left_ss = sum((x - left_mean) ** 2 for x in left)
    right_ss = sum((y - right_mean) ** 2 for y in right)
    denominator = math.sqrt(left_ss * right_ss)
    return numerator / denominator if denominator else None


def spearman_rho(reference: list[float], estimate: list[float]) -> float | None:
    return _pearson(_average_ranks(reference), _average_ranks(estimate))


def categorical_agreement(units: list[dict[str, Any]]) -> dict[str, Any]:
    pairs = []
    for unit in units:
        ratings = [str(value) for value in unit.get("ratings", []) if value is not None]
        if len(ratings) == 2:
            pairs.append(ratings)
    flat = [rating for pair in pairs for rating in pair]
    counts = Counter(flat)
    comparable = len(pairs)
    raw_agreement = sum(left == right for left, right in pairs) / comparable if comparable else None
    observed_disagreement = 1 - raw_agreement if raw_agreement is not None else None
    total = len(flat)
    expected_agreement = (
        sum(count * (count - 1) for count in counts.values()) / (total * (total - 1))
        if total > 1 else None
    )
    expected_disagreement = 1 - expected_agreement if expected_agreement is not None else None
    alpha = (
        1 - observed_disagreement / expected_disagreement
        if observed_disagreement is not None and expected_disagreement not in {None, 0}
        else None
    )
    present_both = sum(left == right == "PRESENT" for left, right in pairs)
    present_one = sum((left == "PRESENT") != (right == "PRESENT") for left, right in pairs)
    positive_agreement = (
        2 * present_both / (2 * present_both + present_one)
        if 2 * present_both + present_one else None
    )
    return {
        "comparable_units": comparable,
        "category_counts": dict(sorted(counts.items())),
        "raw_agreement": raw_agreement,
        "krippendorff_alpha_nominal": alpha,
        "positive_agreement_present": positive_agreement,
        "unresolved_rating_rate": counts.get("UNRESOLVED", 0) / total if total else None,
    }


def numeric_agreement(pairs: list[dict[str, Any]]) -> dict[str, Any]:
    values = [
        (float(row["reference"]), float(row["estimate"]))
        for row in pairs
        if row.get("reference") is not None and row.get("estimate") is not None
    ]
    reference = [row[0] for row in values]
    estimate = [row[1] for row in values]
    differences = [est - ref for ref, est in values]
    absolute = [abs(value) for value in differences]
    relative = [abs(est - ref) / abs(ref) for ref, est in values if ref != 0]
    octave_flags = [bool(row.get("octave_or_tactus_error")) for row in pairs if row.get("reference") is not None and row.get("estimate") is not None]
    bias = statistics.fmean(differences) if differences else None
    difference_sd = statistics.stdev(differences) if len(differences) > 1 else None
    return {
        "aligned_pairs": len(values),
        "spearman_rho": spearman_rho(reference, estimate) if values else None,
        "median_absolute_error": statistics.median(absolute) if absolute else None,
        "mean_absolute_error": statistics.fmean(absolute) if absolute else None,
        "p90_absolute_error": _quantile(absolute, 0.9),
        "median_absolute_percentage_error": statistics.median(relative) if relative else None,
        "octave_or_tactus_error_rate": sum(octave_flags) / len(octave_flags) if octave_flags else None,
        "mean_bias": bias,
        "bland_altman_95_limits": (
            [bias - 1.96 * difference_sd, bias + 1.96 * difference_sd]
            if bias is not None and difference_sd is not None else None
        ),
    }


def beat_f_measure(reference: list[float], estimate: list[float], tolerance_seconds: float = 0.07) -> dict[str, Any]:
    reference = sorted(float(value) for value in reference)
    estimate = sorted(float(value) for value in estimate)
    used: set[int] = set()
    true_positive = 0
    for predicted in estimate:
        candidates = [
            (abs(predicted - observed), index)
            for index, observed in enumerate(reference)
            if index not in used and abs(predicted - observed) <= tolerance_seconds
        ]
        if candidates:
            _, index = min(candidates)
            used.add(index)
            true_positive += 1
    precision = true_positive / len(estimate) if estimate else 0.0
    recall = true_positive / len(reference) if reference else 0.0
    f_measure = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "reference_beats": len(reference),
        "estimated_beats": len(estimate),
        "true_positive": true_positive,
        "precision": precision,
        "recall": recall,
        "f_measure": f_measure,
        "tolerance_seconds": tolerance_seconds,
    }


def execute(payload: dict[str, Any]) -> dict[str, Any]:
    mode = payload.get("mode")
    result: dict[str, Any]
    if mode == "CATEGORICAL_DOUBLE_ANNOTATION":
        result = categorical_agreement(payload.get("units") or [])
    elif mode == "NUMERIC_REFERENCE_COMPARISON":
        result = numeric_agreement(payload.get("pairs") or [])
    elif mode == "BEAT_REFERENCE_COMPARISON":
        songs = []
        for row in payload.get("songs") or []:
            songs.append({
                "case_id": row.get("case_id"),
                **beat_f_measure(row.get("reference_beats") or [], row.get("estimated_beats") or []),
            })
        result = {
            "song_count": len(songs),
            "median_f_measure": statistics.median([row["f_measure"] for row in songs]) if songs else None,
            "p10_f_measure": _quantile([row["f_measure"] for row in songs], 0.1),
            "songs": songs,
        }
    else:
        return {
            "schema": "HOOKLAB_MEASUREMENT_CALIBRATION_REPORT_v1",
            "status": "AUDIT_UNSUPPORTED_CALIBRATION_MODE",
            "calibration_executed": False,
            "scientific_d_unlocked": False,
            "engine_version": ENGINE_VERSION,
        }
    return {
        "schema": "HOOKLAB_MEASUREMENT_CALIBRATION_REPORT_v1",
        "status": "CALIBRATION_METRICS_COMPUTED_NOT_FEATURE_PROMOTED",
        "mode": mode,
        "calibration_executed": True,
        "result": result,
        "association_test_executed": False,
        "conditioned_deduction_created": False,
        "scientific_d_unlocked": False,
        "engine_version": ENGINE_VERSION,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = execute(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
