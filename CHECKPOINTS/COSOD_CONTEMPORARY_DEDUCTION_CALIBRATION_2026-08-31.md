# CoSoD contemporary evidence-to-deduction calibration checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
State: `CONTEMPORARY_CALIBRATION_OBSERVED / 331 AUTHORIZED ROWS / NO GENERATIVE RULE PROMOTED`

## Provider and admissibility
CoSoD is a CC0 dataset of 331 multi-artist collaborations appearing on Billboard Hot 100 Year-End charts from 2010 through 2019. Its documented analytical schema contains formal-section timestamps plus vocal pitch statistics and production annotations. All 331 metadata rows and all 331 analysis identities resolved and joined in the observed run.

Observed controlled run: `33413625906`
Artifact: `9766118491`
Digest: `sha256:9249be0172c3bc5ed40bfc0c85a7f9b1f1fefcaf2466b9a91d5f110ada3cf3e7`

## Falsification-oriented result: chorus timing
First chorus onset did not meet the exploratory association gate for Year-End chart strength:
- absolute first-chorus onset: n=330, rho=.0948, BH q=.1576.
- controlled for year + collaboration-type/gender: partial rho=.0748, p=.1755.
- first-chorus onset / last annotated section start: n=330, rho=.0922, BH q=.1576.

Together with the independent McGill historical calibration, this provides cross-cohort evidence against promoting a universal HookLab rule that an earlier chorus implies greater chart success. It does not establish that chorus timing is irrelevant in every contemporary, genre-specific, platform-specific or experimental population.

## Exploratory vocal result
`aggregate_vocal_pitch_span_hz` showed a small association with stronger Year-End position:
- n=329, rho=.1745, BH q=.00743.
- after year + collaboration-type/gender controls: partial rho=.1834, p=.000829.

This is registered only as `INTERPRETATION_CANDIDATE`. It is NOT a melodic-range rule: the feature spans provider-reported vocal pitch statistics across sections and potentially multiple performers. Genre/style, exposure, artist history, performer count/register mixture, production and other confounds remain.

## Feature-semantic correction
The schema audit confirmed the exact CoSoD columns: Pitch min, Pitch Q1, Pitch median, Pitch Q3 and Pitch max. The observed pitch association is therefore not a column-selection artifact. The implementation now explicitly names the feature `aggregate_vocal_pitch_span_hz` and labels the ratio to the last annotated section start as an annotated-timeline ratio rather than true song-duration proportion.

## Theoretical matching boundary
Peer-reviewed experimental literature supports the general proposition that vocal presence and F0-related variation can carry perceptual/emotional information and influence perceived arousal. That literature does not demonstrate that a larger aggregate pitch span causes commercial success. Theory therefore provides plausibility for further investigation, not promotion.

## Epistemic result
The evidence-to-creative deduction architecture has now passed two observed-data calibrations:
1. historical Billboard structural/harmonic evidence;
2. contemporary Billboard collaboration structural/vocal evidence.

It has also demonstrated non-promotion: a plausible industry-style early-chorus rule was not accepted when two observed cohorts failed to support it.

## Current readiness
Readiness estimates, not effect sizes:
- evidence-to-deduction conceptual framework: 100%
- fail-closed code: 100%
- observed historical calibration: 100%
- observed contemporary subpopulation calibration: 100%
- cross-cohort non-promotion test: 100%
- candidate positive-hypothesis interpretation: ~45% (association + partial controls + partial theory plausibility; independent replication/stronger confound control absent)
- MIDI promotion for D001: 0% and correctly blocked.
- overall project readiness estimate: ~89%.

## Next gate
Build a normalized vocal-variability feature suitable for musical interpretation (prefer semitone/log-frequency scale and performer-aware aggregation), test whether the CoSoD association survives that correction, and seek independent authorized replication. In parallel continue mapping the 300-song contemporary outcome frame to licensed musical evidence. No MIDI should be generated from D001 until these gates pass.
