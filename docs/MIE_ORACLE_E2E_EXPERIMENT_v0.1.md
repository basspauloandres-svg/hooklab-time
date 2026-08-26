# MIE ORACLE E2E EXPERIMENT v0.1

Status: EXPERIMENTAL / NOT BASELINE
Date: 2026-08-26

## Purpose

Demonstrate the minimum end-to-end architecture required by MIE before replacing the external source separator.

## Authoritative inputs

- Source separation oracle: Moises stems from the same aligned recording.
- Beat/tactus: Beat This v1.9.3 approved baseline.
- Melody representation: P30-SCORE-002 recovered representation / melody-engine reference.
- Harmony input: `Other` stem only for the current harmonic experiment.
- Harmonic inference: Motor -> musical contextual prior -> Motor re-query.

## Explicit exclusions

This experiment does not attempt to train or replace the source separator. It does not inherit v0.5 LOCK, v0.6 melody subtraction, STEM ORACLE pitch-class aggregation, or other abandoned prototype logic. Previous experiments are evidence/control only.

## Architecture under test

```text
FULL AUDIO
    |
    +--> SOURCE SEPARATOR ORACLE (Moises)
    |       |
    |       +--> VOICE ----------> MELODY ENGINE / P30-type representation
    |       |
    |       +--> OTHER ----------> HARMONIC SENSOR <-> MUSICAL AI <-> SENSOR
    |       |
    |       +--> BASS -----------> BASS EVIDENCE (reserved; not yet fused)
    |
    +--> BEAT THIS v1.9.3 -------> TACTUS COORDINATES

Outputs remain separate until each engine is validated.
```

## Current empirical observations

1. Analysis of the complete mix produced an approximate harmonic reconstruction but admitted spurious notes.
2. Organizing harmonic evidence with the approved tactus improved temporal intelligibility.
3. A contextual Motor-AI-Motor pass improved the perceptual harmonic result relative to the raw sensor.
4. Combining bass + guitars + Other did not improve the reconstruction in the STEM ORACLE test.
5. Restricting harmonic analysis to the Moises `Other` stem produced a substantially clearer harmonic reconstruction in the evaluator's perceptual judgment.
6. Applying Motor-AI-Motor directly to `Other` improved it further by removing part of the leaked-note problem.

These observations are experimental and do not establish general performance beyond the current recording.

## Immediate validation target

Do not refine chord labels, voice leading, tonal function, or style priors yet.

First validate three independent channels:

### T — Time
Beat This v1.9.3 provides stable tactus coordinates.

### M — Melody
Voice stem -> melody engine -> representation comparable with P30-SCORE-002.

### H — Harmony
Other stem -> harmonic sensor -> Motor-AI-Motor -> reconstructed harmonic audio.

Success condition: T, M, and H can be produced automatically from aligned oracle stems without manual editing inside each engine.

## Later integration

Only after T, M, and H are independently stable:

1. align all representations on the same absolute timeline;
2. introduce bass evidence;
3. allow cross-engine queries without allowing one engine to overwrite another's observations;
4. infer tonal center and harmonic function;
5. evaluate full transcription against the recording.

## Separator replacement criterion

Moises is a temporary oracle, not a required final dependency.

An automatic/open separator can replace it only if its outputs preserve downstream MIE utility. The primary criterion is not generic SDR alone. It is whether:

- vocal output supports reliable melody extraction;
- Other/piano output supports harmonic Motor-AI-Motor reconstruction;
- bass output preserves useful low-frequency pitch evidence;
- alignment remains stable enough for Beat This coordinates.

## Engineering rule

GitHub is the experimental laboratory and artifact store. Chat is used for reasoning, audit, experimental decisions, and perceptual reports. New experiments must be autonomous implementations of the tested principle rather than accumulated patches over prior prototypes.
