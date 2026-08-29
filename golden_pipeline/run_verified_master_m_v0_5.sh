#!/usr/bin/env bash
set -euo pipefail

# Controlled M-only preparation from the verified full master.
# H and T are never recomputed by this script.

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 FULL_MASTER.mp3 OUTPUT_DIR" >&2
  exit 2
fi

MASTER="$1"
OUT="$2"
EXPECTED_MASTER_SHA="23fbd8c816f59f21802c2fd4b91f48a315c2006a023992430ca10d8654264fb2"
EXPECTED_WINDOW_SHA="854fc7c62c05745cb1da5d7073d8c2b848152b3d6a7762ca103a54706e36a342"

mkdir -p "$OUT/input" "$OUT/stems" "$OUT/probe"

MASTER_SHA=$(sha256sum "$MASTER" | awk '{print $1}')
if [[ "$MASTER_SHA" != "$EXPECTED_MASTER_SHA" ]]; then
  echo "REFUSED: full-master SHA mismatch: $MASTER_SHA" >&2
  exit 3
fi

ffmpeg -y -ss 13.3 -to 40.7 -i "$MASTER" -ar 44100 -ac 2 "$OUT/input/golden_source_window.wav"
WINDOW_SHA=$(sha256sum "$OUT/input/golden_source_window.wav" | awk '{print $1}')
if [[ "$WINDOW_SHA" != "$EXPECTED_WINDOW_SHA" ]]; then
  echo "REFUSED: deterministic source-window SHA mismatch: $WINDOW_SHA" >&2
  exit 4
fi

DEMUCS_ARGS=(-n htdemucs --two-stems=vocals -o "$OUT/stems")
if [[ -n "${DEMUCS_REPO:-}" ]]; then
  DEMUCS_ARGS+=(--repo "$DEMUCS_REPO")
fi
TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 python -m demucs "${DEMUCS_ARGS[@]}" "$OUT/input/golden_source_window.wav"
VOCALS=$(find "$OUT/stems" -type f -name vocals.wav -print -quit)
if [[ -z "$VOCALS" ]]; then
  echo "REFUSED: HTDemucs vocals stem not found" >&2
  exit 5
fi

python mie_core/run_structural_probe.py \
  --vocal "$VOCALS" \
  --output "$OUT/probe"

python mie_core/evaluate_m_gate.py "$OUT/probe/MIE_STRUCTURAL_PROBE_v0_4.json"

echo "Verified source-window M probe completed. H/T remain frozen; no audible substitution rendered."
