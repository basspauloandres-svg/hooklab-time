# Dance-Pop T1 qualification matrix layer — checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Layer ID: `DANCE_POP_T1_QUALIFICATION_MATRIX_v1`
State: `IMPLEMENTED / VALIDATION_CODED / INITIAL_FAIL_CLOSED / EMPIRICAL_QUALIFICATION_PENDING`

## Purpose
Convert the 25-song T1 discovery queue into an auditable 25×gate matrix without allowing discovery metadata to increase scientific N.

## Mandatory gates
1. mass_success
2. identity
3. genre_style
4. version
5. symbolic_source
6. full_song
7. provenance
8. full_tmt

Each gate uses exactly one of: `PASS`, `AUDIT`, `FAIL`, `PENDING`.

Row semantics:
- all eight PASS -> `QUALIFIED_FOR_MATRIX_X`
- any FAIL -> `REJECTED`
- otherwise any AUDIT -> `AUDIT`
- otherwise -> `PENDING`

Scientific promotion is intentionally outside this layer and remains a later gate.

## Code and tests
- `mie_core/t1_qualification_matrix_builder.py`
- `mie_core/test_t1_qualification_matrix_builder.py`

Tests encode:
- discovery alone never qualifies a row;
- all eight PASS are required for Matrix-X qualification;
- AUDIT remains distinct from FAIL;
- FULL_SONG or any other FAIL rejects the row.

## Initial evidence state
`experiments/gate_b2/DANCE_POP_T1_QUALIFICATION_EVIDENCE_CURRENT_v1.json` starts with zero scientific PASS assignments for the 25 discovery candidates. This is deliberate fail-closed behavior.

Current scientific count therefore remains T0=5 qualified rows. The queue of 25 is not counted as T1.

## Approval condition for next layer
This layer may be promoted from implementation to empirically populated only as gate evidence is observed and persisted with provenance. T1 freezes only when 25 additional rows satisfy all eight gates, producing 30 total qualified rows. Rejections and AUDIT cases remain permanently retained.

## Invariants
- `scientific target population != songs available in Lakh/LMD`
- `candidate discovery != scientific promotion`
- `preview/fragment != FULL_SONG`
- `AUDIT != FAIL`
- `missing evidence != PASS`
