"""Fail-closed cross-track generalization gate for MIE candidates.

The gate evaluates one result per held-out track.  It deliberately works with
anonymous track/group hashes and macro track summaries, never with titles,
artists, filenames, frame pools, or song-specific templates.
"""

from __future__ import annotations

from statistics import median


INVARIANT_ID = "MIE_CROSS_TRACK_GENERALIZATION_INVARIANT_v1"
SCIENTIFIC_MINIMUM_INDEPENDENT_ALIGNED_TRACKS = 30

LOWER_IS_BETTER = (
    "false_silence_ratio",
    "sustain_fragmentation_rate",
    "onset_error_ms_median",
    "offset_error_ms_median",
    "octave_confusion_rate",
    "repeated_harmony_state_rate",
)
HIGHER_IS_BETTER = ("voiced_overlap_iou",)


def _finite_number(value):
    return isinstance(value, (int, float)) and value == value and value not in (float("inf"), float("-inf"))


def _track_delta(track, metric):
    baseline = track.get("baseline", {}).get(metric)
    candidate = track.get("candidate", {}).get(metric)
    if not _finite_number(baseline) or not _finite_number(candidate):
        return None
    if metric in LOWER_IS_BETTER:
        return float(baseline) - float(candidate)
    return float(candidate) - float(baseline)


def evaluate_cross_track_generalization(
    held_out_tracks,
    *,
    primary_metrics=("false_silence_ratio", "sustain_fragmentation_rate", "repeated_harmony_state_rate"),
    noninferiority_tolerances=None,
    scientific_minimum_tracks=SCIENTIFIC_MINIMUM_INDEPENDENT_ALIGNED_TRACKS,
):
    """Evaluate a track-agnostic candidate without pooling frame observations.

    Positive deltas always mean improvement.  A candidate must preserve the
    frozen tactus for every track.  Per-track abstention is valid and selects
    the baseline rather than fabricating an improvement.
    """
    tracks = [dict(item) for item in held_out_tracks or []]
    tolerances = dict(noninferiority_tolerances or {})
    base = {
        "invariant_id": INVARIANT_ID,
        "evaluation_unit": "INDEPENDENT_HELD_OUT_TRACK",
        "aggregation": "MACRO_BY_TRACK",
        "generation_class": "D0_EXPLORATORY",
        "scientific_d_unlocked": False,
        "general_accuracy_claim_allowed": False,
    }
    if not tracks:
        return dict(base, status="AUDIT_INSUFFICIENT_TRACKS", evaluated_track_count=0)

    identities = [item.get("track_id_hash") for item in tracks]
    groups = [item.get("group_id_hash") for item in tracks]
    if any(not value for value in identities + groups):
        return dict(base, status="AUDIT_PROVENANCE_INCOMPLETE", evaluated_track_count=len(tracks))
    if len(set(identities)) != len(identities) or len(set(groups)) != len(groups):
        return dict(base, status="AUDIT_DATA_LEAKAGE", evaluated_track_count=len(tracks))
    if any(item.get("identity_features_used") is not False for item in tracks):
        return dict(base, status="AUDIT_SONG_SPECIFIC_LOGIC", evaluated_track_count=len(tracks))
    if any(item.get("split") != "HELD_OUT" for item in tracks):
        return dict(base, status="AUDIT_DATA_LEAKAGE", evaluated_track_count=len(tracks))
    if any(item.get("beat_tactus_unchanged") is not True for item in tracks):
        return dict(base, status="NO_PROMOTION_TACTUS_REGRESSION", evaluated_track_count=len(tracks))

    usable = [item for item in tracks if item.get("candidate_state") != "ABSTAIN_INSUFFICIENT_EVIDENCE"]
    abstained = len(tracks) - len(usable)
    if not usable:
        return dict(
            base,
            status="HOLD_FOR_MORE_CASES",
            evaluated_track_count=len(tracks),
            candidate_track_count=0,
            abstained_track_count=abstained,
        )

    metric_summary = {}
    for metric in tuple(dict.fromkeys(tuple(primary_metrics) + LOWER_IS_BETTER + HIGHER_IS_BETTER)):
        deltas = [_track_delta(item, metric) for item in usable]
        deltas = [value for value in deltas if value is not None]
        if not deltas:
            continue
        metric_summary[metric] = {
            "macro_median_improvement": median(deltas),
            "improved_track_count": sum(value > 0 for value in deltas),
            "unchanged_track_count": sum(value == 0 for value in deltas),
            "degraded_track_count": sum(value < 0 for value in deltas),
            "evaluated_track_count": len(deltas),
        }

    missing_primary = [metric for metric in primary_metrics if metric not in metric_summary]
    if missing_primary:
        return dict(
            base,
            status="AUDIT_METRIC_INCOMPLETE",
            missing_primary_metrics=missing_primary,
            evaluated_track_count=len(tracks),
            metric_summary=metric_summary,
        )
    if any(metric_summary[metric]["macro_median_improvement"] <= 0 for metric in primary_metrics):
        return dict(
            base,
            status="HOLD_TRACK_SPECIFIC_GAIN",
            evaluated_track_count=len(tracks),
            metric_summary=metric_summary,
        )

    for metric, tolerance in tolerances.items():
        summary = metric_summary.get(metric)
        if summary and summary["macro_median_improvement"] < -abs(float(tolerance)):
            return dict(
                base,
                status="NO_PROMOTION_NONINFERIORITY_FAILED",
                failed_metric=metric,
                evaluated_track_count=len(tracks),
                metric_summary=metric_summary,
            )

    status = (
        "GENERALIZATION_PASS"
        if len(tracks) >= scientific_minimum_tracks
        else "ENGINEERING_MULTICASE_SMOKE_PASS"
    )
    return dict(
        base,
        status=status,
        evaluated_track_count=len(tracks),
        candidate_track_count=len(usable),
        abstained_track_count=abstained,
        scientific_replication_requirement_met=len(tracks) >= scientific_minimum_tracks,
        metric_summary=metric_summary,
    )
