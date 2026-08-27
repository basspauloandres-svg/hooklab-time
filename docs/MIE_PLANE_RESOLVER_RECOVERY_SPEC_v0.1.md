# MIE Plane Resolver Recovery Spec v0.1

Date: 2026-08-27
Status: experimental specification; do not promote to baseline until regression passes.

## Purpose
Recover the missing stage between probabilistic F0 evidence and the historically accepted R1.x melody representation. This stage addresses octave/plane ambiguity without altering R1.3 post-segmentation rules.

## Frozen evidence
- Historical temporal grid: 11.609977324263 ms. Timestamp evidence alone does not distinguish 44.1 kHz/512 from 22.05 kHz/256.
- R1.3 Recovery Harness v0.2: structural PASS (18 R1.2 events -> 14 recovered; 14/14 near matches), not parametric PASS.
- Historical D0 uses a continuous `voicing_probability` field.
- F0/Voicing Fingerprint Audit v0.1 ranks pYIN/probabilistic YIN as the strongest documentary candidate, but identity is unproven.
- Direct pYIN replay on the mixed Luis Miguel source shows correct local pitch in several regions and octave/subharmonic failures in others.

## Core hypothesis
The missing resolver does not invent melody notes. It selects among octave-related F0 hypotheses and preserves a locally coherent melodic plane before R1.1/R1.2/R1.3 aggregation.

## Candidate state per frame
For each voiced frame with raw MIDI estimate m(t), construct octave-related candidates:

C(t) = {m(t)-24, m(t)-12, m(t), m(t)+12, m(t)+24}

subject to a broad vocal/melodic admissible range. No candidate is accepted solely because it lies in a preferred octave.

## Evidence terms
Each candidate receives a score from independent evidence terms:
1. Acoustic evidence: pYIN voiced probability / F0 probability where available.
2. Local continuity: distance from the recent melodic trajectory.
3. Persistence: support across neighboring frames.
4. Octave ambiguity penalty: discourage rapid ±12/±24 flips unsupported by persistence.
5. Region consistency: favor the plane supported by the median/robust center of the current voiced region.
6. Silence/reset logic: after a sufficiently long unvoiced gap, reduce continuity prior rather than forcing the previous register.

## Sequence model
Use dynamic programming/Viterbi over octave-plane candidates plus silence. The resolver must operate before R1.1/R1.2/R1.3 event consolidation.

Provisional objective:

score(c_t) = acoustic(c_t) + persistence(c_t) + region(c_t)
             - lambda1 * local_jump(c_{t-1}, c_t)
             - lambda2 * unsupported_octave_flip(c_{t-1}, c_t)

All lambdas are experimental parameters and must be selected by historical regression, not by listening to new songs.

## Regression target
The resolver is acceptable only if, on the historical Luis Miguel fragment, the full chain approaches:

AUDIO -> probabilistic F0 -> PLANE RESOLVER -> R1.1 -> R1.2 -> R1.3

and reproduces the preserved R1.3 gold events in:
- event count,
- MIDI pitch,
- temporal boundaries on the recovered frame grid,
- region pitch centers,
- voicing summaries.

## Anti-overfit rule
The 14 R1.3 gold notes may be used only for scoring candidate parameterizations after inference. They must never be injected as pitch templates or register targets during decoding.

## Stop conditions
Reject a candidate resolver if it:
- achieves pitch agreement by hard-coding the historical register;
- suppresses genuine short notes to reduce octave errors;
- changes R1.3 rules to compensate for front-end errors;
- performs well only after manual correction of the source.

## Next implementation
Build a replay harness that accepts the historical audio, runs probabilistic F0 on the frozen 11.609977 ms grid, decodes octave-plane candidates by Viterbi, then reports blind regression against R1.3 gold. Do not add Beat This or harmony during this experiment.
