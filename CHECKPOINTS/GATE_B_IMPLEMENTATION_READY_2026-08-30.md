# Gate B checkpoint — 2026-08-30

Status: `IMPLEMENTATION_READY / HUMAN_OBSERVATIONS_PENDING`

Canonical protocol: `docs/HUMAN_TTFP_BASELINE_PROTOCOL_v1_0.md`.

Implemented components:
- `mie_core/gate_b_human_ttpf_trial.py`
- `mie_core/gate_b_trial_template_v1.json`
- `mie_core/test_gate_b_human_ttpf_trial.py`
- `.github/workflows/gate-b-human-ttfp-tests.yml`

Scientific invariants:
1. Gate B is populated only by observed human/traditional workflow timings.
2. Simulated, estimated, synthetic, retrospectively reconstructed, or model-generated timings are invalid.
3. The TTFP clock stops only when the predefined minimum output contract is satisfied.
4. Raw per-participant/per-task observations are retained before summaries.
5. Engine latency remains frozen separately at the existing technical benchmark and is not rerun merely to optimize the comparison.
6. `TTFP_HookLab_assisted` must remain separate from pure engine latency when human candidate-review time is later observed.
7. A descriptive speed ratio may be calculated after observed data exist; it is not evidence of equivalent artistic quality.
8. No claim that HookLab is faster than human/traditional practice is permitted until observed Gate B evidence exists and output comparability has been audited.

Current state:
- implementation: complete enough for reproducible data capture and validation;
- observed valid human trials: 0;
- Gate B scientific state: `PENDING_OBSERVATIONS`;
- Gate C remains downstream of Gate B empirical population and Gate A external validation state.
