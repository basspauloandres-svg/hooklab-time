# Statistical Analysis No-Reprocess Invariant v1

Status: CANONICAL
Branch: `mie/golden-forensic-v0.3`
Purpose: prevent future chats/agents from reopening resolved statistical design or mining arbitrary columns for publishable-looking associations.

## Mandatory startup order
Before any new statistical analysis, read in this order:
1. `CHECKPOINTS/MIGRATION_CHECKPOINT_2026-08-31_v1.md`
2. `docs/checkpoints/START_NEXT_CHAT_STATISTICAL_DEDUCTION_ANALYSIS_v1.txt`
3. this file.

Do not begin analysis until these three artifacts have been integrated.

## NO-REPROCESS RULE
The next chat/agent MUST NOT:
- redesign the statistical philosophy;
- revert from deduction to hit prediction;
- re-run already closed hypothesis families merely to search for significance;
- change thresholds after observing results;
- treat all numeric columns as admissible features;
- promote a correlation because it is statistically significant;
- reinterpret an already NO_PROMOTION result as positive without genuinely new evidence;
- merge provider ontologies without demonstrated concordance;
- treat M300 discovery rows as if every row contained scientifically eligible musical evidence.

A closed hypothesis may be reopened only when `NEW_EVIDENCE=true` and the new evidence is explicitly identified (new qualified population, independent provider, corrected representation, preregistered alternative operationalization, or independent replication). Reopening must receive a new ANALYSIS_ID and preserve the previous result.

## FEATURE ADMISSIBILITY GATE — REQUIRED BEFORE STATISTICAL TESTING
No variable/column may enter inferential analysis until a Feature Admissibility Record exists with all mandatory fields below.

`FEATURE_ID`
`CONSTRUCT_NAME` — musical/contextual phenomenon the feature purports to represent.
`ANALYTICAL_LAYER` — OUTCOME | EXPOSURE | CONTEXT | MUSICAL | TEXT_PROSODY | GENRE_STYLE | AUDIENCE.
`OPERATIONAL_DEFINITION` — exact mathematical/observational definition.
`UNIT_SCALE` — seconds, semitones, proportion, count, rank, etc.
`SOURCE_PROVIDER`
`SOURCE_VERSION`
`VERSION_IDENTITY_STATUS`
`MEASUREMENT_PROCEDURE`
`MEASUREMENT_ERROR_OR_UNCERTAINTY`
`REPRESENTATION_CALIBRATION_STATUS` — required for F0/note-derived melody features.
`MUSICAL_OR_THEORETICAL_RELEVANCE` — why this construct can answer the stated research question.
`PREDECLARED_QUESTION`
`PREDECLARED_DIRECTION_OR_TWO_SIDED`
`OUTCOME_TO_BE_TESTED`
`POPULATION_SCOPE`
`KNOWN_CONFOUNDERS`
`FORBIDDEN_INTERPRETATIONS`
`PROVENANCE`
`ADMISSIBILITY_DECISION` — ADMIT | AUDIT | REJECT.

If any mandatory field is missing -> `AUDIT_FEATURE_NOT_DEFINED` and the feature cannot enter inferential testing.

## WHY THIS EXISTS
A machine can calculate associations between arbitrary columns. That does not make those associations meaningful musical evidence. The gate prevents statements analogous to “feature X must occur at minute Y” from emerging merely because an unplanned numerical relationship appears in a matrix.

Examples already observed in HookLab:
- early-chorus timing appeared plausible as an industry claim but did not survive promotion across the executed cohorts;
- aggregate vocal pitch span showed a preliminary association in raw Hz, then disappeared when represented more appropriately in semitones and controlled. The raw association therefore cannot be promoted.

## ANALYSIS REGISTRATION GATE
Before computing inferential statistics, create:
`ANALYSIS_ID`
`RESEARCH_QUESTION`
`POPULATION_SCOPE`
`OUTCOME`
`ADMISSIBLE_FEATURE_IDS`
`PRIMARY_TESTS`
`SECONDARY_TESTS`
`COVARIATES`
`MULTIPLICITY_FAMILY`
`EFFECT_SIZE_CRITERION`
`UNCERTAINTY_REPORTING`
`ROBUSTNESS_PLAN`
`REPLICATION_REQUIREMENT`
`STOP/PROMOTION_RULE`.

Exploratory analyses must be labelled `EXPLORATORY`. Results discovered during exploration cannot silently become confirmatory; they require a new independent confirmatory analysis/replication.

## PROMOTION RULE
A result can be considered for `PROMOTE_TO_CONDITIONED_DEDUCTION` only if:
- feature = ADMIT;
- population/outcome were explicit;
- representation is calibrated where required;
- statistical gate is passed without post-hoc threshold changes;
- multiplicity is controlled;
- effect size is musically interpretable;
- relevant confounders/alternative explanations are documented;
- robustness is satisfactory;
- replication requirement is satisfied or the result remains HOLD_FOR_REPLICATION;
- theoretical interpretation is supported by verifiable scientific literature;
- provenance is complete.

Otherwise: `NO_PROMOTION` or `AUDIT`.

## CLOSED / NON-PROMOTED FAMILIES AT THIS CHECKPOINT
Do not reprocess without NEW_EVIDENCE:
1. universal early-chorus timing -> NO_PROMOTION under tested cohorts;
2. tested formal repetition/architecture variables in M300×CoSoD -> NO_PROMOTION;
3. raw aggregate vocal pitch-span association -> NO_PROMOTION after semitone normalization/controls.

These do not mean universal irrelevance. They mean the current evidence does not justify a HookLab creative rule.

## REQUIRED OUTPUT SEPARATION
Every analysis must end with five separate statements:
`DATA_SAYS:` observed measurements only.
`STATISTICS_SAY:` statistical relationships, effect/uncertainty and scope only.
`THEORY_SAYS:` literature-supported interpretation and competing explanations.
`GENERATION_TESTS:` only deductions actually eligible for musical realization.
`PRODUCER_DECIDES:` human creative evaluation; never back-projected as proof of market success.

## MIGRATION COMMAND
If a future chat is asked to “continue the statistics”, it must continue from the first unresolved registered analysis/gate. It must not restart from raw M300 columns or rediscover previously tested relationships. When uncertain whether an analysis was already executed, search the repository/checkpoints first.
