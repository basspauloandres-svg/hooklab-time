# MIGRATION CHECKPOINT — HookLab/TIME-MIE — 2026-09-04 — MIE Melody Recovery v1

STATUS: `CANONICAL HANDOFF / NO-REPROCESS / FAIL-CLOSED`  
REPOSITORY: `basspauloandres-svg/hooklab-time`  
WORKING BRANCH: `codex/mie-continuity-alignment-v0.3.4`  
LOCAL TIP BEFORE THIS CHECKPOINT: `d59feabd9a9287a51d9bf0bf67fe7d26bb60ed7e`  
PUBLISHED REMOTE v0.3.4 TIP: `6f44f21971d5bf581fc3531215d74c9c856b80c0`

## 0. Start here in a new chat

Read this file completely before proposing, modifying or rerunning anything.
Then read the companion startup prompt and migration manifest. Complete every
mandatory reading listed there in the stated order.

If a referenced artifact is absent, return
`AUDIT_MIGRATION_MISSING_ARTIFACT`. Investigate repository history before any
reconstruction. Do not recreate a missing artifact from conversational memory.

## 1. Immediate handoff decision

MIE v0.3.4 is rejected for baseline promotion after a held-out producer
evaluation on `Animal.mp3`:

- `MELODY_RECOGNITION = FAIL_UNRECOGNIZABLE`;
- `PRODUCER_EVALUATION = FAIL_REGRESSION`;
- `MIE_V0_3_4_BASELINE_PROMOTION = REJECTED`;
- `T = FROZEN_ENGINEERING_BASELINE_PRESERVED`;
- v0.3.3 is a comparison reference, not a validated baseline;
- v0.3.4 must remain accessible for provenance and must not be merged into
  `main`.

The first action in the next chat is:

`BUILD_AND_AUDIT_MIE_V0_3_5_M_ONLY_MELODY_RECOGNIZABILITY_GATE`

The first sub-gate is:

`DIAGNOSE_SOURCE_SEPARATION_VERSUS_NOTE_SENSOR_RECALL`

Do not begin by tuning thresholds, reconnecting AI, changing harmony or
modifying the beat component.

## 2. Why v0.3.4 failed

The evaluated source and package hashes match. File contamination was not
detected.

The final melody contained 215 events and represented 66.68 seconds of a
245.08-second source, corresponding to 27.2% temporal coverage. This is not an
accuracy estimate. The producer reported that the melody was not recognizable,
which is the functional disposition.

The v0.3.4 gap-recovery layer recovered zero additional rejected candidates.
It extended 49 accepted note tails, while 72 melody gaps of at least 500 ms
remained and the longest gap reached 10.19 seconds. The internal uncalibrated
false-silence diagnostic remained 0.561.

The harmony chain began with 481 raw observations, of which 341 were reported
ambiguous before metric aggregation. The final shared-clock layer retained 100
LOCK states and extended each accepted state to the next accepted change,
reaching 97.5% temporal coverage. This reduced audible silence but crossed
ambiguous or unsupported intervals.

The shared-clock alignment shifted zero boundaries although the median distance
from harmony boundaries to melody onsets was 1.23 tactus units. Its
`DERIVED_CANDIDATE` state therefore documented execution, not successful M/H
alignment.

The complete evidence is frozen in:

- `docs/checkpoints/MIE_V0_3_4_ANIMAL_HELD_OUT_REGRESSION_2026-09-04.md`;
- `data/music_modeling/mie_v0_3_4_animal_regression_audit_v1.json`.

## 3. Canonical MIE component state

### M — melody

Status: `RECOVERY_GATE_ACTIVE / CURRENT_CANDIDATE_FAILED_RECOGNIZABILITY`.

Preserve the recovered lineage:

`HTDemucs vocals -> Basic Pitch candidates/contour/onset -> octave-plane
resolution -> continuity classification -> gap recovery candidate -> audible
resynthesis -> producer evaluation`

The historical 13/14 region replay and the producer's earlier approximate 98%
assessment remain contextual evidence only. They do not establish cross-song
accuracy. For `Animal.mp3`, melody accuracy is not estimable without an
independent reference transcription, and the perceptual result is FAIL.

### H — harmony

Status: `SEPARATE_H_ONLY_DEFECT_REGISTERED`.

The accepted architecture remains:

`harmonic source evidence -> pitch-class candidates -> Motor/Reasoner/Motor ->
LOCK/AMBIGUOUS/ABSTAIN -> persistent state -> audible harmony`

The v0.3.4 implementation defect is that accepted LOCK states were held across
ambiguous or absent evidence. Repair this only in a later H-only experiment.
Do not combine it with the first M-only v0.3.5 experiment.

### T — beat/tactus

Status: `FROZEN_ENGINEERING_BASELINE`.

The producer retained the pulse as substantially correct in the held-out run.
Preserve Beat This, the clock-lineage resolver, event timestamps and
fingerprints byte-for-byte between candidate comparisons. A candidate that
changes T receives `NO_PROMOTION_TACTUS_REGRESSION`.

### AI reasoning

Status: `PROVIDER_NOT_CONNECTED`.

`DETERMINISTIC_CONTEXTUAL_REASONER_v1` is a reproducible candidate-ranking
fallback. It may KEEP, QUERY or DROP observed candidates. It cannot create
missing pitch evidence, rewrite timestamps, force LOCK, cure an unrecognizable
melody or set `scientific_d_unlocked=true`.

## 4. Mandatory v0.3.5 experiment design

Follow the one-module-per-experiment rule.

The first v0.3.5 experiment changes M only. H uses the frozen comparison
reference selected before execution, and T remains byte-identical. Register:

- experiment identifier and parent reference;
- changed module: `M_ONLY`;
- source/work-group hashes without title-based model inputs;
- sensor versions and thresholds;
- raw, accepted, rejected and recovered note counts;
- source-separation diagnostics;
- pitch, octave, onset, offset, continuity and silence residuals separately;
- explicit abstention criteria;
- producer recognizability disposition;
- multicase held-out aggregation;
- regression and stop rules.

Do not use temporal coverage, low output silence or CI success as a substitute
for melody recognizability. Do not manufacture notes to force a complete
preview. If the evidence is insufficient, emit
`ABSTAIN_INSUFFICIENT_MELODY_EVIDENCE` and preserve the previous comparison.

The H-only experiment follows after the M gate and must prevent ambiguity
bridging. A state may persist through supported continuation; an ambiguous
interval remains explicit unless independent evidence resolves it.

## 5. Cross-track generalization invariant

Every correction must be expressed through observable musical evidence:
cents, contour support, onset posterior, fractions of tactus, chroma novelty,
state persistence or calibrated equivalents.

Forbidden model inputs:

- title;
- artist;
- filename;
- known transcription;
- hand-entered song timestamps;
- song-specific melody, register, tempo or chord templates.

All versions of one musical work remain in the same evaluation group. The
evaluation unit is an independent held-out track and summaries are
macro-aggregated by track. A single-track improvement cannot establish
generalization. The existing scientific replication target remains at least 30
independent aligned works; before that threshold, a successful multicase run is
at most `ENGINEERING_MULTICASE_SMOKE_PASS`.

## 6. CI and publication state

The v0.3.4 candidate was published to:

`codex/mie-continuity-alignment-v0.3.4`

Remote commit:

`6f44f21971d5bf581fc3531215d74c9c856b80c0`

Remote actions completed with `success`:

- MIE Core Prototype — run `33799581232`;
- MIE Canonical Component Registry — run `33799581347`;
- Lyric Modeling Coherence Contract — run `33799581133`.

CI success proves executable and contract integrity. It does not override the
held-out producer regression. No pull request was opened and `main` was not
modified by this candidate publication.

## 7. Corpus and lyric-science state

This migration supersedes the earlier temporary
`AUDIT_CORPUS_SOURCE_NOT_RESOLVED` status.

Current canonical source status:

`CANONICAL_INTERNAL_RESEARCH_SOURCE_RESOLVED`

The logical HookLab corpus backbone is C001–C100. The synchronized
CorpusBot/LRCLIB-backed workbook, revision 72 dated 2026-07-22, is the living
internal research source. The revision-1 workbook is a frozen mirror and adds
zero independent cases. Original lyrics remain at the authorized provider;
repository manifests contain locators and provenance rather than lyric text.

POD-LC remains methodological/observational background and cannot become
HookLab variables by default. Matrix X and derived matrices remain distinct
layers. Lakh remains `TEST_LANE_ONLY` and cannot substitute for the HookLab
lyric corpus.

The lyric source gate is resolved, while Feature Admissibility remains blocked.
The exact lyric gate is:

`HUMAN_REVIEW_LANGUAGE_PROPOSALS_AND_RESOLVE_DOCUMENT_VERSION_STATUS_FOR_99_ELIGIBLE_CASES`

C077 remains excluded from the maximum 99-case calibration frame unless an
existing authorized complete version is located. No lyric inferential
statistics have been executed, no narrative feature has been admitted and no
conditioned deduction has been promoted.

The MIE melody-recovery work does not authorize advancing lyric statistics.

## 8. Lyric–prosody–MIDI bridge

Treat `LYRIC_PROSODY_MIDI_BRIDGE_ADMISSIBILITY_v1` as
`CANONICAL_ENGINEERING_BRIDGE`.

The four completion criteria are already corroborated by workflow run
`33460601672`:

1. `CURATED_PROSODY_PASS` produces three MIDI variants;
2. every MIDI has traceable mapping JSON;
3. uncurated or automatically inferred prosody fails closed;
4. no output can set `scientific_d_unlocked=true`.

Therefore:

`BRIDGE_STATUS = ENGINEERING_COMPLETE`

Freeze v1. Do not redesign or reimplement it unless `NEW_EVIDENCE=true` or
`BRIDGE_CONTRACT_VERSION > v1`. Preserve:

`WORD -> SYLLABLE -> STRESS -> ONSET -> DURATION_POLICY -> PITCH -> MIDI ->
HUMAN_EVALUATION`

The six TMT variables remain engineering/descriptive scaffold controls and do
not constitute inferential Feature Admissibility.

## 9. Product and interface state

Canonical UI:

`app/prototype_v1/studio.html`

Canonical test URL on `main`:

`https://raw.githack.com/basspauloandres-svg/hooklab-time/main/app/prototype_v1/studio.html`

The producer completed the mobile manual path through Story Brief, section,
three proposals and listening. The proposals remained musically simple and
were not evidence-assisted. This contextual QA result does not establish
scientific validity.

Do not create parallel UI versions. Inspect the canonical file and CI before
any UI edit. The historical truncation repair at commit
`73907a94f63e76e7daa6af9115aad00ebbd1bbaa` remains an integrity warning.

## 10. Scientific and product invariants

Canonical scientific order:

`DATA SAYS -> STATISTICS SAY -> THEORY SAYS -> GENERATION TESTS -> PRODUCER DECIDES`

Mandatory inference chain:

`FEATURE ADMISSIBILITY -> ANALYSIS REGISTRATION -> STATISTICAL TEST`

Only `PROMOTE_TO_CONDITIONED_DEDUCTION` may enter evidence-assisted generation.
Null, weak and unstable results remain legitimate. AI and producer preference
cannot create an empirical trend or override statistical status.

Reference audio is `AESTHETIC_REFERENCE`, not success evidence.
`D0_EXPLORATORY != SCIENTIFIC_D`.

Preserve:

`STORY_BRIEF != SECTION_FUNCTION != LYRIC_CONTENT`

Manual Story Brief remains operational. Evidence-assisted Story Brief remains
fail-closed until legitimate promoted deductions exist.

## 11. Frozen and no-reprocess components

Do not reopen without the stated trigger:

- early chorus analyses;
- repetition/formal architecture already tested;
- raw aggregated vocal range/amplitude family;
- lyric–prosody–MIDI bridge v1;
- T beat/tactus engineering baseline;
- v0.3.1–v0.3.4 outputs and producer dispositions;
- prior null, weak, audit or rejected results.

Reopening a scientific analysis requires `NEW_EVIDENCE=true`, preservation of
the prior result and a new `ANALYSIS_ID`. Reopening the bridge also permits
`BRIDGE_CONTRACT_VERSION > v1`.

## 12. Current management estimate

The last formally recorded integrated-development estimate remains
approximately 79%. It is a management estimate from the 2026-09-01 migration,
not a scientific measurement. This checkpoint does not manufacture a revised
percentage because the MIE v0.3.4 candidate failed its held-out producer gate.

## 13. External session artifacts

The source audio and generated ZIP are intentionally absent from Git:

- `Animal.mp3` — SHA-256
  `75e1dcbaef2fe3d81818df650acf72d98c306f0262bd9e78bbbc911a42a436a0`;
- `MIE_RECOGNITION_v0_3_4.zip` — SHA-256
  `39afd3c980c3d22e4267a33aee33e5f09895d514fbbcccbbe8ab7ef04789d67a`.

Do not ask the user to reattach these files merely to understand the decision;
the audit metrics and hashes are canonical. Request the exact source again only
when a registered replay requires its bytes, and verify its hash before use.

## 14. Stop conditions for the next chat

Stop and report an audit state if:

- a mandatory artifact is missing;
- a proposed repair consumes song identity or known answers;
- T changes between comparisons;
- M and H are changed in the same registered experiment;
- v0.3.4 is treated as a validated baseline;
- CI success is used as evidence of melody accuracy;
- temporal coverage is labeled recognition accuracy;
- ambiguous harmony is silently converted into LOCK;
- AI is represented as connected when `provider_connected=false`;
- a corpus, analysis or bridge is reconstructed despite a frozen artifact.

## 15. Companion files

- `docs/checkpoints/START_NEXT_CHAT_MIE_MELODY_RECOVERY_2026-09-04_v1.txt`
- `docs/checkpoints/MIGRATION_MANIFEST_2026-09-04_MIE_MELODY_RECOVERY_v1.json`
- `docs/checkpoints/MIE_V0_3_4_ANIMAL_HELD_OUT_REGRESSION_2026-09-04.md`
- `data/music_modeling/mie_v0_3_4_animal_regression_audit_v1.json`
