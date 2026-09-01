# HookLab — Digital Circulation, Chorus and Traffic Gate v0.1

Date: 2026-09-01
Status: **PROSPECTIVE COLLECTION ACTIVE / NO TRAFFIC ASSOCIATION EXECUTED**

## Scientific decision

Digital circulation is registered as an observed outcome layer. It is kept separate from lyric, chorus, melody and beat measurements so that an association cannot be encoded as a compositional fact before testing.

The proposed question has three distinct components:

1. song-level circulation: cumulative views and age-adjusted view velocity;
2. publication-time peaks: maximum observed views per hour within a registered time series;
3. content-level attention: audience retention at independently timestamped chorus intervals.

A publication-time traffic peak does not identify which section of the song attracted attention. A chorus-level statement requires `elapsedVideoTimeRatio` retention data aligned with verified chorus timestamps on the content clock.

## Source audit

The eleven tabs of the canonical 100-song workbook were inspected at their headers. They contain case metadata, documentary lyrics, observations and historical derivatives; they contain no YouTube `video_id`, view snapshots, VPH histories or audience-retention curves.

vidIQ was queried on 2026-09-01. The connection is active with zero available credits and a reported renewable reset at `2026-09-22T13:26:48.585205Z`; therefore, no video search, identity resolution or traffic metric was retrieved.

An independent quota-free public-data route is active through the open Return
YouTube Dislike public endpoint. HookLab retains only provider-reported cached
public views and likes; reconstructed dislike fields and ratings are forbidden.
The provider documents a cache interval of approximately 2–3 days, which is
recorded as measurement latency rather than hidden.

The cross-source identity audit has resolved 15 of 100 cases. The first
automated run captured all 15 verified IDs successfully. This first capture is
a pilot/provenance snapshot outside the future inferential observation window;
it cannot be used to choose a favorable high-traffic threshold.

## Registered candidate outcomes

| Outcome | Meaning | Current status |
|---|---|---|
| `CIRC_YT_VIEW_COUNT_SNAPSHOT_v0_1` | Cumulative views at a dated capture | Pilot 15/15; blocked pending full identity coverage and prospective window |
| `CIRC_YT_LOG_VIEW_VELOCITY_v0_1` | Age-adjusted lifetime circulation | Publication timestamp and full coverage pending |
| `CIRC_YT_PEAK_VPH_v0_1` | Peak observed velocity in a registered series | Source not mapped |
| `RET_YT_CHORUS_AUDIENCE_WATCH_RATIO_DELTA_v0_1` | Chorus retention relative to adjacent windows | Authorization and section alignment absent |
| `THEME_SIMILARITY_HIGH_TRAFFIC_CONTRAST_v0_1` | Corpus-local thematic similarity contrast | Traffic and theme features inadmissible |

## Interpretive boundary

Views depend on exposure conditions that include publication age, channel scale, artist history, genre, language, recommendation systems, paid promotion, external events and video format. These variables require measurement or sensitivity analysis before a musical association can be interpreted.

The words “incidence” and “effect” are reserved for designs that identify a causal contrast. The current planned analyses estimate associations and matched similarity differences; their outputs cannot establish that a chorus, melody, rhythm or theme caused elevated circulation.

Music-video scholarship also indicates that visual and musical information can jointly shape attention and perceived meaning. Consequently, a YouTube-video outcome cannot be attributed exclusively to the song's audio or lyrics without representing the audiovisual layer.

## Required next gate

1. Freeze the rule selecting one canonical official YouTube artifact per `case_id`.
2. Treat the first 15-record snapshot as pilot only; freeze the primary
   circulation outcome, future observation window and high-traffic rule before
   the inferential series begins.
3. Resolve all `video_id` values with documentary identity evidence.
4. Continue daily quota-free snapshots; vidIQ may be evaluated later as an
   optional historical-series source but is not required for prototype collection.
5. Treat chorus retention as a separate lane requiring rights-holder authorization and calibrated section timestamps.
6. Admit lyric, melody and beat features independently before registering their association with circulation.

## Automated collection path without vidIQ or an API key

```bash
python3 mie_core/open_metadata_stack_collector.py collect-verified-snapshot \
  --identity-map data/engagement_modeling/youtube_video_identity_map_v0_1.json \
  --snapshot-dir data/engagement_modeling/snapshots/youtube
```

`.github/workflows/open-metadata-daily-snapshots.yml` runs this lane daily and
fails before commit unless every currently verified identity is complete.
Authorized YouTube Analytics remains necessary for chorus-level retention;
song-level public views cannot substitute for content-clock retention.

## References used for operationalization

- YouTube Analytics API. Metrics and `audienceWatchRatio`: https://developers.google.com/youtube/analytics/metrics
- YouTube Analytics API. `elapsedVideoTimeRatio`: https://developers.google.com/youtube/analytics/dimensions
- YouTube Analytics API. Audience-retention report constraints: https://developers.google.com/youtube/analytics/sample-requests
- YouTube Data API v3. `search.list`: https://developers.google.com/youtube/v3/docs/search/list
- YouTube Data API v3. `videos.list`: https://developers.google.com/youtube/v3/docs/videos/list
- Dasovich-Wilson, J. N., Thompson, M., & Saarikallio, S. (2022). *Exploring Music Video Experiences and Their Influence on Music Perception*. Music & Science, 5. https://doi.org/10.1177/20592043221117651

The references define measurement and interpretation boundaries. Empirical direction remains determined exclusively by registered HookLab data and statistics.
