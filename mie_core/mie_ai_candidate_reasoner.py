"""Provider-neutral advisory reasoning over acoustically observed MIE candidates.

The reasoning layer may rank, retain, query or drop candidates already emitted by
the sensor.  It cannot create acoustic evidence, rewrite timestamps or promote a
scientific state.
"""

from __future__ import annotations

from copy import deepcopy
import json
import urllib.request


SCHEMA_REQUEST = "HOOKLAB_MIE_AI_CANDIDATE_REQUEST_v1"
SCHEMA_RESPONSE = "HOOKLAB_MIE_AI_CANDIDATE_RESPONSE_v1"
ALLOWED_ACTIONS = {"KEEP", "QUERY", "DROP"}


def build_request(units, *, analysis_id, provider="UNCONNECTED_PRIVATE_PROVIDER"):
    normalized = []
    for index, unit in enumerate(units):
        candidates = unit.get("candidates", [])
        normalized.append(
            {
                "unit_id": unit.get("unit_id", f"H-{index:04d}"),
                "start_s": unit["start_s"],
                "end_s": unit["end_s"],
                "sensor_state": unit.get("state", "AMBIGUOUS"),
                "bass_pc": unit.get("bass_pc"),
                "candidates": [
                    {
                        "candidate_id": candidate["candidate_id"],
                        "pitch_class": candidate.get("pitch_class"),
                        "acoustic_score": candidate.get("acoustic_score"),
                        "residual_score": candidate.get("residual_score"),
                    }
                    for candidate in candidates
                ],
            }
        )
    return {
        "schema": SCHEMA_REQUEST,
        "analysis_id": analysis_id,
        "provider": provider,
        "authority": "ADVISORY_CANDIDATE_RANKING_ONLY",
        "scientific_d_unlocked": False,
        "units": normalized,
    }


def validate_response(request, response):
    reasons = []
    if response.get("schema") != SCHEMA_RESPONSE:
        reasons.append("BAD_SCHEMA")
    if response.get("analysis_id") != request.get("analysis_id"):
        reasons.append("ANALYSIS_ID_MISMATCH")
    if response.get("scientific_d_unlocked") is not False:
        reasons.append("SCIENTIFIC_D_MUST_REMAIN_LOCKED")

    requested = {unit["unit_id"]: unit for unit in request.get("units", [])}
    seen_units = set()
    for decision in response.get("decisions", []):
        unit_id = decision.get("unit_id")
        if unit_id not in requested:
            reasons.append(f"UNKNOWN_UNIT:{unit_id}")
            continue
        if unit_id in seen_units:
            reasons.append(f"DUPLICATE_UNIT:{unit_id}")
        seen_units.add(unit_id)
        allowed_candidates = {c["candidate_id"] for c in requested[unit_id]["candidates"]}
        for item in decision.get("candidate_decisions", []):
            candidate_id = item.get("candidate_id")
            if candidate_id not in allowed_candidates:
                reasons.append(f"INVENTED_CANDIDATE:{unit_id}:{candidate_id}")
            if item.get("action") not in ALLOWED_ACTIONS:
                reasons.append(f"BAD_ACTION:{unit_id}:{item.get('action')}")
        if decision.get("force_state") in {"LOCK", "LOCKED", "SCIENTIFIC_D"}:
            reasons.append(f"FORBIDDEN_STATE_OVERRIDE:{unit_id}")
    return {"status": "PASS" if not reasons else "FAIL", "reasons": reasons}


def deterministic_advice(request):
    """Reproduce the current deterministic Motor→reasoner→Motor fallback.

    This is explicitly not represented as a connected AI provider.
    """
    decisions = []
    for unit in request.get("units", []):
        candidates = sorted(
            unit["candidates"],
            key=lambda c: (
                c.get("residual_score") if c.get("residual_score") is not None else -1,
                c.get("acoustic_score") if c.get("acoustic_score") is not None else -1,
            ),
            reverse=True,
        )
        candidate_decisions = []
        for index, candidate in enumerate(candidates):
            residual = candidate.get("residual_score")
            acoustic = candidate.get("acoustic_score")
            score = residual if residual is not None else (acoustic or 0)
            action = "KEEP" if index < 4 and score >= 0.42 else "QUERY" if score >= 0.27 else "DROP"
            candidate_decisions.append(
                {"candidate_id": candidate["candidate_id"], "action": action, "score": score}
            )
        decisions.append(
            {
                "unit_id": unit["unit_id"],
                "candidate_decisions": candidate_decisions,
                "force_state": None,
            }
        )
    return {
        "schema": SCHEMA_RESPONSE,
        "analysis_id": request["analysis_id"],
        "provider": "DETERMINISTIC_CONTEXTUAL_REASONER_v1",
        "provider_connected": False,
        "scientific_d_unlocked": False,
        "decisions": decisions,
    }


def resolve_advice(request, *, endpoint=None, token=None, timeout_s=45):
    """Use a private provider when configured; otherwise use the declared fallback."""
    if not endpoint:
        return deterministic_advice(request)
    headers = {"Content-Type": "application/json", "X-HookLab-Contract": SCHEMA_REQUEST}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    http_request = urllib.request.Request(
        endpoint,
        data=json.dumps(request).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(http_request, timeout=timeout_s) as response:
        result = json.loads(response.read().decode("utf-8"))
    check = validate_response(request, result)
    if check["status"] != "PASS":
        raise ValueError("PRIVATE_AI_RESPONSE_REJECTED:" + ",".join(check["reasons"]))
    return result


def attach_advice(units, request, response):
    check = validate_response(request, response)
    if check["status"] != "PASS":
        raise ValueError("AI_CANDIDATE_RESPONSE_REJECTED:" + ",".join(check["reasons"]))
    output = deepcopy(units)
    by_id = {decision["unit_id"]: decision for decision in response.get("decisions", [])}
    for index, unit in enumerate(output):
        unit_id = unit.get("unit_id", f"H-{index:04d}")
        unit["ai_advice"] = by_id.get(unit_id)
        unit["raw_sensor_state_preserved"] = unit.get("state", "AMBIGUOUS")
    return output
