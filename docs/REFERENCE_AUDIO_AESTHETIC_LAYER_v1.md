# Reference Audio Aesthetic Layer v1

## Purpose
Optional producer-facing layer for a manually supplied audio reference. It supports aesthetic/style direction during preproduction and is intentionally downstream/parallel to scientific corpus analysis.

## Invariants
- Manual upload is permitted only in this optional producer reference layer; it remains prohibited as the ordinary acquisition procedure for Gate A or corpus-scale scientific validation.
- Reference audio != M300 evidence.
- Reference audio != proof of success.
- Reference audio != authorized corpus acquisition.
- The producer/user is responsible for having lawful access to the uploaded reference.
- Processing is private/temporary unless a separate lawful basis permits persistence.
- The layer may describe observable production/style properties and compare generated material to them; it may not copy melody, lyrics or other protected expressive content.
- Provenance must mark every derived field as `REFERENCE_AESTHETIC_CONTEXT`.

## UX role
The interface asks for creative target/text first, then optionally accepts reference audio. Analysis outputs should be organized as aesthetic descriptors (e.g. energy, timbre, density, structural proportions, tempo/rhythm descriptors where technically valid), with explicit separation from evidence-backed HookLab deductions.

## Future implementation gate
Before automated reference analysis is promoted beyond prototype UI, define authorized local processing, temporary-file lifecycle, feature whitelist, similarity/copying safeguards, and provenance schema.
