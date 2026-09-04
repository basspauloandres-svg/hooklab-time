# MIE v0.3.5 — historical regression inventory and sensor diagnosis — 2026-09-04 v1

Status: `NO_REPROCESS_APPLIED / HISTORICAL_GATE_NOT_PASSED`

## Audit result

The repository, all fetched remote branches and the known GitHub Actions runs
were inspected before any request for audio. No real session audio or session
ZIP is tracked in Git. Eight tracked WAV files are synthetic MB01–MB08 controls
and are not musical regression cases.

Six non-expired Actions ZIP artifacts were located. Their server digests were
verified where downloaded, without running separation or recognition. They
preserve structural-probe JSON/MIDI/WAV outputs and public-preview v0.3.1–v0.3.4
M/H/T renders. The latter are not the Animal package and cannot replace it.

The canonical machine-readable inventory is
`data/music_modeling/mie_historical_regression_inventory_v1.json`.

## Historical melody cases

| Case | Existing result | Traceable audio/package | v0.3.5 historical gate |
|---|---|---|---|
| Devuélveme/P30 golden | producer-recognizable frozen M/H/T reference | full-master, crop and integrated-WAV hashes; golden bytes not in Git | pending existing-artifact evaluation |
| Animal v0.3.4 | melody unrecognizable; 215 events; 27.2% time coverage; 72 gaps ≥500 ms; zero recovery | source and recognition-ZIP hashes match; bytes not in Git | fail |
| Independent 281.797 s case | recognizable melodic trajectory with 223 gaps ≥100 ms | duration and listening disposition only; hashes absent | pending existing-artifact evaluation |

The four-variant historical listening report is retained separately: all four
variants sounded identical and the producer concluded that separation was not
the problem in that session. Because its case hash and exact M/H/T linkage were
not recovered, it cannot be silently attached to Animal or generalized.

Generic A/B structural previews, TIME-only cases and RT-001/002/005 are retained
as engineering evidence but are ineligible for the melody recognizability gate.

## SOURCE_SEPARATION_VS_NOTE_SENSOR_RECALL

`DATA SAYS`: one independent reconstruction retained a recognizable trajectory
despite recurrent gaps; Animal retained sparse melody time, recovered no new
candidates and failed producer recognition; one unlinked four-variant session
did not change audibly with the separator variants.

`STATISTICS SAY`: no registered same-source denominator currently measures
independent vocal presence before separation against activity after separation.
The Animal package metadata therefore cannot estimate separator recall, and
27.2% remains temporal coverage rather than accuracy.

`DIAGNOSIS`: historical evidence supports `NOTE_SENSOR_RECALL_BOTTLENECK` as the
priority hypothesis and does not support separator replacement as the first
intervention. The causal split for the traceable Animal failure remains
`ABSTAIN_INSUFFICIENT_MELODY_EVIDENCE` until an existing authorized artifact can
supply the independent aligned observation. No notes may be manufactured to
resolve that abstention.

## Enforced next state

- `changed_module=M_ONLY`;
- `H=FROZEN_PREDECLARED_COMPARISON_REFERENCE_NO_DEVELOPMENT`;
- `T=FROZEN_ENGINEERING_BASELINE_PRESERVED`;
- `new_audio_request_allowed=false`;
- existing v0.3.1–v0.3.4 outputs, hashes and producer dispositions remain intact;
- new works may be requested only after `MIE_v0.3.5_HISTORICAL_GATE_PASSED`.

The next permitted operation is a newly identified v0.3.5 M-only evaluation on
recovered existing historical bytes. If those bytes cannot be recovered, the
result remains abstention; the missing evidence is not silently reconstructed.
