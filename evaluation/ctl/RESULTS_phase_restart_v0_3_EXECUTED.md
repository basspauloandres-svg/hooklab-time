# Phase Restart v0.3 — executed stress results

Date: 2026-08-20

Executed the versioned `stress_phase_restart_v0_3.py` logic with deterministic seed `20260820`, 2,000 trials per condition, on MB06b (true phase restart) and MB07 (continuous clock). Conditions: timing jitter 0/5/10/20 ms and random post-gap event loss 0/10/20/30/40%.

## Main result
Across 80,000 total trials, **wrong binary decisions = 0**. Degradation under severe event loss is expressed as `UNCERTAIN`, not as a false restart/false continuation.

## Selected conditions

| Jitter | Loss | MB06b correct | MB06b uncertain | MB07 correct | MB07 uncertain | Wrong decisions |
|---:|---:|---:|---:|---:|---:|---:|
| 0 ms | 0% | 2000/2000 | 0 | 2000/2000 | 0 | 0 |
| 0 ms | 20% | 1999/2000 | 1 | 1997/2000 | 3 | 0 |
| 0 ms | 30% | 1984/2000 | 16 | 1981/2000 | 19 | 0 |
| 0 ms | 40% | 1900/2000 | 100 | 1923/2000 | 77 | 0 |
| 10 ms | 20% | 2000/2000 | 0 | 1999/2000 | 1 | 0 |
| 10 ms | 30% | 1975/2000 | 25 | 1978/2000 | 22 | 0 |
| 10 ms | 40% | 1909/2000 | 91 | 1893/2000 | 107 | 0 |
| 20 ms | 20% | 1985/2000 | 15 | 1996/2000 | 4 | 0 |
| 20 ms | 30% | 1947/2000 | 53 | 1975/2000 | 25 | 0 |
| 20 ms | 40% | 1843/2000 | 157 | 1905/2000 | 95 | 0 |

## Interpretation
The abstention state solves the previous forced-decision problem in this controlled stress test. Under clean/moderately noisy evidence the resolver retains very high correct classification. As evidence becomes sparse, it increasingly returns `UNCERTAIN` rather than producing an incorrect `CLOCK_STOP_RESTART` or `CLOCK_CONTINUES` decision.

## Boundary of evidence
This result validates the resolver on controlled event streams with simulated jitter/missing events. It does **not** yet validate the mobile audio front-end's ability to produce sufficiently reliable events or audio-activity evidence on arbitrary recordings.

## Next gate
Run MB05/MB06b/MB07 using audio-derived event/activity evidence only. Mobile integration remains blocked until this gate is passed.