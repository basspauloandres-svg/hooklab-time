# HookLab/TIME-MIE — External Vocal Identity Validation Protocol v1.0

Date: 2026-08-30
Scientific gate: A — independent vocal-identity validation
Canonical branch: `mie/golden-forensic-v0.3`

## 1. Purpose

This protocol tests whether the note-bearing symbolic track already identified inside a MIDI/KAR representation corresponds to the principal sung melody in the released recording. It does not re-test symbolic lyric-note binding and does not use alternate MIDI arrangements as the primary reference route.

The existing symbolic result remains source-internal evidence. The released-recording reference is generated independently and is kept separate until the comparison stage.

## 2. Calibration seed

The experiment is restricted initially to the five accepted Dance-Pop targets already carrying strong symbolic lyric-note binding:

- Poker Face — Lady Gaga
- Bad Romance — Lady Gaga
- Tik Tok — Kesha
- Firework — Katy Perry
- Dynamite — Taio Cruz

This set is a technical/scientific validation seed and is not treated as a representative population.

## 3. External reference source

For each song, use a legally accessed released commercial recording or an equivalent directly labeled released-recording reference. Record the exact release/version identifier and provenance before annotation.

The released recording must be independent of the MIDI/KAR source under evaluation. Karaoke MIDI, alternate MIDI arrangements, derived symbolic transcriptions and Lakh variants are excluded as primary external ground truth for this gate.

No copyrighted audio is stored in the repository. The repository stores only provenance, annotation coordinates, derived note events and validation metrics.

## 4. Blinded reference annotation

Reference annotation is performed from audio before exposing the annotator to the candidate MIDI/KAR melody track.

For the minimum defensible seed, annotate three structurally distributed excerpts per song:

1. one verse excerpt containing clearly sung lead-vocal material;
2. one contrasting section when present (pre-chorus, post-chorus or equivalent);
3. one chorus/hook excerpt containing the principal vocal melody.

Each excerpt should contain at least one complete vocal phrase and should avoid regions dominated by spoken material, rap without stable F0, dense vocal stacking where a principal line cannot be operationally identified, or instrumental-only passages. Exclusions are documented rather than silently replaced.

The reference representation is a monophonic note-event table with:

- `song_id`
- `excerpt_id`
- `release_reference`
- `start_s`
- `end_s`
- `midi_pitch`
- `annotation_source = RELEASED_RECORDING_BLINDED`
- `annotator_id`
- `annotation_pass`

A repeated annotation pass on at least one excerpt per song is recommended to quantify intra-annotator consistency. If two qualified annotators are available, inter-annotator agreement is preferred and disagreements are adjudicated before symbolic comparison.

## 5. Comparison representation

After the external annotation is frozen, expose the candidate symbolic vocal track and extract the corresponding song sections.

Two complementary comparisons are required.

### 5.1 Absolute note-event agreement

Where time alignment between the released recording and symbolic representation is available, evaluate note correspondence using standard transcription criteria:

- onset tolerance: 50 ms after local alignment;
- pitch tolerance: 50 cents;
- offset tolerance: 20% of reference-note duration or 50 ms, whichever is larger;
- report precision, recall, F1 and average overlap ratio both with and without offset.

These conventions follow established music-transcription evaluation practice and the `mir_eval.transcription` implementation.

### 5.2 Performance-tolerant melodic identity

Because commercial performance and symbolic arrangements can differ in local timing, identity is also evaluated in a transposition- and tempo-tolerant representation:

- ordered semitone-interval sequence;
- pitch-class contour;
- direction sequence (ascending / descending / repeated);
- normalized inter-onset or duration-ratio sequence where sufficiently stable.

The comparator must retain excerpt-level results and cannot collapse all evidence into one global score.

## 6. Outcome states

The external validation layer uses three states:

- `AUDIO_REFERENCE_PASS`: external released-recording evidence supports the symbolic vocal-track identity for the evaluated seed case.
- `AUDIO_REFERENCE_AUDIT`: evidence is mixed, ambiguous or section-dependent and requires adjudication.
- `AUDIO_REFERENCE_FAIL`: the candidate symbolic track does not reproduce the principal released-recording vocal melody sufficiently to support identity.

These labels are intentionally distinct from `CROSS_REPRESENTATION_PASS` and from the internal MIDI/KAR lyric-note binding statuses.

## 7. Promotion rule for the five-song seed

Scientific promotion is not determined from a single pooled average. Each of the five songs must have independently auditable excerpt-level evidence.

For this calibration seed:

- 5/5 `AUDIO_REFERENCE_PASS`: the seed may be promoted as externally calibrated evidence for the current vocal-identification procedure, subject to explicit limitation to the tested seed and source conditions;
- 4/5 pass: the discrepant case must be audited before promotion;
- fewer than 4/5 pass: scientific promotion remains blocked and the source-identification assumptions must be re-examined.

This is an operational calibration rule for HookLab/TIME-MIE, not a claim of population-level sensitivity or specificity.

## 8. Independence and leakage controls

1. The external annotator must not inspect the candidate MIDI/KAR melody before freezing the reference annotation.
2. Section selection should be based on the released recording and structural audibility, not on regions known to favor the MIDI candidate.
3. All excluded excerpts and reasons are retained.
4. Transposition, temporal warping and ornament reduction are permitted only as declared comparison transforms; the original events remain unchanged.
5. A pass in symbolic-source binding cannot substitute for an external audio-reference result.

## 9. Required outputs

For each song:

- released-recording provenance record;
- frozen external note-event annotation;
- selected symbolic note events for matching sections;
- alignment transform, if any;
- absolute transcription metrics;
- performance-tolerant identity metrics;
- excerpt-level decision;
- song-level decision;
- audit notes.

Aggregate output must report all five song-level outcomes and preserve the existing `scientific_promotion=false` state until the external seed rule is satisfied.

## 10. Methodological references

Poliner, G. E., Ellis, D. P. W., Ehmann, A. F., Gómez, E., Streich, S., & Ong, B. (2007). Melody transcription from music audio: Approaches and evaluation. *IEEE Transactions on Audio, Speech, and Language Processing, 15*(4), 1247–1256. https://doi.org/10.1109/TASL.2006.889797

Salamon, J., Gómez, E., Ellis, D. P. W., & Richard, G. (2014). Melody extraction from polyphonic music signals: Approaches, applications, and challenges. *IEEE Signal Processing Magazine, 31*(2), 118–134. https://doi.org/10.1109/MSP.2013.2271648

Raffel, C., McFee, B., Humphrey, E. J., Salamon, J., Nieto, O., Liang, D., Ellis, D. P. W., & Raffel, C. C. (2014). mir_eval: A transparent implementation of common MIR metrics. In *Proceedings of the 15th International Society for Music Information Retrieval Conference (ISMIR)*.
