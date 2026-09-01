# D001 historical evidence calibration checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
State: `OBSERVED_EMPIRICAL_CALIBRATION_SUCCESS / CONTEMPORARY_D001_STILL_BLOCKED`

## Authorized evidence source
McGill Billboard Project annotations are published by DDMAL under CC0. The provider documents complete chord/structure/timing annotations and Billboard metadata including peak rank and weeks on chart. This cohort covers the historical Billboard period 1958-1991 and is therefore a methodological calibration cohort, not a substitute for the contemporary HookLab target frame.

## Observed execution
GitHub Actions run: `33412991819`
Artifact: `9765881790`
Digest: `sha256:e5207da6b99ef1fccb2d40016641f34edb3ce518c47eeb0231382b80ff25d577`
Workflow conclusion: success.

The parser produced 742 exact title-artist rows with annotations and outcome metadata. Provider documentation reports 740 distinct songs; this 2-row discrepancy is an explicit integrity AUDIT and blocks stronger population claims until reconciled.

## Exploratory results
BH-corrected Spearman tests were run over structural/harmonic features against Billboard weeks-on-chart and peak strength.

Most important falsification-oriented result:
- first chorus relative position vs weeks on chart: n=619, rho=-0.0212, q=.6388 -> no association observed.
- first chorus relative position vs peak strength: n=619, rho=-0.0236, q=.6381 -> no association observed.

Therefore the system must NOT promote an industry-style universal rule that an earlier chorus implies greater Billboard success. This historical null result does not prove that such an effect is absent in contemporary or genre-specific populations.

Exploratory positive associations with weeks on chart were observed for duration, chord-token count and section-event counts. They are NOT promoted because duration mechanically covaries with counts and exposure/period/genre-style have not been controlled.

## Scientific meaning
The Evidence-to-Creative Deduction architecture has now passed an observed-data calibration rather than only a structural placeholder test. It demonstrated both functions required by the project:
1. identify associations that require further interpretation/confound control;
2. refuse to convert a widely plausible compositional claim into a rule when the observed data do not support it.

## Promotion boundary
`scientific_promotion=false`

No MIDI rule is generated from this historical calibration. Contemporary D001 remains blocked until sufficiently eligible contemporary musical rows exist and the actual pattern is interpreted with matched literature and alternative explanations.

## Readiness update
These are readiness estimates, not effect sizes:
- conceptual evidence-to-deduction direction: 100%
- fail-closed implementation: 100%
- structural prototype validation: 100%
- observed historical empirical calibration: 100%
- first contemporary substantive deduction: 0% (still blocked by eligible contemporary musical data)
- evidence-to-deduction layer overall: approximately 60% because the method has passed a real-data calibration but has not yet completed the contemporary pattern -> theory -> MIDI -> producer cycle.
- overall project readiness: approximately 88%; empirical contemporary musical evidence remains the principal bottleneck.

## Next active gate
Use the same evidence architecture to build contemporary eligible rows. Genre/style remains stratification/context rather than a universal gate. Preserve outcome, exposure, context, musical data and audience as separate layers. Do not promote count-like structural associations before duration/confound controls.
