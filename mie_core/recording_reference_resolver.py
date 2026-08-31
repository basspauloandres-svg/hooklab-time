#!/usr/bin/env python3
"""Gate A policy-aware recording reference resolver.

This resolver separates recording identity from audio authorization. It never downloads
or processes audio itself. Downstream extraction may run only when the returned route
has audio_processing_allowed=True.

Provider policy classes are intentionally conservative. A provider can be promoted to
AUTHORIZED_PROCESSING only through explicit documented authorization, license metadata,
or a project-controlled authorization record.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

RESOLVER_VERSION = "HOOKLAB_RECORDING_REFERENCE_RESOLVER_v1.0"

# Default roles reflect documented public API terms reviewed 2026-08-30.
DEFAULT_PROVIDER_POLICY = {
    "musicbrainz": {
        "role": "IDENTITY_METADATA",
        "authorization_class": "METADATA_ONLY",
        "audio_processing_allowed": False,
        "reason": "Open recording/ISRC metadata API; no audio payload is supplied.",
    },
    "youtube_api": {
        "role": "IDENTITY_REACH_METADATA",
        "authorization_class": "AUTOMATION_PROHIBITED",
        "audio_processing_allowed": False,
        "reason": "YouTube API policies prohibit download/cache without prior written approval and prohibit audio separation routes.",
    },
    "apple_itunes_preview": {
        "role": "IDENTITY_VERSION_METADATA",
        "authorization_class": "PROMOTIONAL_STREAM_ONLY",
        "audio_processing_allowed": False,
        "reason": "Apple Search API promo-content terms restrict song previews to promotional, streamed use; analysis rights are not assumed.",
    },
    "spotify_preview": {
        "role": "IDENTITY_VERSION_METADATA",
        "authorization_class": "PREVIEW_NOT_ANALYSIS_AUTHORIZATION",
        "audio_processing_allowed": False,
        "reason": "Preview URLs are deprecated/nullable and existence of a preview is not treated as computational-analysis authorization.",
    },
    "jamendo_api": {
        "role": "RIGHTS_CLEARED_AUDIO_CANDIDATE",
        "authorization_class": "CONDITIONAL_LICENSE",
        "audio_processing_allowed": False,
        "reason": "Eligibility is per-track and use-case dependent; require explicit compatible license plus audiodownload_allowed before processing.",
    },
    "project_authorized_master": {
        "role": "AUTHORIZED_AUDIO",
        "authorization_class": "PROJECT_OR_RIGHTSHOLDER_AUTHORIZED",
        "audio_processing_allowed": False,
        "reason": "Requires an explicit authorization record and automated storage/API reference.",
    },
}


def _explicit_authorization(route: dict) -> bool:
    evidence = route.get("authorization_evidence") or {}
    return bool(evidence.get("explicit_processing_permission")) and bool(evidence.get("evidence_reference"))


def _jamendo_authorized(route: dict) -> bool:
    evidence = route.get("authorization_evidence") or {}
    return (
        bool(evidence.get("audiodownload_allowed"))
        and bool(evidence.get("license_url"))
        and bool(evidence.get("research_processing_compatible"))
    )


def evaluate_route(route: dict) -> dict:
    provider = str(route.get("provider", "")).strip().lower()
    base = dict(DEFAULT_PROVIDER_POLICY.get(provider, {
        "role": "UNCLASSIFIED",
        "authorization_class": "UNVERIFIED",
        "audio_processing_allowed": False,
        "reason": "Provider has no reviewed HookLab authorization policy.",
    }))

    allowed = False
    auth_class = base["authorization_class"]
    reason = base["reason"]

    if provider == "jamendo_api" and _jamendo_authorized(route):
        allowed = True
        auth_class = "EXPLICIT_COMPATIBLE_TRACK_LICENSE"
        reason = "Per-track download flag and compatible license evidence are present."
    elif provider == "project_authorized_master" and _explicit_authorization(route):
        allowed = True
        auth_class = "EXPLICIT_PROJECT_OR_RIGHTSHOLDER_AUTHORIZATION"
        reason = "Explicit processing authorization and evidence reference are present."
    elif _explicit_authorization(route):
        # Allows future institutional/licensed providers without changing scientific logic.
        allowed = True
        auth_class = "EXPLICIT_PROVIDER_PROCESSING_AUTHORIZATION"
        reason = "Explicit provider/contract processing authorization overrides the conservative default role."

    return {
        **route,
        "provider": provider,
        "provider_role": base["role"],
        "authorization_class": auth_class,
        "audio_processing_allowed": allowed,
        "authorization_reason": reason,
        "resolver_version": RESOLVER_VERSION,
        "resolution_timestamp": datetime.now(timezone.utc).isoformat(),
    }


def resolve(payload: dict) -> dict:
    routes = [evaluate_route(r) for r in payload.get("candidate_routes", [])]
    authorized = [r for r in routes if r["audio_processing_allowed"]]
    # Version identity is deliberately upstream/separate; resolver never promotes UNKNOWN.
    eligible = [r for r in authorized if r.get("version_identity_status") == "VERIFIED"]
    selected = eligible[0] if eligible else None
    return {
        "schema": RESOLVER_VERSION,
        "song_id": payload.get("song_id"),
        "target_title": payload.get("target_title"),
        "target_artist": payload.get("target_artist"),
        "target_version": payload.get("target_version"),
        "routes": routes,
        "selected_route": selected,
        "resolution_status": "AUTHORIZED_REFERENCE_READY" if selected else "NO_AUTHORIZED_VERIFIED_REFERENCE",
        "human_action": "NONE" if selected else "AUDIT_ONLY_IF_AUTOMATED_ROUTES_EXHAUSTED",
        "invariant": "DISCOVERY != AUTHORIZED_AUDIO_ACCESS != VERSION_IDENTITY != MELODIC_VALIDATION != SCIENTIFIC_PROMOTION",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    payload = json.loads(Path(a.input).read_text(encoding="utf-8"))
    out = resolve(payload)
    Path(a.output).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"song_id": out["song_id"], "resolution_status": out["resolution_status"]}))


if __name__ == "__main__":
    main()
