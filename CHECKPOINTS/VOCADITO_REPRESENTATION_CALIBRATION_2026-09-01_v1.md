# HookLab/TIME-MIE — Vocadito observed representation calibration checkpoint v1

Date: 2026-09-01
Branch: `mie/golden-forensic-v0.3`
Workflow run: `33453594919`
Head commit: `f5d36568a70b67ad31ba9117844d9cbd31850f94`
Artifact: `vocadito-observed-representation-calibration` (artifact id `9780688225`)
Artifact digest: `sha256:17cc22ff2fc4ee86bdaa814fb326d59e9f2c2f28f1d1a71619a4abbbf5635f9d`

## 1. Scientific role
This execution validates stability of vocal-melody representations only. It does not increase M300 N, does not establish a population-level creative association, and does not unlock `SCIENTIFIC_D` by itself.

## 2. Cohort and design
Dataset: Vocadito.
Observed recordings: 40/40.
Candidate representation: Basic Pitch ONNX estimated from each recording.
Independent human references: note annotator A1 and note annotator A2 on the same performances.
Failures: 0.

Frozen HookLab gate retained unchanged:
- paired items >= 30;
- independent reference explicit;
- same performance/aligned identity;
- at least one core feature with Spearman rho >= .80;
- median absolute error <= predeclared feature-specific tolerance.

A feature is considered dual-reference stable only when it satisfies the same frozen criteria against BOTH A1 and A2.

## 3. Observed results
### `pitch_range_st`
A1: rho = 0.2747031809291908; median absolute error = 9.023418465733641 st; tolerance = 2.0 st.
A2: rho = 0.2434399686088147; median absolute error = 9.229043585104044 st; tolerance = 2.0 st.
Decision: NOT PROMOTED.

### `median_pitch_st`
A1: rho = 0.985591509543582; median absolute error = 0.4436398717288519 st; tolerance = 1.0 st.
A2: rho = 0.9867224234960129; median absolute error = 0.4383798526749949 st; tolerance = 1.0 st.
Decision: REPRESENTATION-STABLE / PROMOTED FOR DOWNSTREAM ASSOCIATION TESTING.

### `median_interval_st`
A1: rho = 0.5308868243538312; median absolute error = 0.36112645004693 st; tolerance = 1.0 st.
A2: rho = 0.6012197147323887; median absolute error = 0.3703691766226882 st; tolerance = 1.0 st.
Decision: NOT PROMOTED because rho < .80 despite acceptable median error.

### `stepwise_motion_share`
A1: rho = 0.670608119919753; median absolute error = 0.09605609708068724; tolerance = 0.10.
A2: rho = 0.6662913030269026; median absolute error = 0.06752474284463683; tolerance = 0.10.
Decision: NOT PROMOTED because rho < .80.

### `pitch_repetition_share`
A1: rho = 0.36270232270739605; median absolute error = 0.0964552634888353; tolerance = 0.10.
A2: rho = 0.519915553000047; median absolute error = 0.07307822696838716; tolerance = 0.10.
Decision: NOT PROMOTED because rho < .80.

## 4. Gate result
A1 gate: `REPRESENTATION_CALIBRATED` with stable feature `median_pitch_st`.
A2 gate: `REPRESENTATION_CALIBRATED` with stable feature `median_pitch_st`.
Dual-reference result: `REPRESENTATION_CALIBRATED_DUAL_REFERENCE`.
Canonical representation-stable allowlist at this checkpoint: `median_pitch_st` only.

## 5. Interpretation boundary
Empirical evidence supports stability of `median_pitch_st` across Basic Pitch ONNX and both independent human note representations in this Vocadito cohort under the frozen HookLab criteria.

This result does NOT imply that median pitch is associated with commercial success, memorability, hook quality or any other outcome. It only authorizes `median_pitch_st` to enter downstream population-association testing. The other four tested core features remain fail-closed for creative deduction until new independent calibration evidence satisfies the frozen criteria.

## 6. Immediate next scientific work
1. Enforce an executable stable-feature allowlist so downstream deduction analysis cannot silently consume unstable melody features.
2. Run a representation-calibrated population association screen restricted initially to `median_pitch_st` on eligible licensed/version-aligned M300 evidence.
3. Apply the existing conditioned-association, controls and multiplicity rules. Do not resurrect the previously rejected pitch-span finding; `pitch_range_st` is explicitly non-promoted here.
4. If no positive eligible association survives, record valid null/non-promotion scientific completion for this branch.
5. Only if a positive association survives all gates may deduction eligibility be considered; `SCIENTIFIC_D` remains BLOCKED until then.

## 7. Canonical state transition
`REPRESENTATION_CALIBRATION_PENDING` -> `REPRESENTATION_CALIBRATED` for the feature family allowlisted as `median_pitch_st`.

`SCIENTIFIC_D`: remains `BLOCKED`.
