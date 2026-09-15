# HookLab Multi-Agent Evidence Architecture v0.1
Date: 2026-09-15
Status: ARCHITECTURAL_NORM

## Principle
Agents accelerate acquisition, processing, auditing and synthesis of evidence. They do not manufacture missing evidence and cannot override deterministic scientific gates.

## Evidence basis for architecture
Recent peer-reviewed scientific systems support role-specialized agents coordinated by an orchestrator, with traceable evidence and tool execution. Sequential/adaptive statistical designs support repeated analysis with prespecified stopping/adaptation rules. HookLab adopts those architectural principles without treating agent consensus as statistical evidence.

## Topology
HOOKLAB ORCHESTRATOR
1. Ingestion Agent — source identity, audio/video normalization, provenance.
2. M+T Analysis Agent — invokes deterministic melody and beat engines; cannot rewrite measurements.
3. Audit Agent — flags octave/register instability, gaps, low confidence, clock disagreement and suspicious events; proposals remain AUDIT_CANDIDATE.
4. Feature Agent — invokes deterministic Feature Engine.
5. Statistical Agent — invokes Statistical Evidence Engine; updates evidence state after every admitted case.
6. Pattern Agent — proposes conditioned pattern candidates, explicitly distinguishing descriptive association from generative rule.
7. Method Agent — checks sampling, multiplicity, stopping/adaptation policy, effective n, uncertainty and validation requirements.
8. Evidence Gate — DETERMINISTIC CODE, not an LLM agent. Sole authority to admit scientific generation.
9. Author Interview Agent — asks only for semantic/intentional information absent from musical evidence; author responses are AUTHOR_PROVIDED.
10. Composition Agent — can generate scientifically only from admitted conditioned rules + traced musical constraints + author/producer input. Otherwise EXPLORATORY_ONLY.
11. Evaluation Agent — compares realization with admitted target constraints and reports deviations; cannot retrospectively relabel failed evidence.

## Shared Evidence Ledger
Every datum/action must carry:
- case_id
- source_id/hash when available
- timestamp/version
- producer engine + version
- state: MEASURED | DERIVED | AI_INFERRED | AUTHOR_PROVIDED | HUMAN_AUDITED | ADMITTED | REJECTED
- supporting event_ids/case_ids
- uncertainty/confidence where applicable
- transformation/derivation identifier
- supersedes/superseded_by when corrected

No agent may convert AI_INFERRED to ADMITTED. Admission requires the deterministic gate plus any required human/scientific validation.

## Continuous evidence loop
NEW CASE -> INGEST -> M+T -> AUDIT -> FEATURE -> HUMAN/SCIENTIFIC ADMISSION -> CORPUS STORE -> STATISTICAL UPDATE -> PATTERN CANDIDATES -> METHOD CHECK -> EVIDENCE GATE.

The loop runs after every admitted case. Real-time computation is permitted; inferential validity remains governed by prespecified statistical rules.

## Sequential-analysis safeguard
Repeated inspection of accumulating data can inflate false-positive risk if conventional fixed-sample inference is repeatedly applied. Therefore HookLab must distinguish:
- DESCRIPTIVE_STREAM: continuous descriptive summaries; never unlocks generation alone.
- SEQUENTIAL_INFERENCE: only procedures with prespecified interim/stopping/adaptation rules.
- CONFIRMATORY_INFERENCE: held-out or otherwise preregistered validation when required.

Agent-driven adaptive sampling is allowed only as TARGET_ACQUISITION guidance until a statistically valid adaptive/sequential design is specified. It cannot silently change the estimand or evidence threshold.

## Evidence-needs protocol
When generation requests a relation unsupported by current data, Statistical/Method agents return:
INSUFFICIENT_EVIDENCE
- target relation
- current effective n
- uncertainty/coverage
- missing strata/context
- recommended evidence acquisition
- whether recommendation is descriptive, sequential-design-compatible, or requires redesign

The Orchestrator may prioritize new analyses accordingly. It may not lower thresholds to obtain a generative answer.

## Failure isolation
Agent disagreement -> preserve alternatives + evidence; no majority vote becomes truth.
Tool failure -> FAIL_CLOSED for affected datum.
Missing provenance -> FAIL_CLOSED.
Insufficient n -> INSUFFICIENT_EVIDENCE.
Model-only prior -> EXPLORATORY_ONLY.
Human semantic decision -> valid AUTHOR_PROVIDED input, never corpus-derived evidence.

## Current implementation target
Wire this topology around existing modules:
- MIE R1.3 melody runtime
- Beat/tactus runtime
- Feature Engine v0.1
- Corpus Statistical Store v0.1
- Statistical Evidence Engine v0.1
- Evidence Generation Gate v0.1

Next executable components: orchestrator state machine, evidence ledger, agent contracts, and audit/admission queue.
