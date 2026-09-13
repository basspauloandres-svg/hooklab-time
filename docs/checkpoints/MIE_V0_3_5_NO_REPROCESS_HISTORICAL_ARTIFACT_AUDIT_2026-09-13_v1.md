# MIE v0.3.5 — NO_REPROCESS historical artifact audit — 2026-09-13 v1

Status: `HISTORICAL_GATE_NOT_PASSED / NEW_AUDIO_BLOCKED / FROZEN_REFERENCE_BINDING_DEFECT_REGISTERED`

## Scope

This checkpoint continues `BUILD_AND_AUDIT_MIE_V0_3_5_M_ONLY_MELODY_RECOGNIZABILITY_GATE` under strict `NO_REPROCESS`. No audio model was rerun, no new audio was requested, H was not developed and T was not modified. Existing GitHub Actions artifacts were downloaded only for byte/content inspection.

The first sub-gate remains:

`DIAGNOSE_SOURCE_SEPARATION_VERSUS_NOTE_SENSOR_RECALL`

The current scientific boundary remains:

- `generation_class=D0_EXPLORATORY`;
- `scientific_d_unlocked=false`;
- producer recognizability remains separate from automatic diagnostics;
- temporal coverage and sensor nonresponse are not melody-accuracy estimates.

## Existing historical package audit

### Published v0.3.4 public-preview artifact

Artifact `9910624179`, workflow run `33799581232`, commit `6f44f21971d5bf581fc3531215d74c9c856b80c0`, ZIP SHA-256 `ffa7de86babeebf62411b629a1121919d95f776dae383a5e4cf478d6c6f5cff5`.

Persisted contents:

- `MIE_CORE_MHT_v0_2.json`;
- `MIE_CORE_MHT_v0_2.wav`;
- `MIE_CORE_MHT_v0_3_1.wav`;
- `MIE_CORE_MHT_v0_3_2.wav`;
- `MIE_CORE_MHT_v0_3_3.wav`;
- `MIE_CORE_MHT_v0_3_4.wav`;
- `melody_basic_pitch.mid`;
- Beat This ONNX cache files.

The package does not persist the HTDemucs vocal stem, Basic Pitch contour/onset tensors or raw Basic Pitch candidate events. `raw_note_candidates` is stored only as a count. Therefore the separator-versus-note-sensor diagnostic cannot be recomputed from this package without reprocessing.

Observed package values: duration `29.9290702948 s`, 94 raw note candidates, 85 accepted candidates, 66 final v0.3.4 melody events, 35 raw beat observations, 29 resolved tactus events, tempo `69.76744186 BPM`, and 12 v0.3.3 harmony states.

Canonical persisted-layer hashes calculated from the JSON are:

- H v0.3.3: `b145cfecdea25c6ed6379d4883dada64de02b834f8a338b8d43afc54d13da22a`;
- T resolved layer: `9f48f26e6f9c9d3b6efc59548a944066306ed7cfe9f86f40ebdb64c40e84f290`;
- stored tactus fingerprint: `a0d50e9c9bd411b9f038a0330bcc924935888ea857eb4c9cbeb189809d8cf73d`.

### Existing post-gate public-preview run

Artifact `9944207067`, workflow run `33891658717`, commit `4f47f8c54ae2353782b138a05b7ceeccdf9e180d`, ZIP SHA-256 `16feb6300d18278765d1f7e65acb6c5dddb996749f6df41f7bc6d312974f9142`.

This artifact already contains a v0.3.5 diagnostic generated during its historical execution. It was inspected without rerun.

Its top-level gate status is `AUDIT_PROVENANCE_INCOMPLETE` because `work_group_hash=null`. The nested diagnostic returns `ABSTAIN_INSUFFICIENT_MELODY_EVIDENCE` with reason `MINIMUM_INDEPENDENT_EVIDENCE_NOT_MET`.

Observed diagnostic values:

- separated-vocal active time: `28.3604651163 s`;
- raw Basic Pitch candidates: `90`;
- conditional note-sensor nonresponse ratio: `0.1193111931`;
- note-sensor evidence sufficient: `true`;
- independent vocal reference present: `false`;
- source-separation claim allowed: `false`.

The ratio `0.1193111931` is a conditional diagnostic within that run. It is not an accuracy estimate and does not establish that the separator was correct.

The run reports H and T as byte-equivalent inside the same execution because reference and candidate were supplied from the same generated objects. This proves within-call non-mutation only.

Persisted-layer hashes for this package are:

- H v0.3.3: `7612297d792b5305a01bdafb2a42f6cb7c14a51ad275feb6919e858c34f4b6e4`;
- T resolved layer: `7f8e3ebd3a9e37a7b1a40d33c44a8ab2612582e0d78f215b5f63abc217427c75`;
- stored tactus fingerprint: `5ba310051d16690311c9ed59842c24190eba5958149243bda675ed5482f09877`.

## Cross-run frozen-reference finding

The two public-preview packages have the same reported duration, beat count, resolved tactus count and tempo. T timestamps are materially stable, while floating beat scores differ slightly. Harmony identities and boundaries are materially stable, while acoustic evidence/margin scores differ. Basic Pitch output also changes from 94 to 90 raw candidates and from 66 to 62 final melody events.

Consequently:

- H historical hash != H post-gate hash;
- T historical hash != T post-gate hash;
- current within-run equality cannot establish byte identity to the predeclared historical H/T reference.

Formal disposition:

`AUDIT_FROZEN_REFERENCE_BINDING_NOT_DEMONSTRATED`

This is promotion-blocking under the existing one-module rule.

## Audit defect

Registered defect:

`MIE-v0.3.5-FROZEN-REFERENCE-BINDING-DEFECT-v1`

The current `build_m_only_experiment_audit` API permits the caller to provide H/T reference and candidate layers produced inside one execution. The current runner passes the same v0.3.3 harmony object as both reference and candidate and the same tactus object as both reference and candidate. Equality is therefore guaranteed unless the audit function itself mutates those objects.

The current test reproduces the same semantics by passing deep copies of one newly created H/T object. It verifies non-mutation, not historical frozen-reference binding.

Before any subsequent audio execution, the audit contract must be hardened so that:

1. H and T hashes are predeclared from an immutable prior package or manifest before candidate execution;
2. candidate H/T hashes are compared against those historical hashes;
3. absent frozen-reference hashes produce a fail-closed audit state;
4. floating-score nondeterminism is documented explicitly rather than silently weakening the byte-identical rule.

No code change is made in this checkpoint because pushes under `mie_core/**` trigger the `MIE Core Prototype` workflow, which acquires and processes preview audio. Such a push would violate the current `NO_REPROCESS / NO_NEW_AUDIO_EXECUTION` boundary.

## Other historical artifacts

Artifact `9706225384` (`mie-structural-regression-v0-4`, SHA-256 `af8e409f3b152edaf35fa1af7984e40f3504a13f0fa5752ac93fd751ac84c511`) contains a core JSON/WAV, Basic Pitch MIDI and structural-probe JSON/MIDI. It does not contain the separated vocal stem or Basic Pitch contour tensor. It remains an engineering structural control rather than an eligible recognizability case.

`Animal` remains the registered held-out failure. Its source SHA-256 is `75e1dcbaef2fe3d81818df650acf72d98c306f0262bd9e78bbbc911a42a436a0` and the evaluated recognition ZIP SHA-256 is `39afd3c980c3d22e4267a33aee33e5f09895d514fbbcccbbe8ab7ef04789d67a`. Those bytes are not tracked in Git. Existing metadata are sufficient to preserve `FAIL_UNRECOGNIZABLE`, while they are insufficient to isolate source-separation versus note-sensor recall causally.

## Current sub-gate disposition

Evidence supports a historical hypothesis that note-sensor recall contributes to melody loss because recognizable-but-gapped cases and zero-recovery failures exist. Existing traceable packages do not yet provide the persisted acoustic layers required to quantify that causal split on an eligible historical case.

Therefore:

- `NOTE_SENSOR_RECALL_BOTTLENECK = HISTORICALLY_SUPPORTED_HYPOTHESIS`;
- `SOURCE_SEPARATION_PRIMARY_CAUSE = NOT_ESTABLISHED`;
- `FORMAL_OUTCOME = ABSTAIN_INSUFFICIENT_MELODY_EVIDENCE`;
- `HISTORICAL_GATE = NOT_PASSED`;
- `NEW_AUDIO_REQUEST_ALLOWED = false`;
- `NEW_AUDIO_EXECUTION_ALLOWED = false`;
- `H = FROZEN`;
- `T = FROZEN_ENGINEERING_BASELINE_PRESERVED`.

## Next allowed action

`HARDEN_FROZEN_REFERENCE_BINDING_AND_CONTINUE_RECOVERY_OF_EXISTING_HISTORICAL_ARTIFACTS_ONLY`

No new audio should be executed until the frozen-reference audit can be enforced without violating `NO_REPROCESS`.
