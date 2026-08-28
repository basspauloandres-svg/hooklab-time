#!/usr/bin/env python3
from structural_reduction import reduce_candidates


def test_preserves_physical_timing_for_kept_events():
    raw=[{"id":"a","start_s":1.013,"end_s":1.227,"midi":60,"confidence":.8,"sensor":"synthetic"}]
    r=reduce_candidates(raw)
    assert r["render_events"][0]["start_s"]==1.013
    assert r["render_events"][0]["end_s"]==1.227


def test_same_pitch_overlap_prefers_confidence():
    raw=[
      {"id":"a","start_s":1.0,"end_s":1.3,"midi":60,"confidence":.6},
      {"id":"b","start_s":1.05,"end_s":1.28,"midi":60,"confidence":.9},
    ]
    r=reduce_candidates(raw)
    assert [e["id"] for e in r["render_events"]]==["b"]


def test_near_tie_different_pitch_is_preserved_but_not_rendered():
    raw=[
      {"id":"a","start_s":1.0,"end_s":1.3,"midi":60,"confidence":.70},
      {"id":"b","start_s":1.05,"end_s":1.28,"midi":64,"confidence":.73},
    ]
    r=reduce_candidates(raw)
    assert len(r["events"])==2
    assert len(r["render_events"])==0
    assert r["ambiguous_count"]==2
    assert all(e["state"]=="AMBIGUOUS" for e in r["events"])


def test_short_event_is_not_rendered():
    raw=[{"id":"x","start_s":2.0,"end_s":2.02,"midi":63,"confidence":.95}]
    r=reduce_candidates(raw)
    assert r["render_count"]==0
    assert any(d["candidate_id"]=="x" and d["reason"]=="SHORT_EVENT_CANDIDATE" for d in r["decisions"])


def test_octave_candidate_requires_context():
    raw=[
      {"id":"a","start_s":0.0,"end_s":.3,"midi":60,"confidence":.8},
      {"id":"b","start_s":.4,"end_s":.7,"midi":72,"confidence":.8},
      {"id":"c","start_s":.8,"end_s":1.1,"midi":61,"confidence":.8},
    ]
    r=reduce_candidates(raw)
    b=[e for e in r["render_events"] if e["id"]=="b"][0]
    assert b["midi"]==60
    assert b["state"]=="PROVISIONAL"
    assert any(d["candidate_id"]=="b" and d["action"]=="OCTAVE_ALTERNATIVE" for d in r["decisions"])


if __name__=='__main__':
    test_preserves_physical_timing_for_kept_events()
    test_same_pitch_overlap_prefers_confidence()
    test_near_tie_different_pitch_is_preserved_but_not_rendered()
    test_short_event_is_not_rendered()
    test_octave_candidate_requires_context()
    print('PASS structural reduction invariants')
