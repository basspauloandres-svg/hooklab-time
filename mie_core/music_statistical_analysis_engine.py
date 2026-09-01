"""Registered numeric statistics for HookLab melody and beat features.

This engine consumes only abstract, calibrated numeric feature records. It does
not decode audio or MIDI, infer features, or promote a compositional rule from
a descriptive distribution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path
from typing import Any

from mie_core.lyric_statistical_analysis_engine import (
    COMPUTATION_ORIGIN,
    TREND_ORIGIN_POLICY,
    audit_registration,
)


ENGINE_VERSION = "hooklab-music-statistical-analysis-engine-v0.1"


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _quantile(values: list[float], probability: float) -> float:
    if not values:
        raise ValueError("empty values")
    if len(values) == 1:
        return values[0]
    position = (len(values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return values[lower]
    weight = position - lower
    return values[lower] * (1 - weight) + values[upper] * weight


def execute_descriptive_numeric(
    registration: dict[str, Any],
    feature_contract: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    audit = audit_registration(registration, feature_contract)
    audit["engine_version"] = ENGINE_VERSION
    if audit["status"] != "ANALYSIS_REGISTRATION_PASS":
        return {
            "schema": "HOOKLAB_MUSIC_ANALYSIS_AUDIT_v1",
            "status": "AUDIT",
            "analysis_id": registration.get("analysis_id"),
            "registration_audit": audit,
            "statistical_computation_executed": False,
            "scientific_d_unlocked": False,
            "engine_version": ENGINE_VERSION,
        }
    if registration.get("analysis_type") != "DESCRIPTIVE_NUMERIC_FINITE_CORPUS":
        return {
            "schema": "HOOKLAB_MUSIC_ANALYSIS_AUDIT_v1",
            "status": "AUDIT",
            "analysis_id": registration.get("analysis_id"),
            "violations": ["UNSUPPORTED_ANALYSIS_TYPE"],
            "statistical_computation_executed": False,
            "scientific_d_unlocked": False,
            "engine_version": ENGINE_VERSION,
        }

    forbidden_fields = {
        "audio",
        "audio_bytes",
        "midi",
        "midi_bytes",
        "raw_events",
        "raw_text",
        "lyrics",
    }
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    violations: list[str] = []
    for row in records:
        if forbidden_fields.intersection(row):
            violations.append("RAW_SOURCE_FIELD_PRESENT")
        case_id = str(row.get("case_id") or "").strip()
        value = row.get("value")
        if not case_id or isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            violations.append("MISSING_CASE_OR_FINITE_NUMERIC_VALUE")
            continue
        if case_id in seen:
            violations.append(f"DUPLICATE_CASE_ID:{case_id}")
            continue
        seen.add(case_id)
        normalized.append({"case_id": case_id, "value": float(value)})

    criteria = registration.get("effect_size_criterion") or {}
    minimum_n = criteria.get("minimum_n")
    if minimum_n is None:
        violations.append("MINIMUM_N_NOT_PREDECLARED")
    elif len(normalized) < int(minimum_n):
        violations.append("INSUFFICIENT_PREDECLARED_N")
    if violations:
        return {
            "schema": "HOOKLAB_MUSIC_ANALYSIS_AUDIT_v1",
            "status": "AUDIT",
            "analysis_id": registration.get("analysis_id"),
            "violations": sorted(set(violations)),
            "statistical_computation_executed": False,
            "scientific_d_unlocked": False,
            "engine_version": ENGINE_VERSION,
        }

    values = sorted(row["value"] for row in normalized)
    median = statistics.median(values)
    deviations = sorted(abs(value - median) for value in values)
    summary = {
        "n": len(values),
        "minimum": values[0],
        "q1": _quantile(values, 0.25),
        "median": median,
        "q3": _quantile(values, 0.75),
        "maximum": values[-1],
        "mean": statistics.fmean(values),
        "median_absolute_deviation": statistics.median(deviations),
    }
    return {
        "schema": "HOOKLAB_MUSIC_DESCRIPTIVE_RESULT_v1",
        "status": "STATISTICAL_RESULT_COMPLETE",
        "analysis_id": registration["analysis_id"],
        "feature_id": feature_contract["feature_id"],
        "population_scope": registration["population_scope"],
        "source_revision": registration["source_revision"],
        "data_says": summary,
        "statistics_say": "DESCRIPTIVE_DISTRIBUTION_ONLY",
        "theory_says": None,
        "generation_tests": None,
        "producer_decides": None,
        "disposition": "NO_PROMOTION",
        "promotion_boundary": "DESCRIPTIVE_NUMERIC_SUMMARY_CANNOT_BY_ITSELF_CREATE_A_CONDITIONED_DEDUCTION",
        "computation_origin": COMPUTATION_ORIGIN,
        "trend_origin_policy": TREND_ORIGIN_POLICY,
        "human_trend_override_applied": False,
        "ai_trend_override_applied": False,
        "literature_direction_applied": False,
        "producer_preference_applied": False,
        "generation_class": "D0_EXPLORATORY",
        "scientific_d_unlocked": False,
        "registration_hash_sha256": _canonical_hash(registration),
        "normalized_input_hash_sha256": _canonical_hash(normalized),
        "engine_version": ENGINE_VERSION,
    }


def _load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="HookLab registered melody/beat numeric statistics")
    parser.add_argument("--analysis", required=True)
    parser.add_argument("--feature-contract", required=True)
    parser.add_argument("--records", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    result = execute_descriptive_numeric(_load(args.analysis), _load(args.feature_contract), _load(args.records))
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0 if result.get("status") == "STATISTICAL_RESULT_COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
