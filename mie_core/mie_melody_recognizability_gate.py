"""Fail-closed M-only recognizability diagnostics for MIE v0.3.5.

This module separates two observable questions:

* did an independently observed vocal interval survive source separation?; and
* did the note sensor respond where the separated vocal stem was active?

A single separated stem can support the second diagnosis.  It cannot, by
itself, prove that missing source vocals were lost by the separator.  That
claim requires an independent, time-aligned vocal-presence observation.  The
gate therefore abstains instead of converting mixture energy or filenames into
vocal ground truth.
"""

from __future__ import annotations

import hashlib
import json
import math
from statistics import median

import numpy as np


EXPERIMENT_ID = "MIE-v0.3.5-M-RECOGNIZABILITY-GATE"
SUB_GATE_ID = "DIAGNOSE_SOURCE_SEPARATION_VERSUS_NOTE_SENSOR_RECALL"
POLICY_ID = "MIE_M_ONLY_SEPARATION_SENSOR_DIAGNOSTIC_v1"
ABSTAIN = "ABSTAIN_INSUFFICIENT_MELODY_EVIDENCE"
HISTORICAL_GATE_BLOCKED = "HISTORICAL_GATE_NOT_PASSED"
BASIC_PITCH_FRAME_HZ = 86.0


def canonical_sha256(value):
    """Hash a JSON-compatible event layer without mutating it."""
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _as_plane(model_output, key):
    value = np.asarray((model_output or {}).get(key, []), dtype=float)
    if value.ndim != 2 or not value.size or not np.isfinite(value).all():
        return None
    return value


def _frame_rms(audio, sample_rate, frame_count):
    signal = np.asarray(audio, dtype=float).reshape(-1)
    if not signal.size or not np.isfinite(signal).all() or sample_rate <= 0 or frame_count <= 0:
        return None
    boundaries = np.linspace(0, signal.size, frame_count + 1, dtype=int)
    rms = np.zeros(frame_count, dtype=float)
    for index, (left, right) in enumerate(zip(boundaries[:-1], boundaries[1:])):
        if right > left:
            rms[index] = math.sqrt(float(np.mean(np.square(signal[left:right]))))
    return rms


def _note_mask(notes, frame_count, frame_hz):
    mask = np.zeros(frame_count, dtype=bool)
    for note in notes or []:
        start = max(0, min(frame_count, int(math.floor(float(note["start_s"]) * frame_hz))))
        end = max(0, min(frame_count, int(math.ceil(float(note["end_s"]) * frame_hz))))
        if end > start:
            mask[start:end] = True
    return mask


def _boolean_reference(values, frame_count):
    if values is None:
        return None
    result = np.asarray(values)
    if result.ndim != 1 or len(result) != frame_count:
        return None
    if result.dtype != bool:
        if not np.issubdtype(result.dtype, np.number) or not np.isfinite(result).all():
            return None
        result = result > 0
    return result.astype(bool, copy=False)


def diagnose_source_separation_vs_note_sensor_recall(
    vocal_audio,
    sample_rate,
    model_output,
    raw_note_candidates,
    *,
    independent_vocal_activity=None,
    contour_threshold=0.25,
    absolute_activity_floor_dbfs=-60.0,
    relative_activity_floor_db=-35.0,
    minimum_evidence_s=0.50,
    bottleneck_ratio=0.35,
):
    """Diagnose observable loss locations without treating proxies as accuracy.

    ``independent_vocal_activity`` must come from a registered acoustic sensor
    or reference that is independent of the candidate separator.  Manual song
    timestamps and known notes are inadmissible.  When it is absent, source
    separation recall remains unidentifiable and only note-sensor nonresponse
    conditional on the separated stem can be assessed.
    """
    contour = _as_plane(model_output, "contour")
    onset = _as_plane(model_output, "onset")
    if contour is None:
        return {
            "policy": POLICY_ID,
            "sub_gate": SUB_GATE_ID,
            "status": ABSTAIN,
            "reason": "BASIC_PITCH_CONTOUR_REQUIRED",
            "generation_class": "D0_EXPLORATORY",
            "scientific_d_unlocked": False,
        }

    frame_count = contour.shape[0]
    rms = _frame_rms(vocal_audio, sample_rate, frame_count)
    if rms is None:
        return {
            "policy": POLICY_ID,
            "sub_gate": SUB_GATE_ID,
            "status": ABSTAIN,
            "reason": "SEPARATED_VOCAL_AUDIO_REQUIRED",
            "generation_class": "D0_EXPLORATORY",
            "scientific_d_unlocked": False,
        }

    peak = float(np.max(rms))
    peak_dbfs = 20.0 * math.log10(max(peak, 1e-12))
    activity_threshold_dbfs = max(float(absolute_activity_floor_dbfs), peak_dbfs + float(relative_activity_floor_db))
    rms_dbfs = 20.0 * np.log10(np.maximum(rms, 1e-12))
    stem_active = rms_dbfs >= activity_threshold_dbfs
    contour_active = np.max(contour, axis=1) >= float(contour_threshold)
    note_active = _note_mask(raw_note_candidates, frame_count, BASIC_PITCH_FRAME_HZ)
    sensor_active = contour_active | note_active
    independent = _boolean_reference(independent_vocal_activity, frame_count)

    minimum_frames = max(1, int(math.ceil(float(minimum_evidence_s) * BASIC_PITCH_FRAME_HZ)))
    stem_active_count = int(np.sum(stem_active))
    stem_active_sensor_silent = int(np.sum(stem_active & ~sensor_active))
    sensor_nonresponse_ratio = (
        stem_active_sensor_silent / stem_active_count if stem_active_count else None
    )

    independent_active_count = int(np.sum(independent)) if independent is not None else None
    independent_active_stem_silent = (
        int(np.sum(independent & ~stem_active)) if independent is not None else None
    )
    separation_nonresponse_ratio = (
        independent_active_stem_silent / independent_active_count
        if independent_active_count
        else None
    )

    sensor_supported = stem_active_count >= minimum_frames
    separation_supported = independent_active_count is not None and independent_active_count >= minimum_frames
    sensor_problem = sensor_supported and sensor_nonresponse_ratio >= float(bottleneck_ratio)
    separation_problem = separation_supported and separation_nonresponse_ratio >= float(bottleneck_ratio)

    if sensor_problem and separation_problem:
        status = "MIXED_SEPARATION_AND_NOTE_SENSOR_RECALL_BOTTLENECK"
    elif separation_problem:
        status = "SOURCE_SEPARATION_RECALL_BOTTLENECK"
    elif sensor_problem:
        status = "NOTE_SENSOR_RECALL_BOTTLENECK"
    elif sensor_supported and separation_supported:
        status = "NO_DOMINANT_RECALL_BOTTLENECK_OBSERVED"
    else:
        status = ABSTAIN

    return {
        "policy": POLICY_ID,
        "sub_gate": SUB_GATE_ID,
        "status": status,
        "reason": None if status != ABSTAIN else "MINIMUM_INDEPENDENT_EVIDENCE_NOT_MET",
        "frame_hz": BASIC_PITCH_FRAME_HZ,
        "frame_count": frame_count,
        "thresholds": {
            "contour": float(contour_threshold),
            "absolute_activity_floor_dbfs": float(absolute_activity_floor_dbfs),
            "relative_activity_floor_db": float(relative_activity_floor_db),
            "minimum_evidence_s": float(minimum_evidence_s),
            "bottleneck_ratio": float(bottleneck_ratio),
        },
        "separated_vocal": {
            "peak_dbfs": peak_dbfs,
            "activity_threshold_dbfs": activity_threshold_dbfs,
            "active_frame_count": stem_active_count,
            "active_time_s": stem_active_count / BASIC_PITCH_FRAME_HZ,
        },
        "note_sensor": {
            "provider": "BASIC_PITCH_CONTOUR_PLUS_RAW_CANDIDATES",
            "raw_candidate_count": len(raw_note_candidates or []),
            "stem_active_sensor_silent_frame_count": stem_active_sensor_silent,
            "conditional_nonresponse_ratio": sensor_nonresponse_ratio,
            "evidence_sufficient": sensor_supported,
        },
        "source_separation": {
            "independent_vocal_reference_present": independent is not None,
            "independent_reference_kind_required": "REGISTERED_ACOUSTIC_SENSOR_OR_REFERENCE_NOT_MANUAL_TIMESTAMPS",
            "independent_active_frame_count": independent_active_count,
            "independent_active_stem_silent_frame_count": independent_active_stem_silent,
            "conditional_nonresponse_ratio": separation_nonresponse_ratio,
            "evidence_sufficient": separation_supported,
            "claim_allowed": separation_supported,
        },
        "interpretation": "DIAGNOSTIC_NOT_MELODY_ACCURACY",
        "identity_features_used": False,
        "raw_observations_mutated": False,
        "generation_class": "D0_EXPLORATORY",
        "scientific_d_unlocked": False,
    }


def build_m_only_experiment_audit(
    diagnostic,
    *,
    parent_reference,
    harmony_reference,
    harmony_candidate,
    tactus_reference,
    tactus_candidate,
    source_sha256,
    work_group_hash,
    sensor_versions,
    producer_recognizability="PENDING_PRODUCER_LISTENING",
):
    """Bind the diagnostic to the one-module experiment contract."""
    harmony_reference_hash = canonical_sha256(harmony_reference)
    harmony_candidate_hash = canonical_sha256(harmony_candidate)
    tactus_reference_hash = canonical_sha256(tactus_reference)
    tactus_candidate_hash = canonical_sha256(tactus_candidate)
    h_fixed = harmony_reference_hash == harmony_candidate_hash
    t_fixed = tactus_reference_hash == tactus_candidate_hash
    status = diagnostic.get("status", ABSTAIN)
    if not source_sha256 or not work_group_hash:
        status = "AUDIT_PROVENANCE_INCOMPLETE"
    elif not h_fixed:
        status = "AUDIT_ONE_MODULE_RULE_VIOLATION_H_CHANGED"
    elif not t_fixed:
        status = "NO_PROMOTION_TACTUS_REGRESSION"
    return {
        "schema": "HOOKLAB_MIE_M_ONLY_RECOGNIZABILITY_AUDIT_v1",
        "experiment_id": EXPERIMENT_ID,
        "parent_reference": parent_reference,
        "changed_module": "M_ONLY",
        "sub_gate": SUB_GATE_ID,
        "status": status,
        "source_sha256": source_sha256,
        "work_group_hash": work_group_hash,
        "sensor_versions": dict(sensor_versions),
        "diagnostic": diagnostic,
        "frozen_layers": {
            "harmony_predeclared_reference_sha256": harmony_reference_hash,
            "harmony_candidate_sha256": harmony_candidate_hash,
            "harmony_byte_equivalent": h_fixed,
            "tactus_reference_sha256": tactus_reference_hash,
            "tactus_candidate_sha256": tactus_candidate_hash,
            "tactus_byte_equivalent": t_fixed,
        },
        "producer_evaluation": {
            "recognizability": producer_recognizability,
            "separate_from_automatic_diagnostics": True,
        },
        "identity_features_used": False,
        "generation_class": "D0_EXPLORATORY",
        "scientific_d_unlocked": False,
        "baseline_promoted": False,
    }


def macro_audit_held_out_tracks(track_audits, *, scientific_minimum_tracks=30):
    """Macro-aggregate one diagnostic per independent held-out work group."""
    tracks = [dict(item) for item in track_audits or []]
    base = {
        "experiment_id": EXPERIMENT_ID,
        "evaluation_unit": "INDEPENDENT_HELD_OUT_TRACK",
        "aggregation": "MACRO_BY_TRACK",
        "generation_class": "D0_EXPLORATORY",
        "scientific_d_unlocked": False,
        "general_accuracy_claim_allowed": False,
    }
    if not tracks:
        return dict(base, status="AUDIT_INSUFFICIENT_TRACKS", evaluated_track_count=0)
    track_hashes = [item.get("track_id_hash") for item in tracks]
    group_hashes = [item.get("work_group_hash") for item in tracks]
    if any(not value for value in track_hashes + group_hashes):
        return dict(base, status="AUDIT_PROVENANCE_INCOMPLETE", evaluated_track_count=len(tracks))
    if len(set(track_hashes)) != len(tracks) or len(set(group_hashes)) != len(tracks):
        return dict(base, status="AUDIT_DATA_LEAKAGE", evaluated_track_count=len(tracks))
    if any(item.get("split") != "HELD_OUT" or item.get("identity_features_used") is not False for item in tracks):
        return dict(base, status="AUDIT_SONG_SPECIFIC_LOGIC_OR_SPLIT_LEAKAGE", evaluated_track_count=len(tracks))
    if any(item.get("frozen_layers", {}).get("tactus_byte_equivalent") is not True for item in tracks):
        return dict(base, status="NO_PROMOTION_TACTUS_REGRESSION", evaluated_track_count=len(tracks))
    if any(item.get("frozen_layers", {}).get("harmony_byte_equivalent") is not True for item in tracks):
        return dict(base, status="AUDIT_ONE_MODULE_RULE_VIOLATION_H_CHANGED", evaluated_track_count=len(tracks))

    statuses = [item.get("diagnostic", {}).get("status", ABSTAIN) for item in tracks]
    ratios = [
        item.get("diagnostic", {}).get("note_sensor", {}).get("conditional_nonresponse_ratio")
        for item in tracks
    ]
    ratios = [float(value) for value in ratios if isinstance(value, (int, float)) and math.isfinite(value)]
    abstained = sum(status == ABSTAIN for status in statuses)
    return dict(
        base,
        status="HOLD_FOR_RECOGNIZABILITY_EXPERIMENT",
        evaluated_track_count=len(tracks),
        abstained_track_count=abstained,
        diagnostic_status_counts={state: statuses.count(state) for state in sorted(set(statuses))},
        macro_median_note_sensor_nonresponse_ratio=median(ratios) if ratios else None,
        scientific_replication_requirement=int(scientific_minimum_tracks),
        scientific_replication_requirement_met=len(tracks) >= int(scientific_minimum_tracks),
        producer_recognizability_outcomes=[
            item.get("producer_evaluation", {}).get("recognizability", "UNREPORTED") for item in tracks
        ],
        baseline_promoted=False,
    )


def audit_historical_regression_inventory(inventory):
    """Fail closed before any new-work request or H/T development.

    This consumes provenance only.  It never invokes an audio model and is
    therefore compatible with NO_REPROCESS.
    """
    cases = list((inventory or {}).get("cases", []))
    base = {
        "schema": "HOOKLAB_MIE_HISTORICAL_GATE_AUDIT_v1",
        "experiment_id": EXPERIMENT_ID,
        "no_reprocess": True,
        "changed_module": "M_ONLY",
        "harmony_development_allowed": False,
        "tactus_state": "FROZEN_ENGINEERING_BASELINE_PRESERVED",
        "new_audio_request_allowed": False,
        "generation_class": "D0_EXPLORATORY",
        "scientific_d_unlocked": False,
        "baseline_promoted": False,
    }
    if not cases:
        return dict(base, status="AUDIT_HISTORICAL_INVENTORY_EMPTY")
    if any(not item.get("case_id") or not item.get("provenance") for item in cases):
        return dict(base, status="AUDIT_PROVENANCE_INCOMPLETE")
    if len({item["case_id"] for item in cases}) != len(cases):
        return dict(base, status="AUDIT_DUPLICATE_HISTORICAL_CASE")
    if any(item.get("reprocessed") is not False for item in cases):
        return dict(base, status="AUDIT_NO_REPROCESS_VIOLATION")

    eligible = [item for item in cases if item.get("historical_gate_eligible") is True]
    passed = [item for item in eligible if item.get("v0_3_5_historical_gate") == "PASS_RECOGNIZABLE"]
    failed = [item for item in eligible if item.get("v0_3_5_historical_gate") == "FAIL_UNRECOGNIZABLE"]
    pending = [item for item in eligible if item.get("v0_3_5_historical_gate") not in {
        "PASS_RECOGNIZABLE", "FAIL_UNRECOGNIZABLE"
    }]
    status = "HISTORICAL_GATE_PASSED" if eligible and len(passed) == len(eligible) else HISTORICAL_GATE_BLOCKED
    return dict(
        base,
        status=status,
        inventory_case_count=len(cases),
        eligible_case_count=len(eligible),
        passed_case_count=len(passed),
        failed_case_count=len(failed),
        pending_case_count=len(pending),
        new_audio_request_allowed=status == "HISTORICAL_GATE_PASSED",
        blocking_case_ids=[item["case_id"] for item in failed + pending],
    )
