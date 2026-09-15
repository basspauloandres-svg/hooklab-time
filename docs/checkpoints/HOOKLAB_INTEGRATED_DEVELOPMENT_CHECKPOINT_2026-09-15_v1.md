# HookLab Integrated Development Checkpoint — 2026-09-15 v1

Status: `PENDING_CANONICALIZATION`
Purpose: single restart point for the next HookLab development stage. Future work must begin here before performing historical repository searches.

## 1. Scientific objective preserved
HookLab is an experimental system for extracting auditable musical evidence from a corpus/reference set, deriving conditioned statistical structure, and generating new melody realizations through traceable inductive/deductive constraints. Audio/MIDI transcription is an intermediate measurement instrument, not the final research objective.

## 2. Recovered historical implementation lineage
The following lineage is confirmed in repository history and must be treated as inherited development rather than reinvented functionality:

- `cc5b0a76...` — MIE Core sensor pipeline dependencies.
- `0eb3cd60...` — MIE Core prototype GitHub Actions workflow.
- `d516b66c...` — initial MIE Core fusion pipeline.
- `53e7fbe9...` — Beat This + stem-aware MIE Core fusion.
- `83b6ee22...` — MIE Core v0.2 run on authorized Luis Miguel preview.
- `ddcac29d...` — MIE v0.2 structural quantization over P30-SCORE-002.
- `2ad3ed52...` — MIE Harmonic Ear v0.2 real-tactus prototype.

## 3. Recovered MIE Core architecture
Historical implementation explicitly reports `trained sensors -> MIE fusion -> M+H+T`.

Recovered sensor/fusion components include:
- source/stem separation with HTDemucs;
- melody candidate extraction with Basic Pitch on separated vocals;
- melody fusion gates using confidence, minimum duration, overlap resolution and local melodic continuity;
- temporal/beat sensor, later upgraded toward Beat This ONNX;
- harmony estimation from harmonic/chroma evidence, later stem-aware with other+bass evidence;
- harmonic LOCK/AMBIGUOUS state logic;
- neutral synthesis of melody, harmony and temporal pulse for listening/audit;
- JSON/MIDI outputs and physical-time events.

This is the technical ancestor of the integrated instrument. The browser MIDI Explorer is an inspection/audition surface, not the system architecture itself.

## 4. Integrated architecture to continue
`CANONICAL CORPUS / REFERENCE`
→ `SOURCE IDENTITY + PROVENANCE`
→ `MIE CORE MULTISENSOR EXTRACTION`
→ `EVIDENCE/AI FUSION WITH UNCERTAINTY`
→ `HUMAN AUDIT`
→ `CASE ANALYSIS PACKAGE`
→ `FEATURE ENGINE`
→ `CORPUS STATISTICAL MODEL`
→ `INDUCTIVE PATTERN DISCOVERY`
→ `CONDITIONED DEDUCTIVE RULES`
→ `GENERATIVE CONSTRAINT ENGINE`
→ `MOTIF / FIGURE / PHRASE / GLOBAL TRAJECTORY`
→ `NEUTRAL AUDIO REALIZATION`
→ `COMPARATIVE HUMAN EVALUATION`.

## 5. Evidence states
Every musical datum must retain provenance and one explicit epistemic state. Minimum states:
- `OBSERVED_ACOUSTIC`
- `MODEL_ESTIMATED`
- `AI_INFERRED`
- `HUMAN_AUDITED`
- `CANONICAL_ADMITTED`
- `AMBIGUOUS`
- `BLOCKED`

AI inference may propose candidates for unresolved regions but must not silently convert uncertainty into observed fact. Scientific admission remains controlled by the relevant measurement/calibration gate.

## 6. Case Analysis Package
Each analyzed work/reference must ultimately produce one versioned package containing at least:
- case/source identity and immutable provenance;
- audio/source transformation log;
- melody events and confidence/provenance;
- beat/tactus/tempo events and confidence/provenance;
- harmony events and confidence/provenance;
- fusion decisions and unresolved alternatives;
- human audit decisions;
- derived analytical features;
- engine/config versions;
- scientific admissibility state.

This package is the bridge between MIE extraction and corpus-level statistics.

## 7. Statistical/generative variables inherited from HookLab research
The downstream feature/statistical engine must preserve the variables already identified in the research program: note-duration distributions; metric attack positions; syncopation type/proportion; phrase onset type (thetic/anacrusic/acephalous); interval sequences; step/leap proportions; melodic direction and contour; range; density; exact/transformed repetition; climax position/singularity; rests/breathing; cadential behavior; melody-harmony relation; and functional classification of non-chord tones where evidence supports it.

Generation is hierarchical and joint in pitch/time:
`INTERVAL -> INTERVAL SEQUENCE -> MELODIC FIGURE -> MOTIF -> PHRASE -> GLOBAL TRAJECTORY`.
Rhythm and pitch must not be generated as independent afterthoughts.

## 8. Product architecture
The tangible product is `HookLab Workbench`, composed of modules rather than a monolithic transcriber:
1. Corpus/Reference Manager.
2. MIE Core multisensor engine.
3. Fusion/Inference engine.
4. Audit console with synchronized A/B listening.
5. Feature Engine.
6. Statistical Model explorer.
7. Conditioned Generative Engine.
8. Neutral Audio Comparator.
9. Provenance/Audit/Checkpoint registry.

## 9. Scientific boundary
Product usability and scientific admissibility are separate. Experimental extraction/inference may be exposed for inspection while its state remains explicit. CAL-MEL-001 and other registered gates remain fail-closed for scientific admission. MIE output cannot serve as both estimate and independent calibration reference.

## 10. Current implementation priority
Do not restart historical searches by default. Continue from the recovered MIE Core lineage and integrate existing components into the Workbench.

Development order:
A. freeze/reproduce latest recoverable MIE Core baseline;
B. define stable Case Analysis Package schema;
C. connect Corpus/Reference Manager to MIE Core;
D. expose fusion uncertainty and human audit;
E. implement Feature Engine over audited events;
F. accumulate case-level features into corpus statistical store;
G. validate registered measurement gates;
H. activate conditioned statistical/inductive-deductive modeling only for admitted features;
I. connect the existing HookLab generative hierarchy;
J. produce controlled neutral audio comparisons.

## 11. Restart rule
A future session must first read this checkpoint plus the canonical change registry and current scientific contracts. Historical repository archaeology is required only when this checkpoint explicitly marks an inherited component as unresolved or when new contradictory evidence appears.

## 12. Anti-reprocessing rule
A recovered historical capability must be promoted into this integrated lineage with provenance, version and status. Once promoted and validated, it must not be rediscovered or redesigned without evidence of regression, contradiction or methodological inadequacy.

Next gate: `REPRODUCE_AND_FREEZE_MIE_CORE_BASELINE`.
Scientific generation unlocked: `NO`.
