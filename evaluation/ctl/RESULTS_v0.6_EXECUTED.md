# CTL v0.6 — executed regression/noise stress

## Deterministic MB01–MB04
Using the pre-specified microbenchmark reference event sequences:
- MB01 constant 120: 0 discontinuities — PASS.
- MB02 accelerando 80→140: 0 discontinuities — PASS.
- MB03 ritardando 140→70: 0 discontinuities — PASS.
- MB04 abrupt 120→80: 1 discontinuity — PASS, but v0.6 reports it at 21.0 s because two changed inter-event intervals are required.

Thus v0.6 improves robustness but loses the near-boundary localization of v0.5 if the reported timestamp is the end of the first changed interval.

## Monte Carlo timing-jitter stress (1000 runs per sigma per case)
Gaussian independent event-time jitter was added before detection.

- sigma 3 ms: MB01/02/03 false discontinuity runs = 0/1000 each; MB04 correct single-discontinuity runs = 1000/1000. Mean MB04 detection ≈20.99997 s.
- sigma 5 ms: MB01/02/03 false discontinuity runs = 0/1000 each; MB04 correct = 1000/1000. Mean MB04 detection ≈21.0083 s.
- sigma 10 ms: MB03 false discontinuity runs = 1/1000; MB04 correct = 953/1000. Mean successful detection ≈21.1876 s.
- sigma 20 ms: MB01/02/03 false-discontinuity runs = 1/6/23 per 1000; MB04 correct = 619/1000.

## Correction derived from execution
The robust detector can confirm a new regime only after observing later intervals, but the structural change point can be localized retrospectively to the *start* of the first confirmed changed interval. This is not zero-latency online detection: it separates `localized_t` from `confirmed_t`.

A corrected v0.7 therefore must export both timestamps. On clean MB04 events this gives `localized_t=20.25 s`; confirmation necessarily occurs later because the first event at 20.25 s is also compatible with continuation of the old 120-BPM clock.

## Decision
v0.6 is not integrated as final CTL. Preserve its robust median/MAD gate, but correct timestamp semantics in v0.7. Do not claim causal detection at 20.25 s; claim retrospective localization at 20.25 s after subsequent confirmation.