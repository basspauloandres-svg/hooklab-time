# MB06 phase audit — critical benchmark finding

Date: 2026-08-20

## Executed check
`phase_restart_v0_2_robust.py` was stress-tested against the actual deterministic MB06 event construction, not the prose description.

## Finding
The existing MB06 generator uses:
- pre-gap tempo: 100 BPM (IBI = 0.600 s)
- last pre-gap reference beat: 11.650 s
- first post-gap reference beat: 15.250 s

Difference: 15.250 - 11.650 = 3.600 s = exactly 6 × 0.600 s.

Therefore the post-gap clock is **phase-compatible with uninterrupted extrapolation**. The current MB06 stimulus does not contain the phase restart that its intended semantics claimed.

## Consequence
A phase-only observable detector cannot distinguish current MB06 from a long attack dropout with the same continued phase. In the executed stress harness, MB06 restart detection was 0/1000 even with zero jitter and zero missing events, while MB07 continuation was correctly rejected as restart 1000/1000. This is not evidence that the detector failed to observe an existing phase shift; the benchmark itself contains no phase shift.

## Methodological decision
Do not tune the detector to force MB06 to pass. Mark the previous MB06 `CLOCK_STOP_RESTART` PASS as invalid because it depended on supplied ground-truth semantics rather than an observable phase difference.

Preserve original MB06 unchanged for provenance. Create a new corrected condition (MB06b) with an explicitly non-integer phase restart and pre-register its exact ground truth before testing. The original MB06 remains useful as an identifiability control: from event timing alone, a stopped clock that restarts on the extrapolated phase is observationally indistinguishable from a continuous hidden clock.

## Status correction
- MB05: controlled silence semantics remains valid.
- MB06 original: **benchmark semantic mismatch discovered; automatic clock-stop identification NOT solved.**
- MB07: continuation semantics remains valid.

This finding supersedes any earlier statement that original MB06 had demonstrated an observable new phase.