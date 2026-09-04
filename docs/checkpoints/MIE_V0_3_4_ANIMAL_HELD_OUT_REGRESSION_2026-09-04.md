# MIE v0.3.4 — Animal held-out regression audit

Date: 2026-09-04  
Status: `PRODUCER_EVALUATION_FAIL_REGRESSION / REJECTED_FOR_BASELINE_PROMOTION`

## 1. Scope and evidence boundary

This audit evaluates the MIE v0.3.4 candidate on the independently supplied
audio `Animal.mp3`. The audio is an authorized session reference and is not
stored in the repository. Its SHA-256 is:

`75e1dcbaef2fe3d81818df650acf72d98c306f0262bd9e78bbbc911a42a436a0`

The evaluated package is `MIE_RECOGNITION_v0_3_4.zip`, SHA-256:

`39afd3c980c3d22e4267a33aee33e5f09895d514fbbcccbbe8ab7ef04789d67a`

The source hash recorded in the recognition JSON exactly matches the supplied
audio. This rules out a source-file mismatch for this run. The audit is an
engineering and producer-evaluation result; it is not a scientific accuracy
estimate or Feature Admissibility result.

## 2. Canonical disposition

- `MELODY_RECOGNITION = FAIL_UNRECOGNIZABLE`
- `PRODUCER_EVALUATION = FAIL_REGRESSION`
- `MIE_V0_3_4_BASELINE_PROMOTION = REJECTED`
- `MIE_V0_3_4_ARTIFACT_RETENTION = PROVENANCE_ONLY`
- `MIE_V0_3_3_ROLE = COMPARISON_REFERENCE_NOT_VALIDATED_BASELINE`
- `T_STATUS = FROZEN_ENGINEERING_BASELINE_PRESERVED`
- `generation_class = D0_EXPLORATORY`
- `scientific_d_unlocked = false`

The producer reported that the reconstructed melody was not recognizable.
This judgment is preserved as the functional outcome. Automated coverage and
residual diagnostics must not be translated into a melody-accuracy percentage.

## 3. Verified measurements

### 3.1 Source and tactus

- source duration recorded by MIE: `245.0808163265 s`;
- resolved tactus events: `477` from `480` raw beat observations;
- estimated tempo: `120.0 BPM`;
- metric state: `METRIC_LOCK`;
- producer disposition for pulse: retained as substantially correct;
- T fingerprints were unchanged between candidate comparisons.

### 3.2 Melody

- raw Basic Pitch candidates: `290`;
- initially accepted candidates: `228`;
- final melody events: `215`;
- v0.3.4 newly recovered candidates: `0`;
- final represented melody time: `66.68 s`;
- final temporal coverage: `0.272`;
- gaps of at least `250 ms`: `93`;
- gaps of at least `500 ms`: `72`;
- maximum melody gap: `10.19 s`;
- diagnostic false-silence ratio: `0.5608082348`;
- voiced-overlap IoU: `0.3405261602`;
- median pitch-ridge residual: `66.6667 cents`;
- median onset residual: `75.6506 ms`;
- median offset residual: `91.0601 ms`;
- diagnostic octave-confusion rate: `0.03125`.

The post-run event-level octave resolver changed 14 of 215 notes: seven by
`+12`, five by `-12`, one by `+24` and one by `-24` semitones. Those changes
were not validated against a human reference transcription in this case.

### 3.3 Harmony and M/H alignment

- raw harmony observations: `481`;
- observations reported as ambiguous before metric aggregation: `341`;
- metric-aligned LOCK windows: `114`;
- persistent states before shared-clock extension: `100`;
- final harmony states: `100`;
- final harmony coverage: `238.94 s` or `0.975` of the source duration;
- shared-clock boundary shifts performed: `0`;
- median harmony-boundary distance to nearest melody onset: `1.2286` tactus
  units;
- additional active source frames filled by held harmony: approximately
  `0.515` of active source time.

The diagnostic chroma-template agreement was `0.646` in regions supported by
the pre-existing accepted harmony windows and `0.504` in regions filled by
holding an accepted state across missing or ambiguous evidence. These scores
are uncalibrated within-track diagnostics; their direction supports the
producer-reported regression and cannot be presented as general accuracy.

### 3.4 Audible-output behavior

Using 20 ms windows and a `-45 dBFS` activity threshold, the v0.3.3 comparison
render contained approximately `0.347` silent windows, while the v0.3.4 core
render contained approximately `0.021`. The reduction came principally from
near-continuous harmonic holding, while the final melody-event coverage rose
only to `0.272` and no rejected note candidate was recovered.

The waveform correlation between the v0.3.3 and v0.3.4 core renders was
approximately `0.760`. This confirms a substantial audible change, but it does
not establish improved transcription.

## 4. Root-cause finding

The principal failure is not file contamination. It is a mismatch between the
candidate's engineering gates and musical recognizability:

1. The melody gap-recovery layer extended some accepted tails but recovered no
   additional rejected candidate on this track.
2. The shared-clock harmony function filtered to LOCK states and then extended
   each accepted state until the next accepted state, crossing intervals whose
   source evidence had been ambiguous or absent.
3. The alignment layer returned `DERIVED_CANDIDATE` even though it shifted zero
   harmonic boundaries and its median distance to melody onsets remained
   greater than one tactus unit.
4. The final audible mix therefore sounded fuller while the melody remained
   sparse and the harmony occupied unsupported intervals.
5. The connected-provider flag was `false`. The current
   `DETERMINISTIC_CONTEXTUAL_REASONER_v1` ranks observed candidates only; it
   neither supplies missing acoustic evidence nor performs learned correction.

## 5. CI interpretation

The three remote GitHub Actions runs for the published v0.3.4 commit completed
successfully:

- MIE Core Prototype: run `33799581232`;
- MIE Canonical Component Registry: run `33799581347`;
- Lyric Modeling Coherence Contract: run `33799581133`.

Those runs establish executable integrity and contract compliance. Synthetic
and structural CI does not establish perceptual melody recognition or
cross-track musical generalization. This case demonstrates why producer
evaluation and held-out tracks remain separate promotion gates.

## 6. General repair boundary

The next experiment must not encode title, artist, filename, known notes,
manual timestamps or a song-specific template. One module changes per
experiment.

The first v0.3.5 experiment is M-only and must diagnose sensor recall before
post-processing:

1. distinguish source-separation loss from note-sensor rejection;
2. retain competing pitch/octave candidates until convergent evidence resolves
   them;
3. require plane evidence for every recovered interval;
4. abstain when evidence cannot support a recognizable contour;
5. compare against the same frozen H reference and byte-identical T events;
6. report producer recognizability separately from automatic residuals;
7. evaluate on multiple independent tracks before any baseline decision.

The harmony ambiguity-bridging defect is registered for a later H-only
experiment. It must not be repaired simultaneously with the M-only v0.3.5
experiment.

## 7. No-reprocess rule

Preserve all v0.3.1–v0.3.4 outputs and measurements. Do not rerun this source
merely to search for a favorable result. A rerun requires a registered new
experiment, changed module declaration, new analysis identifier and retained
prior result.
