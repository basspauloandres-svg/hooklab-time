# Golden Pipeline forensic status v0.3

Date: 2026-08-28

## Confirmed evidence

- Golden audible baseline: `MIE_P30_HARMONIA_BEAT_v0_1(1).wav`.
- Golden SHA-256: `de8381ef9322e73bf295db40a9dffeb0528469502313ea949c4c9018fe9cd940`.
- Golden geometry: mono PCM16, 44.1 kHz, 1,208,340 samples, 27.4 s.
- Recovered executable renderer: `app-mie-p30-harmony-beat-v0.1.html`.
- Renderer SHA-256 recorded by the migration bundle: `8ae79a4c6f92cea9d48a6aea5cd1cc3d4496dbd993e9cf0d229e6fcfcb4c5541`.
- Embedded representation: 72 P30 events, 33 harmony units and 32 Beat This tactus events rendered inside 13.3–40.7 s.
- P30 preserves original physical onsets/offsets; the recovered evidence contains no global onset/duration quantization.
- The migration bundle states that two source-workspace copies of the golden WAV were byte-identical.

## Correction to the previous forensic interpretation

The migration checkpoint explicitly designates the HTML as the recovered exact renderer. That provenance claim remains the official project evidence and must not be downgraded merely because an independent Node.js port failed to reproduce the same PCM hash.

`golden_pipeline/render_recovered_renderer.js` is a portability/reproduction harness, not the historical browser execution itself. Its output SHA-256 is:

`c09f31d3c9eb63ca5142f4cf3eb827ab1540e11959ca073ccd244916292672c4`

The harness output has the same WAV geometry and approximately 0.9555 sample correlation with the golden. This establishes that the port is close but not byte-identical. It does **not** establish that the recovered HTML is a different renderer, nor does it prove that any particular M, H or T synthesis component changed historically. Differences may arise from execution/runtime details that have not yet been isolated.

Therefore the corrected unresolved statement is:

`independent Node.js reproduction harness -> byte-identical golden PCM`

The renderer identity itself remains **RECOVERED/ACCEPTED according to checkpoint provenance**.

## Diagnostic evidence versus hypothesis

A residual spectrum from the non-identical Node.js port showed energy near 1 kHz. The recovered HTML click function uses 1450 Hz plus a 2200 Hz partial. Because the residual contains the combined consequences of all sample-level differences and normalization, this observation cannot by itself identify the beat synthesizer as the cause. Beat-synthesis difference is retained only as an unconfirmed hypothesis and is not an engineering decision.

## Additional bundle component evidence

The migration bundle contains `MIE_OTHER_MOTOR_IA_MOTOR_A_v0_1.wav`, `MIE_OTHER_MOTOR_IA_MOTOR_B_v0_1.wav`, and `MIE_P30_melodia_con_tactus_real_v0_4.wav`. Direct waveform correlations against the golden under zero-lag alignment are approximately 0.454, 0.551 and -0.057 respectively. These comparisons establish only that the files are not zero-lag waveform copies of the golden; they do not by themselves establish causal genealogy or component independence.

## STAB-004 -> P30 status

The current repository assets `mie-stab004-p30-reconstruction-v0.1.js` and `v0.1.2.js` explicitly declare `historical_code_exact:false`. They remain experimental reconstructions rather than recovered historical code.

The migration bundle preserves the final 72-event P30 representation and tactus-relative projection, while the upstream STAB-004 event set and an operation-by-operation historical transformation log have not been recovered in the inspected materials. `MIE_R13_recovery_report_v0_2.json` documents a separate R1.2 -> R1.3 experiment on 14 events and must remain separate from STAB-004 -> P30.

Checkpoint-level historical facts retained as constraints for reconstruction are: approximately 442 events conserved, approximately 16 ornaments removed, five strong octave repairs, original timing retained, and no aggressive global onset quantization. These are constraints on a future generic reducer, not sufficient evidence to recreate the exact historical algorithm.

Thus:

`historical STAB-004 evidence -> exact P30 transformation code` remains **UNRESOLVED**.

## Structural Reduction implementation status

`mie_core/structural_reduction.py` now separates internal hypotheses from renderable events. `AMBIGUOUS` alternatives are preserved in provenance and excluded from `render_events`, preventing unresolved competing pitches from being synthesized simultaneously. Physical start/end times of surviving events remain unchanged.

GitHub Actions run `33219782675` passed all initial structural invariants and executed the first M-only probe on the regression preview. Observed counts were:

- raw Basic Pitch candidates: 91
- retained structural hypotheses: 84
- renderable events before micro-ornament stage: 82
- ambiguous hypotheses: 2
- raw density: approximately 3.062 events/s
- render density: approximately 2.759 events/s
- render/raw ratio: approximately 0.901

The frozen MIE Core v0.2 path produced 83 rendered melody events from the same 91 sensor candidates. Therefore Structural Reduction v0.2 improved formal traceability and ambiguity handling, but its event-count reduction over the previous gate was only one event. It is **not promoted** as a sufficient P30-like reducer on that evidence alone.

A context-relative micro-ornament stage has therefore been added as a separate experimental module. It uses local duration ratios and return-contour evidence rather than fixed song positions. A replay against the run-10 structural output identified one valid small pitch excursion under the unchanged thresholds after correcting a false-positive case in which a same-pitch 59→59→59 fragmentation had initially qualified. The rule now requires a real pitch excursion of at least one semitone.

This replay is engineering evidence only; the current GitHub Actions validation must confirm it on the latest commit before promotion.

## Generic validation

The workflow now contains an isolated `generic-a` M-only job using a contrasting public preview. The same reducer parameters are applied without per-song adjustment. This job exists specifically to prevent Luis Miguel from becoming a parameter source. No generic-song result is yet accepted until the corresponding workflow run completes successfully and its artifact is inspected.

## Frozen engineering rule

Harmony B and Beat This remain frozen while M is reconstructed/substituted. Modern sensor output must pass through a structural-reduction interface before rendering. Luis Miguel remains regression evidence, not a parameter source.

## Golden regression roles

1. The recovered HTML is the executable golden renderer evidence.
2. The golden WAV is the perceptual and artifact baseline.
3. The Node.js harness tests portability/reproducibility and must report any byte mismatch without redefining the historical provenance.
4. Structural/event regression is mandatory even when byte identity is unavailable across runtimes.
5. Promotion still requires the audible golden gate and generic-song validation.

## Current engineering decision

The reducer architecture is retained; the current parameterization is still experimental. Audio audition remains closed. The next accepted milestone requires: latest structural invariants PASS, regression probe PASS, generic-A probe PASS, explicit comparison of density/ambiguity/continuity across both songs, and only then controlled M substitution into the frozen golden H/T integration path.
