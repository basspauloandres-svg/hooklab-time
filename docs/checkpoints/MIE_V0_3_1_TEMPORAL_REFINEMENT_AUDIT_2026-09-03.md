# MIE v0.3.1 — Temporal refinement audit

Date: 2026-09-03
Status: candidate implementation; producer A/B and multicaso regression pending.

## Source evidence

- Source audio SHA-256: `3ddc366cfd6be56ccb8742b9430709881a1e040b25f7d7e31f608e0b3cac4106`.
- Submitted v0.3 package SHA-256: `a29b5156442191a48f4b24c4b977b236b3372d255afd520235fb3edc44231fbc`.
- Duration: 281.7973696145125 seconds.
- v0.3 output: 495 accepted melody events, 544 post-threshold Basic Pitch candidates, 517 Beat This observations, and 518 beat-synchronous harmony units.
- Harmony states: 183 `LOCK`; 335 `AMBIGUOUS`.

The audio hash equals the package `reference_sha256`, so the submitted source and the successful Colab execution are traceably identical.

## Observed limitations

### T — pulse/tactus

The v0.3 report contains 81 adjacent Beat This intervals below 0.4 seconds between 30 and 100 seconds. From 100 seconds onward, the detected layer is stable around a 0.56-second interval, or 107.142857 BPM. The previous resynthesis also accented every fourth array element without downbeat evidence.

An offline application of the candidate clock-lineage resolver to the preserved v0.3 observations yields 431 tactus events across four evidence-acquired runs. It retains 416 observed events, adds 15 explicitly marked low-evidence clock deductions, and keeps the median resolved tempo at 107.142857 BPM. This is an engineering simulation on one case, not a calibration result.

### M — melody

The v0.3 package reports 49 fewer accepted events than post-threshold candidates. Its exported Basic Pitch MIDI contains 552 note events, 57 of which do not match the accepted monophonic layer; 46 of those fall in MIDI 48–84. MIDI velocity is not equivalent to Basic Pitch confidence, so the package alone cannot validly promote those events back into the melody.

v0.3.1 therefore performs recovery inside the original runtime, where confidence and temporal evidence remain available. A candidate is added only inside a short bounded gap, with evidence on both sides, pitch continuity and explicit `RECOVERED_CANDIDATE` provenance. It never assigns curated status.

### H — harmony

The v0.3 harmony sensor evaluates one unit per raw beat boundary. The candidate layer retains all raw units and aggregates only `LOCK` evidence between metrically strong boundaries. Meter and strong-time alignment remain fail-closed until Beat This downbeat observations reach a consistent `METRIC_LOCK`.

## Implemented candidate changes

1. Preserve raw Beat This observations separately from resolved tactus.
2. Integrate a Python clock acquisition/continuity layer derived from the existing HookLab TIME clock lineage.
3. Capture Beat This downbeat output and require consistent meter evidence before strong-time alignment.
4. Remove the synthetic `index % 4` downbeat assumption from both resynthesis paths.
5. Preserve raw accepted melody and identify every added event as `RECOVERED_CANDIDATE`.
6. Add audition-only micro-legato of at most 45 ms across short, pitch-compatible gaps without changing source timestamps.
7. Preserve raw harmony and expose `HARMONY_METRIC_ALIGNED` as a separate derived layer.
8. Keep `generation_class=D0_EXPLORATORY` and `scientific_d_unlocked=false`.

## Gate

Current disposition: `ENGINEERING_CANDIDATE_AWAITING_PRODUCER_AB_AND_MULTICASE_REGRESSION`.

This increment does not establish a 98% accuracy claim, Feature Admissibility, a population tendency, or scientific promotion. The next evidence is a producer A/B comparison on the same source followed by blind multicaso regression with independent reference annotations.
