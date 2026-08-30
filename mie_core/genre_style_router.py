#!/usr/bin/env python3
"""Genre/Style Cohort Router v1.0.

Engineering purpose:
- keep only a compact global registry in memory;
- resolve the requested genre/style as a multi-label query;
- retrieve only the statistically relevant cohort;
- build/use local corpus reference statistics for real-time analysis;
- fall back hierarchically when the requested cohort is too small.

Epistemic rule: genre/style route data access and comparison scope. They do not
imply quality, success or predictor importance. Inferential decisions remain under
data_first_guard.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Optional
import math

@dataclass(frozen=True)
class SongIndexRow:
    song_id: str
    genres: tuple[str, ...]
    styles: tuple[str, ...]
    year: Optional[int] = None
    market: Optional[str] = None
    fingerprint_uri: Optional[str] = None
    reference_uri: Optional[str] = None

@dataclass(frozen=True)
class CohortQuery:
    genres: tuple[str, ...] = ()
    styles: tuple[str, ...] = ()
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    market: Optional[str] = None
    min_n: int = 30
    max_n: int = 500


def norm(x: str) -> str:
    return ' '.join(x.strip().lower().split())


def overlap_score(row: SongIndexRow, q: CohortQuery) -> float:
    rg={norm(x) for x in row.genres}; rs={norm(x) for x in row.styles}
    qg={norm(x) for x in q.genres}; qs={norm(x) for x in q.styles}
    g=(len(rg&qg)/len(qg)) if qg else 0.0
    s=(len(rs&qs)/len(qs)) if qs else 0.0
    # Style is more specific than genre for retrieval; this is a routing priority,
    # not an inferential success weight.
    if qg and qs: return 0.4*g+0.6*s
    if qs: return s
    if qg: return g
    return 0.0


def hard_filters(row: SongIndexRow, q: CohortQuery) -> bool:
    if q.year_min is not None and (row.year is None or row.year < q.year_min): return False
    if q.year_max is not None and (row.year is None or row.year > q.year_max): return False
    if q.market is not None and norm(row.market or '') != norm(q.market): return False
    return True


def select_cohort(rows: Iterable[SongIndexRow], q: CohortQuery):
    rows=list(rows)
    stages=[
        ('GENRE_STYLE_EXACT', q),
        ('STYLE_ONLY', CohortQuery(styles=q.styles, year_min=q.year_min, year_max=q.year_max, market=q.market, min_n=q.min_n, max_n=q.max_n)),
        ('GENRE_ONLY', CohortQuery(genres=q.genres, year_min=q.year_min, year_max=q.year_max, market=q.market, min_n=q.min_n, max_n=q.max_n)),
        ('GENRE_STYLE_NO_MARKET', CohortQuery(genres=q.genres, styles=q.styles, year_min=q.year_min, year_max=q.year_max, min_n=q.min_n, max_n=q.max_n)),
    ]
    for stage,qq in stages:
        scored=[(overlap_score(r,qq),r) for r in rows if hard_filters(r,qq)]
        scored=[x for x in scored if x[0] > 0]
        scored.sort(key=lambda x:(x[0], x[1].year or -1), reverse=True)
        cohort=[r for _,r in scored[:qq.max_n]]
        if len(cohort) >= qq.min_n:
            return {'stage':stage,'n':len(cohort),'song_ids':[r.song_id for r in cohort],
                    'query':qq,'status':'LOCAL_REFERENCE_READY'}
    # Sparse-data state: do not pretend local statistics are stable.
    best=sorted([(overlap_score(r,q),r) for r in rows if hard_filters(r,q)],key=lambda x:x[0],reverse=True)
    best=[r for s,r in best if s>0][:q.max_n]
    return {'stage':'SPARSE_COHORT','n':len(best),'song_ids':[r.song_id for r in best],
            'query':q,'status':'DESCRIPTIVE_ONLY_NEEDS_MORE_DATA'}


def active_memory_plan(selection: dict):
    """Minimal memory contract for real-time analysis."""
    return {
        'keep_global_in_memory':['song_id','genres','styles','year','market','fingerprint_uri','reference_uri'],
        'load_on_demand':['selected fingerprints','local reference statistics','validated model slice if available'],
        'do_not_load_by_default':['raw audio','full lyrics corpus','all song objects','all feature matrices'],
        'cohort_size':selection['n'],
        'selection_stage':selection['stage'],
        'status':selection['status'],
    }
