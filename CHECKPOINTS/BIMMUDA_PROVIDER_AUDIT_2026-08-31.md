# BiMMuDa provider audit — checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Layer: `BIMMUDA_PROVIDER_ADMISSIBILITY_v1`
State: `IMPLEMENTED / TECHNICALLY_SUITABLE / LICENSE_PERMISSION_AUDIT_REQUIRED`

## Evidence
BiMMuDa contains manually transcribed full main-melody MIDI files, section MIDI files, lyrics and metadata for the top five Billboard Year-End singles from 1950–2022. The repository README states that the transcriptions were checked multiple times by different individuals.

Observed target-population intersections in the repository include:
- Rihanna — Umbrella (`2007_02_full.mid`)
- Carly Rae Jepsen — Call Me Maybe (`2012_02_full.mid`)

The repository is public, but GitHub repository metadata reports `license=null`, and no explicit dataset-file license was observed in the repository README during this audit. The associated TISMIR article is CC BY 4.0; that article license is not being treated as proof that the repository MIDI/lyrics files carry the same authorization.

## Decision
Current provider state: `PROVIDER_AUDIT_REQUIRED`.

This is not a technical rejection. BiMMuDa is highly compatible with the symbolic requirements of HookLab. Scientific ingestion is blocked only on explicit dataset-file licensing or research/computational-processing permission.

## Code and tests
- `mie_core/bimmuda_provider_admissibility_gate.py`
- `mie_core/test_bimmuda_provider_admissibility_gate.py`
- `experiments/gate_b2/BIMMUDA_PROVIDER_AUDIT_CURRENT_v1.json`

## Approval condition
BiMMuDa may become `PROVIDER_ADMISSIBLE` only when an authoritative provider statement establishes either:
1. an explicit dataset license permitting the intended computational research use; or
2. explicit research permission that covers computational processing of the dataset files.

## Downstream lock
Until approval, BiMMuDa entries may be used for provider/candidate discovery and coverage auditing, but must not be counted as new Matrix X scientific rows solely because the files are publicly downloadable.

## Next action
Resolve authorization from an authoritative BiMMuDa/provider source. In parallel, the observed catalog overlap may be mapped against the T1 queue without increasing qualified N.
