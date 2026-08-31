# HookLab/TIME-MIE — Gate A T0 Provider Exhaustion Matrix

Date: 2026-08-30
Branch: `mie/golden-forensic-v0.3`
Gate: A — independent released-recording vocal identity
Status: observed provider-resolution pass; audio validation pending only where an authorized computational route is actually provisioned.

## Scientific semantics

Pipeline invariant:

`TARGET → PROVIDER_RESOLUTION → AUTHORIZED_COMPUTATIONAL_ACCESS → VERSION_IDENTITY → AUDIO_ANALYSIS → VOCAL_EXTRACTION → AUDIO↔MIDI VALIDATION → PASS | AUDIT | FAIL`

Outcome semantics:
- `PASS`: authorized released-recording reference obtained and audio↔MIDI validation passes.
- `FAIL`: authorized released-recording reference obtained correctly and audio↔MIDI validation fails.
- `AUDIT / REFERENCE_UNAVAILABLE`: configured legitimate routes are exhausted without an authorized processable released-recording reference. This is not an algorithmic validation failure.

Acquisition, version identity, audio authorization and melodic validation remain separate gates.

## Providers reviewed

1. **MusicBrainz** — identity/version metadata only. Useful for recording/release identity; supplies no audio payload.
2. **MassiveMusic/7digital public preview** — audio bytes are available to authorized API clients, but preview use is a playback service with logging/licensing requirements; public preview availability is not interpreted as authorization for arbitrary computational extraction.
3. **MassiveMusic/7digital Fingerprinting Environment** — explicitly designed for bulk computational analysis. Client software runs inside MassiveMusic infrastructure; media remains inside their licensed boundary; access is restricted by partner ID, IP whitelist and per-partner label-group whitelist. This is the preferred commercial-catalogue Gate A route when provisioned.
4. **MassiveMusic Media Transfer / Content Delivery** — can deliver licensed catalogue audio, but requires partner/licensor authorization and technical due diligence. It is eligible only after the relevant project agreement explicitly covers the intended computational processing.
5. **Jamendo / MTG-Jamendo** — explicit research/Creative-Commons processing route for tracks in that catalogue. No evidence was found that the five T0 major-label recordings are present as their released commercial masters; therefore it does not resolve T0.
6. **Freesound API** — API terms explicitly permit processing/analysis in accordance with each content license. Search evidence for T0 did not identify the released commercial masters; similarly named/derived sounds cannot satisfy released-version identity.
7. **AcoustID** — fingerprint/identity service; does not provide source audio and therefore cannot satisfy Gate A audio evidence.
8. **YouTube / Apple / Spotify consumer or preview surfaces** — not accepted as computational audio sources absent explicit provider/rightsholder processing authorization. Playback availability is not processing authorization.

## T0 × provider matrix

The identifiers below are recorded only when independently resolved. `IDENTITY_ONLY` means the provider contributes identity/provenance but cannot feed vocal extraction. `CONDITIONAL_AUTHORIZED_ROUTE` means the provider architecture explicitly supports computational analysis, but this project must still be provisioned and the relevant label catalogue whitelisted before audio access.

| song | provider | identifier/version evidence | duration evidence | access modality | computational authorization | resolution |
|---|---|---|---|---|---|---|
| Poker Face — Lady Gaga | MusicBrainz | official release; album version; 2008 recording/release evidence | ~3:57 in MusicBrainz release evidence | metadata API/web | metadata only | IDENTITY_ONLY |
| Poker Face — Lady Gaga | MassiveMusic Fingerprinting | catalogue lookup required after partner provisioning | to be verified against target registry | in-provider VM + HTTP media endpoint | explicitly supports client-installed media analysis; label whitelist required | CONDITIONAL_AUTHORIZED_ROUTE |
| Poker Face — Lady Gaga | MassiveMusic Media Transfer | catalogue lookup required | to be verified | licensed media transfer | licensor/client agreement required | CONDITIONAL_AUTHORIZED_ROUTE |
| Poker Face — Lady Gaga | Jamendo/MTG-Jamendo | no released-master match established | — | CC/research audio | allowed only for matching licensed track | REFERENCE_UNAVAILABLE |
| Poker Face — Lady Gaga | Freesound | search surfaced derivative MuseNet improvisations, not released master | derivative clips ~20–29 s | API licensed sounds | processing permitted per sound license, but wrong version/identity | REFERENCE_UNAVAILABLE |
| Bad Romance — Lady Gaga | MusicBrainz | official release group; original/explicit recording evidence | ~4:54–4:55 | metadata | metadata only | IDENTITY_ONLY |
| Bad Romance — Lady Gaga | MassiveMusic Fingerprinting | catalogue lookup required after partner provisioning | to be verified | in-provider VM | explicit analysis environment; label whitelist required | CONDITIONAL_AUTHORIZED_ROUTE |
| Bad Romance — Lady Gaga | MassiveMusic Media Transfer | catalogue lookup required | to be verified | licensed media transfer | licensor/client agreement required | CONDITIONAL_AUTHORIZED_ROUTE |
| Bad Romance — Lady Gaga | Jamendo/MTG-Jamendo | no released-master match established | — | CC/research audio | matching licensed track required | REFERENCE_UNAVAILABLE |
| Bad Romance — Lady Gaga | Freesound | no released-master match established | — | API licensed sounds | matching licensed track required | REFERENCE_UNAVAILABLE |
| TiK ToK — Kesha | MusicBrainz | recording evidence and original hit version | ~3:20–3:21 in release evidence | metadata | metadata only | IDENTITY_ONLY |
| TiK ToK — Kesha | MassiveMusic Fingerprinting | catalogue lookup required after partner provisioning | to be verified | in-provider VM | explicit analysis environment; label whitelist required | CONDITIONAL_AUTHORIZED_ROUTE |
| TiK ToK — Kesha | MassiveMusic Media Transfer | catalogue lookup required | to be verified | licensed media transfer | licensor/client agreement required | CONDITIONAL_AUTHORIZED_ROUTE |
| TiK ToK — Kesha | Jamendo/MTG-Jamendo | no released-master match established | — | CC/research audio | matching licensed track required | REFERENCE_UNAVAILABLE |
| TiK ToK — Kesha | Freesound | no released-master match established | — | API licensed sounds | matching licensed track required | REFERENCE_UNAVAILABLE |
| Firework — Katy Perry | MusicBrainz | target recording identifiable; snippet release is explicitly partial and is rejected for Gate A | full target must be separately resolved | metadata | metadata only | IDENTITY_ONLY |
| Firework — Katy Perry | MassiveMusic Fingerprinting | catalogue lookup required after partner provisioning | to be verified | in-provider VM | explicit analysis environment; label whitelist required | CONDITIONAL_AUTHORIZED_ROUTE |
| Firework — Katy Perry | MassiveMusic Media Transfer | catalogue lookup required | to be verified | licensed media transfer | licensor/client agreement required | CONDITIONAL_AUTHORIZED_ROUTE |
| Firework — Katy Perry | Jamendo/MTG-Jamendo | no released-master match established | — | CC/research audio | matching licensed track required | REFERENCE_UNAVAILABLE |
| Firework — Katy Perry | Freesound | no released-master match established | — | API licensed sounds | matching licensed track required | REFERENCE_UNAVAILABLE |
| Dynamite — Taio Cruz | MusicBrainz | official single/released recording; lead vocal explicitly Taio Cruz | ~3:24 target track evidence | metadata | metadata only | IDENTITY_ONLY |
| Dynamite — Taio Cruz | MassiveMusic Fingerprinting | catalogue lookup required after partner provisioning | to be verified | in-provider VM | explicit analysis environment; label whitelist required | CONDITIONAL_AUTHORIZED_ROUTE |
| Dynamite — Taio Cruz | MassiveMusic Media Transfer | catalogue lookup required | to be verified | licensed media transfer | licensor/client agreement required | CONDITIONAL_AUTHORIZED_ROUTE |
| Dynamite — Taio Cruz | Jamendo/MTG-Jamendo | no released-master match established | — | CC/research audio | matching licensed track required | REFERENCE_UNAVAILABLE |
| Dynamite — Taio Cruz | Freesound | no released-master match established | — | API licensed sounds | matching licensed track required | REFERENCE_UNAVAILABLE |

## Provider exhaustion result

For the current unauthenticated/public project environment, no provider has supplied an immediately processable, explicitly authorized released-master audio object for any of the five T0 songs.

This result is `AUDIT / REFERENCE_UNAVAILABLE`, not `FAIL`.

A legitimate scalable route **does exist**: MassiveMusic's Fingerprinting Environment is explicitly designed for bulk analysis of licensed media without exporting the audio from its controlled infrastructure. It therefore changes the Gate A problem from “find a legal workaround” to “provision a licensed computational-analysis provider”. The pipeline must detect credentials/partner provisioning automatically and proceed without user audio uploads when available.

## Current observed rates

Denominator = 5 T0 songs.

- resolver coverage rate (immediately authorized processable released recording): **0/5 = 0%**
- automatic validation rate: **0/5 = 0%**
- audit / reference-unavailable rate: **5/5 = 100%**
- true validation failure rate: **0/5 = 0%**

These rates describe the current provider-access state, not the expected performance of the melodic identity algorithm.

## Next executable transition

`REFERENCE_UNAVAILABLE` cases are retried automatically when a provider adapter reports both:
1. project-level computational-processing authorization/provisioning; and
2. target recording availability under the project's label/territory whitelist.

Only then may the audio-analysis, vocal-extraction and audio↔MIDI validators execute. Human intervention is reserved for `AUDIT` adjudication and provider-account/legal provisioning, never routine per-song audio upload.
