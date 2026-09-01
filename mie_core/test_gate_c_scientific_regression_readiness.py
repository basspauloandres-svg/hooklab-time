from gate_c_scientific_regression_readiness import evaluate

def test_missing_empirical_gates_block_regression():
    out=evaluate({
        "gate_a":{"observed_external_validation":False,"state":"IMPLEMENTATION_COMPLETE"},
        "gate_b":{"valid_human_trial_n":0,"raw_artifacts_retained":False},
        "technical_regression":{"existing_e2e_available":True,"existing_replay_available":True},
        "documentation":{"provenance_manifest_ready":True,"checkpoint_chain_ready":True},
    })
    assert out["state"]=="SCIENTIFIC_REGRESSION_BLOCKED"
    assert "gate_a_observed_external_evidence" in out["blocked_by"]
    assert "gate_b_observed_human_baseline" in out["blocked_by"]

def test_reference_unavailable_never_counts_as_observed_pass():
    out=evaluate({
        "gate_a":{"observed_external_validation":False,"state":"REFERENCE_UNAVAILABLE"},
        "gate_b":{"valid_human_trial_n":1,"raw_artifacts_retained":True},
        "technical_regression":{"existing_e2e_available":True,"existing_replay_available":True},
        "documentation":{"provenance_manifest_ready":True,"checkpoint_chain_ready":True},
    })
    assert out["state"]=="SCIENTIFIC_REGRESSION_BLOCKED"

def test_ready_only_when_all_prerequisites_exist():
    out=evaluate({
        "gate_a":{"observed_external_validation":True,"state":"SEED_EXTERNALLY_CALIBRATED"},
        "gate_b":{"valid_human_trial_n":3,"raw_artifacts_retained":True},
        "technical_regression":{"existing_e2e_available":True,"existing_replay_available":True},
        "documentation":{"provenance_manifest_ready":True,"checkpoint_chain_ready":True},
    })
    assert out["state"]=="SCIENTIFIC_REGRESSION_READY"
