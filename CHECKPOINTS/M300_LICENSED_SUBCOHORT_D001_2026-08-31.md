# M300 licensed target-subcohort D001 checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
State: `52 LICENSED M300 MUSICAL-EVIDENCE INTERSECTIONS / FIRST TARGET-SUBCOHORT TEST COMPLETE / NO POSITIVE RULE PROMOTED`

## Licensed evidence coverage
The exact M300 × CoSoD crosswalk resolved 52 of 300 M300 songs to CC0 CoSoD structural/vocal evidence (17.33% coverage), with one additional identity case retained in AUDIT (`Just Give Me a Reason`: Pink vs P!nk Featuring Nate Ruess).

Run: `33414267477`
Crosswalk artifact: `9766356415`

Coverage availability is not scientific promotion. CoSoD represents collaborations and does not provide FULL_TMT-equivalent evidence for every M300 dimension.

## First target-frame subcohort analysis
Run: `33414440605`
Artifact: `9766427416`
Digest: `sha256:7a690f8f0cc7d3180a6677dbd5b47fa4f4a0c479d58b0893ee8fb1e35a637e93`

Population: exact licensed CoSoD intersections embedded in M300, years 2010-2019, N=52.

Predeclared BH-corrected tests found no supported association for:
- first chorus onset vs within-year M300 rank strength: rho=.1395, q=.6481;
- first chorus onset vs current log Spotify playcount: rho=.0401, q=.7934;
- section-event count vs rank strength: rho=-.0372, q=.7934;
- section-event count vs Spotify: rho=-.1757, q=.6481;
- median section vocal span in semitones vs rank strength: rho=.1447, q=.6481;
- median section vocal span in semitones vs Spotify: rho=.0647, q=.7934.

Decision: `NO_TARGET_SUBCOHORT_ASSOCIATION_PASSED_GATE`.

## Robustness/falsification result
The earlier CoSoD aggregate-Hz pitch-span association was re-expressed as section/performance-aware semitone spans and tested with controls for year, collaboration-type/gender and number of performers with pitch data. No normalized feature survived the association gate. Therefore the candidate positive vocal-variability hypothesis is CLOSED and cannot produce a MIDI rule.

This is a successful fail-closed result rather than a failed project result: the system discarded a representation-sensitive association instead of converting it into a compositional prescription.

## First promoted deductive knowledge
`D001_EARLY_CHORUS_NON_PROMOTION_v1.json` records a cross-cohort negative-knowledge decision. Historical McGill, full CoSoD contemporary calibration and the exact M300×CoSoD target subcohort all fail to support a universal `earlier chorus -> stronger success` rule. Consequently HookLab must not use that industry-style claim as a generative timing constraint on current evidence.

This promotion is `NEGATIVE_KNOWLEDGE / RULE_NON_PROMOTION`; it is not a claim that chorus timing is irrelevant in every scoped population.

## Readiness update
Readiness estimates, not effect sizes:
- evidence-to-deduction architecture: 100%
- historical observed calibration: 100%
- contemporary authorized calibration: 100%
- first M300 licensed musical-evidence subcohort: 52/300 coverage = 17.33% of the discovery frame; N=52 exceeds the provisional N=30 threshold for this bounded subcohort only
- first target-subcohort statistical test: 100%
- first cross-cohort negative deductive knowledge promotion: 100%
- first positive creative deduction -> MIDI: 0%, correctly blocked because no positive association survived robustness gates
- overall project readiness estimate: ~90%.

## Next active gate
Expand licensed musical-evidence coverage beyond the 52 collaboration rows and test additional musically interpretable features rather than searching for significance in the same variables. Preserve separate outcome, exposure/context, musical, textual and genre/style layers. A positive D001 may advance only after robust association, semantic validation, matched theory and independent/scoped replication.
