# Gate B2 robust Dance-Pop cohort readiness — checkpoint

Date: 2026-08-30
Branch: `mie/golden-forensic-v0.3`
Layer: `GATE_B2_ROBUST_COHORT_READINESS_v1`
State: `IMPLEMENTED / CURRENT_EVIDENCE_NOT_READY`

## Corroborated basis
The TSDQP defines the scientific population independently from symbolic-source availability and requires identity, version, FULL_SONG, provenance and FULL_TMT before Matrix X promotion. It defines T0=5, T1=30, T2=50 minimum analytical cohort, with later stability checkpoints.

The existing cohort stability gate requires N>=50, consecutive local stability and absence of persistent directional drift before returning `STABLE_REFERENCE_READY`.

The current canonical evidence identifies five accepted Dance-Pop cases as T0 forensic/technical validation seed. No observed N>=50 Dance-Pop Matrix-X stability artifact was located in the canonical branch during this audit.

## Code
- `mie_core/gate_b2_robust_cohort_readiness.py`

## Current evidence input
- `experiments/gate_b2/DANCE_POP_ROBUST_COHORT_READINESS_CURRENT_v1.json`

## Decision
Current expected state: `ROBUST_COHORT_NOT_READY`.

This is a scientific evidence-state result, not an algorithm failure. It prevents the statistical-rule promotion layer and CT001-D from using T0 as if it were the final analytical reference.

## Downstream lock
`ROBUST_COHORT_APPROVED_FOR_PROMOTION_LAYER` requires all of:
- scientific population confirmed;
- discovery/promotion boundary confirmed;
- identity/version/FULL_SONG/provenance gates confirmed;
- FULL_TMT complete;
- qualified Matrix-X N>=50;
- observed `STABLE_REFERENCE_READY`;
- no persistent directional drift.

## Next action
Continue the already-defined OFFLINE ROBUST BUILD rather than redesign acquisition:
`discover targets -> qualify success -> identity/version -> symbolic source -> FULL_SONG -> FULL_TMT -> Matrix X -> stability evaluation -> robust reference cache`.

Every future promotion of this layer must include the observed matrix/stability artifacts, code/test evidence and a new approval checkpoint under the Scientific Layer Approval Invariant.
