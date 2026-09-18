# HookLab Workbench — Integrated Build Plan v0.2

Date: 2026-09-15
Status: IMPLEMENTATION_ACTIVE

## Decision
Stop treating successive transcription/audition prototypes as the primary development milestone. Build the complete research instrument around the recovered M+T lineage. Audition remains an internal QA surface.

## Operational baseline
M — Melody:
probabilistic F0 candidate front-end -> Plane Resolver over octave-related candidates -> R1.1 voiced-region continuity -> R1.2 duration-sensitive segmentation -> R1.3 region-center pitch classification -> conservative score events.

T — Beat/tactus:
Beat This small pretrained ONNX -> HookLab continuity/CTL -> tactus selection -> deduplication -> physical-time beat output.

Harmony is excluded from the current operational baseline. Historical H artifacts remain preserved but are not required by the current analytical/generative objective.

## Integrated product flow
REFERENCE/CORPUS
-> SOURCE IDENTITY + PROVENANCE
-> M+T ANALYSIS
-> EVIDENCE/AI FUSION + UNCERTAINTY
-> HUMAN AUDIT
-> CASE ANALYSIS PACKAGE
-> FEATURE ENGINE
-> CORPUS STATISTICAL STORE
-> CONDITIONED PATTERN MODEL
-> INDUCTIVE PATTERN DISCOVERY
-> DEDUCTIVE CONSTRAINT APPLICATION
-> HIERARCHICAL GENERATION
-> NEUTRAL AUDIO REALIZATION
-> COMPARATIVE EVALUATION.

## Workbench modules
1. Case Manager: source identity, reference audio, version/hash, analysis state.
2. M+T Engine: recovered melody and Beat This/tactus pipeline on common physical time.
3. Fusion/Audit: observed/model-estimated/AI-inferred/human-audited states with uncertainty retained.
4. Feature Engine: durations, metric attacks, syncopation, onset type, interval sequences, step/leap, direction/contour, range, density, repetition, climax, rests/breathing and other admitted M+T features.
5. Statistical Store: case-level and corpus-level distributions, preserving provenance and admissibility.
6. Pattern Model: conditioned relationships rather than isolated marginal counts.
7. Generator: joint pitch/time hierarchy INTERVAL -> SEQUENCE -> FIGURE -> MOTIF -> PHRASE -> GLOBAL TRAJECTORY.
8. Comparator: source-pattern evidence versus generated realization; listening is evaluation, not transcription endpoint.
9. Audit Registry: engine/config/source hashes, human decisions, scientific gate states, supersession and checkpoints.

## AI role
AI is an inference/fusion lane, not a source of unmarked truth. It may rank or propose candidates for unresolved acoustic regions using documented evidence and learned/general musical constraints. Every inferred datum must retain AI_INFERRED state until audited/admitted. AI must not silently replace missing measurements.

## Scientific separation
A functional module may be available before scientific admission. Statistical/generative use of a feature remains fail-closed until its relevant measurement/calibration gate is passed. Historical regression recovery and generalization validation are distinct.

## Current regression
`app-hooklab-workbench-v0.1.html` is classified FAILED_REGRESSION_BASELINE for melody-register instability because it invokes the simplified `app/prototype_v1/mie_audio_transcription_engine.js` rather than the recovered Plane Resolver/R1.1/R1.2/R1.3 lineage. It must not become the analytical baseline.

## Development gates
G1 RECOVER_M_T_RUNTIME: identify/freeze executable Plane Resolver/R1.x + Beat This runtime.
G2 CASE_PACKAGE_SCHEMA: version source/event/audit/feature contract.
G3 FEATURE_ENGINE: compute M+T analytical variables with provenance.
G4 CORPUS_STORE: aggregate multiple audited cases.
G5 PATTERN_MODEL: conditioned statistical relationships.
G6 GENERATOR_BRIDGE: feed admitted pattern model into hierarchical pitch/time generator.
G7 AUDIO_COMPARATOR: render and compare generated neutral audio.
G8 GENERALIZATION: blind/unseen-reference validation and gate promotion.

## Definition of tangible integrated milestone
The Workbench can take a corpus/reference case, run the recovered M+T engine, retain uncertainty/audit, calculate a Case Analysis Package and analytical features, add admitted data to a corpus statistical store, derive conditioned pattern evidence, instantiate a constrained new pitch/time realization, synthesize neutral audio, and display the full provenance path from source evidence to generated result.

Current gate: G1 RECOVER_M_T_RUNTIME.
