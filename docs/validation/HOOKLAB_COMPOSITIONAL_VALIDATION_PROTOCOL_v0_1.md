# HookLab Compositional Validation Protocol v0.1

Status: PRE-REGISTERED PILOT DESIGN
Date: 2026-09-01
Branch: main

## Objective
Evaluate whether HookLab improves the compositional process and/or the resulting hook relative to two comparison conditions, without treating producer preference as evidence of commercial success or causal population-level effectiveness.

## Primary research question
Under matched creative briefs and time constraints, does HookLab-assisted composition improve hook-level outcomes and process efficiency compared with unassisted composition and general-purpose AI assistance?

## Conditions
A. HUMAN_ONLY — composer/producer works without HookLab or generative AI.
B. GENERAL_AI — composer/producer may use a general-purpose language/generative assistant, without HookLab's reference-analysis, multimodal traceability or D0 realization pipeline.
C. HOOKLAB — composer/producer uses the current HookLab Producer Interface v0.6 and its D0 exploratory multimodal workflow.

## Unit of analysis
One completed hook candidate produced for one standardized creative brief under one condition.

## Pilot scope
- 6 creative briefs.
- Each brief completed once in each of the three conditions.
- Target pilot corpus: 18 hook candidates.
- Same target duration per session: 20 minutes maximum.
- Order of conditions randomized by brief where feasible.

This pilot is intended to test feasibility, measurement reliability and effect-size direction. It is not powered as a definitive confirmatory trial.

## Standardized output per candidate
Each condition must deliver:
- hook text;
- sung/melodic line represented in MIDI or equivalent symbolic form;
- beat/tempo context;
- audio rendering where available;
- elapsed time;
- number of substantive iterations;
- final producer self-rating and decision;
- provenance identifying condition, brief and version.

## Primary outcomes
### Process outcomes
1. TIME_TO_ACCEPTABLE_HOOK_MIN — elapsed minutes until producer declares a candidate acceptable.
2. ITERATION_COUNT — number of substantive revisions before acceptance or timeout.
3. COMPLETION_WITHIN_20_MIN — binary completion outcome.

### Blind expert-rated hook outcomes
Each rated on a 1–7 anchored scale:
1. HOOK_MEMORABILITY
2. TEXT_MELODY_FIT
3. PROSODIC_NATURALNESS
4. MELODIC_COHERENCE
5. RHYTHMIC_FIT_TO_BEAT
6. SINGABILITY
7. LYRICAL_COHERENCE
8. PERCEIVED_ORIGINALITY
9. OVERALL_HOOK_EFFECTIVENESS

## Secondary outcomes
- producer confidence in final candidate;
- proportion ACCEPT / MODIFY / REJECT;
- disagreement between producer and blind raters;
- candidate diversity within HookLab sessions when multiple alternatives are generated.

## Blinding
Blind raters must not be told which condition generated each candidate. Candidate labels must be randomized and stripped of system/tool identifiers.

## Raters
Pilot target:
- >=3 expert raters with composition/production experience.
- A later listener study may add non-expert listeners and delayed recall/memorability tasks.

## Evaluation sequence
1. Same brief distributed across A/B/C.
2. Session timer starts at first compositional action.
3. Condition-specific workflow is followed.
4. Producer freezes one final candidate or reaches timeout.
5. Artifacts are normalized for blind review.
6. Expert raters score each candidate independently.
7. Inter-rater reliability is estimated before interpreting mean ratings.
8. Effect sizes and uncertainty are reported before significance testing.

## Analysis plan — pilot
The pilot remains estimation-first.

For continuous/ordinal ratings:
- report per-condition median, IQR and mean/SD where informative;
- estimate paired within-brief contrasts C-A, C-B and B-A;
- report bootstrap confidence intervals for mean/median paired differences where feasible;
- use non-parametric paired tests only as secondary evidence because N=6 briefs is small.

For process outcomes:
- compare elapsed time and iteration counts within briefs;
- report completion proportions descriptively;
- do not infer population superiority from the pilot alone.

For rater reliability:
- estimate ICC for aggregated continuous ratings when assumptions are adequate;
- otherwise report rank/order agreement and item-level dispersion.

Multiplicity:
- OVERALL_HOOK_EFFECTIVENESS is the primary perceptual outcome for the pilot.
- TIME_TO_ACCEPTABLE_HOOK_MIN is the primary process outcome.
- Other perceptual dimensions are diagnostic secondary outcomes.
- No claim of broad superiority may be made from isolated secondary p-values.

## Interpretation contract
Every result must terminate as:
DATA_SAYS → STATISTICS_SAY → THEORY_SAYS → GENERATION_TESTS → PRODUCER_DECIDES.

The trial must distinguish:
- process improvement;
- perceptual quality improvement;
- producer preference;
- population-level success claims.

Commercial success, virality and causal audience response are outside the inferential scope of this pilot.

## HookLab scientific boundary
- D0_EXPLORATORY != SCIENTIFIC_D.
- HookLab may improve workflow even if no population-level conditioned deduction is promoted.
- A null or mixed result is a valid scientific result.
- No scoring rubric may be modified after seeing condition results without being labeled POST_HOC.

## Pilot success criteria
The pilot is considered operationally successful if:
1. >=90% of planned sessions produce complete provenance;
2. >=80% of blind rating forms are complete;
3. at least 2/3 expert raters show usable agreement on the primary perceptual outcome;
4. primary process and perceptual outcomes can be calculated without reconstructing missing data;
5. no condition identity leaks into blind review.

Evidence of HookLab benefit is considered promising, not confirmatory, if the direction of effect favors HookLab on BOTH:
- OVERALL_HOOK_EFFECTIVENESS; and
- TIME_TO_ACCEPTABLE_HOOK_MIN or ITERATION_COUNT,
with effect estimates and uncertainty reported.

## Version lock
HookLab condition uses Producer Interface v0.6 release commit:
`a47406d860c6acdde650ce368803714a5194c44a`

Any code change during the pilot creates a new software version and must be recorded before additional sessions.
