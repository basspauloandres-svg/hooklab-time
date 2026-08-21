# HookLab TIME — Evidence Index

Checkpoint: 2026-08-20
Repository: `basspauloandres-svg/hooklab-time`

This index is the map of where the technical evidence lives. It should be read together with `CURRENT_STATE.json` and `TRANSFER_HOOKLAB_TIME_v2_0_2026-08-20.md`.

## 1. Current transfer and state

- `TRANSFER_HOOKLAB_TIME_v2_0_2026-08-20.md` — human-readable integral transfer checkpoint.
- `CURRENT_STATE.json` — machine-readable current state, frozen decisions, latest evidence, P0 and continuation order.
- `START_HERE_TRANSFER.md` — minimal bootstrap instructions for a new chat/research session.

## 2. Mobile application lineage

Historical app lineage is preserved in the repository root. Important late-stage files:

- `app-v1.9.html` — first integrated v1.9 pretest attempt; deployment later revealed inherited v1.7 content.
- `app-v1.9-test.html` — cache-safe launcher used to diagnose inherited UI.
- `app-v1.9-direct.html` — direct v1.9 launcher.
- `app-v1.9-mixer.html` — first three-channel mixer wrapper.
- `app-v1.9.3-pretest.html` — single-clock correction, conservative CTL, corrected mixer, metric accent suspended.
- `app-v1.9.4-latency-audit.html` — first phase/latency audit instrumentation.
- `app-v1.9.5-latency-audit-fix.html` — first export fix attempt.
- `app-v1.9.6-latency-audit-exportfix.html` — audit preservation/export correction.
- `app-v1.9.7-offset-calibration.html` — manual click-playback offset calibration; Dime ok salsa aligned perceptually at +115 ms on tested device/path.
- `app-v1.9.8-auto-output-comp.html` — first automatic output compensation attempt; could remain waiting.
- `app-v1.9.9-auto-comp-robust.html` — robust repeated AudioContext latency polling; current experimental app, not yet final-accepted.

Do not infer correctness from version number alone. Acceptance is evidence-driven.

## 3. CTL and clock-state implementation

Located under `evaluation/ctl/`:

- `SPEC_v0.1.md` — initial CTL specification.
- `ctl_v0_1.py`, `ctl_v0_2.py`, `ctl_v0_3.py` — early CTL iterations.
- `ctl_v0_5_event_phase.py` — event-phase iteration.
- `ctl_v0_6_robust_event.py` — robust event logic.
- `ctl_v0_7_localize_confirm.py` — localization/confirmation separation used conceptually in later pretest integration.
- `clock_state_v0_1.py` — clock-state resolver.
- `MULTISCALE_SPEC_v0.4.md` — multiscale design record.

## 4. Phase restart and uncertainty

- `FINDING_MB06_PHASE_AUDIT.md` — phase-related finding.
- `MB06b_PHASE_RESTART_CASE.md` — controlled MB06b case.
- `phase_restart_v0_1.py` — initial resolver.
- `phase_restart_v0_2_robust.py` — robust resolver.
- `phase_restart_v0_3_uncertain.py` — current controlled resolver that can emit `UNCERTAIN` instead of forcing a wrong binary decision.
- `stress_phase_restart_v0_2.py` — v0.2 stress harness.
- `stress_phase_restart_v0_3.py` — v0.3 stress harness.
- `RESULTS_phase_restart_v0.2_STRESS.md` — v0.2 stress results.
- `RESULTS_MB06b_MB07_STRESS_EXECUTED.md` — executed MB06b/MB07 stress evidence.
- `RESULTS_phase_restart_v0_3_EXECUTED.md` — executed v0.3 stress evidence; 80,000 trials were reported with zero wrong binary decisions, insufficient evidence converted to `UNCERTAIN`.

## 5. Audio-derived evidence pipeline

- `audio_evidence_v0_1.py` — WAV front-end; internally revised after RMS/onset failures were identified. Historical filename retained.
- `run_audio_clock_pipeline_v0_1.py` — audio → acoustic evidence → clock-state pipeline.
- `RESULTS_audio_clock_pipeline_v0_2_EXECUTED.md` — executed synthetic WAV-derived evidence for MB05/MB06b/MB07.
- `OFFLINE_REAL_EVIDENCE_v0.1.md` — offline real-evidence record.

Controlled result interpretation preserved in transfer checkpoint:

- MB05 → `SILENCE`.
- MB06b → `CLOCK_STOP_RESTART`.
- MB07 → `CLOCK_CONTINUES`.

These are controlled-benchmark findings, not proof of universal real-music performance.

## 6. Tactus octave / 90–180 ambiguity

- `tactus_octave_v0_1.py` — salience-alternation tactus octave resolver.
- `RESULTS_tactus_octave_v0_1_EXECUTED.md` — controlled MB08 results.

Controlled MB08 evidence: approximately 178.55 BPM detected layer resolved to approximately 89.28 BPM tactus. This is not considered sufficient evidence for general real-music tactus inference.

## 7. Other executed CTL result files

- `RESULTS_clock_state_v0.1_EXECUTED.md`
- `RESULTS_v0.4_EXECUTED.md`
- `RESULTS_v0.5_EXECUTED.md`
- `RESULTS_v0.6_EXECUTED.md`

These remain part of the audit trail and should not be deleted even when superseded.

## 8. Real-audio evidence currently carried into the checkpoint

### Dime ok salsa

Latest valid audit values carried into transfer:

- duration: 209.92 s
- tactus events: 502
- raw Beat This events: 542
- estimated tactus: 167.882 BPM
- algorithm phase median: -0.6 ms
- phase MAD: 6.08 ms
- phase p95 absolute: 349.11 ms
- count-based BPM: 144.448
- median-IBI BPM: 167.879
- perceptually successful manual playback compensation: +115 ms

Interpretation: internal phase median is close to zero, while audible playback needed substantial compensation on the tested device/path. Count-based and median-IBI BPM disagreement remains an unresolved summary/coverage issue requiring segmented audit.

Primary JSON evidence was produced in-chat as `Dime_ok_salsa_resumen(5).json`; the transfer checkpoint transcribes the critical values because chat attachments are not guaranteed to remain repository-resident.

### Animal

Latest valid audit values carried into transfer:

- duration: 245.0209 s
- tactus events: 488
- raw events: 483
- estimated tactus: 119.519 BPM
- algorithm phase median: 1.35 ms
- phase MAD: 3.64 ms
- phase p95 absolute: 13.25 ms
- count-based BPM: 119.524
- median-IBI BPM: 119.52

Interpretation: strong internal agreement and stable pulse evidence. This supports keeping output latency compensation separate from analytical beat/tactus correction.

Primary JSON evidence was produced in-chat as `Animal_resumen.json`; critical values are transcribed into the checkpoint for transfer resilience.

## 9. Known defects that must remain visible

- A v1.9 launcher displayed v1.7 content due to inherited/cached wrapper behavior.
- Early mixer controls did not operate correctly in Safari.
- Multiple predictive clocks caused duplicate/interleaved click events.
- Approximate 1:2 level changes could be misclassified as tempo transitions.
- Early latency-audit export recomputation discarded arrays and emitted null audit fields.
- The manual offset UI had a misleading sign explanation; +115 ms was empirically the successful audible compensation for Dime ok salsa.
- v1.9.8 automatic compensation could remain in a waiting state.

A defect is not considered resolved merely because a later file exists; it must pass the acceptance criteria in `CURRENT_STATE.json`.

## 10. Frozen scope

Until the current P0 is resolved and real-audio validation expands:

- metric accent remains suspended;
- downbeat inference remains suspended;
- meter inference remains suspended;
- analytical beat/tactus timestamps must not be shifted to compensate playback latency;
- single-clock behavior is retained;
- uncertainty is preferable to forced classification when evidence is insufficient.

## 11. Current P0

Automatic audible-output compensation:

1. detect available WebAudio latency after audio context becomes active;
2. apply compensation to click playback only;
3. preserve analytical timestamps;
4. keep detected latency, base compensation, fine adjustment, total compensation, and algorithm-phase statistics as separate exported fields;
5. eliminate waiting-state deadlock;
6. validate first on Dime ok salsa, then Animal, before expanding repertoire.

## 12. Transfer rule

A new session should not reconstruct the project from conversation memory. It should open, in this order:

1. `START_HERE_TRANSFER.md`
2. `CURRENT_STATE.json`
3. `TRANSFER_HOOKLAB_TIME_v2_0_2026-08-20.md`
4. `EVIDENCE_INDEX.md`
5. only then the specific source/result files needed for the next change.

Every new correction should add evidence rather than overwrite the audit trail.
