# T1 symbolic source resolution — batch 01 checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Layer: `T1_SYMBOLIC_SOURCE_RESOLUTION_BATCH01_v1`
State: `IMPLEMENTED / OBSERVED / NO_PASS_SOURCES`

## Cases
- Umbrella — Rihanna feat. Jay-Z
- Call Me Maybe — Carly Rae Jepsen

Both entered this layer with mass-success, identity and genre/style already passing in the current qualification evidence.

## Observed source-resolution result
Multiple real symbolic sources were located for each song, including full-length and commercially licensed MIDI products. However, no located provider simultaneously established:
1. resolved target version;
2. full-length symbolic representation;
3. auditable provenance;
4. legitimate access mode for the pipeline; and
5. explicit authorization for automated computational processing.

Therefore both cases remain `symbolic_source = AUDIT`.

`AUDIT` is not `FAIL`. The result means a plausible source exists but scientific admissibility is not yet established.

## Code
- `mie_core/symbolic_source_admissibility_gate.py`
- `mie_core/test_symbolic_source_admissibility_gate.py`

## Evidence
- `experiments/gate_b2/T1_SYMBOLIC_SOURCE_RESOLUTION_BATCH01_v1.json`

## Scientific boundary
A downloadable, purchasable or commercially licensed MIDI does not automatically authorize automated corpus processing. A platform-declared CC0 label on a copyrighted-song arrangement is not promoted without confirming that the provider/upload has the authority needed for the intended use.

## Decision
- Umbrella: `AUDIT`
- Call Me Maybe: `AUDIT`
- New qualified Matrix-X rows: 0

## Next valid action
Continue automated provider resolution through sources/datasets whose terms explicitly permit computational research processing. Do not substitute previews, demos, stream-only media, or manual user uploads. If no configured legitimate provider yields an admissible symbolic source, retain the case in AUDIT and move to the next T1 candidate rather than weakening the gate.
