# Phase Restart v0.2 — stress execution

Date: 2026-08-20

Executed on deterministic MB06 and MB07 event streams with independent Gaussian timestamp jitter and single missed-post-event perturbations. 1000 Monte Carlo trials per condition/case.

## Clean
- MB06 correct CLOCK_STOP_RESTART: 1000/1000
- MB07 false CLOCK_STOP_RESTART: 0/1000

## Timestamp jitter
| jitter sigma | MB06 correct | MB07 false restart |
|---|---:|---:|
| 3 ms | 1000/1000 | 0/1000 |
| 5 ms | 1000/1000 | 0/1000 |
| 10 ms | 998/1000 | 1/1000 |
| 20 ms | 971/1000 | 18/1000 |

## One missed post-gap event
With one of the first five post-gap events removed, integer-multiple interval folding preserved same-tempo estimation. Across 1000 randomized removals:
- MB06 correct restart: 994/1000
- MB07 false restart: 3/1000

## Decision
v0.2 materially improves robustness over single-event phase decisions and is acceptable as an experimental controlled-evidence component through moderate timing noise. It is not yet validated on arbitrary audio-derived events.

## Regression boundary
No CTL v0.7 MB01–MB04 code changed. Clock-state semantics MB05 remain unchanged.

## Next mandatory gate
Run the combined CTL + clock/evidence + phase-restart pipeline using audio-derived events rather than reference `.beats`. Only after that may a mobile experimental integration be considered.