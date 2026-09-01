# HookLab/TIME-MIE migration checkpoint — 2026-08-31 v1

Branch: `mie/golden-forensic-v0.3`
Purpose: canonical handoff to a new ChatGPT conversation. Continue from this state; do not redesign validated components.

## 1. Scientific identity
HookLab is an Evidence-to-Creative Deduction system, not a hit-prediction engine.
Canonical epistemic chain:
`OBSERVATION -> ASSOCIATION -> INTERPRETATION -> HYPOTHESIS -> CONDITIONED DEDUCTION -> MUSICAL REALIZATION -> HUMAN EVALUATION`.
Prediction != deduction. Association != causation. Industry/social-media/course claims != scientific evidence. Genre/style is primarily an analytical/aesthetic stratification layer, not a universal success gate.

## 2. Core acquisition invariants
Scientific target population != songs available in Lakh/LMD.
Candidate discovery != scientific promotion.
Ordinary manual upload of commercial recordings is prohibited for Gate A. Gate A is automatic legitimate reference resolution -> authorized computational access -> version identity -> audio analysis -> vocal extraction -> audio<->MIDI validation -> PASS/AUDIT/FAIL -> provenance.
REFERENCE_UNAVAILABLE is AUDIT/external unavailability, never algorithmic FAIL.
MassiveMusic Fingerprinting remains optional/fail-closed; without provisioning Gate A may remain IMPLEMENTATION_COMPLETE / EXTERNAL_VALIDATION_PENDING_PROVISIONING.

## 3. M300 observed state
300/300 discovery-frame candidates exist (15 Billboard Year-End ranks per year, 2006-2025). This is a discovery/outcome frame, not 300 scientifically promoted musical rows and not 300 Dance-Pop songs.
Licensed/version-gated musical evidence currently observed:
- CoSoD: 52 exact M300 song identities.
- Harmonix: 55 identity matches initially; 28 version-compatible, 27 AUDIT_VERSION_MISMATCH.
- SALAMI: 0 PASS, 1 AUDIT, 299 REFERENCE_UNAVAILABLE.
- CoSoD ∪ version-compatible Harmonix: 75 unique songs = 25.0% of M300.
Provider ontologies remain separate because post-version overlap is only 5 songs.

## 4. Deductive findings to date
Do not resurrect rejected/non-promoted rules without new evidence.
- Early chorus timing did not survive promotion gates in McGill historical, CoSoD contemporary, or M300×CoSoD analyses.
- Tested formal repetition/architecture variables in M300×CoSoD did not survive multiplicity-controlled promotion.
- Preliminary aggregate vocal pitch-span association disappeared after semitone normalization and controls.
These are non-promotion findings, not universal proof of irrelevance.
No positive population-level creative rule has yet been scientifically promoted.

## 5. DALI
DALI authorization has been requested by the user and remains pending as of this checkpoint.
DALI is optional, not a blocking dependency.
Implemented:
- fail-closed DALI research adapter;
- DALI -> HookLab parser;
- mapping of notes/words/lines/paragraphs, metadata, NCC/ground-truth and descriptive melody/prosody features.
Never use DALI's historical YouTube audio downloader in HookLab.
Without dataset provisioning -> REFERENCE_UNAVAILABLE. Dataset present -> AUDIT_PROVISIONED until schema/version identity validation.

## 6. Melody representation calibration
Calibration corpora (RWC 2.0, MedleyDB, Vocadito etc.) validate representation only and never increase M300 N.
Implemented:
- `melody_representation_calibration_gate.py`
- `representation_calibration_feature_extractor.py`
- `paired_representation_agreement.py`
Frozen requirements include >=30 paired independent items, performance/aligned identity, and at least one stable feature family. F0 != discrete notes; provider annotation != ground truth by default.
Observed calibration execution is still pending.

Canonical operational formulation:
“Reutilizar el workflow existente de GitHub Pages para publicar Producer Interface v0.2. En paralelo, mantener fail-closed el gate de calibración hasta contar con ≥30 pares independientes, identidad/performance alineada y al menos una feature musical con ρ ≥ .80 y error mediano dentro de la tolerancia predeclarada.”

## 7. Listening state
P0 exploratory listening exists and is explicitly non-confirmatory.
Controlled P0 conditions: H, D0 exploratory, H+D0; same text/harmony/tempo/render. P0 response validator exists.
Confirmatory listening gate exists and requires representation_calibrated + deduction_eligible + valid MIDI manifest + standardized audio + provenance + blinding + evaluation schema + stimulus_class=SCIENTIFIC_D.
Current confirmatory state: BLOCKED correctly because D0 is exploratory and no positive scientific D exists.

## 8. UX/product direction
A first HookLab laboratory UX prototype has been created. Product flow:
1. creative objective/text/intention;
2. optional manual `Audio de referencia estética`;
3. HookLab evidence panel;
4. construction/MIDI/audio;
5. timer as secondary measure;
6. producer decision: retain/modify/reject + reason + hook/singability/memorability/creative usefulness.

Reference-audio invariant:
`AESTHETIC_REFERENCE != M300_EVIDENCE != SUCCESS_EVIDENCE != GATE_A_ACQUISITION`.
Manual reference upload is allowed only in this producer-directed aesthetic layer. It must never silently enter the scientific corpus or Gate A. It may later support descriptive local analysis of tempo, energy, timbre, density, form and other style parameters; copying source melody/lyrics is outside scope.

## 9. Completion definition
100% is scientific-chain completion, not acquisition of every possible dataset and not 300/300 rows with every annotation.
A valid null/non-promotion result counts as scientific completion; never manufacture a positive association to reach 100%.
Road-to-100 gates: architecture regression; sufficient scoped evidence; representation calibration; positive-or-null scientific result; deduction eligibility if positive; deterministic MIDI/audio if eligible; confirmatory human evaluation if scientific D exists; Gate A external status correctly qualified; final regression/provenance; final methods/results/limitations/reproducibility documentation.

## 10. Current readiness
Readiness estimates, not effect sizes:
- canonical architecture / discovery architecture / M300 frame / deductive epistemic framework / fail-closed deduction gate: 100% engineering/design;
- core engineering/methodology: ~94%;
- licensed/version-gated M300 musical coverage: 75/300 = 25.0%;
- DALI adapter/parser engineering: 100%, observed ingestion 0% pending external approval;
- melody calibration gate engineering: 100%, observed calibration pending;
- MIDI/audio creative-test infrastructure: ~80%;
- listening protocol/interface: ~95% after executable deployment + browser regression; D0 engine bridge remains pending;
- provenance/checkpoint discipline: ~98%;
- empirical readiness for confirmatory listening: ~65-70%;
- positive scientific rule: 0, correctly.

## 11. Immediate next work in new conversation
Do not ask for P0 subjective ratings first. User explicitly prefers to see and iteratively test the product interface.
Priority order:
A. connect the verified existing D0 generation architecture to the executable producer interface while preserving descriptive/non-causal semantics and manifest provenance;
B. continue observed melody-representation calibration in parallel without waiting for DALI;
C. keep `SCIENTIFIC_D` fail-closed until calibration and deduction eligibility pass;
D. once a calibrated positive association exists, generate SCIENTIFIC_D MIDI/audio and unlock confirmatory H/D/H+D; if no positive eligible result exists, document valid null/non-promotion completion;
E. final regression/checkpoint/documentation.

## 12. Key recent commits
- `1e673678b4a684be8057c159a7537f7f27a05016` Road to 100% criteria.
- `923ad3a3bc316528961194c7a0731e2935bceda5` confirmatory listening unlock gate.
- `218f1038771f6418a709003a94cc75032f9bef7f` current listening lock state.
- `70dcc81911b86fcc76555364a36d317b7a081d60` P0 response validator.
- `c25564e421f6dafba77207b3ba9e64d55e8d1ca1` P0 response template.
- `8ac7669a25f72e7789e2d5fafacf722b0e0febd1` first UX prototype.
- `45e7309beb8cd86ecfea2d78dc818d4cf5fcdf60` aesthetic-reference scientific contract.
- `c170f657cbada5f899dd7c556b4e03c1286b1298` Producer Interface v0.2: aesthetic-reference provenance, SHA-256, session persistence/export, explicit scientific lock states.
- `4fa26ea759a6ab3f7cfc78059f5109fc6d71447e` initial Producer Interface Pages retarget; deployment from experimental branch failed before runner.
- `1c374586add27e5e71324cc9b0e79b49d15fb7ab` default-branch deployment harness established on `main`.
- `59f7de6d50cf19365848e995ac1ad6adcb610a8d` isolated Pages release created at `producer-interface-v0.2/index.html` on `main`.
- `e5bdc5825f3c47ac364c7bc4421e9bc034f0b958` regression target fixed to isolated Producer Interface Pages release; dynamic Pages deployment completed successfully.

## 13. Post-migration progress — Producer Interface v0.2
Approved implementation layer: `AESTHETIC_REFERENCE v0.2`.
Canonical code: `app/prototype_v1/index.html`.
Implemented and versioned:
- local audio upload and playback;
- MIME validation for audio;
- file identity metadata: name, MIME, bytes, last-modified, duration;
- browser-side SHA-256 fingerprint;
- explicit role `AESTHETIC_REFERENCE`;
- explicit `scientific_ingestion=false` and `gate_a_ingestion=false` semantics;
- session identifier;
- local session persistence and JSON export;
- producer evaluation fields and timer persisted in session snapshot;
- evidence/limits/provenance panels wired in producer language;
- D0/SCIENTIFIC_D distinction surfaced; scientific audio/MIDI is not simulated while confirmatory gate is blocked.

Verification status:
- CODED: PASS.
- VERSIONED: PASS (`producer-interface-v0.2`).
- PROVENANCE CONTRACT: PASS by explicit fields and UI declaration.
- CHECKPOINTED: PASS.
- STABLE PUBLIC LINK: PASS at `https://basspauloandres-svg.github.io/hooklab-time/producer-interface-v0.2/`.
- ROOT URL NOTE: `https://basspauloandres-svg.github.io/hooklab-time/` remains the historical HookLab TIME site and must not be used as the Producer Interface target.
- BROWSER INTERACTION REGRESSION: PASS after Pages deployment completion; rerun job `99667202762` in workflow run `33446499868` completed `success`.

Browser regression PASS covers:
- expected v0.2 title/session boot;
- visible scientific boundary contract;
- evidence/limits/provenance panel toggles;
- authorized synthetic WAV upload;
- local SHA-256 provenance;
- explicit Gate A = NO and scientific ingestion = NO;
- local session identifier persistence;
- timer start/stop/reset;
- D0 exploratory state and `SCIENTIFIC_D` lock;
- save/local persistence of creative input and producer decision;
- JSON export and provenance contract;
- clearing the aesthetic reference.

## 14. D0 reuse audit
Existing reusable architecture was inspected before any new generator implementation.
- `preproduction_router.py`: cache-only cohort resolution; online path cannot search/reanalyse corpus.
- `preproduction_constraints_compiler.py`: converts cached cohort statistics into bounded descriptive constraints with semantics `DESCRIPTIVE_COHORT_BOUNDS_NOT_CAUSAL_RULES`.
- `tmt_candidate_generator.py`: deterministic engineering prototype generator; three variants (thetic/anacrustic/syncopated), manifest, simple audio render, no source melody input.
- `testlane_mt_audio_demo.py`: technical MT-only smoke test and explicitly not model evidence.
Operational decision: reuse this architecture for exploratory D0. Do not relabel it SCIENTIFIC_D. A browser integration may adapt/bridge this engine only after equivalence/provenance verification; no duplicate unverified generator should become canonical.

## 15. Calibration execution audit
The calibration chain is implemented but observed calibration remains pending.
- provider-neutral feature extractor computes pitch range, median pitch, median interval, stepwise motion share and pitch repetition share;
- paired agreement computes Spearman rho and median absolute error;
- fail-closed gate requires >=30 paired items, independent reference, aligned/performance identity, and >=1 stable core feature meeting thresholds.
The existing melodic cross-representation workflow is a separate symbolic validation path and does not by itself satisfy the independent vocal melody representation calibration requirement.

## 16. Deployment/regression closure
The initial root deployment created a misleading apparent success because the repository's dynamic Pages publication continued serving the historical HookLab TIME root. Browser regression correctly detected title `HookLab TIME v1.8`, preventing a false PASS.

Resolution:
- preserve historical Pages root;
- publish Producer Interface v0.2 as isolated release `/producer-interface-v0.2/` on `main`;
- maintain canonical implementation source on `mie/golden-forensic-v0.3`;
- execute browser-level Playwright regression against the isolated release;
- regression PASS only after dynamic Pages deployment completed.

This closes section 11.A and 11.B at product-interface level. Aesthetic-reference provenance remains scientifically isolated. D0 engine connectivity remains the immediate product task; observed melody calibration remains the immediate scientific task.

Immediate next canonical work:
1. Build a verified bridge from existing D0 generation architecture into Producer Interface v0.2, preserving descriptive/non-causal semantics, deterministic identifiers and manifest provenance.
2. Add audible D0 variant selection/playback and downloadable MIDI/audio only under `stimulus_class=D0_EXPLORATORY`; do not expose it as `SCIENTIFIC_D`.
3. Acquire/prepare >=30 independent paired calibration items and execute observed melody-representation calibration.
4. If calibration + positive conditioned association pass, promote deduction eligibility and generate SCIENTIFIC_D; otherwise document valid null/non-promotion completion.
5. Execute final regression/checkpoint/documentation after each approved layer.

## Migration instruction
Read this checkpoint completely together with the canonical project documents. Continue exactly from sections 11, 13, 14, 15 and 16. Do not restart Gate A, acquisition design, M300 discovery, deductive-framework design, DALI integration design or P0 protocol design. Any new layer approved by the user must be corroborated, explicitly coded, versioned and checkpointed before becoming canonical.
