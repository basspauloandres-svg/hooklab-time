# HookLab/TIME-MIE — Target Song Discovery & Qualification Pipeline (TSDQP) v1.0

Date documented: 2026-08-30
Branch: `mie/golden-forensic-v0.3`
Status: recovered architectural decision from development history; this document closes a migration-documentation gap.

## Purpose

Define the procedure used to locate candidate songs, qualify them as mass-success targets, resolve identity/version, acquire an auditable symbolic representation, and promote only valid full-song cases into FULL_TMT and Matrix X.

This pipeline is upstream of TMT analysis. Lakh/LMD or any other MIDI repository is a source of symbolic representations, not the definition of the scientific population.

## Population logic

Target universe: commercially released mass-success songs within a rolling window of approximately the most recent two decades at the time of corpus construction.

Mass-success qualification is based on documented large-scale circulation. The active HookLab criterion retains YouTube and Spotify evidence. Social-network metrics such as TikTok/Instagram were explicitly removed from HookLab and deferred to a future release-analytics module.

The target universe may include global and Hispanic/Latin repertoire. `Despacito` was explicitly identified during development as an example of a high-circulation Hispanic target worth attempting when it satisfies the remaining gates.

## Pipeline

`MASS-SUCCESS UNIVERSE`
→ `TARGET DISCOVERY`
→ `IDENTITY`
→ `MASS-SUCCESS EVIDENCE`
→ `GENRE::STYLE`
→ `VERSION`
→ `SYMBOLIC SOURCE RESOLUTION`
→ `FULL_SONG`
→ `FULL_TMT`
→ `MATRIX X`
→ `ROBUST REFERENCE CACHE`

## Discovery versus approval

Fuzzy metadata matching is permitted for candidate discovery only. It is never sufficient for scientific promotion.

Candidate discovery may use artist/title/release/duration/identifiers and other metadata to retrieve possible symbolic representations. Promotion requires independent passage through identity, version, coverage, provenance, and analysis-quality gates.

## Source roles

### Music metadata / identity sources
Used to resolve artist, title, release, duration, versions, and identifiers where available.

### YouTube
Used as evidence of mass-scale circulation under the active success criterion.

### Spotify
Used as a second active circulation/success signal.

### Apple/previews or equivalent metadata sources
May support version identity, duration, and release resolution when needed.

### Lakh/LMD and other MIDI/KAR sources
Used opportunistically to locate symbolic representations. Their holdings must never be treated as the target population. Availability bias in symbolic repositories is a known acquisition limitation and must not redefine the corpus scientifically.

## Three separate qualification questions

### IDENTITY
Is this representation actually the target composition/song?

### VERSION
Does it correspond sufficiently to the intended commercial/released version for the planned analysis?

### COVERAGE
Does the symbolic representation cover the complete song rather than a fragment, excerpt, or materially shortened arrangement?

These gates must remain separate. A plausible title match does not establish version or full-song coverage.

## Symbolic acquisition sequence

`target song`
→ metadata search / candidate generation
→ candidate MIDI/KAR representations
→ artist/title crossmatch
→ version/duration/structure checks
→ exact file resolution
→ provenance/hash registration when available
→ MIDI/KAR audit
→ FULL_SONG gate
→ FULL_TMT analyzer
→ Matrix X append

Once a representation is approved, the exact source should be cached and identified reproducibly so that online/light analysis does not repeat discovery.

## Known rejection example

`I Gotta Feeling` was retained as an important negative control/example: a candidate symbolic representation showed an approximately 54-second duration discrepancy relative to the target released version. The case was excluded rather than relaxing the version/coverage gate to increase N.

## Initial accepted Dance-Pop validation seed

The initial accepted validation cohort consisted of:
- Poker Face
- Bad Romance
- TiK ToK
- Firework
- Dynamite

These are T0 validation-seed cases, not the final analytical population.

## Corpus scale logic

- T0 = 5: forensic/technical validation seed
- T1 = 30: pilot
- T2 = 50: minimum analytical cohort
- 75 / 100 / 125: stability checkpoints
- continue beyond these values when distributions remain unstable or the genre::style stratum is heterogeneous

N alone does not establish representativeness. Robust-corpus sufficiency is determined empirically through distributional stability gates.

## Offline/online separation

### OFFLINE ROBUST BUILD
`discover targets`
→ qualify success
→ resolve identity/version
→ acquire symbolic source
→ audit FULL_SONG
→ FULL_TMT
→ Matrix X
→ stability evaluation
→ cache robust reference

### ONLINE/LIGHT PREPRODUCTION
`cached ROBUST reference`
→ router
→ constraints
→ structural candidates

The online path must not search the corpus again or rebuild the master reference. This separation is central to the preproduction-speed objective.

## Bias control

Symbolic-source availability must be audited by release period, genre::style, language/market where relevant, and source coverage. A cluster of available MIDI files from one historical period cannot be interpreted as evidence that the underlying genre::style population is concentrated in that period.

## Scientific boundary

This pipeline establishes acquisition and qualification logic. It does not by itself establish statistical representativeness, released-recording vocal identity, or causal relationships between musical features and commercial success. Those claims require their respective validation gates.

## Migration invariant

Future chats/agents must preserve this distinction:

`scientific target population != songs available in Lakh/LMD`

and

`candidate discovery != scientific promotion`.

Do not remove or weaken identity, version, FULL_SONG, provenance, genre::style, or FULL_TMT gates merely to increase corpus size.
