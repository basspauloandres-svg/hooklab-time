# CTL v0.1 — offline test on real HookLab evidence

Input source: the already exported HookLab-Mobile-BeatThis-v1.7 JSON summaries for MB01–MB04. No audio was reprocessed and no HookLab parameters were changed.

Extraction rule for this diagnostic pass: midpoint of each `rhythmic_state_segment`; prefer `onset_bpm` with `onset_periodicity` as confidence when available; use beat evidence only when onset BPM is unavailable. This is a diagnostic extraction rule, not a final fusion policy.

## Results

| Case | CTL v0.1 result | Interpretation |
|---|---|---|
| MB01 | ~119.73→119.73 BPM; 16 STABLE; 0 discontinuities | PASS: no regression on constant tempo. |
| MB02 | ~84.91→137.92 BPM; 18 DRIFT_UP, 2 STABLE; 0 discontinuities | PROMISING/PASS structural: converts the evidence into one increasing trajectory instead of five runs. |
| MB03 | ~134.53 BPM downward; predominantly DRIFT_DOWN; 0 discontinuities | PROMISING but extraction contaminated at final segment because onset BPM becomes null and fallback beat evidence is at a different metrical level. Do not interpret final ~90.42 BPM as ground-truth endpoint performance. |
| MB04 | ~119.73 BPM then gradual DRIFT_DOWN; 0 discontinuities | FAIL: CTL v0.1 smooths the true 120→80 jump instead of declaring a discontinuity. |

## Main inference
CTL v0.1 demonstrates that a continuous trajectory representation can eliminate the spurious run fragmentation seen in MB02/MB03 without breaking MB01. However, the same smoothing mechanism currently absorbs MB04's true abrupt change as drift. Therefore CTL v0.1 is **not eligible for mobile integration**.

## Required next change
Do not tune a song-specific threshold. Introduce a discontinuity test based on persistent model mismatch relative to the expected local slope/uncertainty, while preserving gradual drift. Evidence fusion must also keep Beat This and onset observations as parallel hypotheses rather than switching to beat evidence merely because onset BPM is null.

## Decision
- MB01 gate: pass.
- MB02 gate: structural pass/promising.
- MB03 gate: structural pass/promising, endpoint not interpretable under current extraction rule.
- MB04 gate: fail.
- Integration into HookLab app: **blocked** until MB04 is resolved without regression in MB01–MB03.
