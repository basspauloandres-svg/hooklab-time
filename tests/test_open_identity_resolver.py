import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mie_core.open_identity_resolver import build_review_queue, resolve_identity_map  # noqa: E402


manifest = {
    "records": [
        {"case_id": "C001", "title": "Preserved", "artist": "Artist"},
        {"case_id": "C002", "title": "Exact Song", "artist": "Artist feat. Guest"},
        {"case_id": "C003", "title": "Ambiguous", "artist": "Artist"},
        {"case_id": "C004", "title": "Official Choice", "artist": "Artist"},
        {"case_id": "C005", "title": "Two Variants", "artist": "Artist"},
    ]
}
identity_map = {
    "records": [
        {"case_id": "C001", "video_id": "preserved01", "identity_review_status": "VERIFIED"},
        {"case_id": "C002", "video_id": None, "identity_review_status": "PENDING"},
        {"case_id": "C003", "video_id": None, "identity_review_status": "PENDING"},
        {"case_id": "C004", "video_id": None, "identity_review_status": "PENDING"},
        {"case_id": "C005", "video_id": None, "identity_review_status": "PENDING"},
    ]
}


def musicbrainz(title, artist):
    if title == "Exact Song":
        return [{"video_id": "abcdefghijk", "source": "MUSICBRAINZ", "source_record_id": "mbid"}]
    if title == "Official Choice":
        return [
            {"video_id": "official001", "source": "MUSICBRAINZ", "source_record_id": "mb1"},
            {"video_id": "topic000001", "source": "MUSICBRAINZ", "source_record_id": "mb2"},
        ]
    if title == "Two Variants":
        return [
            {"video_id": "variant0001", "source": "MUSICBRAINZ", "source_record_id": "mb3"},
            {"video_id": "variant0002", "source": "MUSICBRAINZ", "source_record_id": "mb4"},
        ]
    return []


def wikidata(title, artist):
    if title == "Ambiguous":
        return [{"video_id": "zyxwvutsrqp", "source": "WIKIDATA", "source_record_id": "Q1"}]
    return []


def youtube(title, artist):
    if title == "Exact Song":
        return [{
            "video_id": "abcdefghijk",
            "source": "YTDLP_SEARCH",
            "source_record_id": "abcdefghijk",
            "title_match": True,
        }]
    if title == "Ambiguous":
        return [{
            "video_id": "different00",
            "source": "YTDLP_SEARCH",
            "source_record_id": "different00",
            "title_match": True,
        }]
    return []


def oembed(video_id, title, artist):
    if video_id == "abcdefghijk":
        return {
            "video_id": video_id,
            "source": "YOUTUBE_OEMBED",
            "source_record_id": video_id,
            "title_match": True,
            "artist_match": True,
        }
    if video_id == "zyxwvutsrqp":
        return None
    if video_id == "official001":
        return {"video_id": video_id, "source": "YOUTUBE_OEMBED", "title": "Artist - Official Choice (Official Music Video)", "title_match": True, "artist_match": True}
    if video_id == "topic000001":
        return {"video_id": video_id, "source": "YOUTUBE_OEMBED", "title": "Official Choice", "author_name": "Artist - Topic", "title_match": True, "artist_match": True}
    if video_id == "variant0001":
        return {"video_id": video_id, "source": "YOUTUBE_OEMBED", "title": "Artist - Two Variants (Live)", "title_match": True, "artist_match": True}
    if video_id == "variant0002":
        return {"video_id": video_id, "source": "YOUTUBE_OEMBED", "title": "Artist - Two Variants (Remix)", "title_match": True, "artist_match": True}
    return None


updated, audit = resolve_identity_map(manifest, identity_map, musicbrainz, wikidata, oembed, youtube)
by_id = {row["case_id"]: row for row in updated["records"]}
assert by_id["C001"]["video_id"] == "preserved01"
assert by_id["C002"]["video_id"] == "abcdefghijk"
assert by_id["C002"]["identity_verification_method"] == "AUTOMATED_CROSS_SOURCE_V1"
assert by_id["C003"]["identity_review_status"] == "PENDING"
assert by_id["C004"]["video_id"] == "official001"
assert by_id["C004"]["identity_review_status"] == "VERIFIED"
assert by_id["C005"]["identity_review_status"] == "PENDING"
assert audit["previously_verified_preserved"] == 1
assert audit["auto_verified_this_run"] == 2
assert audit["automatic_single_source_promotion"] is False
assert audit["scientific_d_unlocked"] is False

youtube_calls = []
empty_map = {"records": [{"case_id": "C006", "video_id": None, "identity_review_status": "PENDING"}]}
empty_manifest = {"records": [{"case_id": "C006", "title": "No Anchor", "artist": "Artist"}]}
_, empty_audit = resolve_identity_map(
    empty_manifest,
    empty_map,
    lambda title, artist: [],
    lambda title, artist: [],
    lambda video_id, title, artist: None,
    lambda title, artist: youtube_calls.append((title, artist)) or [],
)
assert youtube_calls == [("No Anchor", "Artist")]
assert empty_audit["resolutions"][0]["provider_status"]["YTDLP_SEARCH"] == "COMPLETE_DISCOVERY_ONLY_NO_INDEPENDENT_ID_ANCHOR"
assert empty_audit["resolutions"][0]["provider_status"]["YOUTUBE_OEMBED"] == "SKIPPED_NO_INDEPENDENT_ID_ANCHOR"

discovery_map = {"records": [{"case_id": "C007", "video_id": None, "identity_review_status": "PENDING"}]}
discovery_manifest = {"records": [{"case_id": "C007", "title": "Discovery", "artist": "Artist"}]}
discovery_updated, discovery_audit = resolve_identity_map(
    discovery_manifest,
    discovery_map,
    lambda title, artist: [],
    lambda title, artist: [],
    lambda video_id, title, artist: None,
    lambda title, artist: [{
        "video_id": "discovery01",
        "source": "YTDLP_SEARCH",
        "source_record_id": "discovery01",
        "source_url": "https://www.youtube.com/watch?v=discovery01",
        "title": "Discovery (Official Music Video)",
        "title_match": True,
    }],
)
assert discovery_updated["records"][0]["identity_review_status"] == "PENDING"
assert discovery_audit["auto_verified_this_run"] == 0
discovery_resolution = discovery_audit["resolutions"][0]
assert discovery_resolution["resolution_status"] == "IDENTITY_REVIEW_PENDING"
assert discovery_resolution["candidates"][0]["independent_sources"] == ["YTDLP_SEARCH"]

review_queue = build_review_queue(discovery_audit)
assert review_queue["schema"] == "HOOKLAB_OPEN_IDENTITY_REVIEW_QUEUE_v1"
assert review_queue["unresolved_count"] == 1
assert review_queue["records"][0]["case_id"] == "C007"
assert review_queue["records"][0]["popularity_based_selection_forbidden"] is True
assert review_queue["records"][0]["single_source_promotion_forbidden"] is True
assert review_queue["automatic_single_source_promotion"] is False
assert review_queue["scientific_d_unlocked"] is False
assert "VIEW_COUNT" in review_queue["forbidden_selection_inputs"]

resolved_only = dict(discovery_audit)
resolved_only["resolutions"] = [{"case_id": "C008", "resolution_status": "AUTO_VERIFIED_CROSS_SOURCE"}]
assert build_review_queue(resolved_only)["records"] == []

print("OPEN_IDENTITY_RESOLVER_PASS")
