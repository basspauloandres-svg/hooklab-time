# International Research Symbolic Provider Registry — checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Layer: `INTERNATIONAL_RESEARCH_SYMBOLIC_PROVIDER_REGISTRY_v1`
State: `IMPLEMENTED / PROVIDER_CLASSIFICATION_ACTIVE / T1_CROSSWALKS_PENDING`

## Purpose
Identify legitimate symbolic-data providers for research without allowing provider availability to redefine the HookLab scientific target population.

## Corroborated providers
- BiMMuDa: technically suitable and 7/25 T1 matches observed, but dataset license/processing permission remains `AUDIT_REQUIRED`.
- CCMusic: Zenodo description explicitly states free use by computational musicology/MIR researchers and provides MIDI/WAV/lyrics resources.
- POP909: public research dataset with MIT-licensed repository and explicit processing examples; target-song copyright/provenance must still be evaluated before scientific promotion.
- Lakh Pianoroll Dataset: CC BY 4.0 derivative dataset; remains auxiliary and cannot become the primary alternative-arrangement route.
- Pop-K: CC BY-NC augmented modern-pop symbolic dataset; useful for method/model validation, not direct full-song target qualification.
- Pop1K7: research-oriented open Zenodo dataset; exact dataset license remains to be verified.

## Code
- `mie_core/international_research_provider_gate.py`
- `experiments/gate_b2/INTERNATIONAL_RESEARCH_SYMBOLIC_PROVIDER_REGISTRY_v1.json`

## Gate rule
Provider-level PASS requires explicit research/open license, explicit computational processing, and provenance. Even provider PASS never makes a song a scientific row automatically; the song must independently pass TSDQP identity/version/genre-success/FULL_SONG/FULL_TMT gates.

## Current scientific N
Unchanged. Provider discovery and provider permission do not increment Matrix X.

## Next valid action
Cross the 18 T1 songs not covered by BiMMuDa against CCMusic, POP909, Pop1K7 and other explicitly research-authorized catalogs. Record exact matches separately from provider eligibility, then run song-level qualification on any observed matches.
