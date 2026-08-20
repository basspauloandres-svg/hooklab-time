# HookLab TIME — Continuous Tempo Layer (CTL) SPEC v0.1

Status: **pre-implementation specification**. Metric/downbeat/accent layer remains frozen.

## Purpose
Replace the current assumption `one pulse run ≈ one tempo` with a continuous temporal trajectory capable of representing stable tempo, gradual drift and true discontinuities without solving perceptual tactus-level ambiguity yet.

## Scope
Phase A addresses MB01–MB04 only. MB05–MB07 clock/evidence semantics and MB08 tactus-level selection are explicitly out of scope.

## Inputs
At each analysis step, CTL receives local observations from independent evidence sources:
- Beat This beat-event evidence;
- time-domain onset periodicity evidence;
- observation confidence / periodicity;
- timestamp and local window support.

Neither Beat This nor onset evidence has permanent authority.

## State variables
For time t, CTL maintains:
- `tempo_bpm(t)` — local tempo trajectory;
- `phase(t)` — predicted beat phase;
- `confidence(t)` — confidence in the active trajectory;
- `tempo_slope(t)` — local derivative / trend;
- `mode(t)` — `SEARCH | LOCK | TRACK | RE_EVALUATE`;
- `tempo_state(t)` — `STABLE | DRIFT_UP | DRIFT_DOWN | DISCONTINUITY`.

## Core behavior
### SEARCH
Generate plausible local temporal hypotheses from available evidence. Do not select T/2T/3T perceptual level here.

### LOCK
Require persistence across multiple observations before accepting a trajectory. A single local peak cannot establish a new regime.

### TRACK
Predict the next tempo/phase from trajectory history. Compatible observations update the trajectory. Gradual coherent changes alter `tempo_slope` and become DRIFT rather than new runs.

### RE_EVALUATE
Enter only after persistent prediction error. Competing hypotheses are reconsidered. A discontinuity is emitted only when a new trajectory explains evidence materially better than continuation of the current trajectory.

## Tempo-state semantics
- `STABLE`: slope is small relative to local uncertainty.
- `DRIFT_UP`: sustained positive slope with coherent phase evolution.
- `DRIFT_DOWN`: sustained negative slope with coherent phase evolution.
- `DISCONTINUITY`: observations cannot be plausibly explained by continuation/drift of the previous trajectory.

Thresholds are not song-specific and are not fixed here before pilot distributions are observed.

## Outputs
CTL must export:
- `tempo_curve`: timestamp, bpm;
- `phase_curve`;
- `confidence_curve`;
- `tempo_state_segments`;
- `discontinuities`;
- `evidence_trace`: source observations and confidence;
- `rejected_hypotheses`: alternatives and rejection reason;
- `ctl_version`.

## Acceptance tests fixed before coding
### MB01 — constant 120 BPM
Expected: one trajectory, STABLE, zero discontinuities, no regression relative to v1.7.

### MB02 — linear accelerando 80→140 BPM
Expected: one coherent increasing trajectory, predominantly DRIFT_UP; no discontinuities caused solely by accelerando.

### MB03 — linear ritardando 140→70 BPM
Expected: one coherent decreasing trajectory, predominantly DRIFT_DOWN; no discontinuities caused solely by ritardando.

### MB04 — abrupt 120→80 BPM at ~20 s
Expected: STABLE → one DISCONTINUITY → STABLE; retain correct pre/post tempo levels and improve transition latency relative to v1.7 (~5.8 s) without introducing false discontinuities in MB01–MB03.

## Explicit non-goals
- Do not solve 90 vs 180 BPM perceptual tactus selection (MB08).
- Do not decide meter, downbeat or accent.
- Do not classify silence vs fermata vs attack dropout yet (MB05–MB07).
- Do not use song-specific parameters.
- Do not use a hard rule such as `BPM > X => divide by 2`.

## Regression rule
A CTL change is rejected if it improves MB02/MB03/MB04 while degrading MB01 or creating new discontinuities in previously passing conditions.

## Comparison design
Run the same generated audio through:
- `B1-current`: HookLab v1.7 behavior;
- `B1-CTL`: identical upstream evidence + CTL enabled.

No metric/downbeat information may influence either output.

## Next implementation step
Implement CTL as an isolated module with an enable/disable switch and deterministic JSON trace. First prototype should favor auditability over parameter optimization.