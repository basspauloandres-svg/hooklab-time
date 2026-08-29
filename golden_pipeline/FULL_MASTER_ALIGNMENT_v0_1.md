# Full-master alignment v0.1

Date: 2026-08-29
Status: VERIFIED SOURCE WINDOW

## Authoritative source supplied by user

File: `Devuélveme El Amor(3).mp3`

SHA-256:

`23fbd8c816f59f21802c2fd4b91f48a315c2006a023992430ca10d8654264fb2`

Decoded duration at 22.05 kHz mono analysis:

`245.5278004535 s`

This duration is consistent with the historical complete-song analysis and the Apple Music catalog duration (~245.493 s). The uploaded file is therefore accepted as the full-master source for the current regression.

## Verified golden physical window

Historical interval:

`13.3 s <= t < 40.7 s`

Deterministic extraction command:

```bash
ffmpeg -y -ss 13.3 -to 40.7 -i INPUT.mp3 -ar 44100 -ac 2 golden_source_window.wav
```

Extracted WAV geometry:

- duration: `27.4 s`
- sample rate: `44100 Hz`
- channels: `2`
- sample width: `16 bit`
- frames per channel: `1,208,340`
- SHA-256: `854fc7c62c05745cb1da5d7073d8c2b848152b3d6a7762ca103a54706e36a342`

## Engineering consequence

The previous Apple-preview alignment problem is no longer a blocker. M v0.5 must be executed directly on this verified physical window. No preview offset, beat-pattern inference, lyric timing or editorial-preview mapping is permitted in the golden substitution experiment.

The controlled experiment is now:

`full master -> exact crop 13.3–40.7 -> HTDemucs vocals -> Basic Pitch candidates -> Structural Reduction -> Ornament Reduction -> Plane Resolver v0.5 -> M substitution`

while:

- Harmony B remains frozen;
- Beat This v1.9.3 remains frozen;
- renderer identity guards remain active.

## Current runtime limitation

The local execution environment contained the Demucs package but did not contain the HTDemucs weights in cache and had no network access to retrieve them. This is an infrastructure limitation, not an alignment or model decision. No alternate separator or simplified pitch extractor was substituted.
