import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from mie_core.mie_recognition_contract import normalize
from mie_core.mie_temporal_refinement import (
    align_harmony_to_shared_clock_v2,
    align_harmony_to_metric,
    consolidate_harmony_persistence,
    recover_melody_gaps,
    resolve_metric_grid,
    resolve_tactus,
)


def test_conservative_gap_recovery_preserves_origin():
    accepted = [
        {"start_s": 0.0, "end_s": 0.30, "midi": 60, "confidence": 0.9},
        {"start_s": 0.70, "end_s": 1.00, "midi": 62, "confidence": 0.9},
    ]
    raw = accepted + [
        {"start_s": 0.36, "end_s": 0.62, "midi": 61, "confidence": 0.45},
        {"start_s": 0.37, "end_s": 0.60, "midi": 84, "confidence": 0.8},
    ]
    events, audit = recover_melody_gaps(raw, accepted)
    assert len(events) == 3
    assert audit["recovered_candidate_count"] == 1
    recovered = [event for event in events if event["recovery_state"] == "RECOVERED_CANDIDATE"]
    assert recovered[0]["midi"] == 61
    assert recovered[0]["recovery_basis"]["provider"] == "BASIC_PITCH_RAW_CANDIDATE"
    assert audit["automatic_curated_status"] is False


def test_tactus_suppresses_subdivisions_and_keeps_raw_separate():
    raw = []
    for index in range(40):
        time = index * 0.56
        raw.append({"t": time, "score": 0.95})
        if 8 <= index < 18:
            raw.append({"t": time + 0.22, "score": 0.65})
    raw.sort(key=lambda item: item["t"])
    tactus, audit = resolve_tactus(raw, 23.0)
    assert len(raw) == 50
    assert 38 <= len(tactus) <= 42
    assert abs(audit["tempo_bpm"] - 107.142857) < 1.0
    assert audit["raw_observation_count"] == 50
    assert all(item["clock_state"] in {"OBSERVED", "DEDUCED_LOW_EVIDENCE"} for item in tactus)


def test_metric_lock_and_harmony_alignment_are_fail_closed():
    tactus = [{"t": index * 0.5, "score": 0.9, "clock_state": "OBSERVED", "run": 1} for index in range(24)]
    downbeats = [{"t": index * 2.0, "score": 0.95} for index in range(6)]
    grid, metric = resolve_metric_grid(tactus, downbeats)
    assert metric["state"] == "METRIC_LOCK"
    assert metric["meter_beats"] == 4
    assert grid[0]["metric_strength"] == "DOWNBEAT"
    assert grid[1]["metric_strength"] == "STRONG"

    raw_harmony = []
    for index in range(20):
        raw_harmony.append(
            {
                "start_s": index * 0.5,
                "end_s": (index + 1) * 0.5,
                "root_pc": 0 if index < 8 else 5,
                "quality": "maj",
                "intervals": [0, 4, 7],
                "evidence": 0.8,
                "margin": 0.08,
                "bass_bonus": 0.08,
                "state": "LOCK" if index != 3 else "AMBIGUOUS",
            }
        )
    aligned, audit = align_harmony_to_metric(raw_harmony, grid, 10.0)
    assert audit["state"] == "HARMONY_METRIC_ALIGNED"
    assert audit["ambiguous_preserved_count"] == 1
    assert all(item["alignment_state"] == "HARMONY_METRIC_ALIGNED" for item in aligned)
    assert all(item["start_s"] in {point["t"] for point in grid} for item in aligned)

    abstained, failed = align_harmony_to_metric(raw_harmony, [], 10.0)
    assert abstained == []
    assert failed["state"] == "METRIC_ALIGNMENT_ABSTAIN"


def test_contract_exports_raw_and_derived_provenance_without_unlocking_d():
    raw = {
        "duration_s": 2.0,
        "notes": [{"start_s": 0.1, "end_s": 0.4, "midi": 60, "confidence": 0.8, "recovery_state": "RECOVERED_CANDIDATE"}],
        "notes_raw_accepted": [],
        "raw_note_candidates": 2,
        "beats": [{"t": 0.0, "score": 0.9, "clock_state": "OBSERVED", "run": 1, "metric_strength": "DOWNBEAT"}],
        "beat_observations_raw": [{"t": 0.0, "score": 0.9}],
        "downbeat_candidates_raw": [{"t": 0.0, "score": 0.8}],
        "harmony": [{"start_s": 0.0, "end_s": 2.0, "root_pc": 0, "quality": "maj", "state": "LOCK", "alignment_state": "HARMONY_METRIC_ALIGNED"}],
        "harmony_raw": [],
        "harmony_metric_aligned": [],
        "metric_grid": [{"t": 0.0, "metric_strength": "DOWNBEAT"}],
        "melody_recovery": {"recovered_candidate_count": 1},
        "tactus_resolution": {"policy": "TEST"},
        "harmony_alignment": {"state": "TEST"},
    }
    result = normalize(raw, session_id="S", reference_sha256="abc", sensor_version="v0.3.1")
    assert result["status"] == "PASS"
    assert result["scientific_d_unlocked"] is False
    assert result["transcription"]["melody_events"][0]["recovery_state"] == "RECOVERED_CANDIDATE"
    assert result["transcription"]["beat_events"][0]["metric_strength"] == "DOWNBEAT"
    assert result["observation_layers"]["raw_note_candidate_count"] == 2
    assert result["derived_layers"]["metric_grid"][0]["metric_strength"] == "DOWNBEAT"


def test_harmony_is_persistent_state_and_ambiguous_units_remain_explicit():
    harmony = [
        {"start_s": 0.0, "end_s": 0.5, "root_pc": 0, "quality": "maj", "intervals": [0, 4, 7], "evidence": 0.8, "margin": 0.08, "state": "LOCK"},
        {"start_s": 0.5, "end_s": 1.0, "root_pc": 0, "quality": "maj", "intervals": [0, 4, 7], "evidence": 0.9, "margin": 0.07, "state": "LOCK"},
        {"start_s": 1.0, "end_s": 1.5, "root_pc": 5, "quality": "maj", "intervals": [0, 4, 7], "evidence": 0.7, "margin": 0.01, "state": "AMBIGUOUS"},
        {"start_s": 1.5, "end_s": 2.0, "root_pc": 5, "quality": "maj", "intervals": [0, 4, 7], "evidence": 0.85, "margin": 0.08, "state": "LOCK"},
    ]
    derived, audit = consolidate_harmony_persistence(harmony, tactus_period_s=0.5)
    assert len(derived) == 3
    assert derived[0]["end_s"] == 1.0
    assert derived[0]["source_unit_indices"] == [0, 1]
    assert derived[1]["state"] == "AMBIGUOUS"
    assert audit["coalesced_boundary_count"] == 1
    assert audit["raw_observations_mutated"] is False
    assert audit["identity_features_used"] is False


def test_metric_grid_uses_regular_consensus_phase_despite_outlier():
    tactus = [{"t": index * 0.5, "score": 0.9, "clock_state": "OBSERVED", "run": 1} for index in range(28)]
    downbeats = [{"t": value, "score": 0.95} for value in (0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 10.5)]
    grid, audit = resolve_metric_grid(tactus, downbeats)
    assert audit["state"] == "METRIC_LOCK"
    assert audit["phase"] == 0
    assert audit["phase_consistency"] >= 0.70
    assert audit["grid_policy"] == "REGULAR_CONSENSUS_PHASE_v2"
    downbeat_indices = [item["tactus_index"] for item in grid if item["metric_strength"] == "DOWNBEAT"]
    assert downbeat_indices == [0, 4, 8, 12, 16, 20, 24]


def test_shared_clock_alignment_closes_gaps_without_changing_identity_or_melody():
    tactus = [{"t": index * 0.5, "score": 0.9} for index in range(8)]
    melody = [{"start_s": 0.52, "end_s": 0.8, "midi": 60, "confidence": 0.8}]
    harmony = [
        {"start_s": 0.0, "end_s": 0.8, "root_pc": 0, "quality": "maj", "intervals": [0, 4, 7], "state": "LOCK"},
        {"start_s": 0.8, "end_s": 1.08, "root_pc": 2, "quality": "min", "intervals": [0, 3, 7], "state": "AMBIGUOUS"},
        {"start_s": 1.08, "end_s": 1.8, "root_pc": 5, "quality": "maj", "intervals": [0, 4, 7], "state": "LOCK"},
        {"start_s": 2.42, "end_s": 3.0, "root_pc": 7, "quality": "7", "intervals": [0, 4, 7, 10], "state": "LOCK"},
    ]
    melody_before = [dict(item) for item in melody]
    derived, audit = align_harmony_to_shared_clock_v2(harmony, melody, tactus, tactus_period_s=0.5)
    assert [(item["root_pc"], item["quality"]) for item in derived] == [(0, "maj"), (5, "maj"), (7, "7")]
    assert derived[0]["end_s"] == derived[1]["start_s"] == 1.0
    assert derived[1]["end_s"] == derived[2]["start_s"] == 2.5
    assert audit["gapless_between_accepted_states"] is True
    assert audit["harmonic_identity_changed"] is False
    assert audit["melody_moved"] is False
    assert audit["identity_features_used"] is False
    assert audit["ambiguous_observation_count"] == 1
    assert melody == melody_before


if __name__ == "__main__":
    test_conservative_gap_recovery_preserves_origin()
    test_tactus_suppresses_subdivisions_and_keeps_raw_separate()
    test_metric_lock_and_harmony_alignment_are_fail_closed()
    test_contract_exports_raw_and_derived_provenance_without_unlocking_d()
    test_harmony_is_persistent_state_and_ambiguous_units_remain_explicit()
    test_metric_grid_uses_regular_consensus_phase_despite_outlier()
    test_shared_clock_alignment_closes_gaps_without_changing_identity_or_melody()
    print("MIE_TEMPORAL_REFINEMENT_PASS")
