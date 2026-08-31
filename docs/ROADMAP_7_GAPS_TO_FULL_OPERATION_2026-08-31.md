# HookLab/TIME-MIE — 7-gap closure roadmap to full operation

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Status: CANONICAL EXECUTION PLAN

## Scope
This plan closes the seven currently identified gaps without reopening validated Gate A, M300, DALI, P0 or deductive-framework components.

## Gap 1 — Aesthetic reference -> Analyzer bridge
Target: an authorized local `AESTHETIC_REFERENCE` can be submitted to an analysis execution layer without entering M300, SUCCESS_EVIDENCE or GATE_A.
Required contract: ephemeral audio processing; persist derived JSON/provenance, not source audio; `scientific_ingestion=false`; `gate_a_ingestion=false`.
Acceptance: same session SHA-256 is traceable from Producer Interface request to analyzer result.

## Gap 2 — Analyzer results in Producer Interface
Target: show producer-facing descriptive acoustic results from the existing sensor stack.
Minimum fields: tempo/BPM estimate, beat/downbeat timing summary, duration, sensor status/provenance and explicit descriptive-only semantics.
Acceptance: UI renders returned analysis JSON and labels it `AESTHETIC_REFERENCE_ANALYSIS`, never scientific population evidence.

## Gap 3 — Executable remote analysis mechanism
Constraint: GitHub Pages is static and cannot run Python/ffmpeg/Beat This.
Target: authenticated/controlled execution endpoint or job broker for `run_fulltrack_sensor_regression.py` / Analyzer v1.
Acceptance: upload -> ephemeral analysis -> JSON response/result -> source-audio deletion is demonstrated E2E.

## Gap 4 — Stable versioned public URL
Target: one immutable/versioned Producer Interface route that is not overwritten by the historical HookLab TIME root.
Acceptance: browser regression confirms expected title/version/assets and no root collision.

## Gap 5 — Full product E2E regression
Canonical flow: creative brief -> aesthetic audio -> SHA/provenance -> acoustic analysis -> D0 generation -> listen -> MIDI/manifest -> timer -> producer evaluation -> session JSON.
Acceptance: automated regression passes every stage with synthetic/authorized test audio.

## Gap 6 — Observed melody-representation calibration
Fail-closed criteria: >=30 independent paired items; performance/identity alignment; >=1 musical feature with Spearman rho >= .80 and median absolute error within its predeclared tolerance.
Acceptance: observed calibration report generated and gate decision recorded. Calibration corpora do not increase M300 N.

## Gap 7 — Scientific completion branch
If calibration and a positive conditioned association pass: promote deduction eligibility, generate deterministic `SCIENTIFIC_D`, then unlock confirmatory H/D/H+D.
If no positive eligible association exists: record valid null/non-promotion scientific completion; do not manufacture a rule.
Acceptance: final methods/results/limitations/reproducibility package + regression + provenance + checkpoint.

## Execution order
A. Close gaps 1-3 as one Audio Analyzer Bridge layer.
B. Close gap 4 and deploy a versioned integrated interface.
C. Close gap 5 with E2E browser/backend regression.
D. Execute gap 6 in parallel as soon as >=30 valid pairs are prepared.
E. Resolve gap 7 according to observed evidence.

## Current reusable components
- Producer Interface v0.3 and D0 browser adapter.
- `run_fulltrack_sensor_regression.py` acoustic sensor path.
- Beat This v1.0.0 + verified ONNX model hashes in Analyzer v1 Real E2E workflow.
- `analyzer_v1_orchestrator.py`.
- melody representation calibration extractor/agreement/gate.

## Prohibited shortcuts
- Do not treat aesthetic-reference analysis as M300 evidence.
- Do not persist commercial/reference source audio in repository artifacts.
- Do not label D0 as `SCIENTIFIC_D`.
- Do not lower calibration thresholds to achieve completion.
- Do not use the historical Pages root as proof of Producer Interface version identity.
