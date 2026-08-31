# Pre-listening readiness checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
State: `ENGINEERING_NEAR_COMPLETE / LISTENING_TEST_NOT_YET_SCIENTIFICALLY_UNLOCKED`

## Newly frozen gate
`mie_core/melody_representation_calibration_gate.py` prevents melody-derived features from becoming creative deductions until F0/note representation stability is observed on independent calibration material.

Required before positive melodic deduction:
- >=30 paired calibration items;
- independent reference;
- same performance/aligned identity;
- stable core feature(s), provisionally rho >= .80 and feature-specific median absolute error within declared tolerance.

Calibration providers are external methodological corpora (e.g. RWC 2.0, MedleyDB, Vocadito) and never increase M300 N.

## Current project readiness
Percentages are readiness estimates, not empirical effect sizes.

- Canonical architecture / branch continuity: 100%
- Discovery and qualification architecture: 100%
- M300 discovery frame: 100% (300/300)
- Evidence-to-Creative-Deduction epistemic framework: 100%
- Fail-closed deduction gate: 100%
- Licensed structural/vocal-analysis coverage of M300: 25% (75/300 version-gated unique rows)
- DALI adapter/parser engineering: 100%
- DALI observed ingestion: 0% pending external access approval
- Melody representation calibration gate engineering: 100%
- Melody representation calibration observed execution: 0% at this checkpoint
- Positive population-level creative rule promoted: 0% (correctly none yet)
- Negative/non-promotion evidence: operational; early-chorus, tested formal repetition/architecture, and normalized aggregate pitch-span hypotheses have not passed promotion gates
- MIDI/audio creative-test infrastructure: ~80%; scientific activation remains blocked until a positive conditioned deduction survives the evidence chain
- Human listening protocol/application: ~85%; should not be used as confirmatory evidence before a legitimate D-condition stimulus exists
- Provenance/checkpoint discipline: ~97%
- Overall engineering/methodological readiness: ~93%
- Overall empirical readiness for confirmatory listening: ~65%

## Listening-test decision
A UI can be technically opened now, but a confirmatory H/D/H+D listening experiment would be premature. The scientific unlock requires:
1. representation calibration for at least one melody feature family;
2. a positive scoped association that survives the frozen statistical gate and relevant controls;
3. interpretation/theory matched to that observed pattern;
4. conditioned MIDI realization with provenance;
5. standardized audio render;
6. then H/D/H+D listening evaluation.

Exploratory usability/listening tests remain allowed if explicitly labelled exploratory and are not used to validate the scientific claim.
