# Tactus Octave v0.1 — executed synthetic benchmark

Date: 2026-08-20

The resolver was executed on audio-derived spectral-flux event salience from synthetic MB01–MB04 and MB08. No meter/downbeat/accent label is used.

## Results
- MB01 constant 120: BASE_LAYER_SUPPORTED; selected ~120.42 BPM; parity salience ratio 1.016. No false halving.
- MB02 accelerando 80→140: BASE_LAYER_SUPPORTED; descriptive median layer ~115.07 BPM; parity salience ratio 1.079. No false halving.
- MB03 ritardando 140→70: BASE_LAYER_SUPPORTED; descriptive median layer ~110.17 BPM; parity salience ratio 1.008. No false halving.
- MB04 abrupt 120→80: BASE_LAYER_SUPPORTED; descriptive median layer ~120.42 BPM; parity salience ratio 1.005. No false halving.
- MB08 90 tactus / 180 subdivision: HALF_TIME_SUPPORTED; base detected layer ~178.55 BPM; selected tactus ~89.28 BPM; stronger parity salience ratio 3.266; every-other-event regularity essentially zero in the deterministic synthetic audio.

## Interpretation
The synthetic MB08 half/double ambiguity is resolved by an alternating event-salience pattern rather than a fixed BPM range. MB01–MB04 do not trigger the halving rule in this execution.

## Boundary
This is a controlled-benchmark result only. It does not demonstrate general tactus selection in real music where salience alternation can reflect meter, orchestration, syncopation, or production rather than perceptual tactus. Real-audio validation is mandatory before integration.
