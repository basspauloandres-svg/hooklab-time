"""Experimental time-frequency plane registration for MIE melody.

This module consumes the frame-level ``contour`` and ``onset`` tensors already
produced by Basic Pitch.  It never changes those sensor observations.  It
builds an explicitly derived note layer and a diagnostic residual vector for
producer A/B evaluation.

The implementation remains D0_EXPLORATORY and is not a Feature Admissibility
decision or a scientific unlock.
"""

from __future__ import annotations

import numpy as np


BASIC_PITCH_FRAME_HZ = 86.0
BASIC_PITCH_BASE_MIDI = 21.0
BASIC_PITCH_CONTOUR_BINS_PER_SEMITONE = 3
BASIC_PITCH_CONTOUR_FIRST_SEMITONE_CENTER_BIN = 1
FEATURE_ID = "M_TF_PLANE_REGISTRATION_RESIDUAL_v0_1"
CONTINUITY_V2_POLICY = "TACTUS_NORMALIZED_NEURAL_SUSTAIN_CONTINUITY_v2"


def _as_plane(model_output, key):
    value = np.asarray((model_output or {}).get(key, []), dtype=float)
    if value.ndim != 2 or not value.size or not np.isfinite(value).all():
        return None
    return value


def _midi_to_contour_bin(midi):
    return int(
        round((float(midi) - BASIC_PITCH_BASE_MIDI) * BASIC_PITCH_CONTOUR_BINS_PER_SEMITONE)
        + BASIC_PITCH_CONTOUR_FIRST_SEMITONE_CENTER_BIN
    )


def _frame(time_s, frame_count):
    return min(frame_count, max(0, int(round(float(time_s) * BASIC_PITCH_FRAME_HZ))))


def _pitch_support(contour, start_s, end_s, midi, radius_bins=2):
    start = _frame(start_s, contour.shape[0])
    end = _frame(end_s, contour.shape[0])
    if end <= start:
        center_frame = _frame((float(start_s) + float(end_s)) / 2.0, contour.shape[0])
        start = max(0, center_frame - 1)
        end = min(contour.shape[0], center_frame + 2)
    center = _midi_to_contour_bin(midi)
    left = max(0, center - radius_bins)
    right = min(contour.shape[1], center + radius_bins + 1)
    if right <= left:
        return 0.0, 0.0
    support = np.max(contour[start:end, left:right], axis=1)
    return float(np.mean(support)), float(np.mean(support >= 0.25))


def _onset_support(onset, time_s, midi, radius_frames=1):
    if onset is None:
        return None
    center_frame = _frame(time_s, onset.shape[0])
    start = max(0, center_frame - radius_frames)
    end = min(onset.shape[0], center_frame + radius_frames + 1)
    pitch_bin = int(round(float(midi) - BASIC_PITCH_BASE_MIDI))
    left = max(0, pitch_bin - 1)
    right = min(onset.shape[1], pitch_bin + 2)
    if end <= start or right <= left:
        return None
    return float(np.max(onset[start:end, left:right]))


def consolidate_sustained_fragments(
    notes,
    model_output,
    *,
    maximum_gap_s=0.14,
    bridge_mean_threshold=0.25,
    bridge_coverage_threshold=0.70,
    repeated_onset_threshold=0.50,
):
    """Join only same-pitch fragments supported by the neural contour plane.

    Raw events are copied and retained through ``source_event_indices``.  A
    detected onset at the second fragment blocks consolidation because it is
    evidence for a genuine repeated note.
    """
    source = sorted(
        (dict(note, _source_index=index) for index, note in enumerate(notes or [])),
        key=lambda note: (note["start_s"], note["end_s"], note["midi"]),
    )
    contour = _as_plane(model_output, "contour")
    onset = _as_plane(model_output, "onset")
    if contour is None:
        return [
            dict(
                {key: value for key, value in note.items() if key != "_source_index"},
                continuity_state="UNCHANGED_NO_PLANE_EVIDENCE",
                source_event_indices=[note["_source_index"]],
            )
            for note in source
        ], {
            "policy": "NEURAL_CONTOUR_SUSTAIN_CONTINUITY_v1",
            "state": "ABSTAIN_NO_CONTOUR",
            "input_event_count": len(source),
            "output_event_count": len(source),
            "merged_boundary_count": 0,
            "raw_observations_mutated": False,
            "automatic_curated_status": False,
        }

    output = []
    merged_boundaries = []
    for note in source:
        clean = {key: value for key, value in note.items() if key != "_source_index"}
        clean["source_event_indices"] = [note["_source_index"]]
        clean["continuity_state"] = "PLANE_EVIDENCE_RETAINED"
        if not output:
            output.append(clean)
            continue
        previous = output[-1]
        gap = float(clean["start_s"]) - float(previous["end_s"])
        same_pitch = int(round(clean["midi"])) == int(round(previous["midi"]))
        if gap < 0 or gap > maximum_gap_s or not same_pitch:
            output.append(clean)
            continue
        bridge_mean, bridge_coverage = _pitch_support(
            contour,
            previous["end_s"],
            clean["start_s"],
            clean["midi"],
        )
        onset_support = _onset_support(onset, clean["start_s"], clean["midi"])
        repeated_onset = onset_support is not None and onset_support >= repeated_onset_threshold
        if (
            bridge_mean >= bridge_mean_threshold
            and bridge_coverage >= bridge_coverage_threshold
            and not repeated_onset
        ):
            previous["end_s"] = clean["end_s"]
            previous["confidence"] = min(
                float(previous.get("confidence", 0.0)),
                float(clean.get("confidence", 0.0)),
                bridge_mean,
            )
            previous["source_event_indices"].extend(clean["source_event_indices"])
            previous["continuity_state"] = "SUSTAIN_FRAGMENT_CONSOLIDATED"
            merged_boundaries.append(
                {
                    "left_source_index": previous["source_event_indices"][-2],
                    "right_source_index": clean["source_event_indices"][0],
                    "gap_s": gap,
                    "bridge_mean": bridge_mean,
                    "bridge_coverage": bridge_coverage,
                    "onset_support": onset_support,
                }
            )
        else:
            output.append(clean)
    return output, {
        "policy": "NEURAL_CONTOUR_SUSTAIN_CONTINUITY_v1",
        "state": "DERIVED_CANDIDATE",
        "provider": "Basic Pitch 0.4.0 contour+onset tensors",
        "input_event_count": len(source),
        "output_event_count": len(output),
        "merged_boundary_count": len(merged_boundaries),
        "merged_boundaries": merged_boundaries,
        "raw_observations_mutated": False,
        "automatic_curated_status": False,
    }


def consolidate_sustained_fragments_v2(
    notes,
    model_output,
    *,
    tactus_period_s,
    maximum_gap_beats=0.50,
    bridge_mean_threshold=0.25,
    bridge_coverage_threshold=0.70,
    repeated_onset_threshold=0.50,
):
    """Classify same-pitch boundaries using normalized time and plane evidence.

    The function consumes the v0.3.2 derived layer and produces a new derived
    candidate.  If a physical tactus or contour plane is unavailable it returns
    an unchanged copy, allowing the caller to select the prior baseline.
    """
    source = sorted((dict(note) for note in notes or []), key=lambda note: (note["start_s"], note["end_s"], note["midi"]))
    contour = _as_plane(model_output, "contour")
    onset = _as_plane(model_output, "onset")
    if not isinstance(tactus_period_s, (int, float)) or not np.isfinite(tactus_period_s) or tactus_period_s <= 0:
        return [dict(note) for note in source], {
            "policy": CONTINUITY_V2_POLICY,
            "state": "ABSTAIN_TACTUS_UNRESOLVED",
            "input_event_count": len(source),
            "output_event_count": len(source),
            "merged_boundary_count": 0,
            "raw_observations_mutated": False,
            "automatic_curated_status": False,
        }
    if contour is None:
        return [dict(note) for note in source], {
            "policy": CONTINUITY_V2_POLICY,
            "state": "ABSTAIN_NO_CONTOUR",
            "input_event_count": len(source),
            "output_event_count": len(source),
            "merged_boundary_count": 0,
            "raw_observations_mutated": False,
            "automatic_curated_status": False,
        }

    maximum_gap_s = float(tactus_period_s) * float(maximum_gap_beats)
    output = []
    boundary_decisions = []
    for note in source:
        clean = dict(note)
        clean.setdefault("source_event_indices", [])
        clean.setdefault("continuity_state", "PLANE_EVIDENCE_RETAINED")
        if not output:
            output.append(clean)
            continue
        previous = output[-1]
        gap = float(clean["start_s"]) - float(previous["end_s"])
        same_pitch = int(round(clean["midi"])) == int(round(previous["midi"]))
        decision = {
            "left_source_event_indices": list(previous.get("source_event_indices", [])),
            "right_source_event_indices": list(clean.get("source_event_indices", [])),
            "gap_beats": gap / float(tactus_period_s),
            "same_pitch": same_pitch,
        }
        if not same_pitch:
            decision["classification"] = "PITCH_TRANSITION"
            boundary_decisions.append(decision)
            output.append(clean)
            continue
        if gap < 0 or gap > maximum_gap_s:
            decision["classification"] = "ABSTAIN_INSUFFICIENT_EVIDENCE"
            boundary_decisions.append(decision)
            output.append(clean)
            continue

        bridge_mean, bridge_coverage = _pitch_support(contour, previous["end_s"], clean["start_s"], clean["midi"])
        onset_support = _onset_support(onset, clean["start_s"], clean["midi"])
        decision.update(
            bridge_mean=bridge_mean,
            bridge_coverage=bridge_coverage,
            onset_support=onset_support,
        )
        if onset_support is not None and onset_support >= repeated_onset_threshold:
            decision["classification"] = "NEW_ARTICULATION"
            boundary_decisions.append(decision)
            output.append(clean)
            continue
        if bridge_mean < bridge_mean_threshold or bridge_coverage < bridge_coverage_threshold:
            decision["classification"] = "ABSTAIN_INSUFFICIENT_EVIDENCE"
            boundary_decisions.append(decision)
            output.append(clean)
            continue

        decision["classification"] = "SUSTAIN_CONTINUATION"
        boundary_decisions.append(decision)
        previous["end_s"] = clean["end_s"]
        previous["confidence"] = min(float(previous.get("confidence", 0.0)), float(clean.get("confidence", 0.0)), bridge_mean)
        previous["source_event_indices"] = list(previous.get("source_event_indices", [])) + list(clean.get("source_event_indices", []))
        previous["continuity_state"] = "TACTUS_NORMALIZED_SUSTAIN_CONSOLIDATED"

    return output, {
        "policy": CONTINUITY_V2_POLICY,
        "state": "DERIVED_CANDIDATE",
        "provider": "Basic Pitch 0.4.0 contour+onset tensors / frozen HookLab tactus",
        "time_unit": "FRACTION_OF_TACTUS",
        "tactus_period_s": float(tactus_period_s),
        "maximum_gap_beats": float(maximum_gap_beats),
        "input_event_count": len(source),
        "output_event_count": len(output),
        "merged_boundary_count": sum(item["classification"] == "SUSTAIN_CONTINUATION" for item in boundary_decisions),
        "boundary_class_counts": {
            state: sum(item["classification"] == state for item in boundary_decisions)
            for state in ("SUSTAIN_CONTINUATION", "NEW_ARTICULATION", "PITCH_TRANSITION", "ABSTAIN_INSUFFICIENT_EVIDENCE")
        },
        "boundary_decisions": boundary_decisions,
        "raw_observations_mutated": False,
        "automatic_curated_status": False,
        "identity_features_used": False,
    }


def _notes_plane(notes, frame_count, bin_count):
    plane = np.zeros((frame_count, bin_count), dtype=float)
    for note in notes or []:
        start = _frame(note["start_s"], frame_count)
        end = _frame(note["end_s"], frame_count)
        center = _midi_to_contour_bin(note["midi"])
        if end <= start or not 0 <= center < bin_count:
            continue
        confidence = max(0.0, min(1.0, float(note.get("confidence", 1.0))))
        for offset, weight in ((0, 1.0), (-1, 0.55), (1, 0.55), (-2, 0.20), (2, 0.20)):
            target = center + offset
            if 0 <= target < bin_count:
                plane[start:end, target] = np.maximum(plane[start:end, target], confidence * weight)
    return plane


def _nearest_errors(reference_times, candidate_times):
    if not reference_times or not candidate_times:
        return None
    errors = [min(abs(candidate - reference) for reference in reference_times) for candidate in candidate_times]
    return float(np.median(errors) * 1000.0)


def plane_residual_metrics(model_output, notes, *, contour_threshold=0.25, onset_threshold=0.50):
    """Compare the neural reference plane with a same-clock note plane.

    The residual remains a vector.  No weighted aggregate or promotion score is
    produced before calibration.
    """
    contour = _as_plane(model_output, "contour")
    onset = _as_plane(model_output, "onset")
    if contour is None:
        return {
            "feature_id": FEATURE_ID,
            "status": "AUDIT_FEATURE_NOT_CALIBRATED",
            "measurement_state": "ABSTAIN_NO_CONTOUR",
            "generation_class": "D0_EXPLORATORY",
            "scientific_d_unlocked": False,
            "residual_vector": None,
        }

    candidate = _notes_plane(notes, *contour.shape)
    ref_strength = np.max(contour, axis=1)
    cand_strength = np.max(candidate, axis=1)
    ref_voiced = ref_strength >= contour_threshold
    cand_voiced = cand_strength > 0
    intersection = ref_voiced & cand_voiced
    union = ref_voiced | cand_voiced
    ref_count = int(np.sum(ref_voiced))

    ref_bin = np.argmax(contour, axis=1)
    cand_bin = np.argmax(candidate, axis=1)
    pitch_error = np.abs(ref_bin[intersection] - cand_bin[intersection]) * (100.0 / 3.0)
    pitch_ridge_error = float(np.median(pitch_error)) if pitch_error.size else None
    octave_multiple = np.round(pitch_error / 1200.0)
    octave_confusion = (
        float(np.mean((octave_multiple >= 1.0) & (np.abs(pitch_error - 1200.0 * octave_multiple) <= 100.0)))
        if pitch_error.size
        else None
    )

    common_pairs = intersection[1:] & intersection[:-1]
    ref_delta = np.diff(ref_bin.astype(float))[common_pairs] * (100.0 / 3.0) * BASIC_PITCH_FRAME_HZ
    cand_delta = np.diff(cand_bin.astype(float))[common_pairs] * (100.0 / 3.0) * BASIC_PITCH_FRAME_HZ
    gesture_error = float(np.median(np.abs(ref_delta - cand_delta))) if ref_delta.size else None

    reference_onsets = []
    if onset is not None:
        strength = np.max(onset, axis=1)
        reference_onsets = [
            index / BASIC_PITCH_FRAME_HZ
            for index in range(1, len(strength) - 1)
            if strength[index] >= onset_threshold
            and strength[index] >= strength[index - 1]
            and strength[index] > strength[index + 1]
        ]
    candidate_onsets = [float(note["start_s"]) for note in notes or []]
    candidate_offsets = [float(note["end_s"]) for note in notes or []]
    ref_transitions = np.flatnonzero(ref_voiced[1:] != ref_voiced[:-1]) + 1
    reference_offsets = [
        index / BASIC_PITCH_FRAME_HZ
        for index in ref_transitions
        if ref_voiced[index - 1] and not ref_voiced[index]
    ]

    fragmentation = 0
    for index in range(1, len(cand_voiced) - 1):
        if ref_voiced[index] and not cand_voiced[index] and cand_voiced[index - 1] and cand_voiced[index + 1]:
            fragmentation += 1

    return {
        "feature_id": FEATURE_ID,
        "status": "AUDIT_FEATURE_NOT_CALIBRATED",
        "measurement_state": "MEASURED_DERIVED_DIAGNOSTIC",
        "provider": "Basic Pitch 0.4.0 contour+onset tensors / HookLab plane registration v0.1",
        "registration": "COMMON_PHYSICAL_CLOCK_NO_WARP_v1",
        "generation_class": "D0_EXPLORATORY",
        "scientific_d_unlocked": False,
        "residual_vector": {
            "pitch_ridge_error_cents_median": pitch_ridge_error,
            "voiced_overlap_iou": float(np.sum(intersection) / np.sum(union)) if np.any(union) else None,
            "false_silence_ratio": float(np.sum(ref_voiced & ~cand_voiced) / ref_count) if ref_count else None,
            "onset_error_ms_median": _nearest_errors(reference_onsets, candidate_onsets),
            "offset_error_ms_median": _nearest_errors(reference_offsets, candidate_offsets),
            "sustain_fragmentation_rate": float(fragmentation / ref_count) if ref_count else None,
            "gesture_slope_error_cents_per_s_median": gesture_error,
            "octave_confusion_rate": octave_confusion,
        },
        "units": {
            "pitch_ridge_error_cents_median": "cents",
            "voiced_overlap_iou": "ratio_0_1",
            "false_silence_ratio": "ratio_0_1",
            "onset_error_ms_median": "milliseconds",
            "offset_error_ms_median": "milliseconds",
            "sustain_fragmentation_rate": "events_per_reference_voiced_frame",
            "gesture_slope_error_cents_per_s_median": "cents_per_second",
            "octave_confusion_rate": "ratio_0_1",
        },
        "weighted_composite": None,
        "raw_observations_mutated": False,
    }
