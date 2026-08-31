# DALI → HookLab Mapping Contract v1

## Scope
This contract maps authorized DALI annotation exports into HookLab evidence without invoking the legacy DALI audio-retrieval helper.

## Source schema used
Official DALI horizontal annotations expose four granularities: notes, words, lines and paragraphs. Note annotations provide text, `[start,end]` time in seconds and frequency information. Entry metadata includes DALI id, artist, title, dataset version, ground-truth flag, NCC score and multimodal metadata.

## Mapping
DALI note -> HookLab vocal note event:
- time -> `start_s`, `end_s`, `duration_s`
- frequency -> `hz`, converted to continuous MIDI pitch by `69 + 12*log2(hz/440)`
- text -> note/syllable textual evidence

Derived evidence may include pitch range in semitones, median pitch, duration statistics, interval movement, repeated-pitch share, stepwise-motion share, IOI and note/text density.

## Quality gate
- DALI ground-truth entry -> `GROUND_TRUTH`
- non-ground-truth with documented `NCC >= 0.8` -> `HIGH_NCC`
- lower/absent NCC -> `AUDIT_ANNOTATION_QUALITY`

The threshold mirrors the DALI construction paper's restrictive global audio/annotation match criterion. It is a provider-internal quality signal, not independent released-recording validation.

## Fail-closed boundaries
1. Parse success does not establish `VERSION_IDENTITY` against a released commercial recording.
2. DALI metadata URLs are never treated as authorization to retrieve audio.
3. `get_audio()` / YouTube helpers are excluded from HookLab.
4. Provider-internal ground truth or NCC does not by itself promote a row to a population-level creative rule.
5. Note-level deductions remain blocked until Representation Calibration validates that F0/note representations do not materially alter the scientific conclusion.

## Output role
DALI is intended to supply licensed melody/lyrics/prosody evidence for M300 crosswalks and later FULL_TMT-compatible feature construction after authorized provisioning.
