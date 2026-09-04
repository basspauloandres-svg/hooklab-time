# MIE v0.3.5 — M-only melody recognizability gate — 2026-09-04 v1

Status: `ENGINEERING_DIAGNOSTIC_IMPLEMENTED / AWAITING_REGISTERED_MULTICASE_AUDIO_AND_PRODUCER_LISTENING`

## Scope

This increment implements the first registered v0.3.5 sub-gate:
`DIAGNOSE_SOURCE_SEPARATION_VERSUS_NOTE_SENSOR_RECALL`. The changed module is
`M_ONLY`; H remains the predeclared v0.3.3 comparison reference and T must be
byte-equivalent between comparisons.

MIE v0.3.4 remains rejected for baseline promotion. Its 27.2% temporal melody
coverage remains a coverage measurement rather than an accuracy estimate, and
the producer disposition remains `FAIL_UNRECOGNIZABLE`.

## Diagnostic boundary

The gate distinguishes evidence that can be observed from evidence that would
require an additional reference. Activity in the separated vocal stem paired
with absent Basic Pitch contour and raw-note response supports
`NOTE_SENSOR_RECALL_BOTTLENECK` as a conditional diagnostic.

A silent vocal stem does not identify source-separation failure by itself. The
mixture can contain instruments, ambience and percussion, so mixture energy is
not vocal ground truth. `SOURCE_SEPARATION_RECALL_BOTTLENECK` is available only
when a registered acoustic vocal-presence observation, independent of the
candidate separator, identifies vocal activity in the same physical frames.

When that independent evidence is absent or too short, the source-separation
attribution remains `ABSTAIN_INSUFFICIENT_MELODY_EVIDENCE`. The gate creates no
notes, modifies no raw observations and reports no melody-accuracy percentage.

## Registered measurements

The implementation reports separated-stem activity, Basic Pitch conditional
nonresponse, optional independent-reference conditional nonresponse and their
evidence denominators. Thresholds are frozen in the registration artifact and
remain general acoustic quantities rather than song-specific rules.

Each run records the source hash, work-group hash, sensor versions, H reference
and candidate hashes, T reference and candidate hashes, diagnostic disposition
and producer recognizability outcome. Missing work-group provenance fails as
`AUDIT_PROVENANCE_INCOMPLETE`.

## Multicase and producer gate

The aggregation unit is an independent held-out track, with every version of a
musical work retained in one group. Aggregation is macro by track; frame pooling
cannot support promotion.

The current sub-gate localizes a possible bottleneck and does not establish
recognizability. Producer listening remains a separate outcome, and every
multicase diagnostic remains `HOLD_FOR_RECOGNIZABILITY_EXPERIMENT` until a later
registered M-only candidate is evaluated against these findings.

The scientific replication target remains 30 independent aligned tracks.
Meeting that count does not unlock Scientific D automatically;
`generation_class=D0_EXPLORATORY` and `scientific_d_unlocked=false` remain fixed.

## Implementation

- `mie_core/mie_melody_recognizability_gate.py`
- `tests/test_mie_melody_recognizability_gate.py`
- `data/music_modeling/mie_v0_3_5_m_only_recognizability_gate_registration_v1.json`
- `mie_core/run_mie_core.py`

## Current disposition

- sub-gate contract: `IMPLEMENTED`;
- synthetic contract tests: `PASS_LOCAL`;
- registered independent audio executions: `0`;
- producer recognizability evaluations for v0.3.5: `0`;
- melody correction selected: `NONE`;
- baseline promotion: `REJECTED_PENDING_EVIDENCE`;
- later ambiguity-safe H repair: `DEFERRED_H_ONLY_EXPERIMENT`.
