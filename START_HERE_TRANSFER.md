# START HERE — HookLab TIME transfer bootstrap

Checkpoint date: 2026-08-20
Transfer version: 2.0
Repository: `basspauloandres-svg/hooklab-time`

## Purpose

This file exists so a new chat or research session can continue without reconstructing prior discussion.

## Mandatory reading order

Before proposing or changing anything, read:

1. `CURRENT_STATE.json`
2. `TRANSFER_HOOKLAB_TIME_v2_0_2026-08-20.md`
3. `EVIDENCE_INDEX.md`
4. the specific implementation/result files referenced by the current P0.

## Current state in one paragraph

HookLab TIME has progressed from synthetic CTL/phase/tactus microbenchmarks into real-audio mobile pretesting. Controlled MB01–MB08 work produced experimental solutions for clock continuity, phase restart, silence, event loss and 90/180 tactus ambiguity. Mobile v1.9.x then exposed implementation defects: inherited v1.7 UI, mixer failure, multiple predictive clocks, false octave/tempo transitions, audit-export data loss and audible output latency. The analytical beat/tactus path is currently kept separate from playback compensation. Real-audio audits show near-zero internal phase on Dime ok salsa and Animal, while Dime ok salsa required an empirically successful +115 ms audible playback compensation on the tested device/path. Automatic compensation remains the current P0; meter, downbeat and metric accent are frozen.

## Do not reopen these decisions without new executed evidence

- one active predictive clock at a time;
- conservative CTL;
- approximate 1:2 level changes are not automatically tempo transitions;
- `UNCERTAIN` is allowed and preferred over forced decisions under insufficient evidence;
- metric accent OFF;
- downbeat OFF;
- meter inference OFF;
- output latency must be corrected in playback, not by shifting analytical beat/tactus timestamps;
- algorithm phase and acoustic/output latency must remain separate quantities.

## Current P0

Build/verify automatic audible-output compensation so that:

- the AudioContext does not remain indefinitely in `waiting` once playback starts;
- available WebAudio latency is detected numerically;
- base compensation uses the full detected value, including decimals where available;
- manual fine adjustment defaults to 0 and is only residual calibration;
- total compensation = base compensation + fine adjustment;
- only click playback timing is compensated;
- analytical beat/tactus timestamps remain unchanged;
- exported JSON contains separate fields for detected latency, base compensation, fine adjustment, total compensation and algorithm-phase metrics.

## Regression order

1. Dime ok salsa — controlled repeat because +115 ms manual compensation previously aligned perceptually.
2. Animal — stable-tempo independent case with strong internal phase agreement.
3. Only after both pass, expand to contrasting real songs.

## Key real-audio reference values

Dime ok salsa: 502 tactus events, 542 raw events, estimated tactus 167.882 BPM, phase median -0.6 ms, MAD 6.08 ms, p95 abs 349.11 ms, count BPM 144.448, median-IBI BPM 167.879, successful manual audible offset +115 ms.

Animal: 488 tactus events, 483 raw events, estimated tactus 119.519 BPM, phase median 1.35 ms, MAD 3.64 ms, p95 abs 13.25 ms, count BPM 119.524, median-IBI BPM 119.52.

## Current implementation references

- `app-v1.9.7-offset-calibration.html` — manual compensation reference.
- `app-v1.9.8-auto-output-comp.html` — first automatic attempt; waiting-state problem observed.
- `app-v1.9.9-auto-comp-robust.html` — robust polling attempt; experimental, not yet final-accepted.
- `app-v1.9.6-latency-audit-exportfix.html` — valid audit/export base.

## Controlled evidence references

See `EVIDENCE_INDEX.md`. Especially:

- `evaluation/ctl/RESULTS_phase_restart_v0_3_EXECUTED.md`
- `evaluation/ctl/RESULTS_audio_clock_pipeline_v0_2_EXECUTED.md`
- `evaluation/ctl/RESULTS_tactus_octave_v0_1_EXECUTED.md`
- `evaluation/ctl/phase_restart_v0_3_uncertain.py`
- `evaluation/ctl/tactus_octave_v0_1.py`
- `evaluation/ctl/ctl_v0_7_localize_confirm.py`

## Required behavior for the next session

Do not begin by explaining the project again. First inspect the files above, verify the current P0, correct the implementation, execute the regression, and only then explain what was corrected and what evidence changed.

## Restore prompt for a new chat

Copy this sentence after attaching or pointing the new chat to the transfer materials:

> Read `START_HERE_TRANSFER.md`, `CURRENT_STATE.json`, `TRANSFER_HOOKLAB_TIME_v2_0_2026-08-20.md` and `EVIDENCE_INDEX.md` completely. Treat them as the official state of HookLab TIME. Do not reconstruct or reopen resolved decisions. Continue directly from P0: automatic audible-output latency compensation, preserving analytical beat/tactus timestamps and keeping meter/downbeat/accent frozen until regression passes.
