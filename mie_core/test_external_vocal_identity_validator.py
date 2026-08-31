from external_vocal_identity_validator import validate


def _note(s, e, p):
    return {"start_s": s, "end_s": e, "midi_pitch": p}


def test_clean_match_passes():
    ref = [_note(0.0, 0.4, 60), _note(0.5, 0.9, 62), _note(1.0, 1.4, 64), _note(1.5, 1.9, 62)]
    est = [_note(0.01, 0.39, 60), _note(0.51, 0.91, 62), _note(1.01, 1.41, 64), _note(1.49, 1.89, 62)]
    payload = {
        "song_id": "fixture",
        "release_reference": "fixture-release",
        "reference_annotation_frozen": True,
        "independence_attested": True,
        "excerpts": [
            {"excerpt_id": "verse", "reference_notes": ref, "symbolic_notes": est},
            {"excerpt_id": "contrast", "reference_notes": ref, "symbolic_notes": est},
            {"excerpt_id": "hook", "reference_notes": ref, "symbolic_notes": est},
        ],
    }
    out = validate(payload)
    assert out["song_decision"] == "AUDIO_REFERENCE_PASS"
    assert out["scientific_eligibility"] is True


def test_wrong_pitch_fails():
    ref = [_note(0.0, 0.4, 60), _note(0.5, 0.9, 62), _note(1.0, 1.4, 64)]
    est = [_note(0.0, 0.4, 67), _note(0.5, 0.9, 69), _note(1.0, 1.4, 71)]
    payload = {
        "song_id": "fixture",
        "reference_annotation_frozen": True,
        "independence_attested": True,
        "excerpts": [{"excerpt_id": "hook", "reference_notes": ref, "symbolic_notes": est}],
    }
    out = validate(payload)
    assert out["song_decision"] == "AUDIO_REFERENCE_FAIL"


def test_unfrozen_reference_is_not_scientifically_eligible():
    ref = [_note(0.0, 0.4, 60), _note(0.5, 0.9, 62), _note(1.0, 1.4, 64)]
    payload = {
        "song_id": "fixture",
        "reference_annotation_frozen": False,
        "independence_attested": True,
        "excerpts": [{"excerpt_id": "hook", "reference_notes": ref, "symbolic_notes": ref}],
    }
    out = validate(payload)
    assert out["song_decision"] == "AUDIO_REFERENCE_PASS"
    assert out["scientific_eligibility"] is False
