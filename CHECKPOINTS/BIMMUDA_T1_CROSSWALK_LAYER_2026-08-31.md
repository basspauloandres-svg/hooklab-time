# BiMMuDa × T1 coverage crosswalk — checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Layer: `BIMMUDA_T1_CROSSWALK_v1`
State: `IMPLEMENTED / PARTIAL_OBSERVED / PROVIDER_LICENSE_AUDIT_PENDING`

## Purpose
Measure potential symbolic-source coverage of the HookLab T1 Dance-Pop candidate queue using BiMMuDa without treating dataset presence as scientific qualification.

## Corroborated provider structure
BiMMuDa exposes per-song metadata and, when available, a full main-melody MIDI, section MIDIs and lyrics. The repository states that songs were manually transcribed and checked multiple times by different individuals.

## Confirmed T1 intersections
- `Umbrella` (Rihanna) -> `2007_02`, full MIDI + section MIDIs + lyrics observed.
- `Call Me Maybe` (Carly Rae Jepsen) -> `2012_02`, full MIDI + section MIDIs + lyrics observed.

## License boundary
The public GitHub repository currently reports no repository license. Public availability therefore does not establish authorization for HookLab computational processing. All covered rows remain blocked at `BLOCKED_LICENSE_AUDIT` until authoritative permission is resolved.

## Code
- `mie_core/bimmuda_t1_crosswalk_builder.py`
- `mie_core/test_bimmuda_t1_crosswalk_builder.py`

## Evidence state
- `experiments/gate_b2/BIMMUDA_T1_CROSSWALK_OBSERVED_CURRENT_v1.json`

## Scientific decision
`scientifically_promoted_rows = 0` from BiMMuDa at this checkpoint.

## Next valid action
Execute the crosswalk against the full BiMMuDa metadata to quantify total T1 coverage, then resolve the provider authorization/licensing question from an authoritative source before processing any BiMMuDa MIDI for FULL_TMT or Matrix X.

## Invariants
- dataset available != scientific target population
- dataset presence != license authorization
- candidate discovery != scientific promotion
