"""General event-level octave-plane recovery candidate for MIE v0.3.

This does not replace the frozen frame-level Plane Resolver evidence. It supplies
a testable server candidate over Basic Pitch events until exact frame-level
integration is recovered and calibrated.
"""

from __future__ import annotations


def _candidates(midi, minimum, maximum):
    values = {midi + shift for shift in (-24, -12, 0, 12, 24)}
    return sorted(value for value in values if minimum <= value <= maximum)


def resolve_event_octaves(notes, *, minimum=45, maximum=79):
    if not notes:
        return []
    source = sorted((dict(note) for note in notes), key=lambda n: (n["start_s"], n["end_s"]))
    states = [_candidates(int(round(note["midi"])), minimum, maximum) for note in source]
    costs = []
    back = []
    for index, (note, candidates) in enumerate(zip(source, states)):
        raw = int(round(note["midi"]))
        duration = max(0.0, float(note["end_s"]) - float(note["start_s"]))
        row = []
        pointers = []
        for candidate in candidates:
            shift = abs(candidate - raw)
            emission = shift * (0.075 if duration < 0.20 else 0.12)
            if index == 0:
                row.append(emission)
                pointers.append(None)
                continue
            gap = max(0.0, float(note["start_s"]) - float(source[index - 1]["end_s"]))
            options = []
            for previous_index, previous in enumerate(states[index - 1]):
                interval = abs(candidate - previous)
                continuity = interval * 0.025 + max(0, interval - 7) * (0.38 if gap < 0.35 else 0.16)
                options.append((costs[index - 1][previous_index] + continuity + emission, previous_index))
            best_cost, best_pointer = min(options)
            row.append(best_cost)
            pointers.append(best_pointer)
        costs.append(row)
        back.append(pointers)

    selected = [0] * len(source)
    selected[-1] = min(range(len(costs[-1])), key=costs[-1].__getitem__)
    for index in range(len(source) - 1, 0, -1):
        selected[index - 1] = back[index][selected[index]]

    output = []
    for note, candidates, selected_index in zip(source, states, selected):
        raw = int(round(note["midi"]))
        resolved = candidates[selected_index]
        note["midi_raw"] = raw
        note["midi"] = resolved
        note["octave_resolution"] = "RAW" if resolved == raw else f"SHIFT_{resolved - raw:+d}"
        note["octave_corrected"] = resolved != raw
        output.append(note)
    return output

