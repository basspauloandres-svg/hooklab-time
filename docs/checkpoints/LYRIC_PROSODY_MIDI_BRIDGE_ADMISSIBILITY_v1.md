# Lyric–Prosody–MIDI Bridge Admissibility v1

Status: CANONICAL ENGINEERING BRIDGE
Branch: `mie/golden-forensic-v0.3`

## Purpose
Close the previously incomplete interface between text/prosody and MIDI while preserving the statistical no-reprocess invariant and the distinction `D0_EXPLORATORY != SCIENTIFIC_D`.

## Existing evidence boundary
The Lakh lyric full-song lane is an engineering test lane containing synchronized MIDI text events and symbolic melody/rhythm. It is explicitly `TEST_LANE_ONLY; NOT MASSIVE_HIT_EVIDENCE`. Its descriptive constraints cannot be promoted as population success rules.

## Feature admissibility disposition
The following existing TMT variables may be used only as engineering/descriptive scaffold controls in this bridge:
- `tempo_bpm`
- `melodic_register_midi`
- `melodic_range_semitones`
- `melodic_events_per_token`
- `near_tactus_share`
- `text_line_count`

They are **not admitted for new inferential testing by this component**. Any future inferential use must receive a complete Feature Admissibility Record and Analysis Registration under `STATISTICAL_ANALYSIS_NO_REPROCESS_INVARIANT_v1.md`.

## Prosody contract
The bridge requires an explicit curated hook representation:
- `HOOK_ID`
- `LANGUAGE`
- line text
- word boundaries
- syllable segmentation
- lexical/performative stress declaration
- provenance
- `prosody_status=CURATED_PROSODY_PASS`

Automatic syllabification/stress inference is not accepted by this v1 bridge. Missing or unreviewed prosody must fail closed.

## Traceability invariant
Every generated note must be traceable through:

`WORD -> SYLLABLE -> STRESS -> ONSET -> DURATION_POLICY -> PITCH -> MIDI -> HUMAN_EVALUATION`

Extra note events allocated to one syllable are recorded explicitly as melisma events.

## Generation class
All outputs from this bridge remain:

`generation_class=D0_EXPLORATORY`
`scientific_d_unlocked=false`

A null/non-promotion statistical closure must never be circumvented by this bridge. A future `SCIENTIFIC_D` path requires its own eligible conditioned deduction and provenance gate.

## Scientific interpretation
`DATA_SAYS`: this component receives curated text/prosody and an existing structural scaffold.
`STATISTICS_SAY`: nothing new; no inferential statistics are executed here.
`THEORY_SAYS`: text/prosody and musical realization remain conceptually separate layers connected by an explicit mapping rather than post-hoc statistical mining.
`GENERATION_TESTS`: three D0 variants may be realized with lyric meta-events and syllable-to-note mapping.
`PRODUCER_DECIDES`: the producer evaluates musical adequacy; that decision is not back-projected as evidence of market success.

## Completion criterion
The component is engineering-complete when CI confirms:
1. valid curated prosody produces three MIDI variants;
2. every MIDI has a traceable mapping JSON;
3. uncurated/auto-inferred prosody fails closed;
4. outputs cannot unlock `SCIENTIFIC_D`.
