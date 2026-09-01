# First Sample Collection Protocol v1.0

## Purpose
Build the first empirical HookLab/TIME sample with enough heterogeneity and cohort density to support descriptive reference models and later inferential work, without per-song tuning.

## Frozen rules
1. Analyzer parameters remain GLOBAL_FROZEN across songs.
2. Genre/style metadata route cohorts; they never encode desirability or success.
3. Only strict-gate PASS songs enter Matrix X.
4. Failed songs remain in the audit log and count toward generalization diagnostics.
5. No imputation, manual feature weighting, success scoring, or feature ranking is permitted during sample construction.
6. Audio may be used ephemerally; only derived evidence is retained when source policy requires non-persistence.
7. Documentary text provenance remains separate from acoustic timing evidence.

## Operational growth checkpoints
- 0–29 strict PASS: pilot diversification.
- 30–59 strict PASS: cohort densification.
- 60–99 strict PASS: reference stabilization.
- 100+ strict PASS: adaptive stopping review.

These are engineering checkpoints, not statistical power claims.

## Diversity targets for Sample 1
- at least 5 genres;
- at least 10 styles;
- target at least 10 strict-PASS songs in each primary cohort where source availability permits;
- retain variation in recording era, vocal configuration, production density and language when documentary sources permit.

## Adaptive stopping
At N >= 100, compare successive Matrix X snapshots with `distribution_stability.py`. Collection continues while key feature distributions or principal cohort references materially change. A Sample 1 freeze requires documented stability diagnostics plus adequate cohort coverage. Stability is descriptive evidence only and does not by itself establish representativeness.

## Output chain
real sources -> Analyzer -> strict gate -> structural fingerprint -> genre/style cohort -> Matrix X -> cohort reference -> stability diagnostics -> Sample 1 freeze
