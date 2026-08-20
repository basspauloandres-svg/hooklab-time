# CTL v0.5 — Executed results on MB01–MB04

Status: **executed offline correction**, not yet integrated into mobile HookLab.

## What changed
v0.5 moves abrupt-change localization to onset-event / inter-beat-interval (IBI) resolution. Long-window CTL remains conceptually responsible for STABLE/DRIFT context; this event-level detector only proposes abrupt discontinuities.

The test audio was regenerated deterministically from `evaluation/microbenchmark/generate.py`, and click/onset times were recovered from the rendered WAVs with a high-pass + short-envelope peak detector. Recovered onset timing error against the known synthetic beats was <~2.3 ms in MB01–MB04.

## Phase-A result
| Case | Expected discontinuities | CTL v0.5 | Result |
|---|---:|---:|---|
| MB01 constant 120 | 0 | 0 | PASS |
| MB02 accelerando 80→140 | 0 | 0 | PASS |
| MB03 ritardando 140→70 | 0 | 0 | PASS |
| MB04 abrupt 120→80 | 1 | 1 at 20.252 s | PASS |

Ground-truth change point in MB04 is defined at 20.0 s. The first post-change beat occurs at 20.25 s, so the event-level detector localizes the change at 20.252 s (about 0.25 s after the formal change point and essentially at the first observable beat of the new regime).

## Comparison
- HookLab v1.7: transition declared at 25.774 s (~5.8 s late).
- CTL v0.2/v0.3 diagnostic: ~29 s.
- CTL v0.4 multiscale-window prototype: ~23.5 s.
- **CTL v0.5 event-level: 20.252 s.**

## Robustness stress test (timing jitter)
200 Monte Carlo repetitions per condition were run by adding independent Gaussian timing jitter to the known onset sequence:

- 3 ms jitter: MB01/02/03 produced 0 false discontinuities in 200/200 runs; MB04 produced exactly 1 in 200/200, mean localization ~20.250 s.
- 5 ms jitter: same result as 3 ms.
- 10 ms jitter: MB01 and MB02 remained 0/200 false changes; MB03 produced 1 false-change run in 200; MB04 remained 1/200 in every run with mean localization ~20.249 s.
- 20 ms jitter: performance degraded substantially; therefore v0.5 is not yet considered robust enough for unconstrained real-audio integration without confidence gating.

## Interpretation
The latency problem in MB04 was largely caused by using long summary windows to localize a discrete event. Event-level IBI evidence can localize the abrupt change near the first observable beat while leaving gradual accelerando/ritardando intact in this controlled benchmark.

## Decision
**Phase-A controlled gate MB01–MB04 is passed by v0.5 under clean/small-jitter onset evidence.**

Mobile integration remains blocked until event confidence / reliability gating is added, because the 20 ms jitter stress test reveals vulnerability to noisy onset timing.

## Next correction
Add confidence gating and agreement with long-scale CTL so event-level change points are accepted only when:
1. onset timing is reliable;
2. two or more new-regime intervals agree;
3. long-scale trajectory does not already explain the observations as DRIFT;
4. no regression appears on MB01–MB04 under jitter/noise stress.
