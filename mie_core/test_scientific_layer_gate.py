from scientific_layer_gate import evaluate

def approved_layer():
    return {
        "layer_id":"LAYER_X",
        "state":"APPROVED",
        "scientific_basis":{"evidence":["E1"]},
        "decision_record":{"scope":"test"},
        "implementation":{"path":"mie_core/x.py","version":"1"},
        "tests_or_validation":{"status":"PASS"},
        "provenance":{"inputs":["E1"],"outputs":["O1"]},
        "checkpoint":{"path":"CHECKPOINTS/X.md"},
        "approval_decision":True
    }

def test_complete_approved_layer_passes():
    out=evaluate(approved_layer())
    assert out["decision"]=="PASS"
    assert out["downstream_eligible"] is True

def test_implemented_without_validation_is_blocked():
    x=approved_layer();x["state"]="IMPLEMENTED";x["tests_or_validation"]=None
    out=evaluate(x)
    assert out["decision"]=="BLOCKED"
    assert "tests_or_validation" in out["missing_requirements"]

def test_missing_checkpoint_is_blocked():
    x=approved_layer();x["checkpoint"]=None
    out=evaluate(x)
    assert out["decision"]=="BLOCKED"

def test_approval_flag_required():
    x=approved_layer();x["approval_decision"]=False
    assert evaluate(x)["decision"]=="BLOCKED"
