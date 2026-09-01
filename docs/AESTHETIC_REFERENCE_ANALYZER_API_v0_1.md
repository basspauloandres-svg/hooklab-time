# HookLab Aesthetic Reference Analyzer API v0.1

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Status: CANONICAL API CONTRACT

## Endpoint
`POST /v1/analyze-reference`
Content-Type: `multipart/form-data`

Required fields:
- `audio`: authorized user-selected audio file.
- `session_id`: current Producer Interface session identifier.
- `reference_sha256`: browser-computed SHA-256 of the exact uploaded file.

Optional fields:
- `client_version` (e.g. `producer-interface-v0.4-mobile`).

## Processing contract
1. Receive audio into ephemeral server storage/RAM.
2. Compute server SHA-256 and compare with `reference_sha256`.
3. Reject on mismatch.
4. Execute existing HookLab acoustic sensor stack (ffmpeg + melody sensor + Beat This path) without promoting the input into Gate A/M300/scientific evidence.
5. Normalize derived output through `aesthetic_reference_analysis_contract.py`.
6. Delete source/intermediate audio before successful response completion; also delete in failure/finally paths.
7. Return derived JSON only.

## Success response
HTTP 200
```json
{
  "schema": "HOOKLAB_AESTHETIC_REFERENCE_ANALYSIS_v0.1",
  "status": "PASS",
  "session_id": "HL-...",
  "role": "AESTHETIC_REFERENCE_ANALYSIS",
  "semantics": "DESCRIPTIVE_SESSION_REFERENCE_ONLY",
  "scientific_ingestion": false,
  "gate_a_ingestion": false,
  "m300_ingestion": false,
  "success_evidence_ingestion": false,
  "source_audio_persistence": "NONE",
  "reference_sha256": "...",
  "duration_s": 0.0,
  "tempo_bpm_median": 0.0,
  "beat_count": 0,
  "beat_times_s": [],
  "beat_sensor": "Beat This",
  "beat_status": "VALID",
  "melody_event_count": 0,
  "melody_range_raw": [null, null],
  "sensor_version": "...",
  "beat_model_sha256": "...",
  "mel_model_sha256": "...",
  "contract": "AESTHETIC_REFERENCE != M300_EVIDENCE != SUCCESS_EVIDENCE != GATE_A_ACQUISITION"
}
```

## Failure behavior
- 400: missing/unsupported upload or invalid session fields.
- 409: SHA-256 mismatch.
- 413: file exceeds configured size limit.
- 422: analysis completed but normalized sensor contract fails.
- 500/503: execution/backend unavailable.

Failure responses must never claim scientific evidence and must not retain source audio.

## Browser/mobile requirements
- HTTPS required in production.
- CORS allow-list must include only canonical Producer Interface origins/routes.
- Do not expose GitHub or backend credentials to the browser.
- UI should use an AbortController-capable request and render UPLOADING / ANALYZING / PASS / FAIL.

## Deployment neutrality
The contract is provider-neutral. A conforming implementation may run on a container service, VM, or equivalent backend capable of Python/ffmpeg/Beat This. The Producer Interface depends only on this HTTP contract, not the hosting vendor.
