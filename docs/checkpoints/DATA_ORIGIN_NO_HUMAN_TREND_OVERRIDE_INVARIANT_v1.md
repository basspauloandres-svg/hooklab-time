# HookLab/TIME-MIE — Data-Origin / No Human Trend Override Invariant v1

Date: 2026-09-01  
Status: `CANONICAL_SCIENTIFIC_INVARIANT`

## Rule

The existence, direction and magnitude of every empirical tendency must originate in the registered computation applied to the canonical data. Human judgment, literature, AI output and producer preference cannot create, reverse, strengthen, rescue or promote an empirical result.

Canonical order:

`DATA -> CALIBRATED MEASUREMENT -> REGISTERED STATISTICS -> EMPIRICAL RESULT -> THEORY INTERPRETATION -> GENERATION TEST -> PRODUCER DECISION`

## Human role boundary

Human participation is permitted for:

- construct definition before analysis;
- source and measurement-integrity review;
- annotation when the construct requires human observation;
- calibration and adjudication under a frozen codebook;
- preregistration of population, outcome, test, effect criterion, multiplicity, robustness and stopping rules;
- evaluation of generated realizations after the empirical result is closed.

Human participation cannot:

- set an expected empirical direction;
- select a test after viewing results;
- edit engine-computed effect estimates or uncertainty;
- convert a null, weak or unstable result into a positive rule;
- use aesthetic preference as evidence of a corpus tendency;
- promote a deduction outside the statistical engine.

Human annotation is treated as a measurement instrument. Its contribution is represented through provider/version, independent coding, reliability, error estimates and adjudication provenance. Annotation content cannot determine the direction of the later statistical result.

## Machine-enforced registration fields

Every analysis registration must include:

- `expected_direction=null`;
- `trend_origin_policy=REGISTERED_DATA_AND_STATISTICS_ONLY`;
- `human_trend_override_allowed=false`;
- `ai_trend_override_allowed=false`;
- `literature_sets_empirical_direction=false`;
- `producer_preference_used_as_evidence=false`.

Any violation yields `AUDIT_ANALYSIS_NOT_REGISTERED`.

## Machine-enforced result provenance

Promotion requires all of the following:

- `computation_origin=REGISTERED_STATISTICAL_ENGINE`;
- immutable analysis registration identifier;
- source revision and feature version;
- normalized input hash;
- engine version;
- `human_trend_override_applied=false`;
- `ai_trend_override_applied=false`;
- `literature_direction_applied=false`;
- `producer_preference_applied=false`.

Any missing or contradictory field yields `AUDIT` before effect, uncertainty, robustness or replication are considered.

## Interpretation boundary

Literature may interpret, contextualize or challenge the empirical result after computation. The producer may judge musical usefulness after generation. Neither layer modifies the statistical disposition stored by the engine.

## Current state

This invariant does not authorize analysis of the corpus. Feature Admissibility and Analysis Registration remain mandatory. At adoption, zero corpus statistical tests and zero conditioned deductions have been produced.
