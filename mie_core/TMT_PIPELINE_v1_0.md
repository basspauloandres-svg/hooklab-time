# HookLab-TIME TMT Pipeline v1.0

Purpose: convert each song into comparable Text-Melody-Time evidence before corpus statistics.

## Frozen order
1. Source provenance
2. Text documentary observation
3. M sensor
4. M structural reduction
5. M plane resolution
6. Text-window alignment
7. Acoustic syllable-nucleus detection
8. Syllable-melody boundary refinement
9. T: Beat This tactus
10. TMT relational alignment
11. Text repetition grouping
12. Multimodal recurrence
13. Internal recurrence profile
14. Contextual salience
15. Feature vector
16. Quality control

## Frozen rules
- H is `FROZEN_CONTEXTUAL_ONLY`.
- Text never sets pitch.
- Syllable evidence may merge M boundaries only when independent onset and pitch-continuity evidence agree.
- Beat This tactus is not automatically a downbeat.
- Metric phase may remain `AMBIGUOUS`.
- Uncertain events are recorded, never silently corrected.
- Single-song measurements are not success predictors.
- Statistical relevance must emerge from the corpus.
- No song-specific threshold tuning is permitted before the first unchanged generalization run.

## Pilot parameters
- Fragmentation pitch spread: <= 1 semitone.
- Fragmentation gap: <= 80 ms.
- Nucleus/event boundary tolerance: 180 ms.
- Internal recurrence profile: 10 normalized position bins.
- Salience weights remain exploratory and are not frozen for inferential use.

## Generalization gate
The next song is processed with this pipeline unchanged. Failures are documented before parameters are modified. The schema is promoted to corpus-ready only after multi-song regression.
