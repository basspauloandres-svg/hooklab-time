# HookLab/TIME-MIE — AI Coherence/Reasoning Layer Invariant v1

Status: CANONICAL INVARIANT
Scope: lyric modeling, Story Brief, section realization, full-song continuity, multimodal generation.

## Purpose

The AI Coherence/Reasoning Layer is a contextual reasoning and integration layer. Its purpose is to maintain coherence across evidence, Story Brief, narrative state, section function, lyric content, prosody, melody, beat relation and previously approved sections.

It is NOT the statistical engine and it MUST NOT determine empirical trends.

## Canonical architecture

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

This architecture is invariant.

## Statistical boundary

The AI layer may consume only:

1. raw session/context information that is explicitly permitted for creative use;
2. Story Brief information supplied by the producer;
3. evidence-assisted features with disposition PROMOTE_TO_CONDITIONED_DEDUCTION;
4. approved prior section state;
5. musical reference features that have already passed their applicable measurement/calibration gates.

The AI layer MUST NOT:

- discover and promote statistical trends by itself;
- override Feature Admissibility;
- override Analysis Registration;
- override multiplicity, robustness, sensitivity or replication gates;
- convert HOLD_FOR_REPLICATION, NO_PROMOTION or AUDIT into generative rules;
- convert D0_EXPLORATORY into SCIENTIFIC_D;
- infer causal claims from associations;
- treat industry discourse as scientific evidence.

## Evidence hierarchy

DATA SAYS -> STATISTICS SAY -> THEORY SAYS -> GENERATION TESTS -> PRODUCER DECIDES

AI COHERENCE/REASONING operates between conditioned deductions/Story Model and generation tests. It cannot alter upstream evidence status.

## Required inputs

The layer should receive an explicit state object containing, when available:

- SESSION_ID
- REFERENCE_AUDIO_PROVENANCE
- PROMOTED_CONDITIONED_DEDUCTIONS
- STORY_BRIEF
- NARRATIVE_STATE
- SECTION_FUNCTION
- SECTION_INTENTION
- APPROVED_SECTIONS
- OPEN_NARRATIVE_THREADS
- CLOSED_NARRATIVE_THREADS
- CHARACTER_STATE
- POINT_OF_VIEW
- TEMPORAL_STATE
- EMOTIONAL_TRAJECTORY_STATE
- MUSICAL_CONSTRAINTS
- PROSODIC_CONSTRAINTS
- FORBIDDEN_CONTENT/CLAIMS

## Story/section separation

The following are distinct objects and MUST remain separated:

STORY_BRIEF != SECTION_FUNCTION != LYRIC_CONTENT

SECTION_FUNCTION is structural metadata. Labels such as verse, chorus, pre-chorus, bridge, intro, post-chorus and outro MUST NOT become lyric tokens merely because they are metadata.

## Full-song continuity responsibilities

Before realizing a new section, the AI layer should evaluate:

- what narrative information has already been disclosed;
- what emotional state has already been established;
- which characters are active or referenced;
- which relationships/conflicts are established;
- which narrative threads remain open;
- whether the proposed section merely repeats prior semantic content;
- the formal role of the target section;
- continuity of point of view and temporal frame;
- compatibility with the approved Story Brief;
- compatibility with promoted conditioned deductions;
- compatibility of text with prosodic/melodic capacity.

## Section-function reasoning

The layer may use SECTION_FUNCTION to condition the role of a realization, but never as lyrical vocabulary by default.

Examples of allowable reasoning:

- a verse may advance or specify narrative information;
- a pre-chorus may prepare a transition/tension function;
- a chorus/hook may consolidate a salient central proposition;
- a bridge may introduce contrast, reframing or new information;
- an outro may close, suspend or restate according to the Story Model.

These are compositional hypotheses/roles, not universal empirical laws. Evidence-assisted constraints require their own statistical promotion status.

## Coherence gate

Each candidate realization should return a coherence audit with at least:

- STORY_BRIEF_ALIGNMENT
- SECTION_FUNCTION_ALIGNMENT
- CHARACTER_CONTINUITY
- POINT_OF_VIEW_CONTINUITY
- TEMPORAL_CONTINUITY
- EMOTIONAL_TRAJECTORY_CONTINUITY
- REDUNDANCY_WITH_APPROVED_SECTIONS
- OPEN_THREAD_ADVANCEMENT
- LYRIC_PROSODY_COMPATIBILITY
- LYRIC_MELODY_CAPACITY_COMPATIBILITY
- EVIDENCE_BOUNDARY_STATUS

Disposition:

COHERENCE_PASS | COHERENCE_REVISE | AUDIT_EVIDENCE_BOUNDARY

COHERENCE_PASS permits presentation to the producer. It does not imply quality, success, scientific validation or producer approval.

## AI output contract

The layer must output an auditable object containing:

- AI_REASONING_LAYER_VERSION
- INPUT_STATE_ID
- EVIDENCE_IDS_CONSUMED
- STORY_BRIEF_ID
- TARGET_SECTION
- PRIOR_APPROVED_SECTION_IDS
- COHERENCE_AUDIT
- GENERATION_CONSTRAINTS
- FORBIDDEN_INFERENCES
- CANDIDATE_REALIZATION_IDS
- HUMAN_EVALUATION_REQUIRED = true

Internal chain-of-thought is not a project artifact and must not be stored. Store only structured inputs, decisions, constraints, audit outcomes and provenance needed for reproducibility.

## Human authority

The producer remains the final creative decision-maker.

AI output is a candidate realization or coherence recommendation. Producer evaluation may accept, modify or reject it.

PRODUCER_DECIDES remains the terminal decision in the generative chain.

## Fail-closed behavior

If upstream evidence status is missing, contradictory or not promoted, the AI layer must exclude that evidence-assisted rule and record the reason.

If Story Brief and prior approved sections conflict materially, return COHERENCE_REVISE rather than silently rewriting the approved state.

If an evidence boundary would be violated, return AUDIT_EVIDENCE_BOUNDARY.

## Canonical invariant

AI MAY INTEGRATE, CONDITION, CHECK COHERENCE AND GENERATE CANDIDATES.
AI MAY NOT CREATE THE EMPIRICAL TREND THAT JUSTIFIES A CONDITIONED DEDUCTION.

The empirical trend belongs to the registered statistical analysis; theoretical interpretation belongs to THEORY SAYS; creative realization belongs to GENERATION TESTS; acceptance belongs to PRODUCER DECIDES.