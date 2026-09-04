import copy
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from mie_core.mie_melody_recognizability_gate import (
    ABSTAIN,
    BASIC_PITCH_FRAME_HZ,
    audit_historical_regression_inventory,
    build_m_only_experiment_audit,
    diagnose_source_separation_vs_note_sensor_recall,
    macro_audit_held_out_tracks,
)


def fixture(*, duration_s=2.0, sample_rate=8600, stem_active=True, sensor_active=True):
    frame_count = int(duration_s * BASIC_PITCH_FRAME_HZ)
    audio = np.zeros(int(duration_s * sample_rate), dtype=float)
    if stem_active:
        audio[:] = 0.2 * np.sin(2 * np.pi * 220 * np.arange(len(audio)) / sample_rate)
    contour = np.zeros((frame_count, 264), dtype=float)
    onset = np.zeros((frame_count, 88), dtype=float)
    if sensor_active:
        contour[:, 118] = 0.8
    return audio, sample_rate, {"contour": contour, "onset": onset}


def test_active_vocal_stem_without_sensor_response_diagnoses_sensor_recall():
    audio, sample_rate, model_output = fixture(sensor_active=False)
    result = diagnose_source_separation_vs_note_sensor_recall(audio, sample_rate, model_output, [])
    assert result["status"] == "NOTE_SENSOR_RECALL_BOTTLENECK"
    assert result["note_sensor"]["conditional_nonresponse_ratio"] == 1.0
    assert result["source_separation"]["claim_allowed"] is False
    assert result["interpretation"] == "DIAGNOSTIC_NOT_MELODY_ACCURACY"
    assert result["scientific_d_unlocked"] is False


def test_source_separation_loss_requires_independent_vocal_activity():
    audio, sample_rate, model_output = fixture(stem_active=False, sensor_active=False)
    without_reference = diagnose_source_separation_vs_note_sensor_recall(audio, sample_rate, model_output, [])
    assert without_reference["status"] == ABSTAIN
    independent = np.ones(model_output["contour"].shape[0], dtype=bool)
    with_reference = diagnose_source_separation_vs_note_sensor_recall(
        audio,
        sample_rate,
        model_output,
        [],
        independent_vocal_activity=independent,
    )
    assert with_reference["status"] == "SOURCE_SEPARATION_RECALL_BOTTLENECK"
    assert with_reference["source_separation"]["claim_allowed"] is True
    assert with_reference["source_separation"]["conditional_nonresponse_ratio"] == 1.0


def test_missing_contour_abstains_without_manufacturing_notes():
    audio = np.ones(8600)
    result = diagnose_source_separation_vs_note_sensor_recall(audio, 8600, {}, [])
    assert result["status"] == ABSTAIN
    assert result["reason"] == "BASIC_PITCH_CONTOUR_REQUIRED"


def test_experiment_audit_enforces_h_and_t_immutability():
    diagnostic = {"status": "NOTE_SENSOR_RECALL_BOTTLENECK"}
    harmony = [{"start_s": 0.0, "end_s": 1.0, "state": "LOCK", "root_pc": 0}]
    tactus = [{"t": 0.0, "score": 0.9}, {"t": 0.5, "score": 0.9}]
    harmony_before = copy.deepcopy(harmony)
    tactus_before = copy.deepcopy(tactus)
    audit = build_m_only_experiment_audit(
        diagnostic,
        parent_reference="MIE_CORE_v0.3.4_REJECTED_PROVENANCE",
        harmony_reference=harmony,
        harmony_candidate=copy.deepcopy(harmony),
        tactus_reference=tactus,
        tactus_candidate=copy.deepcopy(tactus),
        source_sha256="a" * 64,
        work_group_hash="b" * 64,
        sensor_versions={"separator": "HTDemucs", "note_sensor": "Basic Pitch 0.4.0"},
    )
    assert audit["changed_module"] == "M_ONLY"
    assert audit["frozen_layers"]["harmony_byte_equivalent"] is True
    assert audit["frozen_layers"]["tactus_byte_equivalent"] is True
    assert audit["producer_evaluation"]["separate_from_automatic_diagnostics"] is True
    assert harmony == harmony_before
    assert tactus == tactus_before

    changed_t = copy.deepcopy(tactus)
    changed_t[1]["t"] += 0.01
    failed = build_m_only_experiment_audit(
        diagnostic,
        parent_reference="MIE_CORE_v0.3.4_REJECTED_PROVENANCE",
        harmony_reference=harmony,
        harmony_candidate=harmony,
        tactus_reference=tactus,
        tactus_candidate=changed_t,
        source_sha256="a" * 64,
        work_group_hash="b" * 64,
        sensor_versions={},
    )
    assert failed["status"] == "NO_PROMOTION_TACTUS_REGRESSION"


def track(index, diagnostic_status="NOTE_SENSOR_RECALL_BOTTLENECK"):
    return {
        "track_id_hash": f"track-{index}",
        "work_group_hash": f"work-{index}",
        "split": "HELD_OUT",
        "identity_features_used": False,
        "diagnostic": {
            "status": diagnostic_status,
            "note_sensor": {"conditional_nonresponse_ratio": 0.5},
        },
        "frozen_layers": {"harmony_byte_equivalent": True, "tactus_byte_equivalent": True},
        "producer_evaluation": {"recognizability": "PENDING_PRODUCER_LISTENING"},
    }


def test_macro_gate_aggregates_by_track_and_never_promotes_diagnostic():
    result = macro_audit_held_out_tracks([track(1), track(2), track(3)])
    assert result["status"] == "HOLD_FOR_RECOGNIZABILITY_EXPERIMENT"
    assert result["aggregation"] == "MACRO_BY_TRACK"
    assert result["macro_median_note_sensor_nonresponse_ratio"] == 0.5
    assert result["baseline_promoted"] is False
    assert result["general_accuracy_claim_allowed"] is False
    assert result["scientific_d_unlocked"] is False


def test_macro_gate_rejects_duplicate_work_groups_and_h_changes():
    duplicate = [track(1), track(2)]
    duplicate[1]["work_group_hash"] = duplicate[0]["work_group_hash"]
    assert macro_audit_held_out_tracks(duplicate)["status"] == "AUDIT_DATA_LEAKAGE"
    changed_h = track(3)
    changed_h["frozen_layers"]["harmony_byte_equivalent"] = False
    assert macro_audit_held_out_tracks([changed_h])["status"] == "AUDIT_ONE_MODULE_RULE_VIOLATION_H_CHANGED"


def test_runtime_has_no_identity_or_manual_timestamp_inputs():
    source = (pathlib.Path(__file__).resolve().parents[1] / "mie_core" / "mie_melody_recognizability_gate.py").read_text()
    forbidden = ("song_title", "artist_name", "known_notes", "manual_timestamps", "Animal.mp3", "Luis Miguel")
    assert not any(value in source for value in forbidden)


def test_historical_gate_blocks_new_audio_and_h_until_existing_cases_pass():
    inventory = {
        "cases": [
            {
                "case_id": "HIST-001",
                "provenance": ["immutable-checkpoint"],
                "reprocessed": False,
                "historical_gate_eligible": True,
                "v0_3_5_historical_gate": "PENDING_EXISTING_ARTIFACT_EVALUATION",
            },
            {
                "case_id": "CONTROL-001",
                "provenance": ["synthetic-control"],
                "reprocessed": False,
                "historical_gate_eligible": False,
                "v0_3_5_historical_gate": "NOT_APPLICABLE",
            },
        ]
    }
    result = audit_historical_regression_inventory(inventory)
    assert result["status"] == "HISTORICAL_GATE_NOT_PASSED"
    assert result["new_audio_request_allowed"] is False
    assert result["harmony_development_allowed"] is False
    assert result["tactus_state"] == "FROZEN_ENGINEERING_BASELINE_PRESERVED"
    inventory["cases"][0]["v0_3_5_historical_gate"] = "PASS_RECOGNIZABLE"
    passed = audit_historical_regression_inventory(inventory)
    assert passed["status"] == "HISTORICAL_GATE_PASSED"
    assert passed["new_audio_request_allowed"] is True


def test_canonical_historical_inventory_is_fail_closed():
    path = pathlib.Path(__file__).resolve().parents[1] / "data" / "music_modeling" / "mie_historical_regression_inventory_v1.json"
    inventory = json.loads(path.read_text())
    result = audit_historical_regression_inventory(inventory)
    assert result["inventory_case_count"] == 7
    assert result["eligible_case_count"] == 3
    assert result["status"] == "HISTORICAL_GATE_NOT_PASSED"
    assert result["new_audio_request_allowed"] is False


if __name__ == "__main__":
    test_active_vocal_stem_without_sensor_response_diagnoses_sensor_recall()
    test_source_separation_loss_requires_independent_vocal_activity()
    test_missing_contour_abstains_without_manufacturing_notes()
    test_experiment_audit_enforces_h_and_t_immutability()
    test_macro_gate_aggregates_by_track_and_never_promotes_diagnostic()
    test_macro_gate_rejects_duplicate_work_groups_and_h_changes()
    test_runtime_has_no_identity_or_manual_timestamp_inputs()
    test_historical_gate_blocks_new_audio_and_h_until_existing_cases_pass()
    test_canonical_historical_inventory_is_fail_closed()
    print("MIE_M_ONLY_MELODY_RECOGNIZABILITY_GATE_PASS")
