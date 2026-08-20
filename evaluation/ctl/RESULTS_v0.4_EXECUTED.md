# CTL v0.4 — executed multiscale experiment

This file records an executed experiment, not a design proposal.

## Procedure
The MB01–MB04 stimuli were regenerated deterministically from the versioned `evaluation/microbenchmark/generate.py` specification. A higher-resolution onset stream was extracted directly from the generated waveform. Local tempo was estimated on a short ~2 s scale with 0.5 s evaluation spacing, while a longer ~6 s context was used to estimate the ongoing tempo slope. A candidate discontinuity required persistent short-scale departure from the long-scale trajectory; drifting long-scale contexts used stricter permission than stable contexts.

## Results
| Case | Expected | CTL v0.4 executed result |
|---|---|---|
| MB01 | stable 120, 0 discontinuities | 0 discontinuities — PASS |
| MB02 | continuous 80→140 drift, 0 discontinuities | 0 discontinuities — PASS |
| MB03 | continuous 140→70 drift, 0 discontinuities | 0 discontinuities — PASS |
| MB04 | one abrupt 120→80 change at ~20 s | 1 discontinuity at ~23.5 s — PARTIAL PASS |

## Comparison for MB04
- ground truth: ~20.0 s
- HookLab v1.7: 25.774 s (latency ~5.8 s)
- CTL v0.2/v0.3 diagnostic: ~29 s
- CTL v0.4 multiscale: ~23.5 s (latency ~3.5 s)

Thus v0.4 improves abrupt-change localization by about 2.3 s relative to the current mobile v1.7 result while preserving zero false discontinuities in MB01–MB03.

## Interpretation
The multiscale hypothesis is supported provisionally: long windows are useful for stable/drift context, while shorter evidence improves localization of an abrupt regime change. The remaining ~3.5 s latency is not considered solved.

## Decision
- Do not claim abrupt-change localization solved.
- Preserve v0.4 as the best Phase-A prototype so far.
- Do not tune thresholds specifically to force MB04 to 20 s.
- Next correction should target the remaining localization latency using event-level/phase evidence before mobile integration, while retaining the MB01–MB03 regression gate.
- Meter/downbeat/accent remain frozen.