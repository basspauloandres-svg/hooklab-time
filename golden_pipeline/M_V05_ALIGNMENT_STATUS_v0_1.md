# M v0.5 → Golden H/T alignment status v0.1

Date: 2026-08-29
Status: BLOCKED — source identity is known, physical preview offset is not verified.

## Purpose

Record the evidence required before the structurally validated M v0.5 stream may replace P30 inside the frozen golden Harmony B + Beat This renderer.

This document prevents a future session from converting a plausible temporal offset into an asserted alignment.

## Confirmed evidence

- M v0.5 passed the structural regression + generic A + generic B gate with zero resolver-introduced large jumps and zero octave-or-more interval worsening in all three cases.
- Regression audio is the authorized Apple/iTunes preview of Luis Miguel, `Devuélveme El Amor`.
- Historical workflow commit `83b6ee229fe982b54865f9b18d58a64ded8b3ff7` downloads the preview URL directly and applies no `-ss`/seek or timeline offset. The downloaded preview is approximately 29.93 s long.
- Frozen golden reference window is 13.3–40.7 s on the full-song physical timeline.
- `Devue_lveme_El_Amor_completo.json` contains the full-song Beat This/tactus timeline; the Beat This timestamps embedded in `app-mie-p30-harmony-beat-v0.1.html` are members of that full-song timeline.
- Frozen renderer SHA-256: `8ae79a4c6f92cea9d48a6aea5cd1cc3d4496dbd993e9cf0d229e6fcfcb4c5541`.
- Frozen golden WAV SHA-256: `de8381ef9322e73bf295db40a9dffeb0528469502313ea949c4c9018fe9cd940`.

## Rejected alignment

`preview_t + 13.3 s -> full-song_t` is REJECTED.

Reasons:

1. It was initially suggested only by the golden window start, not by source provenance.
2. Tactus comparison gives median absolute error about 31.82 ms and maximum about 63.15 ms.
3. The mapped opening melody does not correspond to the frozen P30 opening: M v0.5 begins around MIDI 64/62 while P30 at 13.3 s begins 48→57→59→60→62.
4. Therefore `+13.3 s` must never be passed to `prepare_m_injection.py` as `same-source-confirmed` evidence.

## Why beat alignment alone is insufficient

The song has a stable tactus near 70 BPM. Consequently many different full-song offsets align a 30 s preview beat train to the full-song tactus with small residuals.

Examples from the current diagnostic, using nearest full-song tactus event for each preview Beat This event:

| Candidate offset | Median abs. error | Mean abs. error | Max abs. error | Decision |
|---:|---:|---:|---:|---|
| 13.26475 s | 8.38 ms | 11.67 ms | 31.96 ms | ambiguous |
| 17.56335 s | 9.19 ms | 14.52 ms | 34.70 ms | ambiguous |
| 22.70724 s | 5.60 ms | 8.55 ms | 25.97 ms | ambiguous |
| 43.28127 s | 6.14 ms | 7.91 ms | 22.71 ms | ambiguous |
| 70.71791 s | 5.03 ms | 6.69 ms | 24.70 ms | ambiguous |

The lowest timing residual is therefore not evidence of the true editorial preview position.

## Melody diagnostic

A joint melody comparison makes ~17.56 s more plausible than +13.3 s within the limited P30 overlap, but the match remains insufficient and is not source-level evidence. This diagnostic must not be promoted to alignment truth because:

- P30 exists only for 13.3–40.7 s;
- M v0.5 is itself the component under evaluation;
- repeated/motivic pitch patterns can create false matches;
- candidate offsets outside the P30 window cannot be ruled out by that comparison.

## Required evidence to unlock rendering

At least one source-level alignment route is required:

1. Recover the original full-song audio used for the golden case and directly cross-correlate it against the Apple preview; or
2. recover a documented Apple preview start offset from an authoritative artifact/source; or
3. recover another full-song acoustic representation independent of M and sufficiently discriminative to establish one unique preview location.

Beat periodicity alone is explicitly insufficient.

## Guarded renderer

`golden_pipeline/render_m_v0_5_substitution.js` is now the only permitted M v0.5 golden substitution path.

It refuses rendering unless:

- canonical renderer SHA matches the frozen renderer;
- Harmony B canonical hash matches the frozen 33-unit array;
- Beat This canonical hash matches the frozen 34-timestamp array;
- `alignment_status == VERIFIED`;
- `same_source_confirmed == true`;
- explicit `alignment_evidence` is present;
- all melody events are LOCK and remain inside 13.3–40.7 s.

CI test `golden_pipeline/test_m_v0_5_substitution_guard.py` verifies two negative invariants: an unverified alignment is rejected and a one-byte renderer change is rejected before audio is written.

## Current decision

M v0.5 remains STRUCTURALLY PASSED / PERCEPTUALLY UNPROMOTED.

Golden M substitution remains BLOCKED ON PHYSICAL ALIGNMENT. Harmony B and Beat This remain frozen and untouched. No audition candidate is authorized from the Apple preview until the alignment gate is satisfied.
