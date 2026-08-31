# HookLab/TIME-MIE — Gate A Automation Invariant v1.0

Date: 2026-08-30
Canonical branch: `mie/golden-forensic-v0.3`
Status: migration-critical architectural invariant

## Purpose

Gate A must be scalable to large corpora and must not depend, as an ordinary procedure, on a user manually downloading or uploading commercial recordings.

## Canonical pipeline

`TARGET REGISTRY`
→ `AUTOMATIC LEGITIMATE REFERENCE RESOLUTION`
→ `VERSION IDENTITY`
→ `AUTHORIZED/TEMPORARY COMPUTATIONAL ACCESS`
→ `VOCAL MELODY EXTRACTION`
→ `AUDIO↔MIDI ALIGNMENT`
→ `METRICS`
→ `PASS / AUDIT / FAIL`
→ `PROVENANCE`

Human intervention is reserved for `AUDIT` cases and for governance/authorization tasks that cannot legally be automated.

## Separation of concerns

The following gates remain separate and independently auditable:

1. `REFERENCE_ACQUISITION`: can HookLab lawfully obtain machine-readable audio bytes or an authorized analysis stream for this recording?
2. `VERSION_IDENTITY`: does the resolved recording correspond to the intended released version?
3. `MELODIC_VALIDATION`: does the independently extracted lead-vocal melody support the symbolic vocal-track identity?

A metadata match cannot substitute for audio authorization. An authorized audio endpoint cannot substitute for version identity. A version match cannot substitute for melodic validation.

## Authorization rule

HookLab may automatically process a source only when the source's documented API/license/contract explicitly permits the required computational access. If the terms are silent, promotional-only, streaming-only without analysis rights, or explicitly prohibit download/separation/modification, the source is classified `METADATA_ONLY` or `AUTOMATION_PROHIBITED` and is not used for Gate A audio processing.

No undocumented endpoint, stream ripping, DRM circumvention, browser capture, or terms-evasion route is permitted.

## Source-role policy

- MusicBrainz or equivalent open metadata: permitted for recording/version identity and ISRC/MBID resolution; it supplies metadata, not audio evidence.
- YouTube API: metadata/reach role only for HookLab. Current YouTube API policies prohibit downloading/caching audiovisual content without prior written approval and prohibit offering audio separation; therefore it is not an automatic Gate A audio source absent explicit written authorization.
- Apple iTunes Search / promotional previews: metadata/version-resolution role only. Apple's documented promo-content terms require promotional use and streaming-only treatment of song previews, so previews are not used as computational Gate A audio evidence unless a separate applicable authorization explicitly permits analysis.
- Spotify Web API previews: metadata/version-resolution role only. Preview URLs are deprecated/nullable and governed as preview content; HookLab does not assume computational-analysis rights from their existence.
- Rights-cleared/open audio APIs or institutional/licensed catalogs: eligible only when the applicable license/API terms explicitly authorize machine retrieval/processing for the intended research use. Per-track authorization flags and license provenance must be retained.
- Project-owned or rights-holder-authorized masters: eligible and preferred when exposed through an authenticated automated storage/API path; manual user upload is not the ordinary pipeline.

## Resolver contract

Every candidate reference must produce a provenance record with at least:

- `song_id`
- `target_title`
- `target_artist`
- `target_version`
- `recording_identifier` (ISRC/MBID/provider ID where available)
- `provider`
- `provider_reference_id`
- `access_mode`
- `authorization_class`
- `authorization_evidence`
- `version_identity_status`
- `audio_processing_allowed`
- `retention_policy`
- `resolution_timestamp`
- `resolver_version`

Only `audio_processing_allowed=true` may enter vocal extraction.

## Scientific invariant

`automatic discovery != authorized audio access != version identity != melodic validation != scientific promotion`

Each transition requires its own evidence.

## Migration invariant

Future chats/agents must not ask the user to manually download or upload the target recordings as the normal Gate A procedure. Before declaring Gate A blocked, they must evaluate documented automated and legitimate reference routes. Sources that do not authorize the required processing must be rejected rather than circumvented.

This invariant complements, and does not replace, the TSDQP invariants:

`scientific target population != songs available in Lakh/LMD`

`candidate discovery != scientific promotion`
