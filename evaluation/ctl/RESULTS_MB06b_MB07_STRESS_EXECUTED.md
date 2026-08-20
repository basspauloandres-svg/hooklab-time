# Executed stress — MB06b vs MB07

Date: 2026-08-20
Detector: `phase_restart_v0_2_robust.py`
Trials: 2,000 per condition, deterministic seed 20260820.

MB06b uses a fixed +0.25-cycle phase restart at the same 100 BPM. MB07 uses phase-compatible continuation at 105 BPM. Tests add Gaussian timing jitter and random post-gap event omission.

## Results summary

With no missing events:
- 0–20 ms jitter: MB06b detection = 100%; MB07 false restart = 0%.
- 30 ms jitter: MB06b detection = 99.75%; MB07 false restart = 0%.

With 10% random post-gap event omission:
- MB06b detection remained 99.1–99.65% across 0–30 ms jitter.
- MB07 false restart remained 0% across all tested jitter levels.
- most MB06b misses corresponded to insufficient retained post-gap events, not wrong continuation classification.

With 20% event omission:
- MB06b detection fell to approximately 93.7–95.2%, depending on jitter.
- MB07 false restart remained 0%.
- the dominant failure mode was insufficient evidence after missing events.

## Interpretation

The robust phase-consensus logic discriminates the corrected phase-restart case from continuous-clock attack dropout under moderate timing noise. Its principal remaining weakness is evidence scarcity when many post-gap events are missing. This should be handled as `UNCERTAIN/INSUFFICIENT_EVIDENCE`, not forced into continuation or restart.

## Decision

Phase Restart v0.2 passes the controlled MB06b/MB07 discrimination gate under moderate jitter and <=10% post-gap event loss. It is not yet validated on audio-derived mobile events. Original MB06 remains retained as an identifiability control rather than a restart-detection benchmark.
