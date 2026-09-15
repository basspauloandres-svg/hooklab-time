# HookLab Workbench MVP v0.1

Date: 2026-09-15
Status: IMPLEMENTATION_SPEC

## Product objective
Turn the existing HookLab/TIME/MIE research into a concrete producer-facing instrument without weakening scientific traceability. The workbench is an executable research instrument, not a replacement for the corpus, calibration, or methodological gates.

## First usable workflow
`LOAD REFERENCE AUDIO -> ANALYZE -> AUDITION -> INSPECT TRACE -> APPROVE/REJECT -> FREEZE RESULT`

The producer-facing experience prioritizes listening. Technical JSON/MIDI/diagnostics remain available for traceability but are secondary to the audition interface.

## MVP screen
One local/browser workbench with:
1. Reference audio loader.
2. Case/source identity panel.
3. Physical-time melody extraction using frozen/selected MIE implementation.
4. Neutral resynthesis player for extracted melody.
5. Optional stable pulse guide kept separate from melody extraction.
6. A/B player: original excerpt versus resynthesized melody.
7. Event table: pitch, onset_s, offset_s, duration_s, confidence and provenance.
8. Producer decision: APPROVE / REJECT.
9. Export: versioned JSON + MIDI where valid + audit manifest.
10. Gate/status panel showing CANONICAL_CURRENT, EXPERIMENTAL, AUDIT_PENDING or BLOCKED states.

## Golden-case acceptance target
First operational target: `Devuélveme El Amor(1).mp3` / Luis Miguel, preserving the recovered project checkpoint. P30-SCORE-002 may be used as recovered historical comparison evidence, never silently as independent ground truth.

The first milestone is reached when the user can load the golden-case audio, press Analyze, hear the extracted/resynthesized melody, compare it against the source, inspect the event trace, and approve or reject the result without manually editing notes.

## Scientific boundary
The workbench may expose experimental outputs before corpus-level calibration is complete, provided their state is visible and they cannot be promoted to scientific evidence automatically. CAL-MEL-001 remains the calibration gate for admissibility of the registered melody measurement features. Product usability and scientific admissibility are separate states.

## Implementation order
MVP-01: executable local/browser shell + audio load/playback.
MVP-02: integrate recovered MIE physical-time event representation.
MVP-03: neutral melody resynthesis + A/B audition.
MVP-04: event/provenance trace + approve/reject.
MVP-05: versioned export and automatic audit manifest.
MVP-06: calibration/reference panel for CAL-MEL-001.
MVP-07: corpus statistics dashboard only after measurement gates pass.
MVP-08: constrained hook generator only after relevant statistical evidence is admitted.

## Anti-reprocessing rules
- Every executable build receives a version.
- Every analysis stores source identity/hash, engine version/config, event output and decision.
- Experimental output never overwrites canonical output.
- A failed build remains reproducible and is marked superseded/failed rather than deleted from history.
- One variable changes per controlled experiment when comparing engine behavior.
- Chat instructions do not alter engine behavior until represented in versioned configuration/code.

## Definition of done for first visible tool
A user-facing executable/browser artifact exists and can complete the golden-case workflow end to end. Documentation alone does not satisfy this milestone.
