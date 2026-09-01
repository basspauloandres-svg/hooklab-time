# Genre/Style Routing Architecture v1.0

## Objective
Enable HookLab/TIME to answer in near-real time without loading the entire corpus into active memory. Genre and style operate as routing dimensions for cohort selection and local statistical reference construction.

## Request flow
`USER REQUEST -> GENRE/STYLE RESOLUTION -> COHORT ROUTER -> LOCAL DATA SLICE -> LOCAL REFERENCE MODEL -> ANALYSIS / GENERATION`

Example:
`genre = reggaeton; style = romantic / mid-tempo`

The router does not load the complete corpus. It consults a compact global index containing identifiers, genre/style labels, time/market metadata and pointers to fingerprints/reference shards. It then loads only the cohort required for the current request.

## Two-level memory design
### Level A — Global lightweight registry
Always resident or rapidly queryable:
- song_id
- genre labels (multi-label)
- style labels (multi-label)
- year/period
- market/territory when available
- pointer to Structural Fingerprint
- pointer to local reference shard

No raw audio, full lyrics or complete Song Objects are required in active memory.

### Level B — Active cohort memory
Loaded on demand after routing:
- selected Structural Fingerprints
- local corpus reference statistics
- validated model parameters relevant to that cohort, when they exist
- optional nearest-neighbour exemplars for audit

After the request, the active cohort can be released.

## Hierarchical fallback
Because genre/style categories may be sparse or fuzzy, cohort selection is hierarchical:
1. requested genre + requested style;
2. requested style;
3. requested genre;
4. requested genre/style without market restriction;
5. sparse cohort state.

The engine must not fabricate statistical stability. If the cohort remains below the minimum empirical size, output status becomes `DESCRIPTIVE_ONLY_NEEDS_MORE_DATA`.

## Genre/style are routing variables, not success rules
Genre and style define the comparison neighbourhood. They do not imply that any musical characteristic is better. The Data First Guard remains authoritative:

`DATA -> STATISTICAL STRUCTURE -> PATTERN -> CONTRAST -> VALIDATION -> DECISION`

Thus, a request for a genre/style means: "retrieve the empirical population most relevant to this request and let its data define the local reference distribution."

## Recommended indexing strategy
At scale, persist the global registry in a small relational/columnar table and shard fingerprints by normalized genre/style keys. A vector index may be added later for fuzzy style similarity, but categorical/multi-label routing remains the first gate because it is transparent and auditable.

## Real-time generation contract
For a future generation request:
1. user specifies or confirms genre/style;
2. router selects empirical cohort;
3. local statistics and validated patterns are loaded;
4. story/persons/tensions and other textual constraints are supplied to the generative layer;
5. the generator works only with validated cohort-derived constraints plus explicit user constraints;
6. output is checked against the same local cohort reference.

## Cache policy
Frequently requested cohorts may have precomputed reference shards and short-lived caches. Cache keys should include normalized genre/style plus relevant period/market filters and a corpus-version hash so stale reference statistics cannot be silently reused after corpus updates.
