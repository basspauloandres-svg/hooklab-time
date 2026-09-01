import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mie_core.open_identity_resolver import resolve_identity_map  # noqa: E402


manifest = {
    "records": [
        {"case_id": "C001", "title": "Preserved", "artist": "Artist"},
        {"case_id": "C002", "title": "Exact Song", "artist": "Artist feat. Guest"},
        {"case_id": "C003", "title": "Ambiguous", "artist": "Artist"},
    ]
}
identity_map = {
    "records": [
        {"case_id": "C001", "video_id": "preserved01", "identity_review_status": "VERIFIED"},
        {"case_id": "C002", "video_id": None, "identity_review_status": "PENDING"},
        {"case_id": "C003", "video_id": None, "identity_review_status": "PENDING"},
    ]
}


def musicbrainz(title, artist):
    if title == "Exact Song":
        return [{"video_id": "abcdefghijk", "source": "MUSICBRAINZ", "source_record_id": "mbid"}]
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


updated, audit = resolve_identity_map(manifest, identity_map, musicbrainz, wikidata, youtube)
by_id = {row["case_id"]: row for row in updated["records"]}
assert by_id["C001"]["video_id"] == "preserved01"
assert by_id["C002"]["video_id"] == "abcdefghijk"
assert by_id["C002"]["identity_verification_method"] == "AUTOMATED_CROSS_SOURCE_V1"
assert by_id["C003"]["identity_review_status"] == "PENDING"
assert audit["previously_verified_preserved"] == 1
assert audit["auto_verified_this_run"] == 1
assert audit["automatic_single_source_promotion"] is False
assert audit["scientific_d_unlocked"] is False

print("OPEN_IDENTITY_RESOLVER_PASS")
