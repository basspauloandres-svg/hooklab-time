from gate_b_human_ttpf_trial import summarize

REQ=["section_form_plan","tempo_metric_recommendation","harmonic_tonal_recommendation","melodic_rhythmic_recommendation","production_constraints"]

def trial(**kw):
    base={"observed":True,"participant_id":"p1","task_id":"t1","ttfp_seconds":120,"admissible_outputs":REQ}
    base.update(kw); return base

def test_unobserved_cannot_populate_gate():
    out=summarize({"trials":[trial(observed=False)]})
    assert out["valid_trial_n"]==0
    assert out["gate_b_state"]=="PENDING_OBSERVATIONS"

def test_incomplete_output_contract_is_invalid():
    out=summarize({"trials":[trial(admissible_outputs=["section_form_plan"])]})
    assert out["valid_trial_n"]==0
    assert "OUTPUT_CONTRACT_INCOMPLETE" in out["trials"][0]["validation_errors"][0]

def test_observed_valid_trial_populates_pilot_descriptively():
    out=summarize({"trials":[trial(ttfp_seconds=120),trial(participant_id="p2",task_id="t2",ttfp_seconds=180)]})
    assert out["valid_trial_n"]==2
    assert out["human_summary"]["median_seconds"]==150
    assert out["gate_b_state"]=="EMPIRICALLY_POPULATED_PILOT"
    assert out["scientific_claim_allowed"] is False
