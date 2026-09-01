# M300 licensed musical coverage + DALI adapter checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
State: `MULTI_PROVIDER_COVERAGE_OBSERVED / DALI OPTIONAL_ADAPTER_IMPLEMENTED / D001 POSITIVE_RULE_NOT_YET_PROMOTED`

## Observed licensed coverage
The current fail-closed provider pipeline has observed:
- CoSoD: 52 exact M300 song identities with licensed contemporary structural/vocal-analysis evidence.
- Harmonix Set: 55 song identities initially resolved; after version-duration identity gate, 28 remain compatible and 27 are `AUDIT_VERSION_MISMATCH`.
- SALAMI: 0 PASS, 1 identity AUDIT, 299 REFERENCE_UNAVAILABLE.
- Version-gated union CoSoD ∪ Harmonix: 75 unique M300 songs = 25.0% of the 300-song discovery frame.
- CoSoD ∩ Harmonix after version gate: 5 songs. This is insufficient to declare ontology equivalence; provider metrics remain separate.

## Negative deductive evidence already retained
Within the licensed CoSoD M300 subcohort, early-chorus timing and the tested formal-repetition/architecture variables did not pass the predeclared promotion gate after multiplicity control. A preliminary aggregate vocal pitch-span association also disappeared after musically appropriate semitone normalization and controls. These are non-promotion findings, not evidence that the variables are universally irrelevant.

## DALI
DALI is retained as an optional research-only melody/lyrics annotation provider. Current public record indicates non-commercial research licensing without a purchase fee, but dataset files require provider-granted access/provisioning.

Implemented:
- `mie_core/dali_research_provider_adapter.py`
- `mie_core/test_dali_research_provider_adapter.py`

Fail-closed invariant:
- no provisioning -> `REFERENCE_UNAVAILABLE` deterministically;
- no previews, scraping, YouTube/video retrieval, commercial-audio substitution or alternate unauthorized downloads;
- dataset present -> `AUDIT_PROVISIONED` until schema/version identity is validated;
- DALI annotation access does not satisfy released-recording Gate A.

## Scientific interpretation
The project now has a defensible licensed structural/vocal-analysis evidence layer for 25% of M300, but it still lacks broad melody-note/lyrics-alignment coverage needed for the first positive evidence-to-creative deduction. The correct next path is to expand licensed melody/prosody evidence and/or provision DALI, then test new musically interpretable features under the frozen deduction gate.

## Readiness estimate
Readiness percentages are engineering/scientific readiness estimates, not effect sizes:
- core architecture/software: 96%
- epistemic/deductive framework: 100%
- discovery frame: 300/300 = 100%
- licensed structural/vocal-analysis M300 coverage: 75/300 = 25.0%
- positive substantive D001 rule promotion: 0% (no positive rule has survived all current gates)
- negative/non-promotion deductive evidence: operational and observed
- overall project readiness: approximately 91%, with remaining risk concentrated in melody/prosody coverage, provider version identity, positive rule replication and MIDI/human creative validation.
