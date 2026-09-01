import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mie_core.youtube_public_metrics_collector import (  # noqa: E402
    _duration_seconds,
    collect_snapshots,
    initialize_map,
)


assert _duration_seconds("PT4M12S") == 252
assert _duration_seconds("PT1H2M3S") == 3723
manifest = {"manifest_id": "TEST", "records": [{"case_id": "C001", "title": "Song", "artist": "Artist"}]}
identity_map = initialize_map(manifest)
assert identity_map["records"][0]["identity_review_status"] == "PENDING"
assert identity_map["scientific_d_unlocked"] is False

identity_map["records"][0].update({"video_id": "abcdefghijk", "identity_review_status": "VERIFIED"})


def fake_request(endpoint, params, key):
    assert key == "TEST_KEY"
    assert endpoint == "videos"
    return {
        "items": [{
            "id": "abcdefghijk",
            "etag": "test-etag",
            "snippet": {
                "title": "Official Song",
                "channelId": "UC-test",
                "channelTitle": "Official Artist",
                "publishedAt": "2020-01-01T00:00:00Z",
                "categoryId": "10",
            },
            "contentDetails": {"duration": "PT4M12S"},
            "statistics": {"viewCount": "123456", "likeCount": "789", "commentCount": "42"},
            "status": {"privacyStatus": "public", "embeddable": True},
        }]
    }


snapshot = collect_snapshots(identity_map, "TEST_KEY", fake_request)
assert snapshot["status"] == "PUBLIC_METRIC_SNAPSHOT_COMPLETE"
assert snapshot["records"][0]["view_count"] == 123456
assert snapshot["records"][0]["duration_seconds"] == 252
assert snapshot["scientific_d_unlocked"] is False
assert snapshot["interpretation"] == "TIMESTAMPED_PUBLIC_SNAPSHOT_NOT_TRAFFIC_PEAK_OR_CAUSAL_EFFECT"

print("YOUTUBE_PUBLIC_METRICS_COLLECTOR_PASS")
