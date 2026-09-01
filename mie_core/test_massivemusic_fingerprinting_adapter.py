from massivementmusic_fingerprinting_adapter import run

def target(): return {"song_id":"poker_face_lady_gaga","title":"Poker Face","artist":"Lady Gaga"}

def test_unprovisioned_is_deterministic_reference_unavailable():
    out=run(target(),env={})
    assert out["status"]=="REFERENCE_UNAVAILABLE"
    assert out["scientific_failure"] is False
    assert out["fallback_attempted"] is False
    assert out["provenance"]["authorization_boundary"]=="FAIL_CLOSED_BEFORE_MEDIA_ACCESS"

def test_provisioned_pass_preserves_provenance():
    env={"HOOKLAB_MM_PARTNER_ID":"x","HOOKLAB_MM_AUTHORIZED_ENV_ID":"vm1","HOOKLAB_MM_TRACK_RESOLVER_CMD":"resolve","HOOKLAB_MM_PIPELINE_CMD":"pipeline"}
    def runner(cmd,payload):
        if cmd=="resolve": return {"ok":True,"data":{"track_id":"t1","version_identity_status":"VERIFIED","authorized_computational_access":True}}
        return {"ok":True,"data":{"validation_decision":"PASS","vocal_extraction":"DONE","audio_midi_alignment":"DONE","metrics":{"f1":.91}}}
    out=run(target(),env=env,runner=runner)
    assert out["status"]=="PASS" and out["scientific_failure"] is False
    assert len(out["provenance"]["stages"])==2

def test_real_validation_failure_is_fail():
    env={"HOOKLAB_MM_PARTNER_ID":"x","HOOKLAB_MM_AUTHORIZED_ENV_ID":"vm1","HOOKLAB_MM_TRACK_RESOLVER_CMD":"resolve","HOOKLAB_MM_PIPELINE_CMD":"pipeline"}
    def runner(cmd,payload):
        if cmd=="resolve": return {"ok":True,"data":{"track_id":"t1","version_identity_status":"VERIFIED","authorized_computational_access":True}}
        return {"ok":True,"data":{"validation_decision":"FAIL","metrics":{"f1":.2}}}
    out=run(target(),env=env,runner=runner)
    assert out["status"]=="FAIL" and out["scientific_failure"] is True
