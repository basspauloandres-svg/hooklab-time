# HookLab/TIME-MIE — Personal Account / Local-First AI Integration Invariant v1

Status: CANONICAL INVARIANT
Scope: AI Coherence/Reasoning Layer, lyric modeling, Story Brief, prototype execution environment.

## Canonical decision

The first operational integration of the AI layer will run in the user's own environment and use the user's own authorized AI account/credential. The prototype is currently for personal, research and non-commercial validation.

The immediate objective is functional and scientific validation of the AI Coherence/Reasoning Layer inside HookLab/TIME-MIE. Commercial multi-user infrastructure is explicitly deferred until the system demonstrates adequate end-to-end performance.

## Current deployment class

DEPLOYMENT_CLASS = PERSONAL_RESEARCH_PROTOTYPE
COMMERCIAL_MODE = false
MULTI_USER_MODE = false
SHARED_BILLING = false
PLATFORM_ACCOUNT_BROKER = false

## Architecture principle

REFERENCE / DATA / STATISTICS / THEORY / CONDITIONED DEDUCTIONS
-> STORY MODEL
-> AI COHERENCE/REASONING
-> SECTION REALIZATION
-> PRODUCER EVALUATION

For the current prototype, AI COHERENCE/REASONING is executed through a user-owned authorized account/credential and a private/local-first runtime path.

## Security invariant

AI credentials, API keys, session tokens or provider secrets MUST NOT be committed to GitHub, embedded in public JavaScript, stored in public manifests, or exposed through GitHub Pages/GitHack.

Public frontend code may call only a local/private adapter endpoint or another secret-preserving execution path.

## Prototype adapter contract

The frontend should communicate with a local/private AI adapter using a provider-neutral request/response contract.

Suggested request:

{
  "schema": "HOOKLAB_AI_COHERENCE_REQUEST_v1",
  "session_id": "...",
  "story_brief": {},
  "section_function": "verse|pre|hook|post|bridge|intro|outro",
  "section_intention": "...",
  "approved_sections": [],
  "conditioned_deductions": [],
  "musical_constraints": {},
  "prosodic_constraints": {},
  "candidate_context": {}
}

Suggested response:

{
  "schema": "HOOKLAB_AI_COHERENCE_RESPONSE_v1",
  "status": "PASS|REVISE|AUDIT",
  "coherence_audit": {},
  "generation_guidance": {},
  "candidate_realizations": [],
  "provider_provenance": {
    "provider": "USER_AUTHORIZED_PROVIDER",
    "model": "...",
    "runtime_class": "PERSONAL_PRIVATE_ADAPTER"
  },
  "human_evaluation_required": true
}

## Provider-neutral rule

The scientific and generative architecture MUST NOT depend conceptually on a single AI vendor. Provider/model is implementation metadata. HookLab interfaces remain provider-neutral so a later migration to a more robust backend does not alter the scientific chain.

## Current priorities

1. Validate coherent Story Brief -> section -> lyric/melody realization.
2. Validate continuity across multiple approved sections.
3. Validate evidence-boundary enforcement.
4. Validate producer usefulness and iteration reduction.
5. Only after these gates pass, evaluate robust hosting, authentication, scaling, billing, observability and multi-user security.

## Deferred architecture

The following are NOT current requirements:

- public multi-user AI authentication;
- commercial billing infrastructure;
- per-user quotas;
- organization tenancy;
- scalable inference gateway;
- production SLA;
- enterprise secret management;
- commercial compliance stack.

These may be designed later if the prototype demonstrates sufficient scientific and creative value.

## Fail-closed rule

If the private/local AI adapter is unavailable, HookLab must report AI_LAYER_UNAVAILABLE and preserve deterministic/non-AI functions. It must not silently substitute an untracked model or expose credentials in the browser.

## Canonical rule

VALIDATE LOCALLY WITH USER-OWNED AUTHORIZATION FIRST.
ROBUST/COMMERCIAL INFRASTRUCTURE COMES AFTER FUNCTIONAL AND SCIENTIFIC VALIDATION.