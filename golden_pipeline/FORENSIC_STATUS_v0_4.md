# Golden Pipeline forensic status v0.4

Date: 2026-08-29
Status: M v0.5 STRUCTURAL PASS / GOLDEN SUBSTITUTION BLOCKED ON PHYSICAL ALIGNMENT

## Authoritative continuity

This checkpoint supersedes `FORENSIC_STATUS_v0_3.md` for current engineering state while preserving v0.3 as genealogy.

Frozen project evidence remains unchanged:

- golden audible baseline: `MIE_P30_HARMONIA_BEAT_v0_1(1).wav`;
- golden WAV SHA-256: `de8381ef9322e73bf295db40a9dffeb0528469502313ea949c4c9018fe9cd940`;
- recovered canonical renderer: `app-mie-p30-harmony-beat-v0.1.html`;
- renderer SHA-256: `8ae79a4c6f92cea9d48a6aea5cd1cc3d4496dbd993e9cf0d229e6fcfcb4c5541`;
- golden geometry: 13.3–40.7 s, mono PCM16, 44.1 kHz, 27.4 s;
- frozen Harmony B: 33 embedded units from the approved Other→Motor→IA→Motor condition B;
- frozen Beat This: 34 embedded timestamps, 32 rendered inside the golden window;
- P30 historical target: 72 melody events with original physical timing.

## M v0.5 structural validation

Plane Resolver v0.5 adds two generic controls to the v0.4 architecture:

1. a conservative prior toward sensor plane `shift=0`;
2. cross-segment plane memory with temporal decay.

It also separates musical large intervals from damage introduced by the resolver through:

- `resolver_introduced_large_jumps`;
- `resolver_worsened_by_octave_or_more`.

GitHub Actions run `33223957593` completed the triple gate on one regression case plus two contrasting generic cases with unchanged parameters.

### Regression — Devuélveme el Amor authorized Apple preview

- raw sensor candidates: 94;
- structural hypotheses: 87;
- pre-ornament render: 85;
- micro-ornament suppressions: 1;
- pre-plane events: 84;
- plane ambiguous: 0;
- final render events: 84;
- structural ambiguous hypotheses: 2;
- maximum final adjacent jump: 8 semitones;
- final jumps ≥10 semitones: 0;
- resolver-introduced large jumps: 0;
- resolver worsening by ≥12 semitones: 0.

### Generic A

- raw sensor candidates: 49;
- final render events: 39;
- maximum final adjacent jump: 14 semitones;
- final jumps ≥10 semitones: 1;
- resolver-introduced large jumps: 0;
- resolver worsening by ≥12 semitones: 0.

The surviving 14-semitone leap is therefore pre-existing musical/sensor evidence, not damage created by the Plane Resolver.

### Generic B

- raw sensor candidates: 39;
- final render events: 37;
- maximum final adjacent jump: 6 semitones;
- final jumps ≥10 semitones: 0;
- resolver-introduced large jumps: 0;
- resolver worsening by ≥12 semitones: 0.

### Synthetic invariants

The structural invariant suite passes, including cross-segment plane-memory checks. M v0.5 is therefore accepted as a **structurally stable candidate for controlled integration**. This is not a perceptual promotion and does not establish equivalence to P30.

## H/T freeze verification

Inspection of the recovered checkpoints confirms the accepted integration target:

`P30-SCORE-002 + Harmony B (Other→Motor→IA→Motor condition B) + Beat This v1.9.3`.

`mie_core/run_mie_core.py` must not be used as the frozen H implementation. Its H path is a beat-synchronous chroma/template classifier with bass bonus; that differs from the accepted condition-B Motor→IA→Motor genealogy. Its T implementation remains useful as Beat This engineering evidence, but the entire v0.2 MHT script is not the frozen golden integration path.

The canonical HTML remains the authoritative executable container for frozen H/T during M substitution.

## Physical alignment blocker

The regression M v0.5 stream was generated from the historical Apple/iTunes preview used by workflow commit `83b6ee229fe982b54865f9b18d58a64ded8b3ff7`.

That commit downloads the preview directly and performs no seek or `-ss` transformation. The preview duration is approximately 29.93 s. The project has confirmed song identity but has not recovered the editorial preview's start position on the 245.5 s full-song timeline.

The initially tempting mapping:

`preview_t + 13.3 s -> full_song_t`

is explicitly rejected. It originates from the golden window boundary rather than source provenance, produces a tactus residual of approximately 31.82 ms median / 63.15 ms maximum, and maps an opening M v0.5 contour around MIDI 64/62 against a frozen P30 opening 48→57→59→60→62.

Full-song Beat This evidence cannot uniquely solve the offset because the song's ~70 BPM tactus is sufficiently regular that many offsets yield low timing residuals. Examples are documented in `M_V05_ALIGNMENT_STATUS_v0_1.md`.

No candidate offset may be labeled `VERIFIED` from beat periodicity or M-vs-P30 similarity alone.

## Guarded substitution path

A dedicated renderer now exists:

`golden_pipeline/render_m_v0_5_substitution.js`

It is the only authorized path for the first M v0.5 → frozen H/T golden substitution. Before writing audio it verifies:

1. canonical renderer SHA-256;
2. canonical frozen Harmony B hash and 33-unit cardinality;
3. canonical frozen Beat This hash and 34-event cardinality;
4. `alignment_status == VERIFIED`;
5. `same_source_confirmed == true`;
6. explicit alignment evidence;
7. LOCK-only M events inside the 13.3–40.7 s window.

CI workflow `Golden M Substitution Guard`, run `33226170743`, passes the negative invariants:

- unverified alignment is refused before WAV creation;
- a one-byte change to the canonical renderer is refused before WAV creation.

## Current gate

M v0.5: **STRUCTURAL PASS**.

Harmony B: **FROZEN**.

Beat This v1.9.3: **FROZEN**.

Golden M substitution: **BLOCKED ON VERIFIED PHYSICAL ALIGNMENT**.

Perceptual promotion: **CLOSED**.

## Next admissible action

Resolve the Apple preview position using source-level evidence. Preferred route: recover the original full-song audio used by the golden case and estimate the preview offset by direct acoustic alignment/cross-correlation. A documented authoritative preview start offset or an equivalently discriminative independent acoustic representation is also admissible.

Only after one unique alignment is verified may `prepare_m_injection.py` produce a VERIFIED manifest and `render_m_v0_5_substitution.js` generate the first controlled audible candidate. The candidate must then be compared against the frozen golden before any baseline promotion.
