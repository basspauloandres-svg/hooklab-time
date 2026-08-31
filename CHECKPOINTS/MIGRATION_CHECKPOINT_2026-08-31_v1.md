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
- listening protocol/interface: ~85%+ and now moving into product UX iteration;
- provenance/checkpoint discipline: ~97%;
- empirical readiness for confirmatory listening: ~65-70%;
- positive scientific rule: 0, correctly.

## 11. Immediate next work in new conversation
Do not ask for P0 subjective ratings first. User explicitly prefers to see and iteratively test the product interface.
Priority order:
A. make the UX prototype actually executable/openable from a stable link and verify every button/function;
B. integrate the aesthetic-reference upload/player and keep its provenance isolated;
C. expose scientific evidence/boundaries clearly in producer language;
D. continue observed melody-representation calibration in parallel without waiting for DALI;
E. once a calibrated positive association exists, generate SCIENTIFIC_D MIDI/audio and unlock confirmatory H/D/H+D;
F. final regression/checkpoint/documentation.

## 12. Key recent commits
- `1e673678b4a684be8057c159a7537f7f27a05016` Road to 100% criteria.
- `923ad3a3bc316528961194c7a0731e2935bceda5` confirmatory listening unlock gate.
- `218f1038771f6418a709003a94cc75032f9bef7f` current listening lock state.
- `70dcc81911b86fcc76555364a36d317b7a081d60` P0 response validator.
- `c25564e421f6dafba77207b3ba9e64d55e8d1ca1` P0 response template.
- `8ac7669a25f72e7789e2d5fafacf722b0e0febd1` first UX prototype.
- `45e7309beb8cd86ecfea2d78dc818d4cf5fcdf60` aesthetic-reference scientific contract.

## Migration instruction
Read this checkpoint completely together with the canonical project documents. Continue exactly from section 11. Do not restart Gate A, acquisition design, M300 discovery, deductive-framework design, DALI integration design or P0 protocol design. Any new layer approved by the user must be corroborated, explicitly coded, versioned and checkpointed before becoming canonical.
