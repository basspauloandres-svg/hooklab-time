"""Fail-closed frozen-reference binding for MIE v0.3.5 M-only experiments.

This module does not run audio models. It verifies that candidate H/T layers are
bound to predeclared immutable hashes rather than to objects created inside the
same execution. This closes the historical-reference defect registered on
2026-09-13.
"""

from __future__ import annotations

import hashlib
import json
import re


SCHEMA = "HOOKLAB_MIE_FROZEN_REFERENCE_BINDING_v1"
PASS = "FROZEN_REFERENCE_BINDING_PASS"
MISSING = "AUDIT_FROZEN_REFERENCE_BINDING_MISSING"
SOURCE_MISMATCH = "AUDIT_FROZEN_REFERENCE_SOURCE_MISMATCH"
H_CHANGED = "AUDIT_ONE_MODULE_RULE_VIOLATION_H_CHANGED"
T_CHANGED = "NO_PROMOTION_TACTUS_REGRESSION"

_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def canonical_sha256(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_reference_manifest(manifest):
    manifest = dict(manifest or {})
    reasons = []
    if manifest.get("schema") != "HOOKLAB_MIE_FROZEN_REFERENCE_MANIFEST_v1":
        reasons.append("BAD_SCHEMA")
    for key in ("source_sha256", "harmony_reference_sha256", "tactus_reference_sha256"):
        value = manifest.get(key)
        if not isinstance(value, str) or not _SHA256.fullmatch(value):
            reasons.append(f"INVALID_{key.upper()}")
    if not manifest.get("reference_artifact"):
        reasons.append("REFERENCE_ARTIFACT_REQUIRED")
    if not manifest.get("reference_commit"):
        reasons.append("REFERENCE_COMMIT_REQUIRED")
    if manifest.get("changed_module") != "M_ONLY":
        reasons.append("CHANGED_MODULE_MUST_BE_M_ONLY")
    return {"status": "PASS" if not reasons else "FAIL", "reasons": reasons}


def audit_candidate_against_frozen_reference(
    *,
    manifest,
    source_sha256,
    harmony_candidate,
    tactus_candidate,
):
    """Compare candidate H/T against immutable predeclared hashes.

    The reference layers themselves are intentionally not accepted as function
    inputs. Their hashes must originate in a manifest created before candidate
    execution. This prevents within-run self-comparison from satisfying the
    M-only rule.
    """
    check = validate_reference_manifest(manifest)
    h_candidate_hash = canonical_sha256(harmony_candidate)
    t_candidate_hash = canonical_sha256(tactus_candidate)
    base = {
        "schema": SCHEMA,
        "changed_module": "M_ONLY",
        "source_sha256": source_sha256,
        "harmony_candidate_sha256": h_candidate_hash,
        "tactus_candidate_sha256": t_candidate_hash,
        "harmony_predeclared_reference_sha256": (manifest or {}).get("harmony_reference_sha256"),
        "tactus_predeclared_reference_sha256": (manifest or {}).get("tactus_reference_sha256"),
        "reference_artifact": (manifest or {}).get("reference_artifact"),
        "reference_commit": (manifest or {}).get("reference_commit"),
        "generation_class": "D0_EXPLORATORY",
        "scientific_d_unlocked": False,
        "baseline_promoted": False,
    }
    if check["status"] != "PASS":
        return dict(base, status=MISSING, reasons=check["reasons"], harmony_byte_equivalent=False, tactus_byte_equivalent=False)
    if source_sha256 != manifest["source_sha256"]:
        return dict(base, status=SOURCE_MISMATCH, reasons=["SOURCE_HASH_MUST_MATCH_PREDECLARED_REFERENCE"], harmony_byte_equivalent=False, tactus_byte_equivalent=False)

    h_fixed = h_candidate_hash == manifest["harmony_reference_sha256"]
    t_fixed = t_candidate_hash == manifest["tactus_reference_sha256"]
    if not h_fixed:
        status = H_CHANGED
    elif not t_fixed:
        status = T_CHANGED
    else:
        status = PASS
    return dict(
        base,
        status=status,
        reasons=[],
        harmony_byte_equivalent=h_fixed,
        tactus_byte_equivalent=t_fixed,
    )
