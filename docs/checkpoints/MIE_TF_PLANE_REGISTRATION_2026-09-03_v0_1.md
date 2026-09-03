# MIE time-frequency plane registration v0.1

Date: 2026-09-03  
Status: `ENGINEERING_CANDIDATE_AWAITING_PRODUCER_AB_AND_MULTICASE_REGRESSION`

## Scope

This increment adds a derived melody-only A/B layer to MIE v0.3.1. It does not
redesign the unified M/H/T engine, change harmony, alter the producer-approved
tactus, or promote any scientific feature.

The implementation operationalizes the representation as:

`Basic Pitch contour/onset tensor -> immutable reference plane -> candidate
note plane -> common-clock registration -> residual vector -> producer A/B`

The representational distinction adapted from Zampronha is documentary:

- indexical: acoustic activation in the neural tensor;
- symbolic: time/frequency coordinates converted to note events;
- iconic: structural similarity between reference and candidate trajectories.

This source supports conceptual operationalization, not empirical validation of
recognition accuracy.

## Axonometric interpretation and engine audit

Axonometry means measurement along axes and, technically, projects a
three-dimensional object onto a two-dimensional view. In HookLab it is useful
as a diagnostic rendering of `(time, pitch, salience)`, not as an acoustic
recognition algorithm. The projected view must never replace measurements in
the native tensor coordinates.

Open-source candidates were assessed as follows:

- **Basic Pitch 0.4.0** — selected neural sensor already present in MIE. Its
  `contour` and `onset` tensors provide the reference plane. License: Apache-2.0.
- **NumPy + librosa 0.11** — selected for same-clock rasterization, salience and
  residual measurements already required by MIE. Librosa license: ISC.
- **scikit-image registration** — retained as a future diagnostic candidate,
  not installed here. Phase cross-correlation estimates a global translation;
  applying it blindly could erase real onset or pitch errors. License:
  BSD-3-Clause.
- **nnAudio** — technically suitable for trainable STFT/CQT front ends and MIT
  licensed, but rejected for this increment because Basic Pitch already emits a
  neural time-frequency tensor and another PyTorch front end would increase
  Colab cost without resolving the current continuity gate.
- **Essentia** — useful MIR toolbox, but not selected because it duplicates
  current components and its AGPL licensing requires a separate product-level
  review.

Decision: `BASIC_PITCH_TENSOR_PLUS_NUMPY_LIBROSA`, with no new runtime
dependency. Any axonometric rendering remains `VISUAL_DIAGNOSTIC_ONLY`.

## Continuity rule

Two fragments can be joined only when all conditions pass:

1. both events have the same MIDI pitch;
2. the gap is at most 140 ms;
3. the Basic Pitch contour has mean support of at least 0.25 through the gap;
4. at least 70% of bridge frames reach 0.25 support;
5. the Basic Pitch onset tensor does not support a repeated attack at the
   second event.

The original events and model tensors remain unchanged. Every derived event
retains `source_event_indices`. Missing contour evidence produces
`ABSTAIN_NO_CONTOUR`.

## Diagnostic vector

`M_TF_PLANE_REGISTRATION_RESIDUAL_v0_1` reports separately:

- median pitch-ridge error in cents;
- voiced overlap IoU;
- false-silence ratio;
- median onset and offset error;
- sustain-fragmentation rate;
- median gesture-slope error;
- octave-confusion rate.

No weighted composite is calculated. Status remains
`AUDIT_FEATURE_NOT_CALIBRATED`.

## A/B outputs

- A: `MIE_CORE_MHT_v0_3_1.wav`, prior temporal-refinement candidate;
- B: `MIE_CORE_MHT_v0_3_2.wav`, same H and T with neural-plane melody
  continuity;
- JSON: both note layers, provenance, continuity decisions and both residual
  vectors.

## Invariants

- `generation_class=D0_EXPLORATORY`
- `scientific_d_unlocked=false`
- raw sensor observations are immutable;
- no absent note is created;
- no song-specific note, register, tempo or chord template is present;
- T is unchanged;
- human listening is required before any engineering baseline decision.

## Next evidence

1. Run same-source A/B producer listening focused on lost sustains and repeated
   attacks.
2. Compare residual-vector direction A versus B without declaring a calibrated
   score.
3. Run blind multicaso regression with independent reference annotations.
4. Keep or reject the continuity layer based on those observations; do not tune
   thresholds to one song.

## Primary technical references

- Spotify, Basic Pitch source and Apache-2.0 license:
  https://github.com/spotify/basic-pitch/tree/v0.4.0
- Basic Pitch paper: https://arxiv.org/abs/2203.09893
- librosa salience documentation:
  https://librosa.org/doc/0.11.0/generated/librosa.salience.html
- scikit-image registration documentation:
  https://scikit-image.org/docs/stable/api/skimage.registration.html
- nnAudio source and MIT license: https://github.com/KinWaiCheuk/nnAudio
- Essentia source and licensing: https://github.com/MTG/essentia
