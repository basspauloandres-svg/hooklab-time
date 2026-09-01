# MIGRATION CHECKPOINT — HookLab/TIME-MIE — 2026-09-01 — Lyric Modeling + AI v1

STATUS: CANONICAL HANDOFF / NO-REPROCESS
REPOSITORY: basspauloandres-svg/hooklab-time
BRANCH: main

## 0. START HERE IN A NEW CHAT

Read this file completely before proposing or changing anything. Then read, in this order:

1. docs/checkpoints/LYRIC_MODELING_STATISTICAL_EVIDENCE_PRINCIPLE_v1.md
2. docs/checkpoints/AI_COHERENCE_REASONING_LAYER_INVARIANT_v1.md
3. docs/checkpoints/AI_PERSONAL_ACCOUNT_LOCAL_FIRST_INVARIANT_v1.md
4. app/prototype_v1/lyric_statistical_model_contract.js
5. app/prototype_v1/narrative_state_engine.js
6. app/prototype_v1/ai_coherence_reasoning_layer.js
7. app/prototype_v1/personal_ai_adapter.js
8. app/prototype_v1/hook_composition_assistant.js
9. app/prototype_v1/studio.html
10. tests/lyric_modeling_coherence_contract.test.js
11. .github/workflows/lyric-modeling-coherence-contract.yml

If any referenced path is missing, record it as AUDIT_MIGRATION_MISSING_ARTIFACT. Do not silently recreate it from memory.

## 1. PROJECT PURPOSE

HookLab/TIME-MIE is being developed as a research/compositional system for evidence-informed song construction. The current priority is not merely UI development. The critical path is scientific lyric modeling integrated with melody, beat, Story Brief, narrative continuity, AI coherence and producer evaluation.

The system is personal/research-first. Commercial/multi-user infrastructure is explicitly deferred until functional and scientific validation.

## 2. CURRENT ESTIMATED EXECUTION

Integrated development estimate at migration: approximately 79%.

Approximate component status:
- interface/UX: 88%
- audio/Beat This: 90%
- D0/melody: 82%
- Story Brief manual: 90%
- narrative state: 70%
- statistical lyric modeling: 65%
- AI Coherence/Reasoning: 72%
- per-section export: 88%
- full-song assembly: 62%
- personal AI actually connected: 30%
- evidence-assisted Story Brief: 35%
- global scientific validation: 66–68%

These are management estimates, not scientific measurements.

## 3. CANONICAL PRODUCT FLOW

REFERENCE AUDIO
-> AUDIO/BEAT ANALYSIS
-> STORY BRIEF MODE
-> STORY BRIEF
-> NARRATIVE STATE
-> SECTION FUNCTION
-> SECTION INTENTION
-> CONDITIONED GENERATION
-> THREE MULTIMODAL CANDIDATES
-> AI COHERENCE AUDIT
-> LISTENING
-> PRODUCER SELECTION
-> PROSODY CURATION
-> MP3/MIDI EXPORT
-> PRODUCER EVALUATION
-> APPROVED SECTION
-> NARRATIVE STATE UPDATE
-> NEXT SECTION
-> FULL SONG ASSEMBLY

## 4. STATISTICAL INVARIANT

Canonical order:

DATA SAYS -> STATISTICS SAY -> THEORY SAYS -> GENERATION TESTS -> PRODUCER DECIDES

The empirical data define the observed tendency. Scientific literature does not define the direction/existence of the empirical trend. Literature supports construct definition/operationalization and later interpretation/contextualization of the observed statistical result.

A numerical association is not automatically a trend.

Mandatory pre-inference chain:

FEATURE ADMISSIBILITY -> ANALYSIS REGISTRATION -> STATISTICAL TEST

Every registered analysis must explicitly declare at least:
- RESEARCH_QUESTION
- POPULATION_SCOPE
- OUTCOME
- ADMISSIBLE_FEATURE_IDS
- PRIMARY_TESTS
- COVARIATES
- MULTIPLICITY_FAMILY
- EFFECT_SIZE_CRITERION
- ROBUSTNESS_PLAN
- REPLICATION_REQUIREMENT
- STOP/PROMOTION_RULE

Statistical interpretation must consider effect size, uncertainty, multiplicity, confounding/alternatives, sensitivity, robustness, measurement error and replication when applicable.

Permitted final dispositions:
PROMOTE_TO_CONDITIONED_DEDUCTION | HOLD_FOR_REPLICATION | NO_PROMOTION | AUDIT

Only PROMOTE_TO_CONDITIONED_DEDUCTION may enter evidence-assisted generation.

Null/weak/unstable results are legitimate scientific results. Literature or producer preference cannot rescue them.

## 5. ANALYSES THAT MUST NOT BE REOPENED WITHOUT NEW EVIDENCE

Previously frozen as already evaluated:
- early chorus;
- repetition/formal architecture already tested;
- raw aggregated vocal range/amplitude family already tested.

Reopening requires NEW_EVIDENCE=true, preservation of prior result and a new ANALYSIS_ID.

## 6. STORY BRIEF DECISION

Story Brief occurs BEFORE section proposal/generation.

Two modes exist:

A. MANUAL/VISIBLE
Producer supplies story, characters, relationship, conflict, point of view, key scene, emotional trajectory and audiovisual/cinematic reference.

B. EVIDENCE-ASSISTED
Must remain FAIL-CLOSED until lyric/narrative features have passed statistical gates and have PROMOTE_TO_CONDITIONED_DEDUCTION.

The hidden/evidence-assisted layer works with abstract features/results. It must never reproduce corpus lyrics.

Strict separation:
STORY_BRIEF != SECTION_FUNCTION != LYRIC_CONTENT

SECTION_FUNCTION is metadata. Verse/chorus/bridge/etc. must never become lyric vocabulary merely because the label exists in metadata.

A regression was created specifically because an earlier bug transformed 'Verso: Traición' into generated wording containing 'verso'. That failure must not recur.

## 7. AI COHERENCE/REASONING DECISION

AI is a contextual integration/coherence layer, not the statistical trend engine.

Architecture:
DATA
-> STATISTICS
-> THEORY
-> CONDITIONED DEDUCTIONS
-> STORY MODEL
-> AI COHERENCE/REASONING
-> SECTION REALIZATION
-> LYRIC + PROSODY + MELODY + BEAT RELATION
-> HUMAN EVALUATION
-> PRODUCER DECISION

AI may integrate, condition, audit coherence and generate candidate realizations.
AI may NOT create the empirical trend that justifies a conditioned deduction.

AI must consume only promoted evidence when operating in evidence-assisted mode.

AI coherence should evaluate, as state becomes available:
- Story Brief alignment;
- section-function alignment;
- character continuity;
- point-of-view continuity;
- temporal continuity;
- emotional trajectory;
- redundancy with approved sections;
- advancement of open narrative threads;
- lyric/prosody compatibility;
- lyric/melody capacity compatibility;
- evidence-boundary status.

Disposition:
COHERENCE_PASS | COHERENCE_REVISE | AUDIT_EVIDENCE_BOUNDARY

COHERENCE_PASS does not mean scientific validation, commercial success or producer approval.

## 8. NARRATIVE STATE

A computable narrative-state engine has been introduced. Its purpose is to prevent each song section from behaving as an isolated generation.

State includes/should include:
- characters;
- relationships;
- conflict;
- point of view;
- temporal state;
- emotional trajectory;
- revealed information;
- open threads;
- closed threads;
- approved-section history.

When a section is approved, narrative state must be updated before the next section is generated.

The intended behavior is that Verse 2 knows what Verse 1/Pre/Chorus have already disclosed and avoids unnecessary semantic repetition.

## 9. PERSONAL AI DEPLOYMENT INVARIANT

First deployment class:
PERSONAL_RESEARCH_PROTOTYPE
COMMERCIAL_MODE=false
MULTI_USER_MODE=false

The AI will initially use the user's own authorized account/environment. Validate scientific and creative usefulness first. Robust/commercial architecture comes later.

Credentials/API secrets MUST NOT be embedded in studio.html, public JS, GitHub Pages, GitHack, manifests or commits.

Architecture:
HookLab Studio -> local/private AI adapter -> user-authorized AI account -> AI Coherence/Reasoning Layer -> structured response -> HookLab.

personal_ai_adapter.js is provider-neutral and fail-closed. A real private endpoint/authentication still needs to be connected.

## 10. AUDIO/MOBILE STATE

The canonical UI is mobile-first and has been tested iteratively on iPhone.

Important historical fixes:
- GitHub Pages routing caused 404s; a raw.githack main-based URL was used successfully during testing.
- audio picker on iPhone initially exposed videos because of audio/*; explicit audio extensions/MIME were introduced;
- SHA propagation to the analyzer was corrected;
- MIME-empty/generic iOS audio handling was broadened;
- Beat This local analyzer is part of the current path.

Do not create versioned parallel interfaces to solve deployment bugs. Keep one canonical studio.html and use git commits for rollback.

## 11. EXPORT/PROPERTY DOCUMENTATION STATE

Per selected section, intended outputs include:
- concrete audible preview before export;
- MP3 realization;
- melody MIDI;
- MIDI with lyric events after CURATED_PROSODY_PASS;
- section manifest/provenance.

The long-term full-song package should consolidate:
- lyric;
- MIDI;
- audio;
- Story Brief;
- hashes/timestamps;
- reference provenance;
- engine versions;
- producer decisions;
- section evolution.

This is useful documentary evidence of fixation/evolution but must not be represented as a substitute for formal intellectual-property registration requirements.

## 12. SCIENTIFIC AUDIO/MUSIC BOUNDARY

Reference audio is AESTHETIC_REFERENCE, not SUCCESS_EVIDENCE.
D0_EXPLORATORY != SCIENTIFIC_D.
No positive rule may be fabricated merely to unlock MIDI/audio.

Melodic scientific features remain subject to calibration. Previously frozen calibration target: at least 30 independent aligned pairs and at least one relevant feature meeting rho >= .80 plus predeclared median-error tolerance before scientific promotion, unless a later canonical checkpoint validly supersedes this.

## 13. IMPORTANT IMPLEMENTATION ARTIFACTS CREATED IN THIS CHAT

Statistical evidence invariant:
- docs/checkpoints/LYRIC_MODELING_STATISTICAL_EVIDENCE_PRINCIPLE_v1.md
- commit 1d58edddf4d90a65cbad4f87ceb5a46f2ee644ca

AI coherence invariant:
- docs/checkpoints/AI_COHERENCE_REASONING_LAYER_INVARIANT_v1.md
- commit d9cc4b9cdf2e3ced321c08b6cb905cba91706dc1

AI personal/local-first invariant:
- docs/checkpoints/AI_PERSONAL_ACCOUNT_LOCAL_FIRST_INVARIANT_v1.md
- commit 678bd5e6ac5db3486995417c7704f98dca3d79a5

Section/lyric separation fix in composition assistant:
- commit 108fd083fc0555e3d60c53ef8b8a1ebd8e1be48a
- regression test commit 548b46fe7e27c5ae5b84f2bf196dd09020cc46cd

Story Brief UI integration:
- commit 9626f2953be99aba2789401fb43a9b47783dd1f3

AI coherence executable module:
- app/prototype_v1/ai_coherence_reasoning_layer.js
- commit 457bf4f365823d27ec63284bd619f77b83e66548

Lyric statistical model contract:
- app/prototype_v1/lyric_statistical_model_contract.js
- commit 4d15341bf0a3fa419b575815a0152c2183abb67c

Narrative state engine:
- app/prototype_v1/narrative_state_engine.js
- commit 41ed917b15b3a31df289082b889d656b10b7ff6a

Canonical studio restoration/integration after detecting truncation:
- app/prototype_v1/studio.html
- commit 73907a94f63e76e7daa6af9115aad00ebbd1bbaa

Personal AI adapter:
- app/prototype_v1/personal_ai_adapter.js
- commit 87d087ee6b1ba17b82cc53aa32bab5fc8a69b96b

Lyric modeling/coherence regression:
- tests/lyric_modeling_coherence_contract.test.js
- commit ab76e560e5b75ae18f7de00634859c2de91ce4d3

CI gate:
- .github/workflows/lyric-modeling-coherence-contract.yml
- commit a17a6b09610211bdd81eee61e880bfbcdcad1785

## 14. KNOWN INTEGRITY WARNING

During this chat, studio.html was accidentally truncated during a large write. This was detected and the same canonical file was restored/integrated in commit 73907a94f63e76e7daa6af9115aad00ebbd1bbaa.

Future chats MUST inspect the current studio.html and CI before making large replacements. Prefer small, auditable changes. Never create studio_v2/studio_new/versioned parallel UI as a workaround.

## 15. CURRENT CRITICAL PATH TO 100%

1. Build the scientific lyric/narrative feature registry from the corpus.
2. For every candidate feature, declare construct, layer, operational definition, unit, provider/version, measurement error, calibration, musical/textual relevance, research question, outcome, population, confounders, forbidden interpretations and provenance.
3. Reject incomplete features with AUDIT_FEATURE_NOT_DEFINED.
4. Register the first lyric analyses before computing associations.
5. Execute statistical analyses with effect + uncertainty + multiplicity + robustness/sensitivity + replication policy.
6. Produce first legitimate PROMOTE_TO_CONDITIONED_DEDUCTION results, if supported. Do not force promotion.
7. Use promoted deductions to unlock Evidence-Assisted Story Brief.
8. Expand structured narrative state for characters/POV/time/emotion/threads.
9. Connect the personal/private AI adapter to the user's authorized AI environment without exposing secrets.
10. Use AI coherence before presenting candidates; store structured audit/provenance, not hidden chain-of-thought.
11. Improve lyric generation beyond generic scaffolds using Story Brief + narrative state + section function + promoted deductions + melody/beat/prosody constraints.
12. Automate prosody suggestions while retaining producer CURATED_PROSODY_PASS.
13. Complete full-song musical realization/concatenation and full-song MP3/MIDI/lyric-MIDI export.
14. Run matched Manual Brief vs Evidence-Assisted Brief A/B evaluation.
15. Complete mobile end-to-end QA on iPhone.
16. Consolidate authorship/provenance export package.
17. Only after scientific/functional validation consider robust commercial/multi-user infrastructure.

## 16. NEXT CHAT FIRST ACTION

Do NOT begin by redesigning the UI or reconnecting AI.

First action should be:

BUILD AND AUDIT THE INITIAL SCIENTIFIC LYRIC/NARRATIVE FEATURE REGISTRY.

Recommended candidate domains to audit, not automatically admit:
- narrative perspective;
- character configuration;
- relationship configuration;
- conflict representation;
- temporality;
- emotional progression;
- textual repetition;
- section function;
- narrative information progression.

Literature may support construct definition/operationalization. DATA/STATISTICS determine observed tendencies. Do not predeclare expected positive directions from literature.

## 17. NO-REPROCESS RULE

Before redoing any analysis, search repository/checkpoints first.

If a prior result exists, continue from the first unresolved gate.

Do not reopen frozen analyses without NEW_EVIDENCE=true.
Do not replace a null result with a new positive rule merely to enable generation.
Do not let AI override statistical status.
Do not let SECTION metadata leak into lyrics.
Do not expose personal AI credentials.
Do not fork the canonical UI merely to fix a bug.

## 18. HANDOFF PROMPT

Use the companion file START_NEXT_CHAT_LYRIC_MODELING_AI_2026-09-01_v1.txt as the first instruction in the new chat after giving access to this repository/checkpoint.
