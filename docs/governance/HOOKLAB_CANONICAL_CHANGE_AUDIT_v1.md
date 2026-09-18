# HookLab Canonical Change & Audit Governance v1

Date: 2026-09-15
Status: CANONICALIZATION_CANDIDATE

## Purpose
Prevent repeated reprocessing caused by unresolved, chat-only, experimental, superseded, or ambiguously promoted decisions.

## Mandatory lifecycle
`finding -> evidence -> diagnosis -> correction -> validation -> canonical update -> commit -> audit record -> checkpoint`

A correction is not considered resolved until the complete lifecycle has been satisfied.

## Authoritative states
- `CANONICAL_CURRENT`: verified and currently operative.
- `SUPERSEDED`: historically retained but replaced by a newer verified state.
- `AUDIT_PENDING`: anomaly or inconsistency identified; correction not yet validated/canonicalized.
- `PENDING_CANONICALIZATION`: verified proposal/correction awaiting promotion to canonical state.
- `EXPERIMENTAL`: may inform testing but cannot silently govern scientific conclusions.
- `RECOVERED_HISTORICAL`: recovered evidence preserved as historical evidence; authority depends on explicit validation.
- `AUDIT_MIGRATION_MISSING_ARTIFACT`: historically referenced original not recovered in accessible evidence space.
- `SOURCE_RECONSTRUCTION`: newly reconstructed source with its own provenance; never represented as recovered original.

## Source hierarchy
1. `hooklab-time/main`: canonical current scientific/technical state after validated promotion.
2. Explicit canonical manifests/contracts/checkpoints versioned in `hooklab-time`.
3. Validated recovery evidence awaiting canonicalization.
4. `corpusbot` historical/experimental/recovery evidence.
5. Chat discussion: continuity aid only; never canonical by itself.

Conflicts are resolved by evidence, version, provenance and explicit supersession, not merely by recency.

## Change record minimum fields
Every promoted change must identify: change_id; date; affected subsystem; previous state; evidence; diagnosis; correction; validation; affected files; new version; commit; downstream impact; superseded artifact if any; unresolved dependencies; next gate.

## Fail-closed rule
No scientific feature, statistical conclusion, generative rule or generation gate may rely on `AUDIT_PENDING`, `PENDING_CANONICALIZATION`, `EXPERIMENTAL`, missing, circularly validated or provenance-unresolved material.

## Current high-priority audit state
- Historical HB-MOD-MIDI-001 originals remain unrecovered in the accessible evidence space and must remain distinct from reconstructed sources.
- CAL-MEL-001 requires >=30 independent aligned reference-estimate pairs before melody measurement features can be admitted through that calibration gate.
- MIE-produced transcription of reference audio is an estimate, not an independent calibration reference.
- HookLab-generated C001 prototypes are experimental generated artifacts, not independent commercial-reference sources.
- P30-SCORE-002 preserves a recovered melody-fragment lane for Devuélveme el Amor, but recovered/estimated melody events must not be relabeled as independent ground truth without independent provenance.
- The previous `corpusbot` recovery branch experienced a truncated ledger write; that branch is evidence/recovery material and must not be treated as canonical current state.

## Operating principle
Resolve one gate before opening the next. Do not reopen a closed problem without new evidence of regression, contradiction or provenance error. Preserve all superseded states for auditability while ensuring only one explicit current canonical state governs downstream work.
