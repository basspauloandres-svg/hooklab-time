# MIE v0.3.5 — Animal controlled M-only execution runtime blocker — 2026-09-13 v1

Status: `ABSTAIN_RUNTIME_DEPENDENCY_UNAVAILABLE / NO_OUTPUT_GENERATED / AUTHORIZATION_PRESERVED`

## Authorization

The producer explicitly authorized a controlled M-only execution on the registered Animal source. The authorized source was verified before execution:

- source SHA-256: `75e1dcbaef2fe3d81818df650acf72d98c306f0262bd9e78bbbc911a42a436a0`;
- historical recognition ZIP SHA-256: `39afd3c980c3d22e4267a33aee33e5f09895d514fbbcccbbe8ab7ef04789d67a`.

The execution scope remained M-only. H and T were excluded from computation and retained as frozen historical references.

## Runtime audit

The available execution environment reported:

- Python `3.13.5`;
- Demucs package installed;
- Basic Pitch package unavailable;
- TensorFlow unavailable;
- ONNX Runtime unavailable;
- no cached Basic Pitch runtime;
- no cached HTDemucs `htdemucs` model weights.

Basic Pitch 0.4.0 declares support through Python 3.11. Substituting another pitch detector would change the registered note sensor and was therefore rejected.

## Controlled attempt

A single HTDemucs command was initiated against the verified Animal source to persist the missing vocal stem. Demucs attempted to obtain the registered `htdemucs` model weights from:

`https://dl.fbaipublicfiles.com/demucs/hybrid_transformer/955717e8-8726e21a.th`

The environment could not resolve the remote host. Model loading failed before source separation began.

Consequently:

- no vocal stem was generated;
- no Basic Pitch inference was executed;
- no contour or onset tensor was generated;
- no raw note candidate set was generated;
- no H or T process was invoked;
- no historical artifact was overwritten;
- no recognizability result was produced.

## Formal disposition

`CONTROLLED_EXECUTION_STATUS = ABSTAIN_RUNTIME_DEPENDENCY_UNAVAILABLE`

`SOURCE_IDENTITY = VERIFIED`

`NO_REPROCESS_POLICY = RESPECTED`

`CHANGED_MODULE = M_ONLY`

`H = FROZEN`

`T = FROZEN_ENGINEERING_BASELINE_PRESERVED`

`CAUSAL_SUB_GATE = NOT_EXECUTED`

`BASELINE_PROMOTION = BLOCKED`

The authorization remains valid for one controlled execution in an environment that contains, before source processing:

1. Python 3.10 or 3.11;
2. HTDemucs model `htdemucs` with recorded model-file hash;
3. Basic Pitch 0.4.0 with a declared supported runtime;
4. frozen H/T reference hashes loaded from the registered manifest;
5. output persistence for vocal stem, Basic Pitch contour/onset tensors, raw note candidates, diagnostic JSON and complete environment manifest.

## Next required intervention

Run the registered controlled notebook or workflow in a network-enabled compatible environment, upload the verified Animal source privately at runtime, and return the resulting diagnostic package. The source audio must not be committed to the public repository.
