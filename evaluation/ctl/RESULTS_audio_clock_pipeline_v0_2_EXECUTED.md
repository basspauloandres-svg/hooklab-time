# Audio-derived clock pipeline v0.2 — executed results

Date: 2026-08-20

This run regenerated the deterministic microbenchmark audio from the repository generator, then passed MB05, corrected MB06b, and MB07 through the audio-derived evidence front-end v0.2 and Phase Restart v0.3. The decision stage did not receive the benchmark case label.

## MB05 — silence/reentry
- gap: 12–18 s
- observed gap active fraction: 0.007722
- detected onset count in file: 62
- final state: `SILENCE`
- confidence: high
- expected state: `SILENCE`
- result: **PASS**

## MB06b — same tempo, true phase restart
- gap: 12–15 s
- tempo: 100 BPM; expected IBI 0.600 s
- observed gap active fraction: 1.000000
- detected onset count in file: 55
- last pre-gap onset: 11.645261 s
- first five post-gap onsets: 15.399546, 15.990499, 16.593039, 17.195578, 17.798118 s
- restart votes: 5/5
- phase errors (cycles): 0.2571, 0.2421, 0.2463, 0.2505, 0.2548
- final state: `CLOCK_STOP_RESTART`
- confidence: high
- expected state: `CLOCK_STOP_RESTART`
- result: **PASS**

## MB07 — attack dropout, continuous internal clock
- gap: 12–20 s
- tempo: 105 BPM; expected IBI ≈0.571429 s
- observed gap active fraction: 1.000000
- detected onset count in file: 49
- last pre-gap onset: 11.680023 s
- first five post-gap onsets: 20.243039, 20.822404, 21.390181, 21.957959, 22.525737 s
- continuation votes: 5/5
- phase errors (cycles): 0.01472, 0.00083, 0.00722, 0.01361, 0.02000
- final state: `CLOCK_CONTINUES`
- confidence: high
- expected state: `CLOCK_CONTINUES`
- result: **PASS**

## Interpretation
The corrected front-end now distinguishes the three controlled states from waveform-derived evidence only: silence, active-audio phase restart, and active-audio attack dropout with clock continuation. This closes the controlled MB05/MB06b/MB07 gate at the synthetic-audio level.

## Boundary
These results do not yet establish generalization to commercial recordings. The next gate is a real-audio pilot while retaining MB01–MB07 as mandatory regression tests.