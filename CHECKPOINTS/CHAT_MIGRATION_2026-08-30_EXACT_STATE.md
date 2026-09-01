# HookLab/TIME-MIE — Chat Migration Checkpoint

Date: 2026-08-30
Repository: `basspauloandres-svg/hooklab-time`
Canonical working branch verified at migration: `mie/golden-forensic-v0.3`
HEAD verified at migration before this checkpoint: `be7da6b5b9ccdb00d1562f7e3fdc695d2bf8e3a5`
Latest substantive commit message: `Persist real-target vocal binding calibration checkpoint`

## Mandatory re-entry rule

The next chat/agent MUST read this checkpoint completely, then inspect the current branch HEAD and the files referenced below BEFORE searching, editing, running workflows, or proposing a new direction. Do not reconstruct project state from partial GitHub searches. Do not restart methodological decisions already closed.

The next chat must explicitly confirm, in one concise message, that it has integrated this checkpoint and identified the current HEAD. Only then may it continue.

## Exact project state at migration

HookLab/TIME-MIE is being developed as a reproducible preproduction-analysis system. The current work separates offline robust corpus construction from fast particular/light analysis. Social-network reach was explicitly REMOVED from the HookLab success criterion and deferred to a future release-analytics development.

### Validated / closed components

1. FULL_TMT analysis architecture and Matrix X pipeline are functional.
2. Cache-first routing, restrictions, and structural candidate generation are functional.
3. ROBUST/LIGHT analysis policy has passed CI.
   - ROBUST: N=5 technical validation seed; N=30 pilot; N>=50 analytical use; N=100 standard target, subject to stability rather than automatic representativeness.
   - LIGHT: N=10–20 contextual comparators; requires a cached ROBUST reference; never rebuilds the master corpus online; `online_corpus_reanalysis=false`.
4. Cohort stability gate has passed CI.
   - N alone does not establish representativeness.
   - Freeze requires sufficient N, consecutive local stability, and absence of persistent directional drift.
5. Melodic confidence triage logic has passed CI.
   - `AUTO_HIGH_CONFIDENCE`
   - `HUMAN_AUDIT`
   - `REJECT_OR_REANALYZE`
   - Triage is not independent proof of released-recording vocal identity.
6. Scaling architecture has been defined for batch processing and checkpoints rather than one-song-at-a-time blocking.
7. Technical TTFP online-path benchmark is closed for the engine path:
   - 30 runs
   - median ≈ 0.0982974605 s
   - mean ≈ 0.0984798348 s
   - p95 ≈ 0.0998141370 s
   - `T_online_search_seconds = 0`
   - `online_corpus_reanalysis = false`
   - path: `cached cohort -> router -> constraints -> 3 structural TMT candidates`
   - human traditional baseline remains pending, so no comparative superiority claim is allowed yet.

### Latest real-target melodic/vocal calibration evidence

Read first: `mie_core/target_vocal_binding_calibration_v1.json`.

Source run: `33338265583`
Source commit: `b0c9fc6846af571179f14c3c7e299bb4136c1341`
Rows: 11
Strong symbolic binding: 8/11 = 0.727273

Accepted Dance-Pop target cohort: 5 songs, all 5 with strong symbolic lyric-note binding inside the symbolic source:
- Poker Face — direct same-track lyric-note binding — alignment 0.9914
- Bad Romance — direct same-track lyric-note binding — alignment 0.9883
- Tik Tok — direct same-track lyric-note binding — alignment 0.9982
- Firework — direct channel-prefix lyric binding — alignment 0.9977
- Dynamite — direct same-track lyric-note binding — alignment 1.0

Interpretation boundary: this strongly supports vocal-track identification INSIDE the MIDI/KAR symbolic representation, but it remains source-internal evidence. It is not yet an independent comparison against the released commercial recording.

Scientific promotion remains `false` until an external or directly labeled reference sample calibrates vocal identity against the released recording.

## Corpus scaling decision

The 5 accepted Dance-Pop songs are a validation seed, not the final analytical dataset.

Planned scale logic:
- T0 = 5: forensic/technical validation seed
- T1 = 30: pilot
- T2 = 50: minimum analytical cohort
- T3 around 75/100/125: stability checkpoints
- Continue to 150/200 or beyond only when distributions remain unstable or the style is heterogeneous
- Larger batch targets (e.g. 500) are engineering scale targets, not automatic representativeness claims

The robust corpus size is determined empirically by stability of distributions, not by a fixed universal N.

## Current unresolved scientific gates

A. Independent vocal-identity validation against a released-recording reference or directly labeled external reference sample.
B. Human/traditional preproduction TTFP comparison under an observed and reproducible protocol.
C. Final integrated regression + scientific documentation after A and B are closed.

## Critical next action

Continue from the latest substantive checkpoint (`target_vocal_binding_calibration_v1.json`). Do NOT redesign the melodic triage logic and do NOT return to searching alternative Lakh arrangements as the primary route; that route had insufficient coverage.

Next priority: design and execute the smallest defensible external/directed-reference validation experiment for vocal identity, using the 5 accepted Dance-Pop targets as the calibration seed. The experiment must preserve the boundary between symbolic-source evidence and released-recording evidence. In parallel, prepare the reproducible human TTFP baseline protocol, but do not claim temporal superiority until observed human data exist.

## Important continuity warning

A previous continuation attempt started searching GitHub/workflows before proving it had read and integrated the checkpoint. That behavior must not recur. Re-entry order is:

1. Read this file completely.
2. Verify current branch and HEAD.
3. Read `mie_core/target_vocal_binding_calibration_v1.json`.
4. Inspect only the files/workflows required by the next unresolved gate.
5. Continue from the exact unresolved gate; do not reconstruct the project from scratch.

## State summary for the new chat

Current global progress estimate used in the previous chat was approximately high-80s percent, but percentages are secondary to gates. The technical prototype is substantially complete; remaining work is concentrated in scientific validation, especially independent vocal identity and observed human TTFP, followed by integrated regression/documentation.

This checkpoint is the canonical chat handoff unless a later checkpoint explicitly supersedes it.
