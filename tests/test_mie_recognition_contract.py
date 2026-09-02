import copy
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from mie_core.mie_ai_candidate_reasoner import (
    attach_advice,
    build_request,
    deterministic_advice,
    validate_response,
)
from mie_core.mie_recognition_contract import normalize
from mie_core.mie_recovery_pipeline import apply_reasoning, harmonic_candidates
from mie_core.mie_octave_plane_resolver import resolve_event_octaves


raw = {
    "duration_s": 2.0,
    "notes": [{"start_s": 0.1, "end_s": 0.5, "midi": 60, "confidence": 0.9}],
    "harmony": [
        {
            "unit_id": "H-0000",
            "start_s": 0.0,
            "end_s": 1.0,
            "root_pc": 0,
            "quality": "maj",
            "state": "LOCK",
            "candidates": [
                {"candidate_id": "C", "pitch_class": 0, "acoustic_score": 0.9, "residual_score": 0.8},
                {"candidate_id": "E", "pitch_class": 4, "acoustic_score": 0.7, "residual_score": 0.6},
            ],
        }
    ],
    "beats": [{"t": 0.0, "score": 0.9}, {"t": 0.5, "score": 0.8}],
}

request = build_request(raw["harmony"], analysis_id="A-1")
response = deterministic_advice(request)
assert validate_response(request, response)["status"] == "PASS"
advised = attach_advice(raw["harmony"], request, response)
assert advised[0]["raw_sensor_state_preserved"] == "LOCK"

hostile = copy.deepcopy(response)
hostile["decisions"][0]["candidate_decisions"].append(
    {"candidate_id": "F_SHARP_NOT_OBSERVED", "action": "KEEP", "score": 1.0}
)
assert validate_response(request, hostile)["status"] == "FAIL"

result = normalize(
    {**raw, "harmony": advised},
    session_id="HL-1",
    reference_sha256="abc",
    sensor_version="MIE_CORE_v0.3-recovery",
    ai_provenance={"provider": response["provider"], "provider_connected": False},
)
assert result["status"] == "PASS"
assert result["scientific_d_unlocked"] is False
assert result["source_audio_persistence"] == "NONE"
assert result["recognition"]["locked_harmony_units"] == 1
assert result["recognition"]["note_beat_harmony_relations"][0]["harmony_unit_id"] == "H-0000"

for missing in ("notes", "harmony", "beats"):
    incomplete = copy.deepcopy(raw)
    incomplete[missing] = []
    failed = normalize(
        incomplete,
        session_id="HL-1",
        reference_sha256="abc",
        sensor_version="test",
    )
    assert failed["status"] == "FAIL"

candidate_units = harmonic_candidates(
    [{"start_s": 0.0, "end_s": 1.0, "root_pc": 0, "intervals": [0, 4, 7], "evidence": 0.8, "margin": 0.1, "state": "LOCK"}]
)
assert {c["pitch_class"] for c in candidate_units[0]["candidates"]} == {0, 4, 7}
reasoned = apply_reasoning({"harmony": candidate_units}, analysis_id="A-2")
assert reasoned["ai_provenance"]["provider"] == "DETERMINISTIC_CONTEXTUAL_REASONER_v1"
assert reasoned["ai_provenance"]["provider_connected"] is False

resolved = resolve_event_octaves(
    [
        {"start_s": 0.0, "end_s": 0.4, "midi": 60},
        {"start_s": 0.42, "end_s": 0.54, "midi": 72},
        {"start_s": 0.56, "end_s": 1.0, "midi": 61},
    ]
)
assert resolved[1]["midi"] == 60
assert resolved[1]["octave_corrected"] is True

print("MIE_RECOGNITION_CONTRACT_PASS")
