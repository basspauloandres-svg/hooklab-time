# Golden Pipeline forensic status v0.3

Date: 2026-08-27

## Confirmed evidence

- Golden audible baseline: `MIE_P30_HARMONIA_BEAT_v0_1(1).wav`.
- Golden SHA-256: `de8381ef9322e73bf295db40a9dffeb0528469502313ea949c4c9018fe9cd940`.
- Golden geometry: mono PCM16, 44.1 kHz, 1,208,340 samples, 27.4 s.
- Recovered renderer: `app-mie-p30-harmony-beat-v0.1.html`.
- Embedded representation: 72 P30 events, 33 harmony units and 32 Beat This tactus events inside 13.3–40.7 s.
- P30 uses original physical onsets/offsets; no global onset/duration quantization is present in the recovered evidence.
- Migration bundle `MIE_MIGRATION_CHECKPOINT_v0_3` independently records the same golden SHA and renderer SHA `8ae79a4c6f92cea9d48a6aea5cd1cc3d4496dbd993e9cf0d229e6fcfcb4c5541`.
- The migration bundle states that two source-workspace copies of the golden WAV were byte-identical. This strengthens artifact identity, but does not by itself prove that the recovered HTML generates those exact PCM samples.

## Executed reproduction

The recovered renderer was reimplemented line-for-line in `golden_pipeline/render_recovered_renderer.js`, preserving Float32 accumulation, synthesis functions, gains, envelopes, sample rate, window and PCM16 normalization.

Executed output SHA-256:

`c09f31d3c9eb63ca5142f4cf3eb827ab1540e11959ca073ccd244916292672c4`

The output has the same WAV geometry as the golden but is not byte-identical. Sample correlation with the golden is approximately 0.9555; best zero-lag alignment remains at lag 0. Therefore the mismatch is not explained by a simple time shift.

## Decision

The following link remains **UNRESOLVED**:

`recovered HTML synthesis implementation -> exact golden PCM samples`

The migration README calls the HTML the “exact recovered renderer”. That is a source claim and is preserved as such. Executed sample-level evidence currently contradicts byte-exact reproduction, so the stronger causal claim is not promoted until the discrepancy is explained.

The HTML is accepted as strong executable evidence for M/H/T event content, synchronization window and a closely related synthesis design. It is not yet accepted as proof of the exact sample-generating renderer.

## Important diagnostic clue

Residual analysis shows substantial energy near 1 kHz, while the recovered HTML click generator uses 1450 Hz plus a 2200 Hz partial. This is consistent with a possible historical synthesis difference in the beat layer. This clue is diagnostic only; it must not be converted into a replacement rule without recovered evidence or a controlled component-identification experiment.

## Additional bundle component evidence

The migration bundle contains three relevant audio predecessors with preserved hashes: `MIE_OTHER_MOTOR_IA_MOTOR_A_v0_1.wav`, `MIE_OTHER_MOTOR_IA_MOTOR_B_v0_1.wav`, and `MIE_P30_melodia_con_tactus_real_v0_4.wav`. Direct waveform comparison shows that none is simply the golden: correlation is approximately 0.454 with Harmony A, 0.551 with Harmony B, and -0.057 with the P30+tactus file under direct sample alignment. They remain genealogy evidence rather than substitute golden renderers.

## STAB-004 -> P30 status

The files `assets/mie-stab004-p30-reconstruction-v0.1.js` and `v0.1.2.js` were created after the historical P30 recovery. Their metadata explicitly states `historical_code_exact:false`. They are therefore classified as experimental reconstructions, not historical evidence of the STAB-004 -> P30 transformation.

The migration bundle's `MIE_P30_real_tactus_projection_v0_4.json` contains the 72 final P30 events and tactus-relative measurements, but does not contain the upstream STAB-004 event set or an operation log explaining event deletion/repair. `MIE_R13_recovery_report_v0_2.json` documents a separate R1.2 -> R1.3 recovery on 14 events and must not be conflated with STAB-004 -> P30.

The exact historical transformation remains **UNRESOLVED**.

## Frozen engineering rule

Do not modify Harmony B or Beat This while reconstructing/substituting M. Do not promote any modern melody sensor output directly to the renderer. The missing interface is a generic structural reducer between sensor evidence and the final melodic representation.

## Reproduction commands

```bash
node golden_pipeline/render_recovered_renderer.js app-mie-p30-harmony-beat-v0.1.html /tmp/recovered.wav
python golden_pipeline/compare_wav.py /path/to/MIE_P30_HARMONIA_BEAT_v0_1\(1\).wav /tmp/recovered.wav
```

## Next forensic target

Run controlled component identification against the actual golden, beginning with isolated beat-synthesis hypotheses while keeping embedded event times fixed. Separately search repository history and migration artifacts for an upstream STAB-004 event set or transformation log. Until either is demonstrated, both links remain explicitly UNRESOLVED.
