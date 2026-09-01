# OPEN METADATA AUTOMATED SNAPSHOT CONTRACT v1

**Status:** CANONICAL DESCRIPTIVE COLLECTION LANE  
**Collection class:** AUTOMATED PUBLIC METADATA SNAPSHOT  
**Scientific boundary:** FAIL-CLOSED

## Purpose

This lane builds a prospective, timestamped series of public circulation
metrics for HookLab cases whose YouTube identities have already been verified.
It replaces paid-quota dependence for prototype snapshots. It does not replace
the HookLab lyric corpus and does not provide retrospective traffic history.

## Mandatory boundaries

1. Only records with `identity_review_status=VERIFIED` may enter a snapshot.
2. Candidate discovery may never assign or promote a verified identity.
3. The collector must not request or download media.
4. Lyrics, captions, descriptions, audio and video must not be persisted.
5. Every snapshot must record collector and provider versions, capture time,
   case ID, video ID, public counts and fetch status.
6. Provider failure remains local to the affected record and is preserved as
   an audit state. The workflow may not call a zero-record or partial snapshot
   complete and may not commit it as a valid scientific input.
7. `generation_class=D0_EXPLORATORY` and
   `scientific_d_unlocked=false` are invariant.
8. A public cumulative view count is a timestamped snapshot. It is not itself
   a traffic peak, causal effect, success rule or conditioned deduction.
9. Inferential use remains blocked behind Feature Admissibility, Analysis
   Registration and Statistical Test.

## Automated schedule

`.github/workflows/open-metadata-daily-snapshots.yml` runs daily at 06:17 UTC,
writes a timestamped JSON plus `latest.json`, validates the scientific boundary
and commits the snapshot to the canonical repository. A workflow artifact is
also retained as recovery evidence.

## Provider

Candidate discovery retains pinned `yt-dlp` as an open-source search lane.
Scheduled metric snapshots use the open Return YouTube Dislike public votes
endpoint without credentials or paid quota. The provider documents that views,
likes and related public fields originate from Google APIs and scraped public
data and may be cached for approximately 2–3 days.

Only `view_count` and `like_count` are retained. `dislikes`, `rawDislikes`,
`rawLikes` and `rating` are prohibited because dislike values may be estimated
or reconstructed. The snapshot records the provider, endpoint contract version,
cache policy and data-lineage statement. A provider change requires an explicit
collector version update and contract regression.

## Completion rule

A workflow run is valid only when at least one verified identity is collected
and every verified identity included in the identity map has
`snapshot_status=SNAPSHOT_COMPLETE`. Any provider outage, identity mismatch,
deleted record or invalid view count fails closed before the commit step.

## Provenance chain

`youtube_video_identity_map_v0_1.json`
→ `open_metadata_stack_collector.py`
→ timestamped snapshot JSON
→ automated contract validation
→ repository commit and workflow artifact.
