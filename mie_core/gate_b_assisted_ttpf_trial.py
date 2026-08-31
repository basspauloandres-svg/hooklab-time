#!/usr/bin/env python3
"""Gate B HookLab-assisted TTFP recorder.
Keeps engine latency and observed human candidate-review time separate.
No simulated or estimated review time is accepted.
"""
from __future__ import annotations
import argparse,json,statistics
from pathlib import Path
ENGINE_MEDIAN_S=0.0982974605

def validate_trial(t):
    errors=[]
    if not t.get("observed"): errors.append("NOT_OBSERVED")
    if not t.get("reviewer_id"): errors.append("MISSING_REVIEWER_ID")
    if not t.get("task_id"): errors.append("MISSING_TASK_ID")
    try:
        review=float(t.get("human_candidate_review_seconds"))
        if review<0: errors.append("NEGATIVE_REVIEW_TIME")
    except Exception: review=None; errors.append("INVALID_REVIEW_TIME")
    engine=float(t.get("engine_latency_seconds",ENGINE_MEDIAN_S))
    assisted=(engine+review) if review is not None else None
    return {**t,"valid":not errors,"validation_errors":errors,"engine_latency_seconds":engine,"human_candidate_review_seconds":review,"ttfp_hooklab_assisted_seconds":assisted}

def summarize(payload):
    rows=[validate_trial(x) for x in payload.get("trials",[])]; vals=[x["ttfp_hooklab_assisted_seconds"] for x in rows if x["valid"]]
    return {"schema":"HOOKLAB_GATE_B_ASSISTED_TTFP_v1.0","valid_trial_n":len(vals),"trials":rows,"assisted_summary":None if not vals else {"median_seconds":statistics.median(vals),"mean_seconds":statistics.mean(vals),"min_seconds":min(vals),"max_seconds":max(vals)},"state":"PENDING_OBSERVATIONS" if not vals else "ASSISTED_OBSERVATIONS_AVAILABLE","interpretation_boundary":"Assisted TTFP is deployment workflow latency; it does not replace pure engine latency and cannot be populated with simulated review time."}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--input",required=True);ap.add_argument("--output",required=True);a=ap.parse_args();out=summarize(json.loads(Path(a.input).read_text()));Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({"valid_trial_n":out["valid_trial_n"],"state":out["state"]}))
if __name__=="__main__":main()
