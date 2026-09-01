# M300 DALI median-pitch association readiness — 2026-09-01 v1

## Scope
Scientific-readiness checkpoint for the transition from representation calibration to population association. This checkpoint does not promote a creative deduction and does not unlock `SCIENTIFIC_D`.

## Representation calibration already closed
- Dataset: Vocadito, 40 recordings, two independent human note references (A1/A2).
- Frozen criteria: n >= 30, Spearman rho >= .80, feature-specific median absolute error tolerance.
- Sole dual-reference stable feature: `median_pitch_st`.
- A1: rho = .986; median absolute error = .444 st.
- A2: rho = .987; median absolute error = .438 st.
- The remaining four tested melody features are excluded from promotion.
- Canonical allowlist: `config/representation_stable_features_v1.json`.

## M300 × DALI public metadata coverage
Workflow: `.github/workflows/m300-dali-public-crossmatch.yml`.
Observed run: `33455566433` on commit `0e6e1ec0b499f8ad91ed9969fe0df25aa262d284`.

Observed result:
- M300 frame: 300/300 rebuilt successfully.
- Automatic DALI metadata candidates: 30/300.
- `ground_truth` or public metadata NCC >= .80: 30/30 candidates.
- Annotation access: `RESTRICTED_ZENODO_REQUEST_REQUIRED`.
- Scientific promotion: false.

The 30th metadata candidate was recovered through an audited orthographic identity normalization: `Pink` == `P!nk`, documented explicitly as `ARTIST_IDENTITY_ALIASES={'p nk':'pink'}`. The automatic match threshold remained unchanged at 8. A near-threshold `E.T. — Katy Perry` candidate was audited and rejected because its best DALI metadata record was a different song (`The One That Got Away`). Therefore the threshold was not relaxed.

## Executable association layer
`mie_core/m300_dali_median_pitch_association.py` is implemented and fail-closed. It:
1. accepts only `HOOKLAB_DALI_ANNOTATION_EVIDENCE_v1.0` records with `PASS_ANNOTATION_PARSE`;
2. verifies `median_pitch_st` against the representation-stable allowlist;
3. requires an explicit released-recording identity manifest with `released_recording_identity=PASS`;
4. tests only `median_pitch_st`;
5. uses the existing M300 association gate: n >= 30, |Spearman rho| >= .20, BH q < .05;
6. tests the existing outcomes `m300_rank_strength` and `log10_spotify_playcount`;
7. never performs automatic scientific or creative-rule promotion.

Software regression run `33455344449` passed. Synthetic fixtures in that regression are software evidence only and are forbidden as scientific evidence.

## Epistemic boundary
`PUBLIC_DALI_METADATA != DALI_ANNOTATION_EVIDENCE != RELEASED_RECORDING_IDENTITY_PASS != POPULATION_ASSOCIATION != CONDITIONED_DEDUCTION`.

Thirty metadata candidates establish potential coverage at the predeclared population minimum. They do not constitute thirty observed association rows because the restricted DALI annotations are not yet provisioned and released-recording identity has not yet been established for all candidates.

## Current gate state
- Representation calibration: PASS for `median_pitch_st` only.
- Potential DALI M300 coverage: 30 candidates, threshold reached.
- DALI annotation provisioning: PENDING.
- Released-recording identity manifest: PENDING.
- Observed population association for `median_pitch_st`: NOT YET EXECUTED.
- `SCIENTIFIC_D`: FAIL-CLOSED / BLOCKED.

## Next valid transition
Provision authorized DALI annotations; parse the 30 candidates with the validated DALI parser; establish released-recording identity PASS per row; execute `m300_dali_median_pitch_association.py`; record either a valid null/non-promoted result or, if an association survives the frozen gate, evaluate it through the existing evidence-to-creative-deduction gate. No threshold or feature substitution is permitted after observation.
