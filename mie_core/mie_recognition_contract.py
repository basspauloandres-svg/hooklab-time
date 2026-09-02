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
            output.append({"beat_index": index, "time_s": float(time), "confidence": score})
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
        },
        "ai_provenance": ai_provenance
        or {"provider": "UNCONNECTED", "authority": "NONE", "provider_connected": False},
        "required_audible_layers": ["melody", "harmony_lock", "beat_tactus"],
    }

