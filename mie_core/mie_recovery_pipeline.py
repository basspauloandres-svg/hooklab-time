"""Recovery helpers that adapt the preserved MIE Core v0.2 report to v0.3."""

from __future__ import annotations

from mie_core.mie_ai_candidate_reasoner import attach_advice, build_request, resolve_advice


def harmonic_candidates(units):
    output = []
    for index, source in enumerate(units):
        unit = dict(source)
        root = int(unit.get("root_pc", 0))
        intervals = unit.get("intervals") or []
        evidence = float(unit.get("evidence", 0.0))
        margin = float(unit.get("margin", 0.0))
        unit["unit_id"] = unit.get("unit_id", f"H-{index:04d}")
        unit["candidates"] = [
            {
                "candidate_id": f"{unit['unit_id']}:PC{(root + int(interval)) % 12}",
                "pitch_class": (root + int(interval)) % 12,
                "acoustic_score": evidence,
                "residual_score": max(0.0, evidence - max(0.0, 0.035 - margin)),
            }
            for interval in intervals
        ]
        output.append(unit)
    return output


def apply_reasoning(raw_report, *, analysis_id, endpoint=None, token=None):
    report = dict(raw_report)
    units = harmonic_candidates(report.get("harmony", []))
    request = build_request(units, analysis_id=analysis_id)
    response = resolve_advice(request, endpoint=endpoint, token=token)
    report["harmony"] = attach_advice(units, request, response)
    report["ai_provenance"] = {
        "provider": response.get("provider"),
        "provider_connected": response.get("provider_connected", bool(endpoint)),
        "authority": "ADVISORY_CANDIDATE_RANKING_ONLY",
        "request_schema": request["schema"],
        "response_schema": response["schema"],
    }
    return report

