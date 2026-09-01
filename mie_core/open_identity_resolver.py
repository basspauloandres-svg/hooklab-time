"""Fail-closed cross-source YouTube identity resolver for HookLab.

Public identifiers are gathered from MusicBrainz, Wikidata and yt-dlp search.
An identity is promoted only when at least two independent providers agree on
one video ID and no competing video reaches the same evidence threshold.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable


RESOLVER_VERSION = "hooklab-open-identity-resolver-v1"
USER_AGENT = "HookLabResearchPrototype/1.0 (https://github.com/basspauloandres-svg/hooklab-time)"
VIDEO_ID_RE = re.compile(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|shorts/|embed/))([A-Za-z0-9_-]{11})")
PLAIN_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
SOURCE_NAMES = {"MUSICBRAINZ", "WIKIDATA", "YTDLP_SEARCH"}


class IdentityResolverError(RuntimeError):
    pass


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(payload)
        temporary = Path(handle.name)
    temporary.replace(path)


def _normalize(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char)).lower()
    text = re.sub(r"\b(official|music|video|audio|lyrics?|lyric|remaster(?:ed)?|hd|4k)\b", " ", text)
    return " ".join(re.findall(r"[a-z0-9]+", text))


def _primary_artist(value: Any) -> str:
    text = str(value or "")
    return re.split(r"\s+(?:ft\.?|feat\.?|featuring|x|&|and)\s+", text, maxsplit=1, flags=re.I)[0].strip()


def _youtube_id(value: Any) -> str | None:
    text = str(value or "").strip()
    if PLAIN_VIDEO_ID_RE.fullmatch(text):
        return text
    match = VIDEO_ID_RE.search(text)
    return match.group(1) if match else None


def _http_json(url: str, attempts: int = 3) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            if error.code in {429, 500, 502, 503, 504} and attempt + 1 < attempts:
                time.sleep(2 ** attempt)
                continue
            raise IdentityResolverError(f"OPEN_PROVIDER_HTTP_{error.code}") from error
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            if attempt + 1 < attempts:
                time.sleep(2 ** attempt)
                continue
            raise IdentityResolverError(f"OPEN_PROVIDER_FAILED_{type(error).__name__}") from error
    raise IdentityResolverError("OPEN_PROVIDER_RETRY_EXHAUSTED")


def musicbrainz_candidates(title: str, artist: str) -> list[dict[str, Any]]:
    query = f'recording:"{title}" AND artist:"{_primary_artist(artist)}"'
    url = "https://musicbrainz.org/ws/2/recording/?" + urllib.parse.urlencode({
        "query": query,
        "fmt": "json",
        "limit": 5,
    })
    search = _http_json(url)
    time.sleep(1.05)
    matched = []
    for recording in search.get("recordings", []):
        if _normalize(recording.get("title")) != _normalize(title):
            continue
        credits = " ".join(
            str(credit.get("name") or (credit.get("artist") or {}).get("name") or "")
            for credit in recording.get("artist-credit", [])
        )
        if _normalize(_primary_artist(artist)) not in _normalize(credits):
            continue
        mbid = recording.get("id")
        if not mbid:
            continue
        detail_url = f"https://musicbrainz.org/ws/2/recording/{mbid}?" + urllib.parse.urlencode({
            "inc": "url-rels+artist-credits",
            "fmt": "json",
        })
        detail = _http_json(detail_url)
        time.sleep(1.05)
        for relation in detail.get("relations", []):
            resource = (relation.get("url") or {}).get("resource")
            video_id = _youtube_id(resource)
            if video_id:
                matched.append({
                    "video_id": video_id,
                    "source": "MUSICBRAINZ",
                    "source_record_id": mbid,
                    "source_url": f"https://musicbrainz.org/recording/{mbid}",
                    "title": recording.get("title"),
                    "artist": credits,
                })
        if matched:
            break
    return matched


def wikidata_candidates(title: str, artist: str) -> list[dict[str, Any]]:
    search_url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({
        "action": "wbsearchentities",
        "search": f"{title} {_primary_artist(artist)}",
        "language": "en",
        "uselang": "en",
        "type": "item",
        "limit": 7,
        "format": "json",
        "origin": "*",
    })
    search = _http_json(search_url)
    ids = [item.get("id") for item in search.get("search", []) if item.get("id")]
    if not ids:
        return []
    entity_url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({
        "action": "wbgetentities",
        "ids": "|".join(ids),
        "props": "labels|descriptions|claims",
        "languages": "en|es",
        "format": "json",
        "origin": "*",
    })
    entities = _http_json(entity_url).get("entities", {})
    matched = []
    for entity_id, entity in entities.items():
        labels = entity.get("labels") or {}
        label = (labels.get("en") or labels.get("es") or {}).get("value")
        if _normalize(label) != _normalize(title):
            continue
        claims = (entity.get("claims") or {}).get("P1651", [])
        for claim in claims:
            value = (((claim.get("mainsnak") or {}).get("datavalue") or {}).get("value"))
            video_id = _youtube_id(value)
            if video_id:
                matched.append({
                    "video_id": video_id,
                    "source": "WIKIDATA",
                    "source_record_id": entity_id,
                    "source_url": f"https://www.wikidata.org/wiki/{entity_id}",
                    "title": label,
                    "description": ((entity.get("descriptions") or {}).get("en") or {}).get("value"),
                })
    return matched


def _yt_dlp_search_session() -> tuple[Callable[[str, str], list[dict[str, Any]]], str]:
    try:
        import yt_dlp
    except ImportError as error:
        raise IdentityResolverError("YT_DLP_NOT_INSTALLED") from error
    client = yt_dlp.YoutubeDL({
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": "in_playlist",
        "playlistend": 5,
        "cachedir": False,
        "socket_timeout": 30,
        "retries": 2,
    })

    def search(title: str, artist: str) -> list[dict[str, Any]]:
        query = f"{title} {artist} official music video"
        result = client.extract_info(f"ytsearch5:{query}", download=False)
        candidates = []
        for rank, entry in enumerate(result.get("entries") or [], start=1):
            video_id = _youtube_id(entry.get("id") or entry.get("url"))
            if not video_id:
                continue
            candidate_title = entry.get("title")
            title_match = _normalize(title) in _normalize(candidate_title)
            candidates.append({
                "video_id": video_id,
                "source": "YTDLP_SEARCH",
                "source_record_id": video_id,
                "source_url": f"https://www.youtube.com/watch?v={video_id}",
                "rank": rank,
                "title": candidate_title,
                "channel": entry.get("channel") or entry.get("uploader"),
                "title_match": title_match,
            })
        return candidates

    return search, yt_dlp.version.__version__


def resolve_case(
    case: dict[str, Any],
    musicbrainz: Callable[[str, str], list[dict[str, Any]]],
    wikidata: Callable[[str, str], list[dict[str, Any]]],
    youtube_search: Callable[[str, str], list[dict[str, Any]]],
) -> dict[str, Any]:
    title, artist = str(case.get("title") or ""), str(case.get("artist") or "")
    evidence = []
    provider_status = {}
    for name, provider in (("MUSICBRAINZ", musicbrainz), ("WIKIDATA", wikidata), ("YTDLP_SEARCH", youtube_search)):
        try:
            rows = provider(title, artist)
            provider_status[name] = "COMPLETE"
            evidence.extend(row for row in rows if row.get("source") == name and _youtube_id(row.get("video_id")))
        except Exception as error:
            provider_status[name] = f"FAILED_{type(error).__name__}"

    by_id: dict[str, dict[str, Any]] = {}
    for row in evidence:
        video_id = _youtube_id(row.get("video_id"))
        if not video_id:
            continue
        bucket = by_id.setdefault(video_id, {"video_id": video_id, "sources": set(), "evidence": []})
        bucket["sources"].add(row["source"])
        bucket["evidence"].append(row)

    eligible = []
    for video_id, bucket in by_id.items():
        sources = bucket["sources"] & SOURCE_NAMES
        yt_rows = [row for row in bucket["evidence"] if row["source"] == "YTDLP_SEARCH"]
        title_supported = any(row.get("title_match") for row in yt_rows) or {
            "MUSICBRAINZ", "WIKIDATA"
        }.issubset(sources)
        if len(sources) >= 2 and title_supported:
            eligible.append(video_id)

    selected = eligible[0] if len(eligible) == 1 else None
    compact_candidates = []
    for video_id, bucket in sorted(by_id.items()):
        compact_candidates.append({
            "video_id": video_id,
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
            "independent_sources": sorted(bucket["sources"]),
            "source_count": len(bucket["sources"]),
            "evidence": bucket["evidence"],
        })
    return {
        "case_id": case.get("case_id"),
        "title": title,
        "artist": artist,
        "provider_status": provider_status,
        "candidates": compact_candidates,
        "resolution_status": "AUTO_VERIFIED_CROSS_SOURCE" if selected else (
            "AUDIT_AMBIGUOUS_CROSS_SOURCE" if len(eligible) > 1 else "IDENTITY_REVIEW_PENDING"
        ),
        "selected_video_id": selected,
        "scientific_d_unlocked": False,
    }


def resolve_identity_map(
    case_manifest: dict[str, Any],
    identity_map: dict[str, Any],
    musicbrainz: Callable[[str, str], list[dict[str, Any]]],
    wikidata: Callable[[str, str], list[dict[str, Any]]],
    youtube_search: Callable[[str, str], list[dict[str, Any]]],
    provider_versions: dict[str, str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    cases = {row.get("case_id"): row for row in case_manifest.get("records", [])}
    resolutions = []
    auto_verified = 0
    for row in identity_map.get("records", []):
        if row.get("identity_review_status") == "VERIFIED" and row.get("video_id"):
            continue
        case = cases.get(row.get("case_id"), row)
        resolution = resolve_case(case, musicbrainz, wikidata, youtube_search)
        resolutions.append(resolution)
        selected = resolution.get("selected_video_id")
        if selected:
            row.update({
                "video_id": selected,
                "video_url": f"https://www.youtube.com/watch?v={selected}",
                "artifact_role": "DOCUMENTED_PUBLIC_MUSIC_VIDEO",
                "identity_review_status": "VERIFIED",
                "identity_verification_method": "AUTOMATED_CROSS_SOURCE_V1",
                "identity_evidence": [
                    f"Independent provider agreement: {', '.join(candidate['independent_sources'])}"
                    for candidate in resolution["candidates"] if candidate["video_id"] == selected
                ],
            })
            auto_verified += 1

    verified = sum(
        row.get("identity_review_status") == "VERIFIED" and bool(row.get("video_id"))
        for row in identity_map.get("records", [])
    )
    total = len(identity_map.get("records", []))
    identity_map["status"] = f"PARTIAL_IDENTITY_REVIEW_{verified}_OF_{total}" if verified < total else "IDENTITY_REVIEW_COMPLETE"
    identity_map["updated_at"] = _utc_now()
    identity_map["identity_resolver_version"] = RESOLVER_VERSION
    identity_map["scientific_d_unlocked"] = False
    audit = {
        "schema": "HOOKLAB_OPEN_IDENTITY_RESOLUTION_AUDIT_v1",
        "created_at": _utc_now(),
        "resolver_version": RESOLVER_VERSION,
        "provider_versions": provider_versions or {},
        "promotion_rule": "EXACTLY_ONE_VIDEO_ID_SUPPORTED_BY_AT_LEAST_TWO_INDEPENDENT_PROVIDERS",
        "previously_verified_preserved": verified - auto_verified,
        "auto_verified_this_run": auto_verified,
        "verified_after_run": verified,
        "total_cases": total,
        "resolutions": resolutions,
        "automatic_single_source_promotion": False,
        "scientific_d_unlocked": False,
    }
    return identity_map, audit


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="HookLab open cross-source identity resolver")
    parser.add_argument("--case-manifest", required=True, type=Path)
    parser.add_argument("--identity-map", required=True, type=Path)
    parser.add_argument("--audit-output", required=True, type=Path)
    args = parser.parse_args()
    youtube_search, yt_dlp_version = _yt_dlp_search_session()
    updated, audit = resolve_identity_map(
        _load(args.case_manifest),
        _load(args.identity_map),
        musicbrainz_candidates,
        wikidata_candidates,
        youtube_search,
        {"yt-dlp": yt_dlp_version, "MusicBrainz": "WS2", "Wikidata": "Action API"},
    )
    _atomic_json(args.identity_map, updated)
    _atomic_json(args.audit_output, audit)
    print(json.dumps({
        "auto_verified_this_run": audit["auto_verified_this_run"],
        "verified_after_run": audit["verified_after_run"],
        "total_cases": audit["total_cases"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
