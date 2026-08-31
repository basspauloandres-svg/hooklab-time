# HookLab/TIME-MIE — Mobile product gate checkpoint v1

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`

## Decision
`LOCAL_ON_DEVICE_ONNX` is the primary mobile path for `AESTHETIC_REFERENCE_ANALYSIS`.
`ONLINE_API` remains a resilience fallback only.

## Corroboration
1. Browser Beat This vs authoritative CLI equivalence PASS (workflow run `33450481336`).
   - relative BPM error: 1.99% (predeclared <=3%)
   - relative beat-count difference: 1.35% (predeclared <=15%)
   - median nearest-beat error: 0 ms (predeclared <=100 ms)
2. Mobile viewport regression initial run `33452456516` correctly FAILed because Android minimum button height was 35 px under the predeclared >=36 px gate.
3. UI-only correction: button `min-height:40px`, commit `26ab819123f869605b474b243c0be99e11ed0d81`.
4. D0 regression after UI correction: PASS.
5. Mobile viewport rerun `33452656212`: PASS.
   - `iphone_webkit`, 390x844: min button height 40 px; no horizontal overflow; D0=true; persisted=true.
   - `android_chromium`, 412x915: min button height 40 px; no horizontal overflow; D0=true; persisted=true.

## Scientific invariants unchanged
`AESTHETIC_REFERENCE != AESTHETIC_REFERENCE_ANALYSIS != M300_EVIDENCE != SUCCESS_EVIDENCE != GATE_A_ACQUISITION`.
`D0_EXPLORATORY != SCIENTIFIC_D`.
`SCIENTIFIC_D` remains fail-closed pending observed melody-representation calibration and deduction eligibility.

## Product status after this gate
- mobile responsive/browser compatibility: PASS automated
- on-device beat analysis equivalence: PASS
- D0 generation after mobile correction: PASS
- ONLINE_API fallback: implementation/deployment pending
- physical-device manual acceptance: pending
- observed scientific calibration >=30 independent pairs: pending and separate from product UX
