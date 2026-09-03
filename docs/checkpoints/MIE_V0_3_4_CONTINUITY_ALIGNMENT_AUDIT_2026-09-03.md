# MIE v0.3.4 — continuity and M/H alignment audit

Status: `CANDIDATE / HOLD_FOR_MULTICASE_HELD_OUT_EVALUATION`

## Observed problem

The second independent listening case retained an accurate audible pulse and recognizable melodic trajectory, while the reconstruction contained recurrent silent gaps and imprecise harmony-to-melody timing. The paired files had equal duration (281.797 s). The reconstruction contained 223 silent runs of at least 100 ms, whereas the source remained substantially continuous. These measurements are diagnostic evidence and are not a reference transcription or an accuracy estimate.

## General correction

M v0.3.4 may extend a note only while the existing vocal contour plane supports the same pitch ridge. It may admit a rejected Basic Pitch candidate only when that observed candidate occupies an uncovered interval and passes confidence, duration and contour-support gates expressed as fractions of the frozen tactus. Missing contour or tactus evidence produces abstention.

H v0.3.4 retains harmonic identity from the existing LOCK/AMBIGUOUS chain. Metric resolution now requires a regular consensus downbeat phase. Accepted harmonic changes are placed on the unchanged tactus within a bounded normalized tolerance, and the preceding accepted harmonic state persists to the next accepted change. Melody timestamps and harmonic identities are never manufactured or changed by this alignment step.

## Preserved boundaries

- T is frozen and must have the same SHA-256 fingerprint in baseline and candidate output.
- Runtime logic cannot consume title, artist, filename, known transcription or manual song timestamps.
- Raw sensor observations remain immutable and traceable.
- Automatic output cannot assign human curation.
- `generation_class=D0_EXPLORATORY`.
- `scientific_d_unlocked=false`.
- The lyric–prosody–MIDI bridge v1 is outside this increment and remains unchanged.

## Promotion gate

v0.3.4 is compared against v0.3.3 by independent held-out musical work. Macro-by-track evidence, non-inferiority on T, producer listening and the existing 30-work requirement remain mandatory. A gain confined to one work receives `HOLD_TRACK_SPECIFIC_GAIN`.
