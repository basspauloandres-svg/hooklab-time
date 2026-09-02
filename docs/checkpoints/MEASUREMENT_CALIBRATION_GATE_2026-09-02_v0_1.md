# HookLab/TIME-MIE — Measurement Calibration Gate — 2026-09-02 v0.1

## Status

`CALIBRATION_DESIGN_REGISTERED_EXECUTION_PENDING_REFERENCE_DATA`

This increment registers measurement calibration. It does not execute a
feature/outcome association, reopen a frozen analysis, or create a conditioned
deduction.

## Empirical frame

- Canonical lyric identity space: `HOOKLAB_C001_C100`.
- Canonical source revision: `72`.
- Eligible documentary frame: 99 cases; C077 remains excluded because every
  existing internal copy is incomplete.
- Frozen lyric calibration sample: 30 cases selected reproducibly from
  provisional language strata.
- Raw lyric text remains in the private authorized source environment.
- Groove, BabySlakh and Lakh remain auxiliary/test lanes and are not HookLab
  corpus observations.

## Registered calibration lanes

### Explicit-person lyric measurement

Two annotators independently label overt person/address evidence. Every core
label requires overall nominal Krippendorff alpha >= .80. An adequately
prevalent language stratum below .67, an undefined coefficient, systematic
language error, or source mismatch remains an audit condition.

Reference: Hayes and Krippendorff (2007),
https://doi.org/10.1080/19312450709336664.

### Melody measurement

At least 30 independent aligned reference/estimate pairs are required. The
registered minimum rank agreement is Spearman rho >= .80. Pitch-range median
absolute error must be <= 1 semitone and its 90th percentile <= 3 semitones;
melody-onset-density median absolute percentage error must be <= 10%.

Melody evaluation must also report bias and 95% limits of agreement. Passing
one descriptor cannot automatically validate the other.

References: Raffel et al. (2014), https://zenodo.org/records/1416528; Bland and
Altman (1986), https://pubmed.ncbi.nlm.nih.gov/2868172/.

### Beat and tempo measurement

At least 30 canonical case-linked real-audio references are required. Beat
matching uses the standard +/-70 ms window. Median per-song F-measure must be
>= .80 and the 10th percentile >= .60. Tempo additionally requires rho >= .80,
median absolute percentage error <= 4%, and octave/tactus error rate <= 10%.

Beat This remains probabilistic evidence. `SEARCH -> LOCK` still requires
independent evidence, margin, temporal persistence and phase/grouping
coherence. Multiple scores from one detector count as one source family.

References: MIREX Audio Beat Tracking,
https://music-ir.org/mirex/wiki/2021:Audio_Beat_Tracking; Schreiber, Urbano and
Müller (2020), https://doi.org/10.5334/tismir.43.

## Fail-closed result

- Features admitted: 0.
- Inferential analyses registered: 0.
- Statistical associations executed: 0.
- Conditioned deductions: 0.
- `generation_class=D0_EXPLORATORY`.
- `scientific_d_unlocked=false`.

The immediate execution gate is human confirmation of language and document
version for the 30 frozen lyric cases, independent double annotation, and
mapping of at least 30 canonical real-audio/melody references.
