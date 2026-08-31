# BiMMuDa × T1 full metadata crosswalk — checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Layer: `BIMMUDA_T1_CROSSWALK_v1`
State: `FULL_METADATA_CROSSWALK_OBSERVED / PROVIDER_LICENSE_AUDIT_PENDING`

## Observed result
Crosswalk of the 25 T1 Dance-Pop discovery candidates against BiMMuDa per-song metadata identifies 7 covered candidates:
- Umbrella — 2007_02
- Just Dance — 2009_03
- Party Rock Anthem — 2011_02
- E.T. — 2011_04
- Call Me Maybe — 2012_02
- Blinding Lights — 2020_01
- Don't Start Now — 2020_04

Coverage: 7/25 = 28%.

## Technical interpretation
BiMMuDa provides full main-melody MIDI plus section-level MIDIs and lyrics for songs with vocal main melodies, except documented exceptions. None of the seven covered T1 songs is listed among the README exceptions. Direct directory inspection has already confirmed full MIDI/sections/lyrics for Umbrella and Call Me Maybe; the remaining five are expected from the dataset contract and metadata identity but remain provider-license blocked for scientific processing.

## Authorization status
The public GitHub repository reports no repository license. The published TISMIR article is open access, but the article license is not being extrapolated to the dataset files. Therefore provider status remains `AUDIT_REQUIRED` and all seven rows remain `scientific_eligibility=BLOCKED_LICENSE_AUDIT`.

## Scientific effect
Scientific Matrix-X N does not change. Dataset presence is coverage evidence, not authorization or scientific promotion.

## Next action
1. Resolve BiMMuDa dataset computational-use authorization from an authoritative project/author source.
2. In parallel, audit alternative research-authorized providers for the 18 T1 candidates not covered by BiMMuDa.
3. Only after authorization may the seven covered rows proceed to version/FULL_SONG/provenance/FULL_TMT qualification.
