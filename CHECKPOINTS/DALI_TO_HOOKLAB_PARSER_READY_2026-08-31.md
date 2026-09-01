# DALI → HookLab parser readiness checkpoint

Date: 2026-08-31
Branch: `mie/golden-forensic-v0.3`
State: `PARSER_IMPLEMENTED / TESTED_STRUCTURALLY / AWAITING_AUTHORIZED_DALI_DATA`

## Implemented
- `mie_core/dali_to_hooklab_parser.py`
- `mie_core/test_dali_to_hooklab_parser.py`
- `docs/DALI_TO_HOOKLAB_MAPPING_CONTRACT_v1.md`

## What the parser can do once DALI access is provisioned
- ingest official horizontal annotation JSON exported with DALI code;
- preserve id, artist, title, dataset version, ground-truth and NCC provenance;
- map note start/end times and vocal frequencies to HookLab-neutral events;
- convert Hz to continuous MIDI pitch;
- compute bounded descriptive melody features: pitch range, median pitch, note duration, interval movement, repeated-pitch share, stepwise-motion share, IOI and text-note density;
- classify provider-internal annotation quality using DALI ground truth or NCC>=0.8.

## Hard exclusions
- legacy DALI `get_audio()` is not used;
- YouTube/video URLs are not used for automated audio retrieval;
- parsing does not satisfy released-recording Gate A;
- parsing does not establish version identity;
- no positive creative rule is promoted from DALI until Representation Calibration and the frozen Evidence-to-Creative Deduction gate are satisfied.

## Current bottleneck
Authorized `dali_data` files are still pending provider approval. Code work needed after approval is now reduced to dataset-version/schema verification, batch export/parse, M300 identity/version crosswalk and calibration.

## Readiness update
- DALI adapter: 100% implementation-ready
- DALI parser/mapping contract: 100% implementation-ready
- DALI observed data ingestion: 0% pending authorization
- melody/prosody pipeline engineering readiness: ~90%
- scientific melody/prosody evidence coverage: unchanged until authorized observations are ingested
