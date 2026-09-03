"""Audible M+H+T reconstruction after recovery and reasoning stages."""

from __future__ import annotations

import numpy as np
import soundfile as sf


def midi_hz(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))


def render(report, output_path, *, sample_rate=44100):
    duration = float(report["duration_s"])
    signal = np.zeros(int(duration * sample_rate) + 1, np.float32)

    def add_tone(start, end, midi, amplitude, harmonic=False):
        left = max(0, int(start * sample_rate))
        right = min(len(signal), int(end * sample_rate))
        if right <= left:
            return
        time = np.arange(right - left) / sample_rate
        remaining = max(0.001, end - start) - time
        envelope = np.clip(np.minimum(1, time / 0.012) * np.minimum(1, np.maximum(0, remaining) / 0.045), 0, 1)
        frequency = midi_hz(midi)
        wave = np.sin(2 * np.pi * frequency * time)
        if harmonic:
            wave += 0.18 * np.sin(4 * np.pi * frequency * time)
        signal[left:right] += amplitude * envelope * wave

    notes = report.get("notes", [])
    for index, note in enumerate(notes):
        # Audition-only micro-legato prevents the envelope from making a
        # detected phrase sound artificially discontinuous. Raw timestamps
        # remain unchanged in the report.
        audible_end = note["end_s"]
        if index + 1 < len(notes):
            next_start = notes[index + 1]["start_s"]
            gap = next_start - audible_end
            if 0 < gap <= 0.075 and abs(int(note["midi"]) - int(notes[index + 1]["midi"])) <= 7:
                audible_end = min(next_start, audible_end + 0.045)
        add_tone(note["start_s"], audible_end, note["midi"], 0.13, True)

    for unit in report.get("harmony", []):
        if unit.get("state") not in {"LOCK", "LOCKED"}:
            continue
        root = 48 + int(unit.get("root_pc", 0))
        kept = None
        advice = unit.get("ai_advice") or {}
        decisions = advice.get("candidate_decisions", [])
        if decisions:
            by_id = {candidate["candidate_id"]: candidate for candidate in unit.get("candidates", [])}
            kept = [by_id[item["candidate_id"]]["pitch_class"] for item in decisions if item.get("action") == "KEEP" and item.get("candidate_id") in by_id]
        if not kept:
            kept = [(int(unit.get("root_pc", 0)) + int(interval)) % 12 for interval in unit.get("intervals", [])]
        for index, pitch_class in enumerate(dict.fromkeys(kept)):
            midi = 48 + pitch_class
            add_tone(unit["start_s"], unit["end_s"], midi, 0.033 if index else 0.041, True)

    beat_items = report.get("beats", [])
    for item in beat_items:
        beat = item.get("t") if isinstance(item, dict) else item
        strength = item.get("metric_strength") if isinstance(item, dict) else None
        left = int(float(beat) * sample_rate)
        right = min(len(signal), left + int(0.05 * sample_rate))
        if left < 0 or right <= left:
            continue
        time = np.arange(right - left) / sample_rate
        frequency = 1100 if strength == "DOWNBEAT" else (950 if strength == "STRONG" else 820)
        amplitude = 0.15 if strength == "DOWNBEAT" else (0.125 if strength == "STRONG" else 0.10)
        signal[left:right] += amplitude * np.exp(-time / 0.014) * np.sin(2 * np.pi * frequency * time)

    peak = float(np.max(np.abs(signal)))
    if peak:
        signal *= 0.92 / peak
    sf.write(output_path, signal, sample_rate)
    return {
        "audible_layers": ["melody", "harmony_lock", "beat_tactus"],
        "melody_render_policy": "RAW_TIMESTAMPS_PLUS_MAX_45MS_AUDITION_MICRO_LEGATO",
        "beat_accent_policy": "METRIC_EVIDENCE_ONLY_NO_INDEX_MODULO_ASSUMPTION",
        "sample_rate": sample_rate,
        "duration_s": duration,
    }
