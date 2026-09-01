"""HookLab lyric statistical engine v0.1.

The engine computes registered results from abstract feature records. It never
reads or emits lyric text and fails closed when direction or result provenance
can be supplied by human, AI, literature, or producer preference.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


ENGINE_VERSION = "hooklab-lyric-statistical-analysis-engine-v0.1"
TREND_ORIGIN_POLICY = "REGISTERED_DATA_AND_STATISTICS_ONLY"
COMPUTATION_ORIGIN = "REGISTERED_STATISTICAL_ENGINE"

REQUIRED_ANALYSIS_FIELDS = (
    "analysis_id",
    "registration_status",
    "analysis_type",
    "research_question",
    "population_scope",
    "outcome",
    "admissible_feature_ids",
    "primary_tests",
    "covariates",
    "multiplicity_family",
    "effect_size_criterion",
    "robustness_plan",
    "replication_requirement",
    "stop_promotion_rule",
    "expected_direction",
    "trend_origin_policy",
    "human_trend_override_allowed",
    "ai_trend_override_allowed",
    "literature_sets_empirical_direction",
    "producer_preference_used_as_evidence",
    "source_revision",
    "feature_registry_id",
)


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def audit_registration(registration: dict[str, Any], feature_contract: dict[str, Any]) -> dict[str, Any]:
    missing = [field for field in REQUIRED_ANALYSIS_FIELDS if field not in registration]
    violations: list[str] = []

    if registration.get("registration_status") != "ANALYSIS_REGISTERED":
        violations.append("REGISTRATION_STATUS_NOT_ANALYSIS_REGISTERED")
    if registration.get("expected_direction") is not None:
        violations.append("EXPECTED_DIRECTION_MUST_BE_NULL")
    if registration.get("trend_origin_policy") != TREND_ORIGIN_POLICY:
        violations.append("INVALID_TREND_ORIGIN_POLICY")

    false_boundaries = (
        "human_trend_override_allowed",
        "ai_trend_override_allowed",
        "literature_sets_empirical_direction",
        "producer_preference_used_as_evidence",
    )
    for field in false_boundaries:
        if registration.get(field) is not False:
            violations.append(f"{field.upper()}_MUST_BE_FALSE")

    feature_id = feature_contract.get("feature_id")
    if feature_contract.get("lifecycle_status") != "FEATURE_ADMISSIBLE":
        violations.append("FEATURE_NOT_ADMISSIBLE")
    calibration = feature_contract.get("calibration") or {}
    calibration_status = calibration.get("status") if isinstance(calibration, dict) else calibration
    if calibration_status not in {"CALIBRATION_PASS", "NOT_REQUIRED_JUSTIFIED"}:
        violations.append("FEATURE_CALIBRATION_NOT_PASS")
    if feature_id not in (registration.get("admissible_feature_ids") or []):
        violations.append("FEATURE_NOT_DECLARED_IN_ANALYSIS")

    status = "ANALYSIS_REGISTRATION_PASS" if not missing and not violations else "AUDIT_ANALYSIS_NOT_REGISTERED"
    return {
        "schema": "HOOKLAB_ANALYSIS_REGISTRATION_AUDIT_v1",
        "analysis_id": registration.get("analysis_id"),
        "feature_id": feature_id,
        "status": status,
        "missing": missing,
        "violations": violations,
        "engine_version": ENGINE_VERSION,
    }


def _wilson_interval(count: int, total: int, z: float = 1.959963984540054) -> list[float]:
    if total <= 0:
        return [0.0, 0.0]
    proportion = count / total
    denominator = 1 + (z * z / total)
    center = (proportion + z * z / (2 * total)) / denominator
    half = z * math.sqrt((proportion * (1 - proportion) / total) + (z * z / (4 * total * total))) / denominator
    return [round(max(0.0, center - half), 8), round(min(1.0, center + half), 8)]


def _leader(counts: Counter[str]) -> tuple[str | None, int, int, bool]:
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    if not ranked:
        return None, 0, 0, False
    lead_label, lead_count = ranked[0]
    second_count = ranked[1][1] if len(ranked) > 1 else 0
    unique = len(ranked) == 1 or lead_count > second_count
    return lead_label, lead_count, second_count, unique


def _leave_one_out_leader_stable(categories: list[str], observed_leader: str) -> bool:
    if len(categories) < 2:
        return False
    for index in range(len(categories)):
        counts = Counter(categories[:index] + categories[index + 1 :])
        leader, _, _, unique = _leader(counts)
        if not unique or leader != observed_leader:
            return False
    return True


def execute_descriptive_categorical(
    registration: dict[str, Any],
    feature_contract: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    audit = audit_registration(registration, feature_contract)
    if audit["status"] != "ANALYSIS_REGISTRATION_PASS":
        return {
            "schema": "HOOKLAB_LYRIC_ANALYSIS_AUDIT_v1",
            "status": "AUDIT",
            "analysis_id": registration.get("analysis_id"),
            "registration_audit": audit,
            "statistical_computation_executed": False,
            "engine_version": ENGINE_VERSION,
        }
    if registration.get("analysis_type") != "DESCRIPTIVE_CATEGORICAL_FINITE_CORPUS":
        return {
            "schema": "HOOKLAB_LYRIC_ANALYSIS_AUDIT_v1",
            "status": "AUDIT",
            "analysis_id": registration.get("analysis_id"),
            "violations": ["UNSUPPORTED_ANALYSIS_TYPE"],
            "statistical_computation_executed": False,
            "engine_version": ENGINE_VERSION,
        }

    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    record_violations: list[str] = []
    forbidden_text_fields = {"lyrics", "lyric_text", "raw_text", "source_text"}
    for row in records:
        if forbidden_text_fields.intersection(row):
            record_violations.append("RAW_TEXT_FIELD_PRESENT")
        case_id = str(row.get("case_id") or "").strip()
        category = str(row.get("category") or "").strip()
        if not case_id or not category:
            record_violations.append("MISSING_CASE_OR_CATEGORY")
            continue
        if case_id in seen:
            record_violations.append(f"DUPLICATE_CASE_ID:{case_id}")
            continue
        seen.add(case_id)
        normalized.append({"case_id": case_id, "category": category})

    if record_violations:
        return {
            "schema": "HOOKLAB_LYRIC_ANALYSIS_AUDIT_v1",
            "status": "AUDIT",
            "analysis_id": registration.get("analysis_id"),
            "violations": sorted(set(record_violations)),
            "statistical_computation_executed": False,
            "engine_version": ENGINE_VERSION,
        }

    criteria = registration.get("effect_size_criterion") or {}
    minimum_n = int(criteria.get("minimum_n", 1))
    if len(normalized) < minimum_n:
        return {
            "schema": "HOOKLAB_LYRIC_ANALYSIS_AUDIT_v1",
            "status": "AUDIT",
            "analysis_id": registration.get("analysis_id"),
            "violations": ["INSUFFICIENT_PREDECLARED_N"],
            "n_eligible": len(normalized),
            "statistical_computation_executed": False,
            "engine_version": ENGINE_VERSION,
        }

    categories = [row["category"] for row in normalized]
    counts = Counter(categories)
    total = len(categories)
    distribution = [
        {
            "category": category,
            "count": count,
            "proportion": round(count / total, 8),
            "wilson_95_interval": _wilson_interval(count, total),
        }
        for category, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    leader, lead_count, second_count, unique_leader = _leader(counts)
    lead_proportion = lead_count / total
    margin = (lead_count - second_count) / total
    leader_interval = _wilson_interval(lead_count, total)
    stable = bool(leader and unique_leader and _leave_one_out_leader_stable(categories, leader))

    effect_pass = (
        lead_proportion >= float(criteria.get("minimum_leading_proportion", 1.0))
        and margin >= float(criteria.get("minimum_margin_over_second", 1.0))
    )
    uncertainty_pass = leader_interval[0] >= float(criteria.get("minimum_leading_wilson_lower_bound", 1.0))
    robustness_pass = stable and registration.get("robustness_plan") == "LEAVE_ONE_OUT_LEADER_STABILITY"

    if not effect_pass or not uncertainty_pass or not robustness_pass:
        disposition = "NO_PROMOTION"
    elif registration.get("replication_requirement") == "REQUIRED" and registration.get("replication_status") != "REPLICATED":
        disposition = "HOLD_FOR_REPLICATION"
    else:
        disposition = "PROMOTE_TO_CONDITIONED_DEDUCTION"

    registration_hash = _canonical_hash(registration)
    input_hash = _canonical_hash(normalized)
    return {
        "schema": "HOOKLAB_LYRIC_ANALYSIS_RESULT_v1",
        "status": "STATISTICAL_RESULT_COMPLETE",
        "analysis_id": registration["analysis_id"],
        "analysis_type": registration["analysis_type"],
        "feature_id": feature_contract["feature_id"],
        "population_scope": registration["population_scope"],
        "source_revision": registration["source_revision"],
        "n_eligible": total,
        "distribution": distribution,
        "data_says": {
            "leading_category": leader,
            "leading_count": lead_count,
            "leading_proportion": round(lead_proportion, 8),
            "margin_over_second": round(margin, 8),
        },
        "statistics_say": {
            "leading_wilson_95_interval": leader_interval,
            "effect_size_criterion_status": "PASS" if effect_pass else "FAIL",
            "uncertainty_status": "ACCEPTABLE" if uncertainty_pass else "NOT_ACCEPTABLE",
            "robustness_status": "PASS" if robustness_pass else "FAIL",
            "multiplicity_control_status": "PASS_SINGLE_REGISTERED_FAMILY",
        },
        "theory_says": None,
        "generation_tests": None,
        "producer_decides": None,
        "disposition": disposition,
        "computation_origin": COMPUTATION_ORIGIN,
        "trend_origin_policy": TREND_ORIGIN_POLICY,
        "human_trend_override_applied": False,
        "ai_trend_override_applied": False,
        "literature_direction_applied": False,
        "producer_preference_applied": False,
        "manual_result_fields_locked": True,
        "registration_hash_sha256": registration_hash,
        "normalized_input_hash_sha256": input_hash,
        "engine_version": ENGINE_VERSION,
    }


def _load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="HookLab registered lyric statistical engine")
    parser.add_argument("--analysis", required=True)
    parser.add_argument("--feature-contract", required=True)
    parser.add_argument("--records", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    result = execute_descriptive_categorical(_load(args.analysis), _load(args.feature_contract), _load(args.records))
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0 if result.get("status") == "STATISTICAL_RESULT_COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
