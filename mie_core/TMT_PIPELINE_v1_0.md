# HookLab-TIME TMT Pipeline v1.0

Purpose: convert each song into comparable Text-Melody-Time evidence before corpus statistics and route analysis/generation to an empirically relevant genre/style cohort.

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
17. Genre/style metadata registration
18. Genre/Style Cohort Router
19. Local Corpus Reference Model for the selected cohort
20. Structural fingerprint comparison or generation constraints derived from validated cohort data

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
- Genre and style are routing variables: they select the empirical cohort to be loaded; they do not predetermine what musical features are favorable.
- The global corpus registry remains lightweight. Full fingerprints, local statistics and validated models are loaded only for the active cohort and may be released after the request.
- Cohort fallback is hierarchical: `genre+style` -> `style` -> `genre` -> broader compatible cohort. If sample support remains insufficient, return `DESCRIPTIVE_ONLY_NEEDS_MORE_DATA`.
- A local cohort may guide inference or generation only through statistics that satisfy the Data First Guard.
- No arbitrary global similarity or success score may be introduced during cohort routing.

## Pilot parameters
- Fragmentation pitch spread: <= 1 semitone.
- Fragmentation gap: <= 80 ms.
- Nucleus/event boundary tolerance: 180 ms.
- Internal recurrence profile: 10 normalized position bins.
- Salience weights remain exploratory and are not frozen for inferential use.

## Memory architecture
### Global registry
Keep only lightweight routing metadata in active memory/index form, such as:
- `song_id`
- genre labels
- style labels
- year/period where available
- market/territory where available
- pointer to structural fingerprint
- pointer to cohort/reference shard

### Active cohort memory
Load on demand only:
- selected fingerprints
- local Corpus Reference Model
- validated cohort-specific statistical models
- minimal provenance required for audit

The active cohort is request-scoped and should be released when no longer needed.

## Data-first control
The cohort router narrows the population. It does not choose the answer. The mandatory direction remains:

`DATA -> STATISTICAL STRUCTURE -> PATTERN -> CONTRAST -> VALIDATION -> DECISION`

Genre/style requests therefore mean: select the empirically relevant data range and let that range determine its statistical structure.

## Generalization gate
The next song is processed with this pipeline unchanged. Failures are documented before parameters are modified. The schema is promoted to corpus-ready only after multi-song regression.
