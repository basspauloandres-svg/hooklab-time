"""Traceable MIE v0.3.1 temporal refinements.

The functions in this module never overwrite sensor observations.  They build
derived candidate layers for audition while retaining explicit abstention.
"""

from __future__ import annotations

from collections import Counter
from statistics import median


def _overlap(a, b):
    return min(a["end_s"], b["end_s"]) - max(a["start_s"], b["start_s"])


def recover_melody_gaps(raw_candidates, accepted):
    """Conservatively recover one Basic Pitch candidate inside a short gap.

    Recovery requires evidence on both sides and close pitch continuity.  The
    returned audit keeps the original accepted events and identifies every
    added event as a candidate-derived recovery, never as ground truth.
    """
    original = [dict(note, recovery_state="RAW_ACCEPTED") for note in accepted]
    selected_keys = {
        (round(n["start_s"], 5), round(n["end_s"], 5), int(n["midi"]))
        for n in accepted
    }
    pool = []
    for note in raw_candidates:
        key = (round(note["start_s"], 5), round(note["end_s"], 5), int(note["midi"]))
        if key in selected_keys:
            continue
        duration = note["end_s"] - note["start_s"]
        if note.get("confidence", 0.0) < 0.22 or duration < 0.045:
            continue
        if any(_overlap(note, kept) > 0.025 for kept in accepted):
            continue
        previous = max(
            (kept for kept in accepted if kept["end_s"] <= note["start_s"]),
            key=lambda kept: kept["end_s"],
            default=None,
        )
        following = min(
            (kept for kept in accepted if kept["start_s"] >= note["end_s"]),
            key=lambda kept: kept["start_s"],
            default=None,
        )
        if previous is None or following is None:
            continue
        left_gap = note["start_s"] - previous["end_s"]
        right_gap = following["start_s"] - note["end_s"]
        if left_gap > 0.45 or right_gap > 0.45:
            continue
        left_interval = abs(int(note["midi"]) - int(previous["midi"]))
        right_interval = abs(int(note["midi"]) - int(following["midi"]))
        if left_interval > 7 or right_interval > 7:
            continue
        score = (
            float(note.get("confidence", 0.0))
            - 0.025 * (left_interval + right_interval)
            - 0.15 * (left_gap + right_gap)
        )
        pool.append((score, note, previous, following))

    # Keep at most one candidate for each original gap.
    best_by_gap = {}
    for score, note, previous, following in pool:
        gap_key = (round(previous["end_s"], 5), round(following["start_s"], 5))
        if gap_key not in best_by_gap or score > best_by_gap[gap_key][0]:
            best_by_gap[gap_key] = (score, note, previous, following)

    recovered = []
    for score, note, previous, following in best_by_gap.values():
        recovered.append(
            dict(
                note,
                recovery_state="RECOVERED_CANDIDATE",
                recovery_basis={
                    "provider": "BASIC_PITCH_RAW_CANDIDATE",
                    "left_interval_semitones": abs(int(note["midi"]) - int(previous["midi"])),
                    "right_interval_semitones": abs(int(note["midi"]) - int(following["midi"])),
                    "left_gap_s": left_gap if previous is None else note["start_s"] - previous["end_s"],
                    "right_gap_s": right_gap if following is None else following["start_s"] - note["end_s"],
                    "selection_score": score,
                },
            )
        )

    events = sorted(original + recovered, key=lambda n: (n["start_s"], n["end_s"]))
    return events, {
        "policy": "CONSERVATIVE_BIDIRECTIONAL_GAP_RECOVERY_v1",
        "raw_candidate_count": len(raw_candidates),
        "original_accepted_count": len(accepted),
        "recovered_candidate_count": len(recovered),
        "final_event_count": len(events),
        "automatic_curated_status": False,
    }


def _period_candidates(events, start, limit=36):
    sample = events[start : start + limit]
    values = []
    for left in range(len(sample)):
        for right in range(left + 1, min(len(sample), left + 4)):
            delta = sample[right]["t"] - sample[left]["t"]
            steps = right - left
            period = delta / steps
            if 0.32 <= period <= 1.25:
                values.append(period)
    return values


def _acquire(events, start):
    candidates = _period_candidates(events, start)
    if not candidates:
        return None
    # Quantized bins choose a locally supported clock without an expected BPM.
    bins = Counter(round(value / 0.02) * 0.02 for value in candidates)
    ranked = [item[0] for item in bins.most_common(6)]
    best = None
    for period in ranked:
        for anchor_index in range(start, min(len(events), start + 8)):
            anchor = events[anchor_index]["t"]
            matched = []
            for step in range(8):
                target = anchor + step * period
                candidates_here = [
                    (abs(item["t"] - target), index, item)
                    for index, item in enumerate(events[anchor_index:], anchor_index)
                    if abs(item["t"] - target) <= min(0.13, period * 0.25)
                ]
                if not candidates_here:
                    continue
                distance, index, item = min(candidates_here)
                matched.append((step, distance, index, item))
            observed = len(matched)
            if observed < 6:
                continue
            error = sum(item[1] for item in matched) / observed
            salience = sum(float(item[3].get("score", 0.0)) for item in matched) / observed
            score = observed / 8 + 0.15 * salience - error / max(period, 1e-9)
            candidate = (score, anchor, period, anchor_index)
            if best is None or candidate[0] > best[0]:
                best = candidate
    return best


def resolve_tactus(raw_beats, duration_s):
    """Resolve evidence-backed pulse runs from Beat This observations.

    This is a Python integration of the existing HookLab acquire/track/clock
    lineage.  It suppresses off-clock subdivisions and permits at most two
    inferred events before releasing the clock.
    """
    events = sorted((dict(item) for item in raw_beats), key=lambda item: item["t"])
    resolved = []
    runs = []
    cursor = 0
    run_id = 0
    while cursor < len(events):
        acquired = _acquire(events, cursor)
        if acquired is None:
            cursor += 1
            continue
        acquisition_score, anchor, period, anchor_index = acquired
        run_id += 1
        target = anchor
        search_index = anchor_index
        misses = 0
        run_events = []
        while target <= duration_s and search_index < len(events):
            tolerance = min(0.13, period * 0.25)
            choices = [
                (abs(events[index]["t"] - target), index, events[index])
                for index in range(search_index, len(events))
                if events[index]["t"] <= target + tolerance
                and events[index]["t"] >= target - tolerance
            ]
            if choices:
                distance, index, observed = min(choices)
                event = {
                    "t": float(observed["t"]),
                    "score": float(observed.get("score", 0.0)),
                    "clock_state": "OBSERVED",
                    "run": run_id,
                    "source_index": index,
                    "phase_error_s": float(observed["t"] - target),
                }
                run_events.append(event)
                search_index = index + 1
                target = observed["t"] + period
                misses = 0
            else:
                misses += 1
                if misses > 2:
                    break
                run_events.append(
                    {
                        "t": float(target),
                        "score": 0.0,
                        "clock_state": "DEDUCED_LOW_EVIDENCE",
                        "run": run_id,
                        "source_index": None,
                        "phase_error_s": None,
                    }
                )
                target += period
        if len(run_events) >= 6:
            resolved.extend(run_events)
            runs.append(
                {
                    "run": run_id,
                    "start_s": run_events[0]["t"],
                    "end_s": run_events[-1]["t"],
                    "period_s": period,
                    "bpm": 60.0 / period,
                    "acquisition_score": acquisition_score,
                    "observed_count": sum(e["clock_state"] == "OBSERVED" for e in run_events),
                    "deduced_count": sum(e["clock_state"] != "OBSERVED" for e in run_events),
                }
            )
        cursor = max(cursor + 1, search_index)

    # De-duplicate at run joins while preserving the higher-evidence event.
    cleaned = []
    for event in sorted(resolved, key=lambda item: item["t"]):
        if cleaned and event["t"] - cleaned[-1]["t"] < 0.16:
            if event["score"] > cleaned[-1]["score"]:
                cleaned[-1] = event
            continue
        cleaned.append(event)
    intervals = [b["t"] - a["t"] for a, b in zip(cleaned, cleaned[1:]) if a["run"] == b["run"]]
    tempo = 60.0 / median(intervals) if intervals else 0.0
    return cleaned, {
        "policy": "HOOKLAB_CLOCK_LINEAGE_PY_v1",
        "raw_observation_count": len(events),
        "resolved_tactus_count": len(cleaned),
        "tempo_bpm": tempo,
        "runs": runs,
        "downbeat_state": "UNRESOLVED",
    }


def resolve_metric_grid(tactus, downbeat_candidates):
    """Lock meter/downbeat only when Beat This downbeats agree consistently."""
    if len(tactus) < 8 or len(downbeat_candidates) < 3:
        return [], {"state": "DOWNBEAT_UNRESOLVED", "reason": "insufficient_evidence"}
    matched = []
    for downbeat in downbeat_candidates:
        distance, index = min((abs(item["t"] - downbeat["t"]), i) for i, item in enumerate(tactus))
        if distance <= 0.18:
            matched.append((index, downbeat, distance))
    matched_indices = sorted(set(index for index, _, _ in matched))
    spacings = [b - a for a, b in zip(matched_indices, matched_indices[1:]) if 2 <= b - a <= 8]
    if len(spacings) < 2:
        return [], {"state": "DOWNBEAT_UNRESOLVED", "reason": "insufficient_consistent_intervals"}
    meter, count = Counter(spacings).most_common(1)[0]
    consistency = count / len(spacings)
    if consistency < 0.70:
        return [], {
            "state": "DOWNBEAT_UNRESOLVED",
            "reason": "meter_interval_inconsistent",
            "candidate_meter_beats": meter,
            "consistency": consistency,
        }
    phase_counts = Counter(index % meter for index in matched_indices)
    phase, phase_count = phase_counts.most_common(1)[0]
    phase_consistency = phase_count / len(matched_indices)
    if phase_consistency < 0.70:
        return [], {
            "state": "DOWNBEAT_UNRESOLVED",
            "reason": "downbeat_phase_inconsistent",
            "candidate_meter_beats": meter,
            "interval_consistency": consistency,
            "phase_consistency": phase_consistency,
        }
    grid = []
    for index, beat in enumerate(tactus):
        strength = None
        if index % meter == phase:
            strength = "DOWNBEAT"
        elif meter % 2 == 0 and (index - phase) % meter == meter // 2:
            strength = "STRONG"
        if strength:
            grid.append({"t": beat["t"], "tactus_index": index, "metric_strength": strength})
            beat["metric_strength"] = strength
    return grid, {
        "state": "METRIC_LOCK",
        "meter_beats": meter,
        "downbeat_matches": len(matched_indices),
        "consistency": consistency,
        "phase": phase,
        "phase_consistency": phase_consistency,
        "grid_policy": "REGULAR_CONSENSUS_PHASE_v2",
    }


def align_harmony_to_shared_clock_v2(harmony, notes, tactus, *, tactus_period_s, maximum_shift_beats=0.35):
    """Place harmonic changes on the frozen tactus and close rendering gaps.

    The harmonic identity remains unchanged. Each accepted change is snapped
    to the nearest observed/deduced tactus within a normalized tolerance. The
    preceding LOCK state then persists to that boundary, preventing an
    accompaniment reattack or an ambiguous window from becoming silence.
    Melody onsets are measured against the same clock for audit only; they do
    not manufacture or move harmonic changes.
    """
    source_all = sorted((dict(unit) for unit in harmony or []), key=lambda unit: (unit["start_s"], unit["end_s"]))
    source = [unit for unit in source_all if unit.get("state") == "LOCK"]
    if not isinstance(tactus_period_s, (int, float)) or tactus_period_s <= 0 or not tactus:
        return source_all, {
            "policy": "TACTUS_SHARED_M_H_ALIGNMENT_v2",
            "state": "ABSTAIN_TACTUS_UNRESOLVED",
            "input_state_count": len(source_all),
            "output_state_count": len(source_all),
            "raw_observations_mutated": False,
        }
    period = float(tactus_period_s)
    maximum_shift_s = period * float(maximum_shift_beats)
    clock = [float(item["t"] if isinstance(item, dict) else item) for item in tactus]
    melody_onsets = [float(note["start_s"]) for note in notes or []]
    output = []
    shifts = []
    for index, unit in enumerate(source):
        clean = dict(unit)
        start = float(clean["start_s"])
        nearest = min(clock, key=lambda time: abs(time - start))
        may_snap = not output or nearest > float(output[-1]["start_s"]) + 1e-8
        if index > 0 and may_snap and abs(nearest - start) <= maximum_shift_s:
            clean["start_s"] = nearest
            shifts.append(nearest - start)
        clean["shared_clock_state"] = "FROZEN_TACTUS_BOUNDARY"
        if output:
            boundary = float(clean["start_s"])
            previous = output[-1]
            previous["end_s"] = boundary
            previous["persistence_state"] = "HELD_UNTIL_NEXT_ACCEPTED_HARMONY_CHANGE"
        if float(clean["end_s"]) > float(clean["start_s"]):
            output.append(clean)
    if output:
        output[-1]["end_s"] = max(float(output[-1]["end_s"]), float(source[-1]["end_s"]))
    deviations = []
    for unit in output[1:]:
        if melody_onsets:
            deviations.append(min(abs(float(unit["start_s"]) - onset) for onset in melody_onsets) / period)
    return output, {
        "policy": "TACTUS_SHARED_M_H_ALIGNMENT_v2",
        "state": "DERIVED_CANDIDATE",
        "time_unit": "FRACTION_OF_TACTUS",
        "tactus_period_s": period,
        "maximum_shift_beats": float(maximum_shift_beats),
        "input_state_count": len(source_all),
        "output_state_count": len(output),
        "ambiguous_observation_count": sum(unit.get("state") != "LOCK" for unit in source_all),
        "boundary_shift_count": sum(abs(value) > 1e-9 for value in shifts),
        "median_abs_boundary_shift_beats": median([abs(value) / period for value in shifts]) if shifts else 0.0,
        "median_harmony_to_nearest_melody_onset_beats": median(deviations) if deviations else None,
        "gapless_between_accepted_states": all(abs(float(left["end_s"]) - float(right["start_s"])) < 1e-8 for left, right in zip(output, output[1:])),
        "melody_moved": False,
        "harmonic_identity_changed": False,
        "raw_observations_mutated": False,
        "identity_features_used": False,
    }


def align_harmony_to_metric(raw_harmony, metric_grid, duration_s):
    """Aggregate LOCK harmony observations between successive strong times."""
    if len(metric_grid) < 2:
        return [], {"state": "METRIC_ALIGNMENT_ABSTAIN", "reason": "metric_grid_unresolved"}
    aligned = []
    bounds = [item["t"] for item in metric_grid]
    if bounds[-1] < duration_s:
        bounds.append(duration_s)
    for start, end in zip(bounds, bounds[1:]):
        source = [
            (index, unit)
            for index, unit in enumerate(raw_harmony)
            if unit.get("state") == "LOCK"
            and start <= (unit["start_s"] + unit["end_s"]) / 2 < end
        ]
        if not source:
            continue
        weights = Counter()
        for _, unit in source:
            identity = (int(unit["root_pc"]), unit["quality"], tuple(unit["intervals"]))
            weights[identity] += max(1e-6, float(unit.get("evidence", 0.0)) * float(unit.get("margin", 0.0)))
        winner, winner_weight = weights.most_common(1)[0]
        total = sum(weights.values())
        support = winner_weight / total if total else 0.0
        if support < 0.60:
            continue
        root, quality, intervals = winner
        supporting = [(index, unit) for index, unit in source if (unit["root_pc"], unit["quality"], tuple(unit["intervals"])) == winner]
        aligned.append(
            {
                "start_s": float(start),
                "end_s": float(end),
                "root_pc": root,
                "quality": quality,
                "intervals": list(intervals),
                "evidence": max(float(unit.get("evidence", 0.0)) for _, unit in supporting),
                "margin": max(float(unit.get("margin", 0.0)) for _, unit in supporting),
                "bass_bonus": max(float(unit.get("bass_bonus", 0.0)) for _, unit in supporting),
                "state": "LOCK",
                "alignment_state": "HARMONY_METRIC_ALIGNED",
                "source_unit_indices": [index for index, _ in supporting],
                "support_share": support,
                "quantization_offset_s": float(start - supporting[0][1]["start_s"]),
            }
        )
    return aligned, {
        "state": "HARMONY_METRIC_ALIGNED" if aligned else "METRIC_ALIGNMENT_ABSTAIN",
        "raw_unit_count": len(raw_harmony),
        "aligned_unit_count": len(aligned),
        "ambiguous_preserved_count": sum(unit.get("state") != "LOCK" for unit in raw_harmony),
    }


def consolidate_harmony_persistence(harmony, *, tactus_period_s, maximum_gap_beats=0.25):
    """Coalesce identical adjacent LOCK windows into harmonic states.

    Repeated instrumental attacks are not encoded as chord changes. Ambiguous
    windows remain explicit and are never bridged or silently promoted.
    """
    source = sorted((dict(unit, _source_index=index) for index, unit in enumerate(harmony or [])), key=lambda unit: (unit["start_s"], unit["end_s"]))
    if not isinstance(tactus_period_s, (int, float)) or tactus_period_s <= 0:
        return [dict({key: value for key, value in unit.items() if key != "_source_index"}) for unit in source], {
            "policy": "TACTUS_NORMALIZED_HARMONY_PERSISTENCE_v1",
            "state": "ABSTAIN_TACTUS_UNRESOLVED",
            "input_state_count": len(source),
            "output_state_count": len(source),
            "coalesced_boundary_count": 0,
            "raw_observations_mutated": False,
        }

    maximum_gap_s = float(tactus_period_s) * float(maximum_gap_beats)
    output = []
    decisions = []
    for unit in source:
        clean = {key: value for key, value in unit.items() if key != "_source_index"}
        clean.setdefault("source_unit_indices", [unit["_source_index"]])
        clean.setdefault("persistence_state", "HARMONY_STATE_RETAINED")
        if not output:
            output.append(clean)
            continue
        previous = output[-1]
        gap = float(clean["start_s"]) - float(previous["end_s"])
        same_identity = (
            int(clean["root_pc"]), clean["quality"], tuple(clean.get("intervals", []))
        ) == (
            int(previous["root_pc"]), previous["quality"], tuple(previous.get("intervals", []))
        )
        both_locked = clean.get("state") == "LOCK" and previous.get("state") == "LOCK"
        if same_identity and both_locked and -1e-6 <= gap <= maximum_gap_s:
            previous["end_s"] = max(float(previous["end_s"]), float(clean["end_s"]))
            previous["evidence"] = min(float(previous.get("evidence", 0.0)), float(clean.get("evidence", 0.0)))
            previous["margin"] = min(float(previous.get("margin", 0.0)), float(clean.get("margin", 0.0)))
            previous["source_unit_indices"] = list(previous.get("source_unit_indices", [])) + list(clean.get("source_unit_indices", []))
            previous["persistence_state"] = "IDENTICAL_LOCK_STATES_COALESCED"
            decisions.append("HARMONY_STATE_CONTINUATION")
        else:
            decisions.append("AMBIGUOUS_PRESERVED" if not both_locked else "HARMONY_CHANGE")
            output.append(clean)

    input_repetitions_all = sum(
        (int(a["root_pc"]), a["quality"], tuple(a.get("intervals", [])))
        == (int(b["root_pc"]), b["quality"], tuple(b.get("intervals", [])))
        for a, b in zip(source, source[1:])
    )
    input_locked_repetitions = sum(
        (int(a["root_pc"]), a["quality"], tuple(a.get("intervals", [])))
        == (int(b["root_pc"]), b["quality"], tuple(b.get("intervals", [])))
        and a.get("state") == b.get("state") == "LOCK"
        for a, b in zip(source, source[1:])
    )
    output_repetitions = sum(
        (int(a["root_pc"]), a["quality"], tuple(a.get("intervals", [])))
        == (int(b["root_pc"]), b["quality"], tuple(b.get("intervals", [])))
        and a.get("state") == b.get("state") == "LOCK"
        for a, b in zip(output, output[1:])
    )
    return output, {
        "policy": "TACTUS_NORMALIZED_HARMONY_PERSISTENCE_v1",
        "state": "DERIVED_CANDIDATE",
        "time_unit": "FRACTION_OF_TACTUS",
        "tactus_period_s": float(tactus_period_s),
        "maximum_gap_beats": float(maximum_gap_beats),
        "input_state_count": len(source),
        "output_state_count": len(output),
        "coalesced_boundary_count": decisions.count("HARMONY_STATE_CONTINUATION"),
        "ambiguous_preserved_count": sum(unit.get("state") != "LOCK" for unit in source),
        "ambiguous_boundary_count": decisions.count("AMBIGUOUS_PRESERVED"),
        "identical_adjacent_state_rate_all_before": input_repetitions_all / max(1, len(source) - 1),
        "repeated_harmony_state_rate_before": input_locked_repetitions / max(1, len(source) - 1),
        "repeated_harmony_state_rate_after": output_repetitions / max(1, len(output) - 1),
        "raw_observations_mutated": False,
        "identity_features_used": False,
    }
