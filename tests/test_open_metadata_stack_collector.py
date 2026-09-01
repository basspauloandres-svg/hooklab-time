import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mie_core.open_metadata_stack_collector import (  # noqa: E402
    collect_verified_snapshot,
    discover_candidates,
    snapshot_filename,
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

print("OPEN_METADATA_STACK_COLLECTOR_PASS")
