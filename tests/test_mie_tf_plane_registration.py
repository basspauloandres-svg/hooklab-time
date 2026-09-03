import copy
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from mie_core.mie_tf_plane_registration import (
    BASIC_PITCH_FRAME_HZ,
    consolidate_sustained_fragments,
    plane_residual_metrics,
)


def planes(duration_s=1.5):
    frames = int(duration_s * BASIC_PITCH_FRAME_HZ) + 2
    return {
        "contour": np.zeros((frames, 264), dtype=float),
        "onset": np.zeros((frames, 88), dtype=float),
    }


def paint_pitch(model_output, start_s, end_s, midi, value=0.9):
    start = int(round(start_s * BASIC_PITCH_FRAME_HZ))
    end = int(round(end_s * BASIC_PITCH_FRAME_HZ))
    contour_bin = int(round((midi - 21) * 3)) + 1
    model_output["contour"][start:end, contour_bin] = value


def paint_onset(model_output, time_s, midi, value=0.9):
    frame = int(round(time_s * BASIC_PITCH_FRAME_HZ))
    model_output["onset"][frame, midi - 21] = value


def test_same_pitch_fragments_merge_only_with_neural_bridge_evidence():
    model_output = planes()
    paint_pitch(model_output, 0.10, 0.82, 60)
    notes = [
        {"start_s": 0.10, "end_s": 0.40, "midi": 60, "confidence": 0.8},
        {"start_s": 0.46, "end_s": 0.82, "midi": 60, "confidence": 0.82},
    ]
    original = copy.deepcopy(notes)
    derived, audit = consolidate_sustained_fragments(notes, model_output)
    assert notes == original
    assert len(derived) == 1
    assert derived[0]["start_s"] == 0.10
    assert derived[0]["end_s"] == 0.82
    assert derived[0]["source_event_indices"] == [0, 1]
    assert derived[0]["continuity_state"] == "SUSTAIN_FRAGMENT_CONSOLIDATED"
    assert audit["merged_boundary_count"] == 1
    assert audit["raw_observations_mutated"] is False
    assert audit["automatic_curated_status"] is False


def test_repeated_onset_blocks_merge():
    model_output = planes()
    paint_pitch(model_output, 0.10, 0.82, 60)
    paint_onset(model_output, 0.46, 60)
    notes = [
        {"start_s": 0.10, "end_s": 0.40, "midi": 60, "confidence": 0.8},
        {"start_s": 0.46, "end_s": 0.82, "midi": 60, "confidence": 0.82},
    ]
    derived, audit = consolidate_sustained_fragments(notes, model_output)
    assert len(derived) == 2
    assert audit["merged_boundary_count"] == 0


def test_silence_and_pitch_change_are_not_filled():
    model_output = planes()
    paint_pitch(model_output, 0.10, 0.40, 60)
    paint_pitch(model_output, 0.48, 0.82, 62)
    notes = [
        {"start_s": 0.10, "end_s": 0.40, "midi": 60, "confidence": 0.8},
        {"start_s": 0.48, "end_s": 0.82, "midi": 62, "confidence": 0.82},
    ]
    derived, audit = consolidate_sustained_fragments(notes, model_output)
    assert len(derived) == 2
    assert audit["merged_boundary_count"] == 0


def test_missing_plane_abstains_fail_closed():
    notes = [{"start_s": 0.10, "end_s": 0.40, "midi": 60, "confidence": 0.8}]
    derived, audit = consolidate_sustained_fragments(notes, {})
    metrics = plane_residual_metrics({}, derived)
    assert len(derived) == 1
    assert audit["state"] == "ABSTAIN_NO_CONTOUR"
    assert metrics["measurement_state"] == "ABSTAIN_NO_CONTOUR"
    assert metrics["scientific_d_unlocked"] is False
    assert metrics["residual_vector"] is None


def test_residual_is_vector_without_composite_or_scientific_unlock():
    model_output = planes()
    paint_pitch(model_output, 0.10, 0.82, 60)
    paint_onset(model_output, 0.10, 60)
    notes = [{"start_s": 0.10, "end_s": 0.82, "midi": 60, "confidence": 0.8}]
    metrics = plane_residual_metrics(model_output, notes)
    expected = {
        "pitch_ridge_error_cents_median",
        "voiced_overlap_iou",
        "false_silence_ratio",
        "onset_error_ms_median",
        "offset_error_ms_median",
        "sustain_fragmentation_rate",
        "gesture_slope_error_cents_per_s_median",
        "octave_confusion_rate",
    }
    assert set(metrics["residual_vector"]) == expected
    assert metrics["weighted_composite"] is None
    assert metrics["status"] == "AUDIT_FEATURE_NOT_CALIBRATED"
    assert metrics["scientific_d_unlocked"] is False
    assert metrics["raw_observations_mutated"] is False
    assert metrics["residual_vector"]["pitch_ridge_error_cents_median"] == 0.0
    assert metrics["residual_vector"]["octave_confusion_rate"] == 0.0


def test_increment_has_no_song_template_and_keeps_same_tactus_for_a_b():
    root = pathlib.Path(__file__).resolve().parents[1]
    module_source = (root / "mie_core" / "mie_tf_plane_registration.py").read_text(encoding="utf-8")
    engine_source = (root / "mie_core" / "run_mie_core.py").read_text(encoding="utf-8")
    forbidden = ("Luis Miguel", "Regálame", "Guaco", "107.142857", "scientific_d_unlocked':True")
    assert not any(value in module_source for value in forbidden)
    assert "synth(notes_v0_3_1,chords,beats,duration,wav_v0_3_1)" in engine_source
    assert "synth(notes,chords,beats,duration,wav)" in engine_source


if __name__ == "__main__":
    test_same_pitch_fragments_merge_only_with_neural_bridge_evidence()
    test_repeated_onset_blocks_merge()
    test_silence_and_pitch_change_are_not_filled()
    test_missing_plane_abstains_fail_closed()
    test_residual_is_vector_without_composite_or_scientific_unlock()
    test_increment_has_no_song_template_and_keeps_same_tactus_for_a_b()
    print("MIE_TF_PLANE_REGISTRATION_PASS")
