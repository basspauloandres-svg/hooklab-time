# CoSoD contemporary Evidence-to-Creative Deduction calibration

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
State: `OBSERVED CONTEMPORARY ASSOCIATION / THEORY+REPLICATION REQUIRED / NO GENERATIVE PROMOTION`

## Observed run
Workflow run `33413476817` completed successfully on the canonical branch and produced artifact `cosod-contemporary-deduction-calibration` (id `9766062366`, digest `sha256:2315f157fe55f29d94fcde01eb66bf4f22bd93676cc69417d66461c3f63a27da`).

The schema audit resolved 331/331 metadata rows and 331/331 analysis rows from the CC0 CoSoD dataset. The contemporary calibration therefore supplies N=331 joined observations for a bounded 2010-2019 Billboard Year-End collaboration subpopulation.

## Exploratory association results
Predeclared gate: N>=100, |Spearman rho|>=0.15, BH-adjusted q<0.05.

Did not pass:
- first chorus time: rho=0.0948, q=0.1576, N=330
- first chorus ratio: rho=0.0922, q=0.1576, N=330
- section-event count: rho=0.0416, q=0.5634, N=331
- duration proxy: rho=0.0147, q=0.7899, N=331

Passed exploratory gate:
- vocal pitch span (Hz) vs year-end peak-strength: rho=0.1745, p=0.00149, BH q=0.00743, N=329

## Interpretation boundary
This is a small observational association in a specific contemporary subpopulation. It is not evidence that increasing vocal pitch span causes commercial success, not a universal pop rule, and not yet a HookLab generative constraint. Exposure, artist history, genre/style, collaboration type and other confounds remain unmodeled here.

The four non-supported variables are scientifically useful negative evidence and remain part of the record. In particular, this calibration does not support an industry-style claim that earlier chorus entry or shorter duration is universally associated with stronger year-end chart position in this subpopulation.

## Consequence for D001
The Evidence-to-Creative Deduction direction has now crossed a stronger prototype threshold: an actual N>300 contemporary dataset produced one bounded association and four explicit non-support results. The supported association advances only to `CANDIDATE_FOR_THEORY_MATCHING_AND_INDEPENDENT_REPLICATION`.

Required before MIDI deduction:
1. verify feature semantics for pitch-span and robustness to outliers/representation;
2. inspect relevant peer-reviewed theory without retrofitting a causal story;
3. stratify/control at least year and available context variables; genre/style remains analytical stratification rather than universal gate;
4. seek independent replication in a second admissible dataset;
5. only then consider a bounded melodic realization experiment.

## Development impact
- Evidence-to-deduction structural prototype: 100%
- Contemporary observed-association calibration: 100%
- Theory matching for first real candidate: 0% at this checkpoint
- Independent replication: 0% at this checkpoint
- Generative promotion: 0%

This checkpoint does not replace the target 300-song discovery frame or promote CoSoD rows into the target Matrix X. Its role is methodological calibration with observed contemporary evidence.
