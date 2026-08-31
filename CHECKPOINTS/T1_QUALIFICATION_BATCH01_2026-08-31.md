# T1 Dance-Pop qualification — observed batch 01 checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Layer: `T1_QUALIFICATION_BATCH01`
State: `OBSERVED_PARTIAL_GATES / NO_NEW_MATRIX_X_ROWS`

## Scope
Five discovery candidates were evaluated only on externally observable early gates: mass-success, metadata identity, and genre/style classification. Version correspondence to a symbolic representation, symbolic-source resolution, FULL_SONG, provenance, and FULL_TMT remain pending until an actual symbolic candidate is resolved and audited.

## Observed results
- Born This Way — mass_success PASS; identity PASS; genre_style AUDIT.
- Umbrella — mass_success PASS; identity PASS; genre_style PASS.
- Call Me Maybe — mass_success PASS; identity PASS; genre_style PASS.
- Don't Start Now — mass_success PASS; identity PASS; genre_style AUDIT because retrieved AllMusic evidence reports Electronic/Club-Dance rather than direct Dance-Pop.
- We R Who We R — mass_success PASS; identity PASS; genre_style AUDIT pending direct song-level Dance-Pop corroboration.

All five exceed the existing engineering broad-reach floors of 100M observed YouTube views and 100M Spotify streams in the sources recorded in `experiments/gate_b2/T1_QUALIFICATION_BATCH01_OBSERVED_v1.json`.

## Code and tests
- `mie_core/t1_observed_evidence_merger.py`
- `mie_core/test_t1_observed_evidence_merger.py`

The merger preserves PASS/AUDIT/FAIL/PENDING semantics and never converts partial evidence into a qualified Matrix-X row.

## Decision
Qualified T1 additions from this batch: 0.
Current scientifically qualified Dance-Pop N remains 5 (T0).

## Next valid layer
For the two genre/style PASS cases (`Umbrella`, `Call Me Maybe`), proceed next to automatic legitimate symbolic-source resolution and then separately evaluate version, FULL_SONG, provenance and FULL_TMT. For the three AUDIT cases, resolve genre/style corroboration in parallel without treating AUDIT as failure.
