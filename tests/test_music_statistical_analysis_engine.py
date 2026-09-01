import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mie_core.music_statistical_analysis_engine import (  # noqa: E402
    ENGINE_VERSION,
    execute_descriptive_numeric,
)


registry = json.loads((ROOT / "data/music_modeling/melody_beat_feature_registry_v0_1.json").read_text())
blocked_feature = next(f for f in registry["features"] if f["feature_id"] == "MEL_PITCH_RANGE_SEMITONES_v0_1")
blocked_analysis = json.loads((ROOT / "data/music_modeling/analysis_registry/AN-MEL-DESC-001.json").read_text())
blocked = execute_descriptive_numeric(blocked_analysis, blocked_feature, [])
assert blocked["status"] == "AUDIT"
assert blocked["statistical_computation_executed"] is False
assert blocked["scientific_d_unlocked"] is False

# Structural fixture only; it is not a HookLab case and never substitutes for corpus data.
feature = {
    "feature_id": "TEST_MUSIC_FEATURE_ONLY",
    "lifecycle_status": "FEATURE_ADMISSIBLE",
    "calibration": {"status": "CALIBRATION_PASS"},
}
analysis = {
    "analysis_id": "TEST-MUSIC-ANALYSIS-ONLY",
    "registration_status": "ANALYSIS_REGISTERED",
    "analysis_type": "DESCRIPTIVE_NUMERIC_FINITE_CORPUS",
    "research_question": "Test numeric engine structure only",
    "population_scope": "TEST_FIXTURE_ONLY",
    "outcome": "test value",
    "admissible_feature_ids": ["TEST_MUSIC_FEATURE_ONLY"],
    "primary_tests": ["FINITE_CORPUS_NUMERIC_DISTRIBUTION"],
    "covariates": [],
    "multiplicity_family": "TEST_SINGLE_FAMILY",
    "effect_size_criterion": {"minimum_n": 4},
    "robustness_plan": "TEST_ONLY",
    "replication_requirement": "REQUIRED",
    "replication_status": "NOT_STARTED",
    "stop_promotion_rule": "fail closed",
    "expected_direction": None,
    "trend_origin_policy": "REGISTERED_DATA_AND_STATISTICS_ONLY",
    "human_trend_override_allowed": False,
    "ai_trend_override_allowed": False,
    "literature_sets_empirical_direction": False,
    "producer_preference_used_as_evidence": False,
    "source_revision": "TEST_FIXTURE_REVISION",
    "feature_registry_id": "TEST_FIXTURE_REGISTRY",
}
records = [
    {"case_id": "T001", "value": 1.0},
    {"case_id": "T002", "value": 2.0},
    {"case_id": "T003", "value": 3.0},
    {"case_id": "T004", "value": 4.0},
]
result = execute_descriptive_numeric(analysis, feature, records)
assert result["status"] == "STATISTICAL_RESULT_COMPLETE"
assert result["data_says"]["median"] == 2.5
assert result["disposition"] == "NO_PROMOTION"
assert result["scientific_d_unlocked"] is False
assert result["human_trend_override_applied"] is False
assert result["ai_trend_override_applied"] is False
assert result["engine_version"] == ENGINE_VERSION
assert len(result["registration_hash_sha256"]) == 64
assert len(result["normalized_input_hash_sha256"]) == 64

raw = records + [{"case_id": "T005", "value": 5.0, "midi_bytes": "forbidden"}]
raw_result = execute_descriptive_numeric(analysis, feature, raw)
assert raw_result["status"] == "AUDIT"
assert "RAW_SOURCE_FIELD_PRESENT" in raw_result["violations"]

print("MUSIC_STATISTICAL_ANALYSIS_ENGINE_PASS")
