# HookLab/TIME-MIE — Human/Traditional TTFP Baseline Protocol v1.0

Date: 2026-08-30
Scientific gate: B — human/traditional preproduction TTFP comparison
Canonical branch: `mie/golden-forensic-v0.3`

## 1. Purpose

This protocol defines the observed human/traditional baseline required before any comparative temporal claim is made about HookLab/TIME-MIE. The technical engine-path benchmark is already closed; this protocol prevents retrospective selection of a human comparator after seeing favorable results.

The primary outcome is time-to-first-preproduction (TTFP): elapsed wall-clock time from receipt of the standardized task package to delivery of the first preproduction output satisfying the predefined minimum output contract.

## 2. Comparison question

Under the same bounded preproduction brief, how long does a qualified human practitioner using a conventional workflow require to produce the first admissible structural preproduction proposal, compared with the already benchmarked HookLab online path?

This experiment measures workflow latency under defined conditions. It does not measure artistic quality, final production quality, creativity, commercial performance or social reach.

## 3. Human participant eligibility

Participants should have demonstrable experience in at least one of the following roles:

- music producer;
- arranger;
- songwriter/composer with preproduction responsibilities;
- music director performing equivalent structural planning.

Record years of experience, primary role, principal DAW/tools and prior familiarity with the test material. The protocol should include more than one participant whenever feasible; a single-person pilot may test feasibility but cannot support broad claims about human practice.

## 4. Standardized task package

Each trial provides the human participant with the same information available to the intended practical workflow at task start. The package must specify:

- target song/project brief;
- style/genre constraints;
- required structural outputs;
- permitted conventional tools;
- start condition;
- stop condition.

The participant must not receive HookLab-generated candidates before the trial.

## 5. Minimum admissible preproduction output

The TTFP clock stops only when the participant has produced a first usable structural proposal containing, at minimum:

1. section/form plan or equivalent structural map;
2. tempo/metric recommendation when applicable;
3. harmonic or tonal structural recommendation when applicable to the brief;
4. melodic/rhythmic structural recommendation relevant to the target;
5. explicit production constraints or directions sufficient to begin realization.

A verbal statement without a recorded artifact does not stop the clock. The output may be text, lead sheet, DAW notes, structured worksheet or another predeclared format, provided it contains the required fields.

## 6. Timing procedure

- `t0`: participant receives and opens the standardized task package and the experimenter states that work may begin.
- continuous wall-clock timing is used;
- pauses requested by the experimenter are subtracted and documented;
- participant-initiated breaks remain part of workflow time unless caused by an external interruption unrelated to the task;
- `t1`: first admissible preproduction artifact is saved/exported and submitted;
- `TTFP_human = t1 - t0`.

Screen recording or equivalent process logging is recommended to audit timing and workflow events. The participant must provide consent for any recording.

## 7. Repeated trials and ordering

Use multiple tasks and counterbalance task order across participants where feasible. Record whether each participant knows the source material beforehand.

A participant should not repeat the same task after receiving feedback from HookLab because that introduces learning and contamination. Practice trials, if used, must use separate material.

## 8. HookLab comparator

The machine comparator remains the already defined online engine path:

`cached cohort -> router -> constraints -> 3 structural TMT candidates`

Existing technical benchmark state:

- 30 runs;
- median approximately 0.0982974605 s;
- mean approximately 0.0984798348 s;
- p95 approximately 0.0998141370 s;
- `T_online_search_seconds = 0`;
- `online_corpus_reanalysis = false`.

The human experiment does not alter or rerun this benchmark merely to obtain a more favorable comparison. If future software changes alter the online path materially, a new versioned machine benchmark is required.

## 9. Analysis plan

Report raw human TTFP values before inferential statistics. Summaries should include:

- n participants;
- n valid trials;
- median;
- mean;
- interquartile range;
- range;
- per-participant and per-task values;
- exclusions with reasons.

The primary comparison is descriptive because the engine timing distribution and human workflow distribution occur at radically different scales and may not satisfy common parametric assumptions. If inferential testing is later added, its model and assumptions must be declared before inspecting the final comparative result.

Report speed ratio only after observed human data exist:

`speed_ratio = median_TTFP_human / median_TTFP_HookLab`

A speed ratio is a latency comparison, not evidence of equivalent artistic quality.

## 10. Bias controls

1. Define admissible human output before observing final human times.
2. Use the same task brief across comparison conditions as far as the workflows permit.
3. Do not expose participants to HookLab candidates before their timed trial.
4. Record prior familiarity with each test song/task.
5. Preserve failed, abandoned and excluded trials with explicit reason codes.
6. Separate system execution time from any human time needed to review or select among HookLab candidates.
7. Do not label the engine superior until human observations have been collected and the output-contract comparability has been audited.

## 11. Human review time as a second measure

For practical deployment, measure a second quantity separately when possible:

`TTFP_HookLab_assisted = engine_latency + human_candidate_review_time`

This measure should not replace the pure engine-path benchmark. Reporting both distinguishes computational latency from real workflow latency.

## 12. Gate-B closure criterion

Gate B may be considered empirically populated when:

- at least one reproducible human pilot has been completed under the defined protocol;
- raw timings and artifacts are retained;
- the admissibility rule has been applied consistently;
- HookLab and human outputs have been checked for minimum-contract comparability.

Broader superiority claims require a larger and more diverse human sample than the minimum pilot.

## 13. Scientific interpretation boundary

Until observed human data are present, HookLab/TIME-MIE may report only its technical engine-path latency. It may not claim faster preproduction than human/traditional practice.
