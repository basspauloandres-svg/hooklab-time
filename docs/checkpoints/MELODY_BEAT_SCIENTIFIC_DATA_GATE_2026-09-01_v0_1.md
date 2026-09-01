# HookLab — Melody + Beat Scientific Data Gate v0.1

Date: 2026-09-01  
Status: **FAIL-CLOSED / NO MUSIC-CORPUS STATISTICS EXECUTED**

## Decision

The lyric data-origin invariant now applies independently to melody and beat/rhythm. Every canonical `case_id` must retain separate source, measurement, calibration, feature, statistical-result and provenance layers for each modality.

`SOURCE DATA -> CALIBRATED MEASUREMENT -> FEATURE ADMISSIBILITY -> ANALYSIS REGISTRATION -> STATISTICAL TEST -> THEORY -> GENERATION TEST -> PRODUCER`

Human annotation may establish measurement references. It may not choose, create or rescue an empirical trend. AI, literature and producer preference have the same prohibition.

## Current audit

| Lane | Existing evidence | Scientific gap | Status |
|---|---|---|---|
| Melody | 100 cases indexed; 68 MIDI recovered; 67 selected melody candidates; frozen M pipeline | Verified source identity, exact provider/executable versions, aligned-pair calibration and predeclared median-error tolerance | `AUDIT_MELODY_MEASUREMENT_NOT_CALIBRATED` |
| Beat/rhythm | Beat This detector, frozen tactus resolver, reproducible `mir_eval` evaluator and controlled synthetic lane | Canonical case-linked real audio, independent beat annotations and predeclared calibration thresholds | `AUDIT_BEAT_SOURCE_AND_CALIBRATION_NOT_RESOLVED` |
| Cross-modal | Shared `C001-C100` namespace exists | Verified `case_id` join plus source revision and physical clock; admissible features in every participating lane | `BLOCKED` |

The linked GigaMIDI/Lakh lane is engineering/descriptive only. It is not the missing HookLab lyric corpus, does not enlarge lyric N and does not unlock `SCIENTIFIC_D`. Session audio analyzed as `AESTHETIC_REFERENCE` also stays outside the scientific corpus.

## Created contracts

- `data/music_modeling/melody_beat_feature_registry_v0_1.json`
- `data/music_modeling/melody_measurement_protocol_v0_1.json`
- `data/music_modeling/beat_rhythm_measurement_protocol_v0_1.json`
- `data/music_modeling/analysis_registry/AN-MEL-DESC-001.json`
- `data/music_modeling/analysis_registry/AN-BEAT-DESC-001.json`
- `mie_core/music_statistical_analysis_engine.py`

The two analysis artifacts are blocked candidates, not registered analyses. The numeric engine accepts only finite abstract values from an admissible, calibrated feature and a valid preregistration. A descriptive distribution always returns `NO_PROMOTION`; an inferential/associational contract must be separately preregistered before any conditioned deduction can exist.

## Frozen boundaries

- Preserve `AUDIO -> shared physical clock -> M + H + T -> synchronization`.
- Preserve physical timestamps; one module cannot silently rewrite another module's observations.
- Preserve `generation_class=D0_EXPLORATORY`.
- Preserve `scientific_d_unlocked=false`.
- Do not tune parameters per song.
- Do not infer a population rule from availability of MIDI, synthetic tactus tests or producer listening.

## First unresolved gates

1. Melody: resolve verified source/provenance for the 67 selected candidates and freeze the median-error tolerance before the already required calibration of at least 30 independent aligned pairs; at least one relevant feature must reach Spearman `rho >= .80`.
2. Beat: map canonical real audio and independent beat annotations by `case_id`, then freeze sample size, annotation protocol and metric thresholds before measurement.
3. Only after both lanes independently pass Feature Admissibility may a cross-modal lyric–melody–beat analysis be registered.

No corpus association, trend, conditioned deduction or scientific generation rule was computed in this increment.
