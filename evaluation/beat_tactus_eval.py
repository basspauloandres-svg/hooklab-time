#!/usr/bin/env python3
"""HookLab TIME — evaluador reproducible B0 vs B1.

Entrada:
  --reference: archivo de tiempos de beat de referencia (una columna en segundos,
               o archivo ASAP con tercera columna que contiene b/db).
  --estimate:  JSON HookLab/Beat This con una lista de tiempos.
  --mode:      b0 usa beats_s; b1 usa tactus_s si existe, y si no beats_s.

Salida: JSON con métricas estándar de mir_eval y diagnósticos HookLab.

No modifica parámetros por canción. La inferencia de metro/downbeat queda fuera de esta fase.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import mir_eval


def _as_float_list(xs: Iterable[float]) -> np.ndarray:
    arr = np.asarray([float(x) for x in xs], dtype=float)
    arr = arr[np.isfinite(arr)]
    arr.sort()
    return arr


def load_reference(path: Path) -> np.ndarray:
    beats = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace(",", "\t").split()
        try:
            t = float(parts[0])
        except (ValueError, IndexError):
            continue
        # ASAP annotation files: keep beat/downbeat rows, ignore other labels.
        if len(parts) >= 3:
            label = parts[2].split(",")[0]
            if label not in {"b", "db"}:
                continue
        beats.append(t)
    return _as_float_list(beats)


def load_estimate(path: Path, mode: str) -> tuple[np.ndarray, dict]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if mode == "b1":
        candidates = [
            obj.get("tactus_s"),
            obj.get("single_tactus_s"),
            obj.get("beats_s"),
        ]
    else:
        candidates = [obj.get("beats_s")]
    xs = next((x for x in candidates if isinstance(x, list) and x), [])
    return _as_float_list(xs), obj


def metrical_level_gap(metrics: dict) -> float:
    return float(metrics.get("Any Metric Level Total", np.nan) - metrics.get("Correct Metric Level Total", np.nan))


def count_spurious_level_switches(obj: dict) -> int | None:
    # Compatible with known HookLab summary variants. If no level trace exists,
    # return None rather than infer it from tempo alone.
    trace = obj.get("tactus_level_trace") or obj.get("pulse_level_trace")
    if not isinstance(trace, list) or len(trace) < 2:
        return None
    labels = []
    for x in trace:
        if isinstance(x, dict):
            labels.append(x.get("level") or x.get("selected_level"))
        else:
            labels.append(str(x))
    labels = [x for x in labels if x in {"T", "2T", "3T"}]
    return sum(a != b for a, b in zip(labels, labels[1:]))


def evaluate(reference: np.ndarray, estimate: np.ndarray, obj: dict) -> dict:
    if len(reference) < 2:
        raise ValueError("La referencia contiene menos de dos beats válidos.")
    if len(estimate) < 2:
        raise ValueError("La estimación contiene menos de dos beats válidos.")

    ref, est = mir_eval.beat.trim_beats(reference), mir_eval.beat.trim_beats(estimate)
    scores = mir_eval.beat.evaluate(ref, est)

    # Nombres de mir_eval preservados para trazabilidad con la literatura/MIREX.
    out = {k: float(v) for k, v in scores.items()}
    out["HookLab_BNM_AMLt_minus_CMLt"] = metrical_level_gap(scores)
    out["HookLab_spurious_T_2T_3T_switches"] = count_spurious_level_switches(obj)
    out["reference_beat_count"] = int(len(ref))
    out["estimate_beat_count"] = int(len(est))
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--reference", required=True, type=Path)
    p.add_argument("--estimate", required=True, type=Path)
    p.add_argument("--mode", choices=["b0", "b1"], required=True)
    p.add_argument("--output", type=Path)
    args = p.parse_args()

    reference = load_reference(args.reference)
    estimate, obj = load_estimate(args.estimate, args.mode)
    result = {
        "schema": "HookLab-TIME-beat-tactus-eval-v0.1",
        "mode": args.mode,
        "reference": str(args.reference),
        "estimate": str(args.estimate),
        "metrics": evaluate(reference, estimate, obj),
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
