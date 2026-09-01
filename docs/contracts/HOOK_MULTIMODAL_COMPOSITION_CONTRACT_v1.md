# HookLab Multimodal Hook Composition Contract v1

Status: CANONICAL DESIGN CONTRACT
Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`

## Purpose
Freeze the compositional role of lyrics in HookLab before Producer Interface integration is considered complete.

## Canonical definition
A HookLab hook is a multimodal compositional unit:

`HOOK = TEXT + PROSODY + VOCAL_RHYTHM + MELODY + RELATION_TO_BEAT`

Lyrics are not merely metadata attached to an already generated MIDI. HookLab must facilitate original lyric candidates together with prosodic and musical realizations, constrained by the abstract, auditable properties extracted from an aesthetic reference and by any scientifically eligible evidence.

## Required generation chain
`AESTHETIC_REFERENCE`
→ `ABSTRACT_STYLE_FEATURES`
→ `COMPOSITIONAL_CONSTRAINTS`
→ `ORIGINAL_HOOK_CANDIDATES`
→ `TEXT + PROSODY + VOCAL_RHYTHM + MELODY + BEAT_RELATION`
→ `MIDI/AUDIO REALIZATIONS`
→ `PRODUCER_EVALUATION`

The reference is a compositional/style reference, not success evidence and not permission to copy protected expression.

## Reference-derived admissible compositional constraints
Reference analysis may describe, when measurable and provenance-complete:
- tempo and beat grid;
- metric placement of vocal attacks;
- phrase/measure relationship;
- syllabic density and phrase density;
- distribution of durations and rests;
- abstract melodic contour/range descriptors when representation is calibrated;
- repetition/contrast patterns as descriptive style properties;
- hook phrase length and text/rhythm interaction;
- other abstract properties that pass the applicable feature/measurement gate.

These constraints must not reproduce lyric phrases, distinctive melodic sequences, or other protected expressive material from the reference.

## Lyric generation requirement
HookLab must support two routes:

### GENERATIVE_ASSISTED
HookLab proposes original hook-text candidates and an explicit prosodic realization compatible with the current beat/melody constraints. Generated prosody must be labeled `GENERATED_PROSODY_CANDIDATE` until accepted or edited by the producer.

### CURATED_INPUT
The producer supplies or edits text, syllabification and stress. After explicit acceptance it may become `CURATED_PROSODY_PASS`.

The existing curated-prosody bridge remains valid as an audit/realization layer, but it is not sufficient by itself to satisfy HookLab's compositional requirement.

## Mandatory traceability
Every realized candidate must preserve:
`reference_id`
→ `abstract_style_feature_ids`
→ `constraint_set_id`
→ `hook_id`
→ `text_candidate_id`
→ `word`
→ `syllable`
→ `stress`
→ `onset`
→ `duration`
→ `pitch`
→ `variant_id`
→ `MIDI/audio artifact`
→ `producer_evaluation_id`.

## Scientific boundary
The statistical invariant remains binding:
`Feature Admissibility → Analysis Registration → Statistical Test`.

Aesthetic-reference features may guide D0 exploratory composition without being represented as population-level success evidence. A positive scientific creative rule may only enter `SCIENTIFIC_D` after the full promotion gate.

Therefore:
- `D0_EXPLORATORY != SCIENTIFIC_D`;
- `AESTHETIC_REFERENCE != SUCCESS_EVIDENCE`;
- producer preference does not retroactively prove population success;
- a null scientific result does not prevent exploratory composition;
- no positive rule may be fabricated to unlock MIDI/audio.

## Producer authority
The producer may ACCEPT, MODIFY, REJECT or REQUEST_VARIATION for each multimodal candidate. Producer decisions are human creative evaluation and must remain separated from population-level scientific claims.

## Completion implication
Producer Interface v0.6 cannot be considered the final lyric integration because it only realizes curated prosody against existing D0 events. Completion requires a generative-assistance layer that proposes original text/prosody candidates conditioned on the beat/melody/style-constraint state, followed by explicit producer curation and the existing auditable MIDI realization bridge.
