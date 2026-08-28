#!/usr/bin/env python3
"""MIE Structural Reduction v0.2.

Conservative interface between melody sensors and the final structural melody.
This module does not claim to reproduce historical STAB-004 -> P30 code.
Every decision is returned as provenance. Experimental thresholds are explicit.
Ambiguous hypotheses are preserved for reasoning but excluded from render_events.
"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Set


@dataclass
class Candidate:
    id: str
    start_s: float
    end_s: float
    midi: int
    confidence: float
    sensor: str = "unknown"

    @property
    def duration_s(self):
        return max(0.0, self.end_s - self.start_s)


@dataclass
class Decision:
    candidate_id: str
    action: str
    reason: str
    state: str
    evidence: Dict[str, Any]


DEFAULT_EXPERIMENTAL = {
    # Engineering hypotheses only. They are not recovered P30 constants.
    "min_duration_s": 0.045,
    "overlap_s": 0.025,
    "octave_tolerance_semitones": 1,
    "octave_jump_min_semitones": 10,
    "confidence_margin": 0.08,
}


def _overlap(a: Candidate, b: Candidate) -> float:
    return max(0.0, min(a.end_s, b.end_s) - max(a.start_s, b.start_s))


def _continuity_cost(midi: int, prev: Optional[Candidate], nxt: Optional[Candidate]) -> float:
    vals=[]
    if prev is not None:
        vals.append(abs(midi-prev.midi))
    if nxt is not None:
        vals.append(abs(nxt.midi-midi))
    return sum(vals)/len(vals) if vals else 0.0


def reduce_candidates(raw: List[Dict[str, Any]], config=None):
    cfg=dict(DEFAULT_EXPERIMENTAL)
    if config:
        cfg.update(config)
    cands=[]
    for i,n in enumerate(raw):
        cands.append(Candidate(
            id=str(n.get("id", f"cand_{i:05d}")),
            start_s=float(n["start_s"]), end_s=float(n["end_s"]),
            midi=int(n["midi"]), confidence=float(n.get("confidence", 0.0)),
            sensor=str(n.get("sensor", "unknown"))))
    cands.sort(key=lambda x:(x.start_s,x.end_s,-x.confidence,x.midi))
    decisions: List[Decision]=[]
    ambiguous_ids: Set[str]=set()

    # 1. Very short events are retained in hypothesis provenance, not promoted to render.
    active=[]
    for c in cands:
        if c.duration_s < cfg["min_duration_s"]:
            ambiguous_ids.add(c.id)
            decisions.append(Decision(c.id,"HOLD","SHORT_EVENT_CANDIDATE","AMBIGUOUS",
                                      {"duration_s":c.duration_s,
                                       "threshold_experimental":cfg["min_duration_s"]}))
        else:
            active.append(c)

    # 2. Resolve strong overlaps conservatively. Different-pitch near ties remain hypotheses only.
    kept=[]
    for c in active:
        conflicts=[q for q in kept if _overlap(c,q) >= cfg["overlap_s"]]
        if not conflicts:
            kept.append(c)
            decisions.append(Decision(c.id,"KEEP","NO_STRONG_OVERLAP","LOCK",{}))
            continue
        q=max(conflicts,key=lambda x:x.confidence)
        margin=c.confidence-q.confidence
        if c.midi==q.midi:
            if c.confidence>q.confidence:
                kept.remove(q); kept.append(c)
                decisions.append(Decision(q.id,"DROP","DUPLICATE_SAME_PITCH_LOWER_CONFIDENCE","LOCK",{"winner":c.id}))
                decisions.append(Decision(c.id,"KEEP","DUPLICATE_SAME_PITCH_HIGHER_CONFIDENCE","LOCK",{"loser":q.id}))
            else:
                decisions.append(Decision(c.id,"DROP","DUPLICATE_SAME_PITCH_LOWER_CONFIDENCE","LOCK",{"winner":q.id}))
        elif abs(margin) >= cfg["confidence_margin"]:
            winner=c if margin>0 else q
            loser=q if margin>0 else c
            if winner is c:
                kept.remove(q); kept.append(c)
            decisions.append(Decision(loser.id,"DROP","OVERLAP_CONFIDENCE_DOMINANCE","LOCK",
                                      {"winner":winner.id,"margin":abs(margin)}))
            if winner is c:
                decisions.append(Decision(c.id,"KEEP","OVERLAP_CONFIDENCE_DOMINANCE","LOCK",
                                          {"loser":q.id,"margin":abs(margin)}))
        else:
            # Preserve both internally but do not synthesize either until a later resolver chooses.
            kept.append(c)
            ambiguous_ids.update([c.id,q.id])
            decisions.append(Decision(c.id,"HOLD","OVERLAP_NEAR_TIE","AMBIGUOUS",
                                      {"other":q.id,"confidence_margin":margin}))
            decisions.append(Decision(q.id,"HOLD","OVERLAP_NEAR_TIE","AMBIGUOUS",
                                      {"other":c.id,"confidence_margin":-margin}))

    kept.sort(key=lambda x:(x.start_s,x.end_s,-x.confidence))

    # 3. Octave-plane alternatives. Preserve timing; pitch change remains PROVISIONAL.
    out=[]
    provisional_ids: Set[str]=set()
    for i,c in enumerate(kept):
        prev=kept[i-1] if i else None
        nxt=kept[i+1] if i+1<len(kept) else None
        base=_continuity_cost(c.midi,prev,nxt)
        alternatives=[]
        for delta in (-12,12):
            m=c.midi+delta
            if 0<=m<=127:
                alternatives.append((m,_continuity_cost(m,prev,nxt)))
        best=min(alternatives,key=lambda x:x[1]) if alternatives else None
        jump_context=((prev and abs(c.midi-prev.midi)>=cfg["octave_jump_min_semitones"]) or
                      (nxt and abs(nxt.midi-c.midi)>=cfg["octave_jump_min_semitones"]))
        if best and jump_context and best[1]+cfg["octave_tolerance_semitones"] < base:
            nc=Candidate(c.id,c.start_s,c.end_s,best[0],c.confidence,c.sensor)
            out.append(nc)
            provisional_ids.add(c.id)
            decisions.append(Decision(c.id,"OCTAVE_ALTERNATIVE","CONTINUITY_FAVOURS_OCTAVE_PLANE","PROVISIONAL",
                                      {"input_midi":c.midi,"output_midi":best[0],
                                       "base_cost":base,"alternative_cost":best[1]}))
        else:
            out.append(c)

    # All hypotheses are retained for audit. Only non-ambiguous candidates may reach synthesis.
    hypothesis_events=[]
    render_events=[]
    for x in out:
        d=asdict(x)
        if x.id in ambiguous_ids:
            d["state"]="AMBIGUOUS"
        elif x.id in provisional_ids:
            d["state"]="PROVISIONAL"
            render_events.append(dict(d))
        else:
            d["state"]="LOCK"
            render_events.append(dict(d))
        hypothesis_events.append(d)

    return {
        "version":"MIE Structural Reduction v0.2",
        "historical_code_exact":False,
        "config_status":"EXPERIMENTAL_NOT_TUNED_TO_REFERENCE_SONG",
        "config":cfg,
        "input_count":len(cands),
        "hypothesis_count":len(hypothesis_events),
        "render_count":len(render_events),
        "ambiguous_count":sum(1 for x in hypothesis_events if x["state"]=="AMBIGUOUS"),
        "events":hypothesis_events,
        "render_events":render_events,
        "decisions":[asdict(x) for x in decisions],
    }
