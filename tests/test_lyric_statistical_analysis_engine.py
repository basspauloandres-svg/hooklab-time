import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mie_core.lyric_statistical_analysis_engine import (  # noqa: E402
    COMPUTATION_ORIGIN,
    ENGINE_VERSION,
    TREND_ORIGIN_POLICY,
    audit_registration,
    execute_descriptive_categorical,
)


blocked = json.loads(
    (ROOT / "data/lyric_modeling/analysis_registry/AN-LNR-POV-DESC-001.json").read_text(encoding="utf-8")
)
candidate_feature = next(
    feature
    for feature in json.loads(
        (ROOT / "data/lyric_modeling/lyric_narrative_feature_registry_v0_1.json").read_text(encoding="utf-8")
    )["features"]
    if feature["feature_id"] == "LNR_POV_EXPLICIT_PERSON_CONFIGURATION_v0_1"
)

blocked_audit = audit_registration(blocked, candidate_feature)
assert blocked_audit["status"] == "AUDIT_ANALYSIS_NOT_REGISTERED"
assert "FEATURE_NOT_ADMISSIBLE" in blocked_audit["violations"]
blocked_result = execute_descriptive_categorical(blocked, candidate_feature, [])
assert blocked_result["status"] == "AUDIT"
assert blocked_result["statistical_computation_executed"] is False

# Structural test fixture only. It is never presented as, merged with, or substituted for the HookLab corpus.
admissible_feature = {
    "feature_id": "TEST_FEATURE_ONLY",
    "lifecycle_status": "FEATURE_ADMISSIBLE",
    "calibration": {"status": "CALIBRATION_PASS"},
}
registered = {
    "analysis_id": "TEST-ANALYSIS-ONLY",
    "registration_status": "ANALYSIS_REGISTERED",
    "analysis_type": "DESCRIPTIVE_CATEGORICAL_FINITE_CORPUS",
    "research_question": "Test engine structure only",
    "population_scope": "TEST_FIXTURE_ONLY",
    "outcome": "test category",
    "admissible_feature_ids": ["TEST_FEATURE_ONLY"],
    "primary_tests": ["FINITE_CORPUS_CATEGORY_COUNTS_AND_PROPORTIONS"],
    "covariates": [],
    "multiplicity_family": "TEST_SINGLE_FAMILY",
    "effect_size_criterion": {
        "minimum_n": 6,
        "minimum_leading_proportion": 0.9,
        "minimum_margin_over_second": 0.8,
        "minimum_leading_wilson_lower_bound": 0.9,
    },
    "robustness_plan": "LEAVE_ONE_OUT_LEADER_STABILITY",
    "replication_requirement": "REQUIRED",
    "replication_status": "NOT_STARTED",
    "stop_promotion_rule": "fail closed",
    "expected_direction": None,
    "trend_origin_policy": TREND_ORIGIN_POLICY,
    "human_trend_override_allowed": False,
    "ai_trend_override_allowed": False,
    "literature_sets_empirical_direction": False,
    "producer_preference_used_as_evidence": False,
    "source_revision": "TEST_FIXTURE_REVISION",
    "feature_registry_id": "TEST_FIXTURE_REGISTRY",
}
fixture = [
    {"case_id": "T001", "category": "A"},
    {"case_id": "T002", "category": "A"},
    {"case_id": "T003", "category": "A"},
    {"case_id": "T004", "category": "A"},
    {"case_id": "T005", "category": "B"},
    {"case_id": "T006", "category": "B"},
]
result = execute_descriptive_categorical(registered, admissible_feature, fixture)
assert result["status"] == "STATISTICAL_RESULT_COMPLETE"
assert result["disposition"] == "NO_PROMOTION"
assert result["computation_origin"] == COMPUTATION_ORIGIN
assert result["trend_origin_policy"] == TREND_ORIGIN_POLICY
assert result["human_trend_override_applied"] is False
assert result["ai_trend_override_applied"] is False
assert result["literature_direction_applied"] is False
assert result["producer_preference_applied"] is False
assert result["engine_version"] == ENGINE_VERSION
assert len(result["registration_hash_sha256"]) == 64
assert len(result["normalized_input_hash_sha256"]) == 64

directional = dict(registered)
directional["expected_direction"] = "positive"
directional_audit = audit_registration(directional, admissible_feature)
assert directional_audit["status"] == "AUDIT_ANALYSIS_NOT_REGISTERED"
assert "EXPECTED_DIRECTION_MUST_BE_NULL" in directional_audit["violations"]

manual_records = fixture + [{"case_id": "T007", "category": "A", "raw_text": "forbidden"}]
manual_result = execute_descriptive_categorical(registered, admissible_feature, manual_records)
assert manual_result["status"] == "AUDIT"
assert "RAW_TEXT_FIELD_PRESENT" in manual_result["violations"]

print("LYRIC_STATISTICAL_ANALYSIS_ENGINE_PASS")
