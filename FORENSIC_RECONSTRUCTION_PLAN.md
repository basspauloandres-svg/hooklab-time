# HookLab TIME — Forensic flat reconstruction v0

Status: infrastructure recovery; NOT a scientific experimental version.

## Non-negotiable validity rule

One experimental build = one runtime + one AudioContext + one active AudioBufferSourceNode + one audible scheduler + one identifiable analytical engine.

No iframe. No redirect. No dependency on another experimental HTML. No nested version execution.

## Provenance to port, not reinterpret

1. Analytical source: `app-v1.6.html` — Beat This small ONNX, audio-onset fallback, rhythmic states, predictiveTrack, resolveTactus, JSON exports.
2. Playback lifecycle: `app-v1.9.28-buffer-clock-playback.html` — decoded AudioBuffer, AudioBufferSourceNode, shared AudioContext, explicit source stop/disconnect, independent track/click GainNodes, scheduler referenced to `startCtx-position`.
3. Audible offset: 0 ms, from the later A/B listening decision. Do not retain v1.9.28's -115.2 ms.
4. Conservative CTL: `app-v1.9.31-recovered-ctl.html` — event-regime transition detection, tactus deduplication, estimated BPM recalculation, metric accents disabled.

## Integration order

A. Flatten v1.6 source into standalone file without changing analysis functions.
B. Remove HTMLMediaElement from audible path only; retain file input/analysis semantics.
C. Port v1.9.28 transport lifecycle literally: ensure/startAt/stopSource/scheduler/gains; offset = 0.
D. Verify playback before CTL: sourceRate 1, single playback, seek/pause/stop, independent gains.
E. Port v1.9.31 CTL modifications directly into the same runtime, not monkey-patched across frames.
F. Verify regression with Dime and Animal before any ITD/CHR work.

## Acceptance audit fields

build_id; git_commit; runtime_count=1; iframe_count=0; audio_context_count=1; active_source_count<=1; audible_scheduler_count<=1; source_playback_rate=1; audible_offset_ms=0; track_gain; click_gain; detector_version; ctl_version; analysis file/BPM/tactus/runs/transitions.

## Scientific status

All ITD/CHR auditory results produced under stacked-wrapper architecture remain INCONCLUSIVE until repeated on this reconstructed baseline.
