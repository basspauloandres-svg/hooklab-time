# HookLab/TIME-MIE — Manual Commercial Reference Audio Layer v0.1

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
Status: `PROPOSED_AND_EVIDENCE_SUPPORTED / IMPLEMENTATION_NEXT`

## Purpose
Add a user-selected, manually supplied **reference audio** layer for preproduction. This layer analyzes a commercial reference chosen for the style/sonic direction of the new song and converts measurable properties into a separate reference profile.

## Scientific rationale
Reference songs are established professional communication artifacts in music production. Vanka et al. (2024, Journal of the Audio Engineering Society) report that professional mixing workflows use reference songs and demo mixes to communicate desired sound, emotion and sonic character. Research on audio-production style transfer also formalizes the use of a reference recording to estimate production-style characteristics (Steinmetz, Bryan & Reiss, 2022; Steinmetz et al., ISMIR 2024).

## Critical separation
This layer is **not corpus evidence** and must never increase robust-cohort N or become statistical evidence merely because the user selected a commercially released track.

Keep separate:
1. `CORPUS_STATISTICAL_EVIDENCE` — population/cohort-derived evidence.
2. `MANUAL_REFERENCE_AUDIO` — one user-selected reference for local creative/style guidance.
3. `PRODUCER_EXPERIENCE` — professional human judgment.

The creative integration may use all three, but provenance must identify which source conditioned each recommendation.

## Input policy
Manual upload is explicitly permitted for this layer because the user is intentionally supplying a reference they are entitled to access for private research/preproduction analysis. The audio is an ephemeral/local analytical input by default.

The layer must not:
- publish or redistribute the uploaded recording;
- commit the copyrighted audio to the repository;
- expose the recording as a dataset artifact;
- treat private/noncommercial intent as proof of copyright permission;
- use the recording to increase the scientific corpus N without separate corpus qualification/licensing.

Persist only derived features, hashes/fingerprints where lawful/appropriate, user-declared identity metadata, analysis configuration and provenance. Raw audio retention should default to `EPHEMERAL_DELETE_AFTER_ANALYSIS` unless an authorized retention basis is explicitly recorded.

## Analysis targets
Initial reference profile should measure/estimate, with confidence and method provenance:
- duration;
- tempo/tactus and meter confidence;
- section boundaries / repetition structure;
- global and section-level loudness/dynamics;
- spectral/timbral descriptors (e.g. brightness/centroid, low-frequency energy, bandwidth where supported);
- stereo-width descriptors where technically supported;
- onset/rhythmic density and pulse characteristics;
- vocal/instrumental segmentation or stem-derived descriptors where the existing analyzer supports them;
- melodic contour/range only when extraction confidence is sufficient;
- production-style descriptors kept distinct from compositional corpus statistics.

## Output
`MANUAL_REFERENCE_PROFILE_v1` containing:
- `reference_id`;
- user-declared title/artist/version;
- cryptographic file hash;
- input duration/format;
- analysis methods and versions;
- feature values + confidence;
- section-level profile;
- provenance;
- retention/deletion state;
- interpretation boundary.

## Integration rule
The preproduction engine may present three clearly labeled recommendation channels:

`DATA SAYS` → robust corpus statistical evidence.

`REFERENCE SAYS` → measurable properties of the manually supplied reference audio.

`PRODUCER DECIDES` → human selection/modification/rejection.

A final HookLab proposal may combine them, but each generated decision must preserve lineage to one or more channels.

## Evaluation opportunity
Gate B2/H+D can additionally record whether a retained/modified creative decision was conditioned by corpus statistics, the manual reference, producer experience, or an explicit combination. This enables analysis of how statistical evidence and situated professional reference listening interact.

## References
Vanka, S. S., Safi, M., Rolland, J.-B., & Fazekas, G. (2024). The Role of Communication and Reference Songs in the Mixing Process: Insights From Professional Mix Engineers. Journal of the Audio Engineering Society, 72(1/2), 5–15. https://doi.org/10.17743/jaes.2022.0123

Steinmetz, C. J., Bryan, N. J., & Reiss, J. D. (2022). Style Transfer of Audio Effects with Differentiable Signal Processing. Journal of the Audio Engineering Society, 70(9), 708–721.
