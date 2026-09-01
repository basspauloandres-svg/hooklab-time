# HookLab/TIME-MIE — Gate B2 MIDI/Audio Creative Contribution Protocol v0.1

Date: 2026-08-30
Canonical branch: `mie/golden-forensic-v0.3`
Status: `PROTOCOL_DRAFT / IMPLEMENTATION_NEXT`

## 1. Scientific priority

The principal value proposition under evaluation is not execution speed. TTFP remains a secondary operational metric. The primary question is whether evidence extracted from the musical corpus can be transformed into a musically usable creative contribution for a producer, joining statistical evidence with professional experience.

## 2. Primary evaluation object

The evaluation object is a constructed song prototype represented in both MIDI and audio, using a predefined controlled text. The prototype must preserve traceability from corpus-derived evidence to audible musical decisions.

Required chain:

`CORPUS DATA → STATISTICAL EVIDENCE → CONDITIONED MUSICAL RULE/HYPOTHESIS → GENERATIVE DECISION → MIDI EVENT/STRUCTURE → AUDIO REALIZATION → PRODUCER DECISION → RETAIN / MODIFY / REJECT`

MIDI is the auditable symbolic representation. Audio is the perceptual representation used for professional evaluation. The controlled text reduces lyrical-content variance during comparison.

## 3. Experimental conditions

### H — Human experience baseline
A qualified producer develops the prototype from the controlled brief/text using their conventional experience, without exposure to HookLab candidates or HookLab statistical recommendations.

### D — Data-derived HookLab condition
HookLab constructs a prototype from the controlled brief/text using only promoted/eligible corpus evidence and the already validated generative architecture. Every generated decision must carry provenance to the statistical evidence/rule that conditioned it.

### H+D — Human plus data condition
A qualified producer receives the HookLab D prototype plus its concise evidence package and may retain, modify, extend, or reject its musical decisions. All actions are recorded.

## 4. Controlled inputs

Across H, D and H+D, hold constant where feasible:
- same controlled text;
- same target genre/style definition;
- same target duration range;
- same production brief;
- same minimum deliverable contract;
- same rendering instrument set for comparison renders, unless the experiment explicitly studies orchestration.

The controlled text must be versioned and frozen before comparative generation.

## 5. Minimum MIDI representation

Each prototype must contain at minimum:
1. tempo and meter events;
2. section markers/form structure;
3. lead-vocal or principal melodic track with lyric-event alignment where technically feasible;
4. harmonic guide;
5. rhythmic guide;
6. stable identifiers linking sections/events to the provenance manifest.

Existing HookLab MIDI generation architecture should be reused rather than redesigned.

## 6. Audio realization

Audio renders must be generated from the frozen MIDI/prototype under a standardized rendering configuration. The purpose is perceptual comparison, not final commercial production. Rendering configuration, instruments/sounds, tempo, sample rate, and any deterministic processing must be recorded in provenance.

## 7. Statistical-evidence package

For each HookLab decision, store:
- evidence_id;
- source cohort/version;
- feature/variable;
- statistic or distributional statement used;
- eligibility/promotion state;
- conditioned rule/hypothesis ID;
- generated target/event IDs;
- confidence/uncertainty where available.

Candidate discovery alone never qualifies as scientific evidence. Only evidence already eligible under the project promotion rules may condition D for scientific evaluation.

## 8. Producer evaluation

For every material HookLab contribution in H+D, record one action:
- `RETAIN` — used materially without structural change;
- `MODIFY` — used as a starting contribution but changed;
- `REJECT` — not used in the developed prototype;
- `EXTEND` — contribution triggers a related development beyond the original candidate.

Also record a concise producer rationale and the resulting MIDI/audio event or section identifier.

## 9. Primary outcomes

Primary outcomes are contribution-based rather than preference-only:

### 9.1 Creative Contribution Retention (CCR)
Descriptive proportion of eligible HookLab contributions that are retained or materially carried forward in H+D.

`CCR = (RETAIN + qualifying MODIFY + qualifying EXTEND) / evaluated HookLab contributions`

The exact qualification rule for MODIFY/EXTEND must be frozen before confirmatory analysis.

### 9.2 Creative lineage coverage
Proportion of evaluated H+D musical decisions for which the complete provenance chain can be reconstructed from statistical evidence to audible outcome.

### 9.3 Producer action profile
Counts/proportions of RETAIN, MODIFY, REJECT and EXTEND by musical dimension: form, tempo/meter, harmony, melody, rhythm, production direction.

## 10. Secondary outcomes

- TTFP human/traditional;
- HookLab engine latency;
- HookLab-assisted review/development time;
- descriptive structural differences between H, D and H+D;
- producer-rated usefulness, only as a secondary subjective measure.

Speed ratios must not be interpreted as evidence of creative quality.

## 11. Interpretation boundaries

A retained HookLab contribution is evidence of professional usability in the observed task, not proof of artistic superiority, originality, commercial success, or causal improvement in quality. A rejected contribution is an observed producer decision and must be retained in the evidence record rather than removed from analysis.

## 12. Immediate implementation sequence

1. freeze one controlled text and task brief;
2. define the statistical evidence manifest consumed by generation;
3. bind evidence/rule IDs to generated MIDI structures/events;
4. generate D as MIDI;
5. render standardized D audio;
6. capture H independently;
7. expose D + evidence package for H+D;
8. record RETAIN/MODIFY/REJECT/EXTEND decisions;
9. compute descriptive contribution and lineage metrics;
10. only after pilot feasibility, define the confirmatory sampling plan.

## 13. Relationship to existing gates

Gate B1 TTFP remains valid as an efficiency sub-study. The observed P001 usability/pre-pilot is retained as developmental evidence and is not promoted retrospectively into the principal creative-effectiveness endpoint.

Gate A remains frozen as `IMPLEMENTATION_COMPLETE / EXTERNAL_VALIDATION_PENDING_PROVISIONING`.

Gate C scientific regression must include Gate B2 readiness/evidence before final scientific closure because creative contribution is now the primary practical validation target.
