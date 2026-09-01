# HookLab Producer Interface — Mobile-first product contract v0.1

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Status: CANONICAL PRODUCT REQUIREMENT

## Product target
HookLab Producer Interface must be usable from a modern mobile browser without local installation of Python, ffmpeg, Beat This, models or command-line tools.

Primary runtime:
`Mobile browser -> Producer Interface -> online analyzer API -> ephemeral Analyzer/Beat This execution -> derived JSON -> same mobile session`.

## Mobile requirements
- Responsive single-column layout at <=700 px.
- Touch targets >=44 CSS px effective height where practical.
- File picker accepts mobile audio MIME types through `accept="audio/*"`.
- Audio reference playback must use native browser audio controls.
- Analysis state must expose: READY / UPLOADING / ANALYZING / PASS / FAIL.
- Producer must be able to inspect BPM/tempo, beat count/timing summary, duration, analyzer provenance and scientific boundary status without horizontal scrolling.
- D0 generation, listening, MIDI/manifest export, timer and evaluation remain available in the same session.
- Session JSON must contain both aesthetic-reference provenance and normalized analysis result.

## Scientific boundary
`AESTHETIC_REFERENCE != AESTHETIC_REFERENCE_ANALYSIS != M300_EVIDENCE != SUCCESS_EVIDENCE != GATE_A_ACQUISITION`.

Aesthetic-reference analysis is descriptive session-level information. It cannot increase M300 N or unlock SCIENTIFIC_D.

## Privacy/data lifecycle
- Source audio is ephemeral in the online analyzer execution layer.
- Persist only derived JSON/provenance unless the user explicitly exports locally on their device.
- API response must echo/verify session_id and reference SHA-256.
- Server-side source audio deletion is an acceptance requirement, not an optimization.

## Versioned URL requirement
Producer Interface must be deployed under a versioned route independent of the historical HookLab TIME root. Root collisions invalidate deployment verification.

## Acceptance
A real mobile-browser E2E test must pass:
1. select audio from device;
2. local playback works;
3. SHA-256 computed;
4. submit to online analyzer;
5. receive normalized analysis JSON;
6. render BPM/beats/duration/provenance;
7. generate/listen/export D0;
8. record producer evaluation;
9. export complete session JSON.
