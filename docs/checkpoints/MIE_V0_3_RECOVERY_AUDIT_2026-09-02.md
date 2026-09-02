# MIE v0.3 Recovery Audit — 2026-09-02

Disposition: `CANDIDATE_NOT_PUBLISHED`

## Completed

- Canonical M/H/T component registry with pinned hashes and release states.
- CI contract protecting melody, harmony, beat and integrated output requirements.
- v0.2 classified as `REJECTED_ENGINE_REGRESSION`.
- Provider-neutral AI request/response boundary.
- Rejection of invented acoustic candidates and scientific-state overrides.
- Deterministic Motor→reasoner→Motor fallback identified as non-connected AI.
- Local/private analyzer service with ephemeral audio processing and SHA-256 check.
- Bearer-token protection and explicit CORS allow-list.
- v0.3 mobile console client with input listening, M+H+T reconstruction listening
  and relational note–beat–harmony table.
- Candidate event-level octave resolver and post-reasoning M+H+T resynthesis.

## Verified locally

- `MIE_CANONICAL_COMPONENT_REGISTRY_PASS`
- `MIE_RECOGNITION_CONTRACT_PASS`
- `MIE_RECOGNITION_BRIDGE_PASS`
- Python and JavaScript syntax checks.

## Not yet verified

The P30 golden browser regression could not execute in the current container because
its Playwright Chromium binary is unavailable. The repository workflow installs the
required browser and can run this test after an authorized candidate-branch push.
The complete HTDemucs/Basic Pitch service was not executed locally because its heavy
runtime dependencies are absent from this container.

## Accuracy boundary

The producer's approximate 98% historical listening assessment remains contextual
evidence. The reproducible documented melody result remains 13/14 historical regions
within ±0.5 semitone. v0.3 cannot be described as 98% accurate or promoted to
baseline until historical and unseen-song regressions complete.

## Next gate

`AUTHORIZE_CANDIDATE_BRANCH_PUSH_AND_RUN_CI_REGRESSIONS`

No v0.3 public console should be presented as functional before its private analyzer
endpoint is deployed and the registered regression gates pass.
