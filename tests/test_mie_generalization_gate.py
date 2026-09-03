import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from mie_core.mie_generalization_gate import evaluate_cross_track_generalization


def track(index, *, delta=0.1, unchanged=True, group=None):
    return {
        "track_id_hash": f"track-{index}",
        "group_id_hash": group or f"work-{index}",
        "split": "HELD_OUT",
        "identity_features_used": False,
        "beat_tactus_unchanged": unchanged,
        "candidate_state": "DERIVED_CANDIDATE",
        "baseline": {
            "false_silence_ratio": 0.4,
            "sustain_fragmentation_rate": 0.2,
            "repeated_harmony_state_rate": 0.3,
            "voiced_overlap_iou": 0.5,
        },
        "candidate": {
            "false_silence_ratio": 0.4 - delta,
            "sustain_fragmentation_rate": 0.2 - delta,
            "repeated_harmony_state_rate": 0.3 - delta,
            "voiced_overlap_iou": 0.5 + delta,
        },
    }


def test_multicase_smoke_never_claims_scientific_unlock():
    result = evaluate_cross_track_generalization([track(1), track(2), track(3)])
    assert result["status"] == "ENGINEERING_MULTICASE_SMOKE_PASS"
    assert result["aggregation"] == "MACRO_BY_TRACK"
    assert result["scientific_replication_requirement_met"] is False
    assert result["scientific_d_unlocked"] is False
    assert result["general_accuracy_claim_allowed"] is False


def test_duplicate_work_group_fails_as_leakage():
    result = evaluate_cross_track_generalization([track(1, group="same"), track(2, group="same")])
    assert result["status"] == "AUDIT_DATA_LEAKAGE"


def test_song_specific_features_fail_closed():
    item = track(1)
    item["identity_features_used"] = True
    result = evaluate_cross_track_generalization([item])
    assert result["status"] == "AUDIT_SONG_SPECIFIC_LOGIC"


def test_tactus_regression_blocks_promotion():
    result = evaluate_cross_track_generalization([track(1), track(2, unchanged=False), track(3)])
    assert result["status"] == "NO_PROMOTION_TACTUS_REGRESSION"


def test_gain_confined_to_one_track_is_held():
    result = evaluate_cross_track_generalization([track(1, delta=0.1), track(2, delta=-0.1), track(3, delta=-0.1)])
    assert result["status"] == "HOLD_TRACK_SPECIFIC_GAIN"


def test_replication_gate_requires_thirty_independent_tracks_and_keeps_d_locked():
    result = evaluate_cross_track_generalization([track(index) for index in range(30)])
    assert result["status"] == "GENERALIZATION_PASS"
    assert result["scientific_replication_requirement_met"] is True
    assert result["scientific_d_unlocked"] is False


def test_runtime_contains_no_named_song_or_artist_branch():
    root = pathlib.Path(__file__).resolve().parents[1]
    source = "\n".join(
        (root / path).read_text(encoding="utf-8")
        for path in (
            "mie_core/mie_generalization_gate.py",
            "mie_core/mie_tf_plane_registration.py",
            "mie_core/mie_temporal_refinement.py",
            "mie_core/run_mie_core.py",
        )
    )
    forbidden = ("Luis Miguel", "Devuélveme", "Regálame", "Guaco", "if song", "if artist")
    assert not any(value in source for value in forbidden)
    assert "FRACTION_OF_TACTUS" in source


if __name__ == "__main__":
    test_multicase_smoke_never_claims_scientific_unlock()
    test_duplicate_work_group_fails_as_leakage()
    test_song_specific_features_fail_closed()
    test_tactus_regression_blocks_promotion()
    test_gain_confined_to_one_track_is_held()
    test_replication_gate_requires_thirty_independent_tracks_and_keeps_d_locked()
    test_runtime_contains_no_named_song_or_artist_branch()
    print("MIE_CROSS_TRACK_GENERALIZATION_GATE_PASS")
