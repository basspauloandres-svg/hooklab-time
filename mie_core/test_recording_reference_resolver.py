from recording_reference_resolver import resolve


def test_metadata_and_restricted_routes_do_not_become_audio_sources():
    out = resolve({
        "song_id": "x",
        "candidate_routes": [
            {"provider": "musicbrainz", "version_identity_status": "VERIFIED"},
            {"provider": "youtube_api", "version_identity_status": "VERIFIED"},
            {"provider": "apple_itunes_preview", "version_identity_status": "VERIFIED"},
            {"provider": "spotify_preview", "version_identity_status": "VERIFIED"},
        ],
    })
    assert out["selected_route"] is None
    assert out["resolution_status"] == "NO_AUTHORIZED_VERIFIED_REFERENCE"
    assert all(not r["audio_processing_allowed"] for r in out["routes"])


def test_explicit_project_authorization_is_eligible_only_after_version_verification():
    base = {
        "provider": "project_authorized_master",
        "authorization_evidence": {
            "explicit_processing_permission": True,
            "evidence_reference": "contract://fixture",
        },
    }
    out_pending = resolve({"song_id": "x", "candidate_routes": [{**base, "version_identity_status": "PENDING"}]})
    assert out_pending["selected_route"] is None
    out_verified = resolve({"song_id": "x", "candidate_routes": [{**base, "version_identity_status": "VERIFIED"}]})
    assert out_verified["resolution_status"] == "AUTHORIZED_REFERENCE_READY"
    assert out_verified["selected_route"]["audio_processing_allowed"] is True


def test_jamendo_requires_track_level_license_evidence():
    denied = resolve({"song_id": "x", "candidate_routes": [{"provider": "jamendo_api", "version_identity_status": "VERIFIED"}]})
    assert denied["selected_route"] is None
    allowed = resolve({
        "song_id": "x",
        "candidate_routes": [{
            "provider": "jamendo_api",
            "version_identity_status": "VERIFIED",
            "authorization_evidence": {
                "audiodownload_allowed": True,
                "license_url": "https://license.example/fixture",
                "research_processing_compatible": True,
            },
        }],
    })
    assert allowed["resolution_status"] == "AUTHORIZED_REFERENCE_READY"
