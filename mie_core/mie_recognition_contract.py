"""Normalize MIE M/H/T measurements into a fail-closed recognition contract."""

from __future__ import annotations

import math


SCHEMA = "HOOKLAB_MIE_RECOGNITION_v0.3"


def _finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _beats(raw):
    output = []
    for index, item in enumerate(raw or []):
        time = item.get("t") if isinstance(item, dict) else item
        score = item.get("score") if isinstance(item, dict) else None
        if _finite(time) and time >= 0:
            output.append(
                {
                    "beat_index": index,
                    "time_s": float(time),
                    "confidence": score,
                    "clock_state": item.get("clock_state") if isinstance(item, dict) else None,
                    "run": item.get("run") if isinstance(item, dict) else None,
                    "metric_strength": item.get("metric_strength") if isinstance(item, dict) else None,
                }
            )
    return output


def _notes(raw):
    output = []
    for index, item in enumerate(raw or []):
        start = item.get("start_s", item.get("on"))
        end = item.get("end_s", item.get("off"))
        midi = item.get("midi", item.get("m"))
        if _finite(start) and _finite(end) and end > start and _finite(midi):
            output.append(
                {
                    "note_index": index,
                    "start_s": float(start),
                    "end_s": float(end),
                    "midi": int(round(midi)),
                    "confidence": item.get("confidence"),
                    "octave_resolution": item.get("octave_resolution", "UNREPORTED"),
                    "recovery_state": item.get("recovery_state", "RAW_ACCEPTED"),
                    "recovery_basis": item.get("recovery_basis"),
                    "continuity_state": item.get("continuity_state"),
                    "source_event_indices": item.get("source_event_indices", []),
                }
            )
    return output


def _harmony(raw):
    output = []
    for index, item in enumerate(raw or []):
        start = item.get("start_s", item.get("start"))
        end = item.get("end_s", item.get("end"))
        state = item.get("state", "AMBIGUOUS")
        if state == "LOCKED":
            state = "LOCK"
        if state not in {"LOCK", "AMBIGUOUS", "ABSTAIN", "REOPEN"}:
            state = "AMBIGUOUS"
        if _finite(start) and _finite(end) and end > start:
            output.append(
                {
                    "unit_id": item.get("unit_id", f"H-{index:04d}"),
                    "start_s": float(start),
                    "end_s": float(end),
                    "root_pc": item.get("root_pc"),
                    "quality": item.get("quality"),
                    "state": state,
                    "confidence": item.get("evidence", item.get("confidence")),
                    "margin": item.get("margin"),
                    "candidates": item.get("candidates", []),
                    "alignment_state": item.get("alignment_state"),
                    "source_unit_indices": item.get("source_unit_indices", []),
                    "support_share": item.get("support_share"),
                    "quantization_offset_s": item.get("quantization_offset_s"),
                    "persistence_state": item.get("persistence_state"),
                    "shared_clock_state": item.get("shared_clock_state"),
                }
            )
    return output


def _nearest_beat(time, beats):
    if not beats:
        return None
    return min(beats, key=lambda beat: abs(beat["time_s"] - time))


def normalize(raw, *, session_id, reference_sha256, sensor_version, ai_provenance=None):
    notes = _notes(raw.get("notes", raw.get("melody")))
    harmony = _harmony(raw.get("harmony"))
    beats = _beats(raw.get("beats"))
    reasons = []
    if not notes:
        reasons.append("MELODY_EVENTS_REQUIRED")
    if not harmony:
        reasons.append("HARMONY_STATES_REQUIRED")
    if not beats:
        reasons.append("BEAT_EVENTS_REQUIRED")
    if not _finite(raw.get("duration_s")) or raw["duration_s"] <= 0:
        reasons.append("DURATION_REQUIRED")
    if reasons:
        return {"schema": SCHEMA, "status": "FAIL", "reasons": reasons, "scientific_d_unlocked": False}

    note_relations = []
    for note in notes:
        beat = _nearest_beat(note["start_s"], beats)
        harmonic = next(
            (unit for unit in harmony if unit["start_s"] <= note["start_s"] < unit["end_s"]), None
        )
        note_relations.append(
            {
                "note_index": note["note_index"],
                "nearest_beat_index": beat["beat_index"] if beat else None,
                "beat_deviation_ms": round((note["start_s"] - beat["time_s"]) * 1000, 3) if beat else None,
                "harmony_unit_id": harmonic["unit_id"] if harmonic else None,
                "harmony_state": harmonic["state"] if harmonic else None,
            }
        )

    return {
        "schema": SCHEMA,
        "status": "PASS",
        "role": "AESTHETIC_REFERENCE_RECOGNITION",
        "semantics": "DESCRIPTIVE_SESSION_REFERENCE_ONLY",
        "session_id": session_id,
        "reference_sha256": reference_sha256,
        "duration_s": float(raw["duration_s"]),
        "sensor_version": sensor_version,
        "generation_class": "D0_EXPLORATORY",
        "scientific_d_unlocked": False,
        "scientific_ingestion": False,
        "source_audio_persistence": "NONE",
        "transcription": {"melody_events": notes, "harmony_states": harmony, "beat_events": beats},
        "recognition": {
            "note_beat_harmony_relations": note_relations,
            "locked_harmony_units": sum(unit["state"] == "LOCK" for unit in harmony),
            "ambiguous_or_abstained_harmony_units": sum(unit["state"] != "LOCK" for unit in harmony),
            "melody_recovery": raw.get("melody_recovery"),
            "tactus_resolution": raw.get("tactus_resolution"),
            "harmony_alignment": raw.get("harmony_alignment"),
        },
        "observation_layers": {
            "notes_raw_accepted": raw.get("notes_raw_accepted", []),
            "raw_note_candidate_count": raw.get("raw_note_candidates"),
            "beat_observations_raw": raw.get("beat_observations_raw", []),
            "downbeat_candidates_raw": raw.get("downbeat_candidates_raw", []),
            "harmony_raw": raw.get("harmony_raw", []),
        },
        "derived_layers": {
            "metric_grid": raw.get("metric_grid", []),
            "harmony_metric_aligned": raw.get("harmony_metric_aligned", []),
            "notes_v0_3_1": raw.get("notes_v0_3_1", []),
            "notes_v0_3_2": raw.get("notes_v0_3_2", []),
            "notes_v0_3_3": raw.get("notes_v0_3_3", []),
            "notes_continuity_derived": raw.get("notes_continuity_derived", []),
            "notes_generalized_derived": raw.get("notes_generalized_derived", []),
            "melody_continuity": raw.get("melody_continuity"),
            "melody_generalization": raw.get("melody_generalization"),
            "melody_gap_recovery": raw.get("melody_gap_recovery"),
            "tf_plane_registration": raw.get("tf_plane_registration"),
            "harmony_v0_3_2": raw.get("harmony_v0_3_2", []),
            "harmony_v0_3_3": raw.get("harmony_v0_3_3", []),
            "harmony_persistence": raw.get("harmony_persistence"),
            "harmony_shared_clock": raw.get("harmony_shared_clock"),
            "cross_track_generalization": raw.get("cross_track_generalization"),
        },
        "ai_provenance": ai_provenance
        or {"provider": "UNCONNECTED", "authority": "NONE", "provider_connected": False},
        "required_audible_layers": ["melody", "harmony_lock", "beat_tactus"],
    }
