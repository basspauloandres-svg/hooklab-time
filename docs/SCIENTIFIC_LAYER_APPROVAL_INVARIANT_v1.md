# HookLab/TIME-MIE — Scientific Layer Approval Invariant v1.0

Date: 2026-08-30
Canonical branch: `mie/golden-forensic-v0.3`
Status: `FROZEN_INVARIANT`

## Purpose

Every newly introduced scientific or generative layer must be independently auditable before it is allowed to control a downstream layer. No layer is considered approved merely because code exists or an output looks plausible.

## Mandatory approval package

A layer may be marked `APPROVED` only when all applicable elements are persisted in the repository:

1. `scientific_basis` — explicit evidence, prior validated component, or documented methodological reason supporting the layer;
2. `decision_record` — what the layer does, what it does not do, and its interpretation boundary;
3. `implementation` — explicit versioned code/configuration/schema;
4. `tests_or_validation` — executable tests, regression evidence, or observed validation when applicable;
5. `provenance` — inputs, versions, source IDs and outputs sufficient to reconstruct the decision chain;
6. `checkpoint` — a dated checkpoint declaring status and the exact conditions under which downstream use is permitted.

If one required element is absent, the layer must remain `PROPOSED`, `IMPLEMENTED_UNVALIDATED`, `AUDIT`, or another non-approved state. Downstream scientific promotion must fail closed.

## Required state machine

`PROPOSED -> IMPLEMENTED -> VALIDATED -> APPROVED -> DOWNSTREAM_ELIGIBLE`

Exceptional states:
- `AUDIT`
- `BLOCKED_EVIDENCE`
- `BLOCKED_PROVISIONING`
- `REJECTED`

No transition may skip directly from `PROPOSED` or `IMPLEMENTED` to `DOWNSTREAM_ELIGIBLE`.

## Scientific invariants

- candidate discovery != scientific promotion;
- empirical distribution != promoted generative rule;
- implementation complete != scientific validation complete;
- reference unavailable != algorithmic failure;
- T0 validation seed != final analytical cohort;
- every downstream generative decision must be traceable to an approved upstream layer.

## Gate B2 application

For the chain

`CORPUS DATA -> STATISTICAL EVIDENCE -> PROMOTED RULE -> GENERATIVE DECISION -> MIDI -> AUDIO -> PRODUCER DECISION`

each arrow represents a controlled transition. A new transition is activated only after the upstream layer has an approval package and checkpoint.

## Migration rule

Future chats/agents must read this invariant before adding or promoting a new scientific layer. If a later checkpoint supersedes a layer, the superseding checkpoint must reference the prior layer ID and explain the evidence for the transition.
