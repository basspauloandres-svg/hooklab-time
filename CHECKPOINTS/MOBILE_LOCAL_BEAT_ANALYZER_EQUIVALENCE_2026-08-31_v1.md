# HookLab mobile local Beat This analyzer — equivalence checkpoint v1

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Authoritative workflow run: `33450481336`
Job: `99679024985`
Status: PASS

## Decision
Promote `LOCAL_ON_DEVICE_ONNX` as the primary mobile analysis path for `AESTHETIC_REFERENCE_ANALYSIS`.
Keep the online API contract as a fallback path for devices/browsers that cannot complete local inference within resource/time limits.

This decision does not promote aesthetic-reference analysis into M300, Gate A, SUCCESS_EVIDENCE or scientific population evidence.

## Predeclared equivalence tolerances
- BPM relative error <= 3%.
- Beat-count relative error <= 15%.
- Median nearest-beat timing error <= 100 ms.

## Observed equivalence result
Public-domain test recording: Amazing Grace Wikimedia Commons fixture.
- Browser local BPM: 39.7351.
- CLI-derived BPM used by equivalence harness: 38.9610389610.
- BPM relative error: 0.0198676 = 1.99% -> PASS.
- CLI beat count: 74.
- Browser beat count: 73.
- Beat-count relative error: 0.0135135 = 1.35% -> PASS.
- Median nearest-beat error: 0.000 s -> PASS.

Overall equivalence status: PASS.

## Provenance
Browser analyzer:
- implementation: `app/prototype_v1/local_beat_this.js`.
- analysis mode: `LOCAL_ON_DEVICE_ONNX`.
- ONNX Runtime Web: 1.29.0.
- Beat This source commit: `089b509247e6fdcec666511c0dcf0d5f39c21e73`.
- beat model SHA-256: `a5f8d39d989f31859454ba27afe61c5317ca95e4d9373e6853e5361b8937172f`.
- mel model SHA-256: `fdd59e65c515331308e4c8841edf99972deca646bdf6197744c2a5b7755e3de9`.

Authoritative comparator:
- Beat This CLI v1.0.0.
- Same verified ONNX model hashes.
- Same public-domain reference audio.

## Scientific contract
`AESTHETIC_REFERENCE != AESTHETIC_REFERENCE_ANALYSIS != M300_EVIDENCE != SUCCESS_EVIDENCE != GATE_A_ACQUISITION`.

Required result fields remain:
- `scientific_ingestion=false`;
- `gate_a_ingestion=false`;
- `m300_ingestion=false`;
- `success_evidence_ingestion=false`;
- `source_audio_persistence=NONE`.

## Product implication
Mobile-first architecture becomes:

`phone browser -> local audio selection -> SHA-256 -> LOCAL_ON_DEVICE_ONNX Beat This -> BPM/beats/downbeats -> Producer Interface session`

Fallback only when local execution is unavailable or fails within declared resource/time constraints:

`phone browser -> ONLINE_API fallback -> ephemeral analyzer execution -> normalized JSON -> source audio deletion`.

## Immediate next gates
1. Mobile browser regression with iPhone/Safari-compatible viewport and Android/Chrome-compatible viewport.
2. Full product E2E: audio -> local analysis -> D0 -> playback -> MIDI/manifest -> producer evaluation -> session JSON.
3. Publish a stable versioned mobile route, preserving historical HookLab TIME root.
4. Implement/validate online API fallback; it is resilience infrastructure, not the primary path after this PASS.
5. Continue >=30-pair melody representation calibration independently; `SCIENTIFIC_D` remains fail-closed.
