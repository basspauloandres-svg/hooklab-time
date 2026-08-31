# Scientific layer approval checkpoint — 2026-08-30

Canonical branch: `mie/golden-forensic-v0.3`
Status: `APPROVED / DOWNSTREAM_ELIGIBLE`
Layer ID: `SCIENTIFIC_LAYER_APPROVAL_INVARIANT_v1`

Approved components:
- scientific basis/decision record: `docs/SCIENTIFIC_LAYER_APPROVAL_INVARIANT_v1.md`
- implementation: `mie_core/scientific_layer_gate.py`
- tests: `mie_core/test_scientific_layer_gate.py`

Approval rule: every new scientific/generative layer must persist scientific basis, decision record, explicit implementation, tests/validation, provenance and checkpoint before it can control a downstream layer. Missing requirements block promotion fail-closed.

Required state sequence:
`PROPOSED -> IMPLEMENTED -> VALIDATED -> APPROVED -> DOWNSTREAM_ELIGIBLE`

This invariant applies immediately to Gate B2 and all later scientific layers. Future migration checkpoints must reference this file or an explicit superseding version before promoting new layers.
