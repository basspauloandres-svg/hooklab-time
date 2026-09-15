# HookLab Evidence Pipeline checkpoint v0.1
Date: 2026-09-15
Branch: integration/mie-r13-producer-v07-20260915

## Implemented
1. Feature Engine v0.1: deterministic M+T-derived case features with event/source/engine provenance.
2. Corpus Statistical Store v0.1: case-level persistent store; replacement by case_id; scientific state preserved.
3. Statistical Evidence Engine v0.1: descriptive aggregation only over ADMITTED cases; minimum-n policy explicit; descriptive statistics never unlock generation by themselves.
4. Evidence Generation Gate v0.1 + Pipeline: fail-closed scientific generation; exploratory output explicitly segregated; unsupported model-prior sources blocked; lyrics require author/producer semantic input plus traced music constraints.

## Invariants
- No descriptive frequency is automatically promoted to a compositional rule.
- scientific_d_unlocked remains false until a separately validated conditioned-rule layer exists.
- GENERAL_COMPOSITIONAL_INTUITION, MODEL_PRIOR_ONLY, UNTRACED_AI_PROPOSAL cannot authorize scientific generation.
- AI-proposed material may exist only under explicit provenance/state and cannot silently become corpus evidence.
- Harmony is not required by this M+T pipeline.

## Regression test
`node tests/evidence_pipeline_v0_1_test.js`
Expected: `PASS evidence pipeline v0.1`.

## Next gate
Integrate these modules into the tangible Workbench UI and implement Case Analysis Package + admission/audit controls so multiple real references can populate the store. Generation remains BLOCKED until conditioned statistical rules are scientifically admitted.
