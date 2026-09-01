import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mie_core.open_metadata_stack_collector import (  # noqa: E402
    RYD_CACHE_POLICY,
    RYD_DATA_LINEAGE,
    RYD_PROVIDER,
    collect_verified_snapshot,
    discover_candidates,
    snapshot_filename,
    _whitelisted_ryd_metrics,
)


def fake_extractor(url):
    if url.startswith("ytsearch"):
        return {"entries": [{
            "id": "abcdefghijk",
            "title": "Song (Official Video)",
            "channel_id": "UC-test",
            "channel": "Artist",
            "duration": 210,
            "view_count": 1000,
        }]}
    return {
        "id": "abcdefghijk",
        "title": "Song (Official Video)",
        "channel_id": "UC-test",
        "channel": "Artist",
        "channel_is_verified": True,
        "upload_date": "20200101",
        "duration": 210,
        "view_count": 1234,
        "like_count": 100,
        "comment_count": 20,
        "availability": "public",
        "description": "This field must never be persisted",
    }


manifest = {"records": [{"case_id": "C001", "title": "Song", "artist": "Artist"}]}
candidates = discover_candidates(manifest, fake_extractor, "TEST")
assert candidates["automatic_identity_selection"] is False
assert candidates["downloads_media"] is False
assert candidates["scientific_d_unlocked"] is False
assert candidates["records"][0]["identity_promotion"] == "FORBIDDEN_AUTOMATICALLY"
assert candidates["records"][0]["candidates"][0]["video_id"] == "abcdefghijk"

identity_map = {
    "records": [
        {"case_id": "C001", "video_id": "abcdefghijk", "identity_review_status": "VERIFIED"},
        {"case_id": "C002", "video_id": "pending0000", "identity_review_status": "PENDING"},
    ]
}
snapshot = collect_verified_snapshot(identity_map, fake_extractor, "TEST", "2026-09-01T12:34:56Z")
assert snapshot["verified_identity_count"] == 1
assert snapshot["complete_snapshot_count"] == 1
assert snapshot["records"][0]["view_count"] == 1234
assert "description" not in snapshot["records"][0]
assert snapshot["downloads_media"] is False
assert snapshot["generation_class"] == "D0_EXPLORATORY"
assert snapshot["scientific_d_unlocked"] is False
assert snapshot_filename("2026-09-01T12:34:56Z") == "youtube_public_snapshot_20260901123456Z.json"


def fake_ryd(video_id):
    assert video_id == "abcdefghijk"
    return {
        "id": video_id,
        "dateCreated": "2026-08-30T00:00:00Z",
        "likes": 101,
        "rawLikes": 7,
        "rawDislikes": 3,
        "dislikes": 999,
        "rating": 1.5,
        "viewCount": 2345,
        "deleted": False,
    }


ryd_snapshot = collect_verified_snapshot(
    identity_map,
    fake_ryd,
    "TEST-RYD",
    "2026-09-01T12:34:56Z",
    provider=RYD_PROVIDER,
    metadata_adapter=_whitelisted_ryd_metrics,
    provider_cache_policy=RYD_CACHE_POLICY,
    provider_data_lineage=RYD_DATA_LINEAGE,
)
ryd_row = ryd_snapshot["records"][0]
assert ryd_snapshot["complete_snapshot_count"] == 1
assert ryd_row["view_count"] == 2345
assert ryd_row["like_count"] == 101
assert ryd_row["provider_record_created_at"] == "2026-08-30T00:00:00Z"
assert ryd_snapshot["provider_cache_policy"] == RYD_CACHE_POLICY
assert ryd_snapshot["retained_metric_fields"] == ["view_count", "like_count"]
for forbidden in ryd_snapshot["explicitly_forbidden_provider_fields"]:
    assert forbidden not in ryd_row


deleted_snapshot = collect_verified_snapshot(
    identity_map,
    lambda video_id: {"id": video_id, "viewCount": 10, "likes": 1, "deleted": True},
    "TEST-RYD",
    "2026-09-01T12:34:56Z",
    provider=RYD_PROVIDER,
    metadata_adapter=_whitelisted_ryd_metrics,
)
assert deleted_snapshot["records"][0]["snapshot_status"] == "AUDIT_PUBLIC_METRICS_NOT_VALID"

print("OPEN_METADATA_STACK_COLLECTOR_PASS")
