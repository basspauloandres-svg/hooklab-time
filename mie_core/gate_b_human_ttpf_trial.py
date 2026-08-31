#!/usr/bin/env python3
"""Gate B observed human/traditional TTFP trial recorder/summarizer.

This module does not simulate human times. It validates observed trial records,
computes descriptive summaries, and keeps engine latency distinct from assisted
human-review latency.
"""
from __future__ import annotations
import argparse,json,statistics
from pathlib import Path

ENGINE_MEDIAN_S=0.0982974605
REQUIRED_OUTPUTS={"section_form_plan","tempo_metric_recommendation","harmonic_tonal_recommendation","melodic_rhythmic_recommendation","production_constraints"}

def validate_trial(t):
    errors=[]
    if not t.get("observed"): errors.append("NOT_OBSERVED")
    if not t.get("participant_id"): errors.append("MISSING_PARTICIPANT_ID")
    if not t.get("task_id"): errors.append("MISSING_TASK_ID")
    try:
        sec=float(t.get("ttfp_seconds"));
        if sec<=0: errors.append("NONPOSITIVE_TTFP")
    except Exception: errors.append("INVALID_TTFP"); sec=None
    outputs=set(t.get("admissible_outputs",[])); missing=sorted(REQUIRED_OUTPUTS-outputs)
    if missing: errors.append("OUTPUT_CONTRACT_INCOMPLETE:"+",".join(missing))
    return {**t,"valid":not errors,"validation_errors":errors,"ttfp_seconds":sec}

def summarize(payload):
    rows=[validate_trial(x) for x in payload.get("trials",[])]; vals=[x["ttfp_seconds"] for x in rows if x["valid"]]
    out={"schema":"HOOKLAB_GATE_B_HUMAN_TTFP_v1.0","observed_trial_n":len(rows),"valid_trial_n":len(vals),"invalid_trial_n":len(rows)-len(vals),"trials":rows,"engine_median_seconds":ENGINE_MEDIAN_S,"scientific_claim_allowed":False}
    if vals:
        sv=sorted(vals); out["human_summary"]={"median_seconds":statistics.median(vals),"mean_seconds":statistics.mean(vals),"min_seconds":min(vals),"max_seconds":max(vals),"speed_ratio_descriptive":statistics.median(vals)/ENGINE_MEDIAN_S}
        out["gate_b_state"]="EMPIRICALLY_POPULATED_PILOT" if len(vals)>=1 else "PENDING_OBSERVATIONS"
    else: out["human_summary"]=None; out["gate_b_state"]="PENDING_OBSERVATIONS"
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--input",required=True);ap.add_argument("--output",required=True);a=ap.parse_args();out=summarize(json.loads(Path(a.input).read_text()))
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({"valid_trial_n":out["valid_trial_n"],"gate_b_state":out["gate_b_state"]}))
if __name__=="__main__":main()
