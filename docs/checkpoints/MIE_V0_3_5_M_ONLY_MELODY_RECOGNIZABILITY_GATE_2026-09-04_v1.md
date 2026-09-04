# MIE v0.3.5 — M-only melody recognizability gate — 2026-09-04 v1

Status: `ENGINEERING_DIAGNOSTIC_IMPLEMENTED / HISTORICAL_GATE_NOT_PASSED`

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

## Historical-first amendment and NO_REPROCESS

The historical regression inventory is now a prerequisite. Existing sources,
hashes, Actions ZIP artifacts, M/H/T outputs and producer dispositions must be
recovered and evaluated before requesting another work. Recovery and hashing of
an immutable artifact are not reprocessing; invoking separation, note sensing
or reconstruction on an old source is a new execution and requires a new
identifier plus `changed_module=M_ONLY`.

The historical evidence supports note-sensor recall as a current priority, but
does not identify the causal split for Animal. The four-variant listening report
is evidence against the separator as primary cause in that session only; it has
no recovered case hash. The independent 281.797 s case had a recognizable but
gapped melody, while Animal had zero newly recovered candidates and failed
recognizability. Together these observations do not provide the registered,
same-source independent vocal-activity comparison required to quantify source
separation recall. The formal sub-gate outcome therefore remains
`ABSTAIN_INSUFFICIENT_MELODY_EVIDENCE`.

Until every eligible historical case records a v0.3.5 M-only recognizability
disposition, `new_audio_request_allowed=false`. H development remains blocked
and T remains `FROZEN_ENGINEERING_BASELINE_PRESERVED`.

## Implementation

- `mie_core/mie_melody_recognizability_gate.py`
- `tests/test_mie_melody_recognizability_gate.py`
- `data/music_modeling/mie_v0_3_5_m_only_recognizability_gate_registration_v1.json`
- `data/music_modeling/mie_historical_regression_inventory_v1.json`
- `mie_core/run_mie_core.py`

## Current disposition

- sub-gate contract: `IMPLEMENTED`;
- synthetic contract tests: `PASS_LOCAL`;
- recovered non-expired Actions ZIP artifacts: `6`;
- eligible historical melody cases: `3`;
- historical v0.3.5 gate: `NOT_PASSED`;
- new-audio request: `BLOCKED`;
- producer recognizability evaluations for v0.3.5: `0`;
- melody correction selected: `NONE`;
- baseline promotion: `REJECTED_PENDING_EVIDENCE`;
- later ambiguity-safe H repair: `DEFERRED_H_ONLY_EXPERIMENT`.
