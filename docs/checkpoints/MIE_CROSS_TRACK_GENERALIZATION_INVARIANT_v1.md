# MIE Cross-Track Generalization Invariant v1

STATUS: CANONICAL ENGINEERING VALIDATION GATE / FAIL-CLOSED

## Purpose

A track may reveal a failure mode. It may not define a track-specific repair.
Every MIE correction must be expressed through observable musical evidence and
must be evaluated on complete held-out tracks before baseline promotion.

## Non-negotiable rules

1. Title, artist, filename, known transcription, hand-entered timestamps and
   song-specific melodic or harmonic templates are forbidden model inputs.
2. All excerpts, mixes, covers and alternate versions belonging to one musical
   work remain in one group and in one split.
3. The evaluation unit is an independent held-out track. Frame pooling is
   forbidden for promotion decisions; summaries are macro-aggregated by track.
4. Parameters are expressed in physical or normalized musical units: cents,
   fractions of tactus, contour support, onset posterior, chroma novelty and
   state persistence.
5. The frozen T component must remain unchanged. A candidate that changes its
   beat count or timestamps receives `NO_PROMOTION_TACTUS_REGRESSION`.
6. Insufficient evidence produces `ABSTAIN_INSUFFICIENT_EVIDENCE` and selects
   the prior baseline for that track.
7. Raw sensor observations are immutable. Candidate substitutions, continuity
   decisions and harmony persistence remain derived layers with provenance.
8. Synthetic tests prove contract behavior only. They do not prove musical
   generalization.
9. A single-track gain receives `HOLD_TRACK_SPECIFIC_GAIN`.
10. `GENERALIZATION_PASS` requires the predeclared scientific replication
    target of at least 30 independent aligned tracks. Until then, a successful
    multicase run is `ENGINEERING_MULTICASE_SMOKE_PASS`.

## Required evaluation sequence

1. Freeze implementation and thresholds.
2. Hash track and work-group identities.
3. Keep every work-group in a single split.
4. Run leave-one-track/group-out evaluation when the sample permits it.
5. Report one residual vector per track.
6. Macro-aggregate track results.
7. Apply preservation, non-inferiority and replication gates.
8. Preserve producer listening as a separate evaluation layer.

## Current v0.3.3 scope

- M: classify boundaries as sustain continuation, new articulation, pitch
  transition or abstention using contour/onset evidence and tactus-relative
  intervals.
- H: represent harmony as a persistent state; identical adjacent LOCK windows
  are coalesced while ambiguous units remain explicit.
- T: frozen and byte-for-byte comparable at the event level between A and B.

The current diagnostic track may enter the frozen regression lane only. It may
not be the sole calibration source and cannot establish general accuracy.

## Scientific boundary

All outputs remain `D0_EXPLORATORY` with `scientific_d_unlocked=false`.
Engineering completion, producer preference and generalization smoke tests do
not constitute inferential Feature Admissibility.
