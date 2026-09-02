# MIE Audio–MIDI Explorer v0.2 — mobile repair

Status: `EXPERIMENTAL_NOT_BASELINE`

The v0.1 wrapper embedded the transcription engine in an iframe. An iPhone test on
2026-09-02 showed that the embedded console rendered as an empty rectangle, hiding
the file input and controls. v0.2 removes the iframe and exposes the complete flow
at the top level:

`AUDIO INPUT -> INPUT LISTENING -> DECODE -> M + H + T -> MIDI + AUDIBLE PREVIEW -> MAPPING JSON`

The frozen Luis Miguel reference and the frozen Beat This console are not modified.
The analysis remains exploratory:

- `generation_class=D0_EXPLORATORY`
- `scientific_d_unlocked=false`
- maximum analyzed duration: 60 seconds
- melody and harmony front ends require producer evaluation and scientific calibration

v0.1 is retained only as implementation genealogy and is not the active mobile test lane.
