# Robust cohort batch controller — checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Layer: `ROBUST_COHORT_BATCH_CONTROLLER_v1`
State: `IMPLEMENTED / VALIDATION_CODED / CURRENT_T0_REGISTERED / T1_DATA_PENDING`

## Corroborated architecture
The existing TSDQP fixes the scientific sequence from mass-success target discovery through identity, version, symbolic source resolution, FULL_SONG, FULL_TMT, Matrix X and robust reference cache. Candidate discovery is distinct from scientific promotion.

The existing `lmd-full-target-audit.yml` already demonstrates an engineering shadow path from exact symbolic target audit to candidate Matrix X, cache, routing, constraints and structural candidates, while explicitly keeping `scientific_promotion=false`.

The existing `prototype_autonomous_public_batch.py` is explicitly labelled `PROTOTYPE_EVIDENCE_NOT_FINAL_SAMPLE` and uses public short previews. Such evidence is therefore excluded from robust scientific-row counts.

## Code
- `mie_core/robust_cohort_batch_controller.py`
- `mie_core/test_robust_cohort_batch_controller.py`

## Current observed ledger
- `experiments/gate_b2/DANCE_POP_ROBUST_BATCH_STATE_T0_v1.json`

Current qualified engineering/forensic candidate count: 5.
Current scientifically promoted count: 0.
Current stage: `T0_VALIDATION_SEED`.
Next checkpoint: T1=30.
Additional qualified rows required to reach T1: 25.

## Controller guarantees
- preview/prototype/fragment evidence cannot count as a robust row;
- identity, version, FULL_SONG, provenance, FULL_TMT, mass-success and genre/style gates must all pass;
- candidate status and scientific promotion remain separate;
- reaching N=50 does not establish representativeness by itself; the cohort stability gate remains downstream and mandatory.

## Scientific boundary
The controller does not discover targets, acquire media, run FULL_TMT, or fabricate Matrix-X rows. It coordinates and audits observed outputs from the already approved upstream pipeline.

## Next layer
Populate the T1 queue through the existing TSDQP using legitimate target-discovery and symbolic-source resolution routes. Every accepted/rejected case must preserve provenance and gate outcomes. When 30 qualified rows exist, persist a T1 checkpoint before proceeding toward T2=50.
