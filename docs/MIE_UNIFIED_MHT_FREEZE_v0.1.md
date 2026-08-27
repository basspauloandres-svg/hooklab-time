# MIE Unified M+H+T Freeze v0.1

Date: 2026-08-27
Status: frozen integration architecture.

## Non-regression rule
The project must not return to isolated replacement prototypes that discard previously validated M, H, or T behavior. Refinement occurs inside a module; the unified pipeline remains intact.

## Pipeline
AUDIO (single source)
→ shared physical clock
→ M melody module
→ H harmony module
→ T beat/tactus module
→ M↔H↔T synchronization
→ unified resynthesis
→ relational analysis.

## M — melody
Current recovery baseline:
- probabilistic F0 candidate family: pYIN remains strongest documentary candidate; identity not fully proven;
- frame period: 11.609977324263 ms frozen;
- octave-plane candidate resolver before R1.x;
- R1.1 continuity/voiced-region logic;
- R1.2 duration-aware segmentation;
- R1.3 region-center/cents classification;
- historical recovery: 13/14 regions within ±0.5 semitone under blind plane inference; unresolved region remains ambiguity, not a hard-coded correction.

M may be refined internally, but must not be replaced by a simple framewise peak detector.

## H — harmony
Preserve the Motor↔IA↔Motor architecture already validated experimentally:
- observation from audio/spectral evidence first;
- bass/context/function can constrain chord hypotheses;
- AI assists candidate ranking and note inclusion/exclusion;
- output must retain LOCK/AMBIGUOUS behavior when evidence is insufficient;
- no chord may be inferred solely from the melody or from a preloaded song template.

H may be refined internally without replacing the unified output.

## T — beat/tactus
Primary detector: Beat This neural inference from the same audio source.
- preserve the validated decoder + Beat This runtime;
- no fixed BPM/metronome may replace T;
- T supplies temporal evidence to M and H after independent observation.

## Shared-clock rule
M, H and T retain physical timestamps from the same decoded audio. Cross-module interaction may refine confidence/interpretation but must not rewrite raw observations.

## Layer rule
Do not stack old experimental pages or engines. Each unified release is rebuilt from frozen module interfaces and currently accepted implementations. Previous prototypes remain regression references only.

## Next gate
Produce a unified audible prototype from one audio source containing:
1. melody resynthesis from current M;
2. harmony resynthesis from current H;
3. Beat This click/tactus from T;
4. one synchronized output.

Acceptance is auditory recognition plus exported machine-readable M/H/T report. A module-specific imperfection is reported explicitly and does not justify dismantling the integrated pipeline.