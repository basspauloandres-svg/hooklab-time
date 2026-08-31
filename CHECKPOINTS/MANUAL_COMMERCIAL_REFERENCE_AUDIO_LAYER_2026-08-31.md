# Manual Commercial Reference Audio Layer — checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Layer ID: `MANUAL_COMMERCIAL_REFERENCE_AUDIO_v1`
State: `EVIDENCE_SUPPORTED / CONTRACT_IMPLEMENTED / ANALYZER_INTEGRATION_PENDING`

## Approved purpose
Allow a producer/researcher to manually supply a commercial audio reference for private preproduction/style analysis. This is an intentional exception to the earlier no-manual-upload rule, which remains valid for Gate A automated external scientific validation. The two paths serve different purposes and must not be conflated.

## Scientific support
Professional reference songs are documented as communication/context tools in mixing and production (Vanka et al., JAES 2024). Reference-recording-based audio production style transfer is also an established research task (Steinmetz, Bryan & Reiss, JAES 2022; later MIR work).

## Frozen separation
- Gate A external validation: automatic legitimate reference resolution; no routine manual user upload.
- Manual Reference Audio Layer: manual upload explicitly allowed because the producer intentionally selects the reference for local style/preproduction guidance.
- Manual reference audio never increases corpus N and never becomes Matrix X population evidence through this path.

## Frozen UX concept
Present three channels separately:
1. `DATA SAYS` — robust cohort statistics.
2. `REFERENCE SAYS` — measured properties of the supplied commercial reference.
3. `PRODUCER DECIDES` — professional judgment and final selection.

## Repository policy
Raw commercial audio must not be committed. Default lifecycle is ephemeral analysis followed by deletion. Persist only derived features, configuration/method versions, confidence, hash, identity metadata and provenance.

## Code
- `mie_core/manual_reference_audio_contract.py`
- `mie_core/test_manual_reference_audio_contract.py`

## Next layer
Implement the `MANUAL_REFERENCE_PROFILE_v1` analyzer by composing existing HookLab audio-analysis components where technically valid. New descriptors require their own validation/approval layer before becoming recommendation-driving features.
