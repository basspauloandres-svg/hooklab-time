# MIE Unified Analysis Engine — Freeze v0.1

Date: 2026-08-27
Status: architectural freeze for continued development.

## Purpose
Preserve the validated direction of a single-audio analysis engine that extracts and integrates melody (M), harmony (H), and beat/tactus (T). Future experiments may replace only the internal implementation of a module; they must not dismantle the unified architecture.

## Frozen top-level architecture

AUDIO UNIQUE INPUT
→ acquisition/decoder
→ M: melody analysis
→ H: harmony analysis
→ T: beat/tactus analysis
→ common physical clock
→ M↔H↔T synchronization
→ unified resynthesis
→ relational analysis layer

## M — Melody module
Current status: active recovery/depuration.

Internal chain:
probabilistic F0 candidate front-end
→ Plane Resolver over octave-related candidates
→ R1.1 voiced-region continuity
→ R1.2 duration-sensitive segmentation
→ R1.3 region-center pitch classification with reduced cents sensitivity
→ conservative score representation

Frozen evidence:
- Historical frame period ≈ 11.609977 ms.
- R1.3 Recovery Harness v0.2: structural PASS from 18 R1.2 events to 14 historical R1.3 regions.
- pYIN/probabilistic YIN is the strongest documentary front-end candidate, identity not yet fully proven.
- Plane Resolver Replay v0.1 on historical Luis Miguel source recovers 13/14 historical regions within ±0.5 semitone without using gold notes during inference.
- Remaining failure must be addressed by generalizable evidence (regional persistence, octave competition, spectral salience, memory through brief gaps), never by song-specific register rules.

## H — Harmony module
Current accepted experimental lineage:
Other stem / harmonic evidence
→ acoustic pitch-class candidates
→ Motor → IA → Motor dialogue
→ spectral residual requery
→ LOCK / AMBIGUOUS / abstain

Relevant preserved artifacts:
- MIE_OTHER_ONLY_v0_1.json
- MIE_OTHER_MOTOR_IA_MOTOR_v0_1.json
- MIE_Harmonic_LOCK_v0_5.json
- MIE_Harmonic_Ear_Real_Tactus_v0_2.json

Rules:
- IA may rank only observed candidates; it cannot invent absent pitches.
- Melody can condition harmony but cannot generate harmony.
- Bass, tactus, melody and spectral evidence are contextual evidence, not hard-coded harmonic truth.
- UNCERTAIN/AMBIGUOUS is a valid output.

## T — Beat/tactus module
Current frozen baseline:
Beat This small pretrained ONNX
→ HookLab continuity/CTL
→ tactus selection
→ deduplication
→ single-clock output

Reference implementation lineage includes app-v1.9.3-pretest and app-mie-decoder-plus-beatthis-v0.1.html.

Rules:
- Beat This remains primary beat detector until new evidence justifies replacement.
- Do not repair playback latency by modifying beat inference.
- Do not reopen metro/downbeat/accent during this integration step.
- T must remain on the same physical clock used by M and H.

## Integration rule
A module may be improved internally only if the API contract to the unified engine remains stable:

M output: time-stamped melody events + confidence/ambiguity
H output: time-stamped harmonic candidate/lock states + confidence/ambiguity
T output: ordered tactus/beat timestamps + confidence/state

All three outputs must preserve original physical time and must not be silently quantized to each other.

## Anti-regression rule
Do not:
- replace M with a simplified frame-max detector;
- replace T with a manual BPM grid;
- replace H with chord labels inferred only from melody;
- reintroduce layered prototype code that contaminates the decoder/runtime;
- use Luis Miguel-specific notes, register, BPM or harmonic progression as decision rules.

## Immediate next gate
1. Complete generic Plane Resolver depuration inside M while keeping current 13/14 historical replay as baseline.
2. Reconnect the improved M module to the already validated T runtime.
3. Reconnect H using the Motor→IA→Motor lineage without changing M or T.
4. Produce one unified resynthesis from a single audio source.
5. Run blind tests on songs not used during development and with contrasting registers/production.

## Acceptance principle
The unified engine is accepted only when improvements generalize across unseen songs. A perfect score on the historical Luis Miguel regression is necessary evidence of recovery but is not sufficient evidence of generalization.
