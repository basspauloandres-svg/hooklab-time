# Golden Pipeline forensic status v0.3

Date: 2026-08-27

## Confirmed evidence

- Golden audible baseline: `MIE_P30_HARMONIA_BEAT_v0_1(1).wav`.
- Golden SHA-256: `de8381ef9322e73bf295db40a9dffeb0528469502313ea949c4c9018fe9cd940`.
- Golden geometry: mono PCM16, 44.1 kHz, 1,208,340 samples, 27.4 s.
- Recovered renderer: `app-mie-p30-harmony-beat-v0.1.html`.
- Embedded representation: 72 P30 events, 33 harmony units and 32 Beat This tactus events inside 13.3–40.7 s.
- P30 uses original physical onsets/offsets; no global onset/duration quantization is present in the recovered evidence.

## Executed reproduction

The recovered renderer was reimplemented line-for-line in `golden_pipeline/render_recovered_renderer.js`, preserving Float32 accumulation, synthesis functions, gains, envelopes, sample rate, window and PCM16 normalization.

Executed output SHA-256:

`c09f31d3c9eb63ca5142f4cf3eb827ab1540e11959ca073ccd244916292672c4`

The output has the same WAV geometry as the golden but is not byte-identical. Sample correlation with the golden is approximately 0.9555; best zero-lag alignment remains at lag 0. Therefore the mismatch is not explained by a simple time shift.

## Decision

The following link remains **UNRESOLVED**:

`recovered HTML synthesis implementation -> exact golden PCM samples`

The HTML is accepted as strong executable evidence for M/H/T event content, synchronization window and a closely related synthesis design. It is not yet accepted as proof of the exact sample-generating renderer.

## Important diagnostic clue

Residual analysis shows substantial energy near 1 kHz, while the recovered HTML click generator uses 1450 Hz plus a 2200 Hz partial. This is consistent with a possible historical synthesis difference in the beat layer. This clue is diagnostic only; it must not be converted into a replacement rule without recovered evidence or a controlled component-identification experiment.

## STAB-004 -> P30 status

The files `assets/mie-stab004-p30-reconstruction-v0.1.js` and `v0.1.2.js` were created after the historical P30 recovery. Their metadata explicitly states `historical_code_exact:false`. They are therefore classified as experimental reconstructions, not historical evidence of the STAB-004 -> P30 transformation.

The exact historical transformation remains **UNRESOLVED**.

## Frozen engineering rule

Do not modify Harmony B or Beat This while reconstructing/substituting M. Do not promote any modern melody sensor output directly to the renderer. The missing interface is a generic structural reducer between sensor evidence and the final melodic representation.

## Reproduction commands

```bash
node golden_pipeline/render_recovered_renderer.js app-mie-p30-harmony-beat-v0.1.html /tmp/recovered.wav
python golden_pipeline/compare_wav.py /path/to/MIE_P30_HARMONIA_BEAT_v0_1\(1\).wav /tmp/recovered.wav
```

## Next forensic target

Recover earlier synthesis code or component outputs that can explain the sample-level difference, while separately locating direct evidence of the historical STAB-004 -> P30 reduction. Until either is demonstrated, both links remain explicitly UNRESOLVED.
