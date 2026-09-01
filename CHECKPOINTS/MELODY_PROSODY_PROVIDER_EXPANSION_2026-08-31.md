# Melody/prosody provider expansion checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
State: `PROVIDER_SPACE_EXPANDED / DALI_PENDING / CALIBRATION_ROUTE_AVAILABLE`

## Canonical starting state
Previous checkpoint remains authoritative: 75/300 M300 songs (25.0%) have version-gated licensed structural/vocal-analysis evidence; no positive D001 rule has been promoted.

## New provider audit
The melody/prosody layer now distinguishes target-coverage providers from calibration/replication corpora.

### DALI
Target-coverage candidate. CC BY-NC-SA 4.0; access request has been submitted by the researcher. Remains `PENDING_PROVISIONING` and fail-closed.

### RWC 2.0 Popular Music
The 2026 community re-release is CC BY-NC 4.0. Its popular-music subset documents aligned MIDI, melody F0, lyrics, vocal/instrumental activity, structure, beats and chords (some richer annotations reside in the archive). This corpus is admissible for method replication/calibration, but it is not M300 and cannot increase M300 N.

### MedleyDB Melody
Royalty-free research multitracks with continuous F0 melody annotations; CC BY-NC-SA 4.0. Suitable for validating melody extraction/representation semantics. It is not a commercial-hit target corpus.

### Vocadito
Small public singing dataset with musician-created F0, two note annotations and lyrics. Particularly useful to test the known ambiguity between continuous F0 and discrete vocal-note representations. Calibration only.

### cante2midi
Open Zenodo note-level singing transcriptions plus predominant-melody F0; useful for stress-testing ornamented singing transcription. Calibration only.

## Scientific decision
Do not search for statistical 'success' rules inside calibration corpora. Their function is to validate the sensor/representation layer so that an eventual M300/DALI association is not an artifact of transcription choices.

This adds a necessary gate before positive creative deduction:
`AUTHORIZED TARGET DATA -> MELODY/PROSODY REPRESENTATION -> CALIBRATION AGAINST INDEPENDENT ANNOTATED CORPORA -> M300 ASSOCIATION -> REPLICATION -> INTERPRETATION -> DEDUCTION -> MIDI`.

## Immediate next gate
Implement a representation-calibration contract that tests continuous F0 -> discrete note conversion sensitivity using independent corpora before any pitch/range/interval statistic can be promoted from DALI or another target provider.
