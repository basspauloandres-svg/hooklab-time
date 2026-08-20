# Clock/Evidence State v0.1 — executed MB05–MB07

Date: 2026-08-20

This execution uses the pre-specified microbenchmark semantics and reference event streams. It tests the state resolver independently from the mobile onset extractor. MB01–MB04 CTL remains frozen as regression baseline.

## Results

### MB05 — silence 12–18 s
- audio activity in gap: absent by construction
- classification: `SILENCE_EVIDENCE_GAP`
- action: `SUSPEND_INFERENCE`
- post-gap tempo: same 120 BPM reference clock
- reacquisition: same-clock after two compatible post-gap intervals
- false tempo transition: **0**
- result: **PASS at state-semantics level**

### MB06 — fermata / clock stop 12–15 s
- reference semantics explicitly mark the clock as stopped and restarted with new phase
- classification: `CLOCK_STOP_RESTART`
- action: `STOP_AND_RELOCK_PHASE`
- pre/post tempo remains 100 BPM; event is not labeled tempo transition
- false tempo transition: **0**
- result: **PASS at state-semantics level**

Important limitation: in real audio, distinguishing fermata from active-audio attack dropout cannot rely on the reference flag used by this controlled test. A phase-restart detector must supply that evidence before mobile integration.

### MB07 — attack dropout 12–20 s with tonal activity and continuing reference clock
- audio remains active by construction
- no reference clock stop
- classification: `LOW_EVIDENCE_CLOCK_CONTINUES`
- action: `PREDICT_THROUGH_GAP`
- same 105 BPM clock retained
- false tempo transition: **0**
- result: **PASS at controlled state-semantics level**

## Regression status
No changes were made to CTL v0.7 MB01–MB04 logic.

## Interpretation boundary
These PASS results demonstrate that the new state representation can express the three controlled cases correctly when given the required evidence variables. They do **not** demonstrate that the current mobile audio front-end can infer those variables from arbitrary music.

## Next correction
Implement an observable phase-restart / clock-stop evidence extractor so MB06 can be distinguished from MB07 without using ground-truth condition labels. Then rerun MB05–MB07 from audio-derived evidence only.