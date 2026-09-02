# MIE Recovery and Recognition Gate — 2026-09-02 v1

Status: `RECOVERY_GATE_ACTIVE`

## Product boundary

MIE is a musical-recognition system. Transcription is its measurement prerequisite:
the system must first recover sufficiently reliable, time-aligned melody, harmony
and beat evidence before it can analyze relations among them or condition
composition assistance.

## Regression finding

`app-mie-audio-midi-explorer-v0.2.html` repaired the mobile upload surface but
introduced an engine regression. It replaced the recovered melody chain with a
simple full-mix Goertzel detector and its audible preview omitted harmony. It is
therefore classified as `REJECTED_ENGINE_REGRESSION` and cannot become a baseline.

The result does not erase prior work. Git history and frozen artifacts retain:

- M: probabilistic F0, octave-plane resolution and R1.1–R1.3 recovery;
- H: acoustic candidates, Motor→IA→Motor ranking and LOCK/AMBIGUOUS behavior;
- T: Beat This neural inference and the approved tactus lineage;
- integrated server path: HTDemucs → trained sensors → M/H/T resynthesis.

## AI boundary

The preserved Motor→IA→Motor artifact implements deterministic contextual priors,
candidate requery and KEEP/QUERY/DROP decisions. It is a reproducible reasoning
prototype rather than a connected private AI provider. A later provider may rank
only observed candidates and must return structured decisions with provenance. It
cannot invent missing acoustic pitches, overwrite raw observations, force LOCK or
unlock scientific evidence.

## Accuracy statement

The producer's approximate 98% assessment is retained as contextual auditory
evidence for the historical exercise. The measured documentary result currently
available is 13/14 recovered melody regions within ±0.5 semitone on the historical
replay. Neither observation establishes general 98% accuracy across songs.

## Mandatory recovery order

1. Enforce `MIE_CANONICAL_COMPONENT_REGISTRY_v1` in CI.
2. Preserve the v0.2 mobile acquisition surface without its rejected engine.
3. Execute M/H/T through the local/private analyzer service contract.
4. Restore audible M + H + T and machine-readable provenance.
5. Pass the historical regression.
6. Run blind regression on unseen songs with contrasting voice, register and mix.
7. Calibrate before scientific Feature Admissibility or population-level claims.

## Change rule

One module may change per experiment. Every candidate records its parent baseline,
changed module, artifacts, hashes, tests and producer disposition. A candidate may
replace a baseline only after all registered regression gates pass.
