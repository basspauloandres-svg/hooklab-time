# CTL v0.4 — Multiscale Evidence Specification

Status: pre-implementation experiment. No mobile integration.

## Problem isolated by v0.1–v0.3
Long local windows support robust STABLE/DRIFT classification but smear abrupt tempo changes. In MB04 the true change occurs at ~20 s; 6 s windows stepped every 2 s mix pre/post-change evidence and delay change-point localization.

## Hypothesis
Use two temporal resolutions with different responsibilities rather than lowering a single threshold:

- **Long scale**: robust trajectory context and STABLE/DRIFT classification.
- **Short scale**: localize candidate discontinuities.

A short-scale candidate cannot independently redefine the trajectory. It only proposes a change point. The long-scale model must confirm that the post-change observations form a coherent regime incompatible with continuation.

## Proposed scales
These are experimental design values, not validated scientific constants:
- long context: preserve current 6 s / 2 s-step evidence for comparability;
- short evidence: derive higher-resolution local tempo evidence from the same audio/onset representation, initially targeting ~2 s windows with denser stepping.

No song-specific tuning is allowed.

## Decision logic
1. Long-scale model estimates trajectory and state: STABLE / DRIFT_UP / DRIFT_DOWN.
2. Short-scale stream computes local tempo observations and confidence.
3. A candidate change point is raised when short-scale evidence departs persistently from the long-scale prediction.
4. Confirmation requires a coherent post-candidate regime and better explanatory fit than continuation.
5. If long-scale state is DRIFT, stronger evidence is required than when it is STABLE.
6. The accepted timestamp is the earliest supported short-scale candidate, not the center/end of a later long window.

## Phase-A acceptance gate
- MB01: 0 false discontinuities.
- MB02: 0 false discontinuities; one continuous DRIFT_UP trajectory.
- MB03: 0 false discontinuities; one continuous DRIFT_DOWN trajectory.
- MB04: exactly 1 discontinuity; localization must improve over v1.7 (~25.774 s) and v0.2/v0.3 (~29 s) without regression in MB01–MB03.

## Required trace
Export for every candidate:
- short-window start/end/center;
- local bpm and confidence;
- long-scale predicted bpm and slope;
- mismatch;
- candidate persistence;
- confirmation score;
- accepted/rejected reason.

## Non-goals
No tactus octave resolution, meter/downbeat/accent, silence/fermata semantics, or MB05–MB08 optimization.

## Falsification condition
If higher temporal resolution fails to improve MB04 localization without creating false changes in MB01–MB03, reject the multiscale hypothesis and move to a more formal state-space/change-point formulation rather than further threshold tuning.