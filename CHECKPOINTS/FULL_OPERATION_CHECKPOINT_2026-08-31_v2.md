# HookLab/TIME-MIE full-operation checkpoint — 2026-08-31 v2

Branch: `mie/golden-forensic-v0.3`
Status: CANONICAL OPERATIONAL CHECKPOINT
Supersedes the operational state of sections 11, 13, 14, 15 and 16 of `MIGRATION_CHECKPOINT_2026-08-31_v1.md`; all earlier scientific invariants remain in force.

## 1. Product closure status
Producer Interface v0.5 is the current integrated product layer.
Public versioned route: `https://basspauloandres-svg.github.io/hooklab-time/producer-interface-v0.5/`.
The historical Pages root is not the canonical Producer Interface URL.

Closed operational gaps:
1. Aesthetic reference -> analyzer bridge: PASS.
2. Analyzer results rendered in Producer Interface: PASS.
3. Executable analysis mechanism: PASS via local on-device ONNX; no backend upload required.
4. Stable versioned public URL: PASS at `/producer-interface-v0.5/`.
5. Full browser product E2E: PASS.

Scientific gaps still open:
6. Observed melody-representation calibration with >=30 valid independent pairs: PENDING OBSERVED DATA.
7. Scientific completion branch: BLOCKED on gap 6 and on whether a positive deduction-eligible association exists.

## 2. Aesthetic reference analysis architecture
The local reference remains strictly isolated:
`AESTHETIC_REFERENCE != M300_EVIDENCE != SUCCESS_EVIDENCE != GATE_A_ACQUISITION`.

Browser flow:
local authorized audio -> local SHA-256 -> local Web Audio decode/resample 22.05 kHz mono -> verified `mel_spectrogram.onnx` -> verified `beat_this_small.onnx` -> beat/downbeat postprocessing -> descriptive session JSON.

No source audio is uploaded by this local path. Output semantics:
- role: `AESTHETIC_REFERENCE_ANALYSIS`;
- analysis_mode: `LOCAL_ON_DEVICE_ONNX`;
- scientific_ingestion=false;
- gate_a_ingestion=false;
- m300_ingestion=false;
- success_evidence_ingestion=false;
- source_audio_persistence=`NONE`.

Beat This source/model identity:
- source repository: `danigb/beat-this-rs`;
- pinned source commit: `089b509247e6fdcec666511c0dcf0d5f39c21e73`;
- Beat This small SHA-256: `a5f8d39d989f31859454ba27afe61c5317ca95e4d9373e6853e5361b8937172f`;
- mel frontend SHA-256: `fdd59e65c515331308e4c8841edf99972deca646bdf6197744c2a5b7755e3de9`;
- ONNX Runtime Web: 1.29.0.

This product analysis is descriptive session evidence. It does not replace the scientific representation-calibration gate and does not increase M300 N.

## 3. Real browser verification
Direct local analyzer regression, GitHub Actions run `33450328103`, job `99678551103`: PASS.
Control: synthetic 3 s click track at 120 BPM.
Observed output:
- tempo_bpm_median: 120;
- beat_count: 7;
- downbeat_count: 4;
- analysis latency: approximately 3103 ms including first model download/compile in the CI browser;
- all ingestion flags false;
- source audio persistence NONE.

Observed stages completed:
`AUDIO_DECODE -> AUDIO_READY -> MODEL_DOWNLOAD -> MODEL_COMPILE_MEL -> MODEL_COMPILE_BEAT -> MODELS_READY -> MEL_INFERENCE -> MEL_READY -> BEAT_INFERENCE_1/1 -> COMPLETE`.

Full Producer Interface E2E, GitHub Actions run `33450441967`, job `99678908692`: PASS.
Verified in one browser session:
creative brief -> aesthetic audio upload -> SHA/provenance -> local Beat This -> BPM/beats -> analysis panel -> D0 generation -> three variants -> MIDI download with `MThd` -> D0 manifest -> timer -> producer decision -> local session persistence -> JSON export.
Observed E2E control result: 120 BPM, 10 beats, 3 D0 variants, `SCIENTIFIC_D=BLOCKED`.

## 4. Interface defect discovered and fixed
Producer Interface v0.5 initially failed to bind handlers because `export.onclick` used JavaScript reserved token `export` as an identifier. This invalidated the inline script and manifested to the user as reference audio not loading.
Canonical fix commit: `f3e72ef47b7b68754ed56b5c5cc952f05d21eb3f`.
Published fix commit on `main`: `39fe8bcc903462c4c05c577b1227b02741c9b6c4`.
A new CI gate now extracts the inline JavaScript from `index.html` and runs `node --check`; run `33450365274` passed. Future syntax regressions must fail CI before product promotion.

## 5. D0 state
D0 remains exploratory and deterministic.
Contract: `D0_EXPLORATORY != SCIENTIFIC_D`.
The browser generator produces thetic, anacrustic and syncopated variants, MIDI, simple audition audio and manifest provenance. It uses no source melody input and performs no online corpus reanalysis.
`SCIENTIFIC_D` remains blocked by design.

## 6. Calibration gate hardening
A prior defect was identified in `paired_representation_agreement.py`: reference independence had been emitted as true without row-level proof.
This was corrected fail-closed in commit `345514fab68c38d3cafa035931a0efa4cd455be7`.
Each pair must now explicitly contain `independent_reference=true`; missing or false values make the aggregate independence condition false. Identity/performance alignment also requires explicit PASS on every row and a non-empty set.
Regression workflow for this condition passed.

Frozen scientific calibration requirement remains:
- >=30 paired independent items;
- same performance or explicitly aligned identity;
- at least one core musical feature with Spearman rho >= .80;
- median absolute error within the feature's predeclared tolerance.

Observed calibration execution is still pending because >=30 validated pairs have not yet been assembled. No synthetic pairs may be used to satisfy this gate.

## 7. Current completion interpretation
Product/engineering interface: operationally complete for the current exploratory producer workflow and verified E2E.
Scientific chain: not yet 100% complete because observed representation calibration and the final positive-or-null deduction decision remain unresolved.
A null/non-promotion outcome is a valid scientific completion. A positive rule must never be manufactured to unlock `SCIENTIFIC_D`.

## 8. Immediate next canonical work
1. Prepare/acquire >=30 genuinely independent aligned representation pairs from eligible calibration sources; do not count them toward M300.
2. Run provider-neutral feature extraction, paired agreement and fail-closed calibration gate.
3. Record feature-level rho and median errors without threshold changes after observation.
4. Re-run conditioned association eligibility using only calibrated representation features.
5. If a positive association becomes deduction-eligible, generate `SCIENTIFIC_D` and unlock confirmatory H/D/H+D. If none becomes eligible, document valid null/non-promotion completion.
6. Final scientific regression, methods/results/limitations/reproducibility documentation and final checkpoint.
