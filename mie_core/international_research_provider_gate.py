#!/usr/bin/env python3
"""Classify symbolic research providers without conflating license with target-population fit."""
from __future__ import annotations

ALLOWED_LICENSE_STATES={"LICENSED_OPEN","RESEARCH_AUTHORIZED","NONCOMMERCIAL_RESEARCH_AUTHORIZED"}

def evaluate(provider):
    reasons=[]
    license_state=provider.get("license_state")
    if license_state not in ALLOWED_LICENSE_STATES:
        reasons.append("LICENSE_OR_RESEARCH_PERMISSION_NOT_SUFFICIENT")
    if provider.get("computational_processing_explicit") is not True:
        reasons.append("COMPUTATIONAL_PROCESSING_NOT_EXPLICIT")
    if provider.get("provenance_available") is not True:
        reasons.append("PROVENANCE_NOT_AVAILABLE")
    research_admissible=not reasons
    target_status=provider.get("target_population_status","UNKNOWN")
    return {
        "provider_id":provider.get("provider_id"),
        "research_admissible":research_admissible,
        "provider_gate":"PASS" if research_admissible else "AUDIT",
        "target_population_status":target_status,
        "scientific_row_eligible":research_admissible and target_status=="QUALIFIED_TARGET_MATCH",
        "blocking_reasons":reasons,
        "invariants":["provider admissible != target population match","dataset available != scientific population"]
    }
