# HookLab/TIME-MIE — DALI pending / parallel scientific closure checkpoint

Date: 2026-09-01
Branch: `mie/golden-forensic-v0.3`
Status: CANONICAL

## Observed external state
The user's Zenodo request for `The DALI dataset (v2)` / record 3576083 is confirmed submitted and pending. At the observed mobile UI state the request status is `Submitted/Enviado`, created approximately six hours earlier. There is no evidence of rejection.

## Decision
DALI remains an optional parallel provider. It is neither abandoned nor allowed to block scientific completion.

## Existing DALI readiness
- M300 public-metadata target set: 30 candidates after audited identity normalization.
- Target manifest linked to canonical M300 `candidate_id` values.
- Authorized-annotation extractor implemented and regression-tested.
- Population association runner implemented and regression-tested.
- Only `median_pitch_st` is representation-calibrated/allowlisted for this path.
- `SCIENTIFIC_D` remains blocked.

## Parallel closure path
While DALI access is pending, scientific closure proceeds from evidence already observed and eligible. The project will consolidate all population tests already executed under their frozen gates and produce a final promotion/non-promotion decision package.

`median_pitch_st` must be reported separately as `REPRESENTATION_CALIBRATED__POPULATION_ASSOCIATION_PENDING_EXTERNAL_PROVISIONING` until >=30 version-aligned note-event representations are available.

This pending feature is not a negative finding and cannot be treated as evidence of absence.

## Scientific completion rule
A valid null/non-promotion result across executable population tests counts as scientific-chain completion. No positive creative rule will be manufactured to reach completion. If DALI is later provisioned, only the pre-registered `median_pitch_st` branch may reopen under the frozen association gate.

## Immediate next execution
1. Build a master registry of all already executed population association tests and their multiplicity-controlled outcomes.
2. Separate `TESTED_NOT_PROMOTED`, `CALIBRATED_BUT_UNTESTED_POPULATION`, and `EXTERNAL_PROVISIONING_PENDING` states.
3. Run a final fail-closed scientific promotion gate over the registry.
4. If no positive eligible association exists, freeze `SCIENTIFIC_D=BLOCKED_NO_POSITIVE_DEDUCTION` and proceed to final methods/results/limitations/reproducibility documentation.
5. If DALI access arrives before final freeze, execute the pre-registered 30-target branch without changing thresholds.
