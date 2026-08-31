# HookLab/TIME-MIE — Gate A Automatic Reference Route Research v1.0

Date: 2026-08-30
Branch: `mie/golden-forensic-v0.3`

## Decision
Gate A ordinary operation is automated. Manual user download/upload of commercial recordings is prohibited as the normal validation route. Human intervention is reserved for AUDIT.

## Required separation
`TARGET REGISTRY` → `RECORDING/VERSION IDENTITY` → `AUTHORIZED AUDIO REFERENCE` → `VOCAL EXTRACTION` → `AUDIO↔MIDI ALIGNMENT` → `MELODIC METRICS` → `PASS/AUDIT/FAIL` → `PROVENANCE`

No stage may silently substitute for another.

## Identity layer
MusicBrainz is retained as the principal open metadata resolver. Its API supports recording search and ISRC lookup; recording entities distinguish specific recorded audio and can expose recording MBIDs, ISRCs, artist credits, dates and durations. This layer is suitable for identity/version resolution but supplies no audio authorization.

ISRC is preferred when available because it identifies a specific sound recording rather than the underlying musical work. Multiple recordings/remixes/live versions can therefore be separated before audio validation.

## Derived-feature layer
AcousticBrainz remains useful as optional independent recording-indexed derived evidence. Its public data are indexed by MusicBrainz recording MBID and licensed CC0, but its documented low-level/high-level descriptors do not provide the vocal note-event ground truth required to close Gate A. It therefore cannot replace released-recording melodic validation.

## Audio authorization layer
Provider availability is not authorization. A playable URL, preview URL, streaming relationship or catalog listing must never be interpreted as permission to download, cache, separate vocals or perform computational analysis.

Routes whose terms do not explicitly authorize the required temporary computational access are classified as metadata/identity evidence only or rejected for automatic processing. The policy-aware `recording_reference_resolver.py` enforces this boundary.

## T0 strategy
For Poker Face, Bad Romance, TiK ToK, Firework and Dynamite:
1. automatically resolve the intended original commercial studio recording;
2. record MBID/ISRC/version/duration provenance where resolvable;
3. query configured authorized-audio providers independently;
4. process only a route carrying explicit processing authorization;
5. if all automated legitimate routes are exhausted, emit `AUDIT`, not a request for manual user upload.

## Scaling invariant
The reference layer must remain provider-pluggable. HookLab must be able to add an institutional, label, research-license, project-authorized, or rights-cleared provider without changing scientific identity or melodic-validation logic.

## Migration invariants
- `scientific target population != songs available in Lakh/LMD`
- `candidate discovery != scientific promotion`
- `recording identity != audio authorization != melodic validation`
- `manual user audio upload != ordinary Gate A procedure`
- `provider availability != processing authorization`
