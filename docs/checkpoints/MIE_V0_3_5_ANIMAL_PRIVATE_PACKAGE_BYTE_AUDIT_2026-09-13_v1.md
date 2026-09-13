# MIE v0.3.5 — Animal private package byte audit — 2026-09-13 v1

Status: `SOURCE_AND_PRIVATE_PACKAGE_BYTES_VERIFIED / NO_REPROCESS_PRESERVED`

## Scope

The user supplied the historical source file and the evaluated private recognition package. The audit was limited to SHA-256 verification, ZIP structure inspection and reading persisted JSON/MIDI/WAV metadata. No separator, note sensor, harmony model, tactus model or resynthesis process was executed.

## Byte verification

Source file:

- supplied filename: `Animal(1).mp3`;
- registered historical identity: `Animal.mp3`;
- byte size: `8,176,436`;
- SHA-256: `75e1dcbaef2fe3d81818df650acf72d98c306f0262bd9e78bbbc911a42a436a0`;
- result: `MATCH_REGISTERED_ANIMAL_SOURCE`.

Private recognition package:

- supplied filename: `MIE_RECOGNITION_v0_3_4(1).zip`;
- byte size: `97,878,869`;
- SHA-256: `39afd3c980c3d22e4267a33aee33e5f09895d514fbbcccbbe8ab7ef04789d67a`;
- result: `MATCH_REGISTERED_PRIVATE_RECOGNITION_PACKAGE`.

The recognition JSON stores `reference_sha256=75e1dcbaef2fe3d81818df650acf72d98c306f0262bd9e78bbbc911a42a436a0`, so package-to-source identity is verified by both external byte hashing and internal package metadata.

## ZIP inventory

The package contains 12 entries:

- `MIE_RECOGNITION_v0_3_4.json`;
- `MIE_RECOGNITION_MHT_v0_3_4.wav`;
- `MIE_CORE_MHT_v0_2.json`;
- `MIE_CORE_MHT_v0_2.wav`;
- `MIE_CORE_MHT_v0_3_1.wav`;
- `MIE_CORE_MHT_v0_3_2.wav`;
- `MIE_CORE_MHT_v0_3_3.wav`;
- `MIE_CORE_MHT_v0_3_4.wav`;
- `melody_basic_pitch.mid`;
- Beat This ONNX cache files and directory metadata.

The package does not contain the separated vocal stem, Basic Pitch contour tensor, Basic Pitch onset tensor or the 290 raw candidate event records. It stores only the raw candidate count. Therefore the registered v0.3.5 causal sub-gate cannot be recomputed from the package under `NO_REPROCESS`.

## Persisted recognition evidence

The recognition JSON is internally valid and reports:

- schema: `HOOKLAB_MIE_RECOGNITION_v0.3`;
- status: `PASS` as a normalization/contract result;
- semantics: descriptive session reference only;
- duration: `245.08081632653062 s`;
- source name: `Animal.mp3`;
- melody events: `215`;
- harmony states: `100`;
- beat events: `477`;
- raw Basic Pitch candidate count: `290`;
- deterministic contextual reasoner connected: `false`;
- scientific D unlocked: `false`.

The `status=PASS` value belongs to the recognition schema validation and must not be represented as producer recognizability or melody accuracy. The producer disposition remains `FAIL_UNRECOGNIZABLE`.

The core report confirms:

- raw accepted melody events: `228`;
- v0.3.1 melody events: `230`;
- v0.3.2 melody events: `216`;
- v0.3.3 melody events: `215`;
- v0.3.4 melody events: `215`;
- plane-supported recovered candidates: `0`;
- tail extensions: `49`;
- T raw observations: `480`;
- T resolved events: `477`;
- tempo: `120 BPM`;
- H v0.3.3 states: `100`;
- H v0.3.4 states: `100`.

The persisted TF-plane residual vector matches the registered regression audit, including pitch-ridge median error `66.6667 cents`, voiced-overlap IoU `0.340526`, false-silence ratio `0.560808`, onset median error `75.6506 ms`, offset median error `91.0601 ms` and octave-confusion ratio `0.03125`. These are derived diagnostics rather than accuracy estimates.

## Scientific disposition

The recovered bytes close the source/package identity uncertainty. They do not close the separator-versus-note-sensor causal question because the required persisted acoustic layers are absent.

Therefore:

- `SOURCE_PACKAGE_IDENTITY = VERIFIED`;
- `PACKAGE_MIXUP_HYPOTHESIS = REJECTED`;
- `MELODY_RECOGNITION = FAIL_UNRECOGNIZABLE`;
- `NOTE_SENSOR_RECALL_BOTTLENECK = HISTORICALLY_SUPPORTED_HYPOTHESIS`;
- `SOURCE_SEPARATION_PRIMARY_CAUSE = NOT_ESTABLISHED`;
- `CAUSAL_SPLIT = ABSTAIN_INSUFFICIENT_MELODY_EVIDENCE`;
- `NO_REPROCESS = ACTIVE`;
- `H = FROZEN`;
- `T = FROZEN_ENGINEERING_BASELINE_PRESERVED`;
- `NEW_AUDIO_EXECUTION = BLOCKED_PENDING_EXPLICIT_AUTHORIZATION`;
- `BASELINE_PROMOTION = REJECTED`.

## Next decision point

The remaining causal sub-gate requires either an already-existing historical vocal stem plus Basic Pitch tensors/raw candidates, or a newly authorized controlled M-only execution that persists those layers and binds H/T to predeclared historical hashes. The present checkpoint authorizes neither reprocessing nor new audio execution.