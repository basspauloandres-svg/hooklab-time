# Gate B Pilot UX freeze — 2026-08-30

Status: `UX_CANDIDATE_READY / EMPIRICAL_PILOT_NOT_STARTED`

The Gate B pilot timer interface has been revised to reduce construct-irrelevant time caused by ambiguous terminology or unclear instructions.

## Invariant
The scientific data model retains canonical field names and meanings. The participant-facing interface uses plain professional language, a short explanation, a format example, and a response field.

Internal scientific field → participant-facing wording:
- `section_form_plan` → “¿Qué partes tendrá la canción y en qué orden?”
- `tempo_metric_recommendation` → “¿A qué velocidad irá la canción y cómo se contará?”
- `harmonic_tonal_recommendation` → “¿Qué base de acordes o centro tonal propones?”
- `melodic_rhythmic_recommendation` → “¿Cómo imaginas el hook o la idea melódica y rítmica principal?”
- `production_constraints` → “¿Cómo debería comenzar a producirse y sonar la canción?”

The first question explicitly defines notation such as `Verso (8)` as a verse lasting 8 bars. Examples are framed only as format demonstrations and must not be treated as preferred musical answers.

## UX acceptance criteria before PILOT_001
1. Participant can explain what each of the five questions asks without methodological assistance.
2. Participant understands that numbers in parentheses indicate bars/compases and are optional.
3. Participant understands when the timer starts and stops.
4. Participant understands that normal thinking, playing, DAW work, and musical experimentation remain inside TTFP.
5. Participant understands that experimental pause is reserved for external interruption.
6. Participant can identify where to enter each answer and where to register the saved artifact.
7. Participant understands that the examples illustrate response format rather than correct musical content.
8. Participant can reach the final/export step without investigator coaching.

If any criterion fails during usability walkthrough, revise UX before collecting a valid TTFP observation. A usability walkthrough is not a Gate B TTFP trial and must not be included in human timing results.

Current app candidate: `app-gate-b-pilot-timer-v0.1.html` with internal schema `HOOKLAB_GATE_B_PILOT_APP_v0.2`.

Next action: participant usability walkthrough. If all eight criteria pass, freeze the candidate for `PILOT_001`; otherwise apply minimal UX corrections and repeat usability walkthrough.
