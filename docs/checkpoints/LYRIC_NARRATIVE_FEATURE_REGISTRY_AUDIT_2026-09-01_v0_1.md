# HookLab/TIME-MIE — Initial Lyric/Narrative Feature Registry Audit v0.1

Date: 2026-09-01  
Registry: `data/lyric_modeling/lyric_narrative_feature_registry_v0_1.json`  
Disposition: `FAIL_CLOSED_SOURCE_RESOLVED_FEATURES_PENDING`

## Governing scope

This audit is governed by the 2026-09-01 HookLab/TIME-MIE migration checkpoint, startup prompt, manifest, and the repository invariants and contracts named there.

POD-LC is methodological background and may support observational definitions when pertinent. It is not the governing HookLab specification. Its six observation lines are not statistical variables, narrative categories, generative features, functional tags, or song-section labels.

No material contradiction between the HookLab checkpoint and a POD-LC antecedent was required to make this audit. Therefore `AUDIT_SCOPE_CONFLICT` is not emitted. Neither M9 nor another prior POD-LC process was reopened.

## Mandatory A–F distinction

| Class | Finding at audit time | Statistical consequence |
|---|---|---|
| A. Present in data/system | The canonical internal source frame contains C001-C100 at synchronized revision 72 with 100 provider IDs. Pilot randomization, validation schemas, Story Brief, narrative-state, section, candidate-text and musical/prosodic fields also exist. | Source text, design assignments and runtime fields do not become calibrated statistical lyric features by existence alone. |
| B. Candidate constructs | Perspective, characters, relationships, conflict, temporality, emotional progression, information progression | Operationalization and corpus mapping remain required. |
| C. POD-LC information | Methodological background and possible observational-definition support, including the six documentary observation lines | Cannot determine empirical variables, directions, categories, or generative rules by default. |
| D. Computationally derived | Proposed explicit-person, referent, relation-edge, temporal-relation, affect-state, and new/given measurements | No proposed measurement is currently present and validated in a mapped HookLab lyric dataset. |
| E. Not yet existent | Calibrated HookLab lyric feature table; completed provider output; measurement-error estimates; admissible narrative outcomes; registered analysis for a new narrative feature | Feature admissibility remains closed. |
| F. Previously analyzed/frozen | Early chorus; repetition/formal architecture; raw aggregated vocal range/amplitude | No reopening without `NEW_EVIDENCE=true`, preservation of the prior result, and a new `ANALYSIS_ID`. |

## Data audit

Repository, Drive metadata and revision history were audited. `POD-LC — Fuente sincronizada 100 canciones`, revision 72, is the canonical internal HookLab source frame. The earlier 100-song evidence workbook is its frozen baseline mirror; identical identities and provider IDs establish that it contributes no additional population.

The repository still contains no calibrated narrative feature table. This is recorded as `CANONICAL_SOURCE_RESOLVED_FEATURE_TABLE_NOT_BUILT`. The descriptions below remain candidate construct specifications rather than statements that variables have been computed, calibrated or associated with an outcome.

## Candidate disposition

| Registry entry | A–F class | Audit status | Reason |
|---|---|---|---|
| `LNR_POV_EXPLICIT_PERSON_CONFIGURATION_v0_1` | B; D proposed | `AUDIT_FEATURE_NOT_DEFINED` | Source frame and measurement protocol are established; language metadata, calibration output and error estimate remain pending. |
| `LNR_CHARACTER_TEXTUAL_REFERENT_CONFIGURATION_v0_1` | B; D proposed | `AUDIT_FEATURE_NOT_DEFINED` | Mention/coreference measurement is a proposal, not an existing calibrated variable. |
| `LNR_RELATION_EXPLICIT_EDGE_CONFIGURATION_v0_1` | B; D proposed | `AUDIT_FEATURE_NOT_DEFINED` | Requires referent resolution and a HookLab relation codebook. |
| `LNR_CONFLICT_REPRESENTATION_v0_1` | B; E | `AUDIT_FEATURE_NOT_DEFINED` | Operational definition and codebook are absent. |
| `LNR_TEMPORAL_EXPLICIT_ANCHOR_RELATION_PROFILE_v0_1` | B; D proposed | `AUDIT_FEATURE_NOT_DEFINED` | TimeML is only a methodological precedent; the lyric-domain provider and calibration do not yet exist. |
| `LNR_EMOTION_EXPLICIT_STATE_TRAJECTORY_v0_1` | B; D proposed | `AUDIT_FEATURE_NOT_DEFINED` | Explicitly represented affect must be separated from listener, performer, and author emotion and then calibrated. |
| `LNR_TEXTUAL_REPETITION_FAMILY_FROZEN` | F | `FROZEN_NO_REPROCESS` | Repetition/formal architecture was already evaluated. |
| `LNR_SECTION_FUNCTION_METADATA_FROZEN` | A and F | `FROZEN_NO_REPROCESS` | Existing structural metadata is preserved; formal architecture is not reopened and labels cannot become lyric tokens. |
| `LNR_INFORMATION_NEW_GIVEN_PROGRESSION_v0_1` | B; D proposed | `AUDIT_FEATURE_NOT_DEFINED` | Requires calibrated referent/event units and a predeclared segmentation sensitivity plan. |

Registry totals: 9 entries; 7 `AUDIT_FEATURE_NOT_DEFINED`; 2 `FROZEN_NO_REPROCESS`; 0 `FEATURE_ADMISSIBLE`.

## Literature boundary

Literature was used only to assess whether a construct could eventually be operationalized and what error sources require attention:

- Alberhasky and Durkee (2024), *Songs tell a story*, offers a lyric narrative-arc precedent while reporting lyric brevity/repetition and segmentation limitations: <https://doi.org/10.1371/journal.pone.0303188>.
- Bamman, Lewke, and Mansoor (2020) supports explicit coreference annotation methodology in literature, not automatic transfer to lyrics: <https://aclanthology.org/2020.lrec-1.6/>.
- Pustejovsky et al. (2003), TimeML, supports explicit temporal expression/event relation specification, not a validated HookLab temporal feature: <https://aaai.org/papers/0005-ss03-07-005-timeml-robust-specification-of-event-and-temporal-expressions-in-text/>.
- Markert, Hou, and Strube (2012) supports fine-grained information-status annotation as a possible method: <https://aclanthology.org/P12-1084/>.
- Mohammad (2022) supports the boundary and ethical caution required for automatic emotion inference: <https://aclanthology.org/2022.cl-2.1/>.

None of these sources establishes the existence or direction of a HookLab empirical tendency.

## Gate decision

Canonical order remains:

`DATA SAYS -> STATISTICS SAY -> THEORY SAYS -> GENERATION TESTS -> PRODUCER DECIDES`

Current gate state:

- Feature admissibility: closed.
- Analysis registration: not opened; no `ANALYSIS_ID` created.
- Statistical tests: not executed.
- Conditioned deductions: none created.
- Evidence-Assisted Story Brief: locked.

The source-mapping gate and first measurement-protocol registration are complete. The current gate is `HUMAN_REVIEW_LANGUAGE_PROPOSALS_AND_RESOLVE_DOCUMENT_VERSION_STATUS_FOR_99_ELIGIBLE_CASES`. The organizer produced 100 provisional language labels without exporting text; C077 remains excluded because every internal copy contains only 8 words and 1 line. Calibration remains blocked until the remaining 99 cases receive curated language and document-version metadata.

The executable statistical engine now exists at `mie_core/lyric_statistical_analysis_engine.py`. Its first candidate registration, `AN-LNR-POV-DESC-001`, remains `BLOCKED_FEATURE_NOT_ADMISSIBLE`; consequently, this implementation changes engine readiness while preserving zero registered analyses and zero corpus statistical computations.
