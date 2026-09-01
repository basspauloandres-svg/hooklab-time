"""YouTube public identity and metric collector for HookLab.

Uses the official YouTube Data API v3 with a private local API key. The key is
read from HOOKLAB_YOUTUBE_API_KEY, never serialized, and never printed.
Search results remain candidates until documentary identity review.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable, Iterable


COLLECTOR_VERSION = "hooklab-youtube-public-metrics-collector-v0.1"
API_ROOT = "https://www.googleapis.com/youtube/v3"
KEY_ENV = "HOOKLAB_YOUTUBE_API_KEY"
DEFAULT_SEARCH_INTERVAL_SECONDS = 3.2
DEFAULT_RATE_LIMIT_RETRY_SECONDS = 65.0
MAX_RATE_LIMIT_ATTEMPTS = 4


class CollectorError(RuntimeError):
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


def _api_key() -> str:
    key = os.environ.get(KEY_ENV, "").strip()
    if not key:
        raise CollectorError(f"{KEY_ENV}_REQUIRED")
    return key


def _request(
    endpoint: str,
    params: dict[str, Any],
    key: str,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    query = urllib.parse.urlencode({**params, "key": key})
    request = urllib.request.Request(
        f"{API_ROOT}/{endpoint}?{query}",
        headers={"Accept": "application/json", "User-Agent": COLLECTOR_VERSION},
    )
    for attempt in range(1, MAX_RATE_LIMIT_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")[:1000]
            if error.code == 429 and attempt < MAX_RATE_LIMIT_ATTEMPTS:
                retry_after = error.headers.get("Retry-After") if error.headers else None
                try:
                    delay = max(float(retry_after), 1.0) if retry_after else DEFAULT_RATE_LIMIT_RETRY_SECONDS
                except ValueError:
                    delay = DEFAULT_RATE_LIMIT_RETRY_SECONDS
                sleep(delay)
                continue
            raise CollectorError(f"YOUTUBE_API_HTTP_{error.code}:{body}") from error
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            raise CollectorError(f"YOUTUBE_API_REQUEST_FAILED:{type(error).__name__}") from error
    raise CollectorError("YOUTUBE_API_RATE_LIMIT_RETRY_EXHAUSTED")


def _chunks(values: list[str], size: int = 50) -> Iterable[list[str]]:
    for start in range(0, len(values), size):
        yield values[start : start + size]


def _duration_seconds(value: str | None) -> int | None:
    if not value:
        return None
    match = re.fullmatch(r"P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value)
    if not match:
        return None
    days, hours, minutes, seconds = (int(part or 0) for part in match.groups())
    return days * 86400 + hours * 3600 + minutes * 60 + seconds


def _integer(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _details(video_ids: list[str], key: str, request: Callable = _request) -> dict[str, dict[str, Any]]:
    details: dict[str, dict[str, Any]] = {}
    for batch in _chunks(video_ids):
        response = request(
            "videos",
            {
                "part": "snippet,contentDetails,statistics,status",
                "id": ",".join(batch),
                "fields": "items(id,etag,snippet(title,channelId,channelTitle,publishedAt,categoryId),contentDetails(duration),statistics(viewCount,likeCount,commentCount),status(privacyStatus,embeddable))",
            },
            key,
        )
        for item in response.get("items", []):
            snippet = item.get("snippet") or {}
            content = item.get("contentDetails") or {}
            stats = item.get("statistics") or {}
            status = item.get("status") or {}
            video_id = item.get("id")
            if not video_id:
                continue
            details[video_id] = {
                "video_id": video_id,
                "video_url": f"https://www.youtube.com/watch?v={video_id}",
                "title": snippet.get("title"),
                "channel_id": snippet.get("channelId"),
                "channel_title": snippet.get("channelTitle"),
                "published_at": snippet.get("publishedAt"),
                "duration_iso8601": content.get("duration"),
                "duration_seconds": _duration_seconds(content.get("duration")),
                "view_count": _integer(stats.get("viewCount")),
                "like_count": _integer(stats.get("likeCount")),
                "comment_count": _integer(stats.get("commentCount")),
                "privacy_status": status.get("privacyStatus"),
                "embeddable": status.get("embeddable"),
                "etag": item.get("etag"),
            }
    return details


def initialize_map(case_manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "HOOKLAB_YOUTUBE_VIDEO_IDENTITY_MAP_v0.1",
        "status": "IDENTITY_REVIEW_PENDING",
        "created_at": _utc_now(),
        "collector_version": COLLECTOR_VERSION,
        "source_case_manifest_id": case_manifest.get("manifest_id"),
        "records": [
            {
                "case_id": record["case_id"],
                "title": record.get("title"),
                "artist": record.get("artist"),
                "video_id": None,
                "identity_review_status": "PENDING",
                "identity_evidence": [],
            }
            for record in case_manifest.get("records", [])
            if str(record.get("case_id", "")).startswith("C")
        ],
        "scientific_d_unlocked": False,
    }


def search_candidates(
    case_manifest: dict[str, Any],
    output_path: Path,
    key: str,
    max_results: int = 5,
    request: Callable = _request,
    search_interval_seconds: float = DEFAULT_SEARCH_INTERVAL_SECONDS,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    existing: dict[str, Any] = {}
    if output_path.exists():
        prior = json.loads(output_path.read_text(encoding="utf-8"))
        existing = {row["case_id"]: row for row in prior.get("records", [])}
    output = {
        "schema": "HOOKLAB_YOUTUBE_SEARCH_CANDIDATES_v0.1",
        "status": "CANDIDATES_ONLY_NOT_IDENTITY_MAP",
        "updated_at": _utc_now(),
        "collector_version": COLLECTOR_VERSION,
        "provider": "YouTube Data API v3",
        "records": [],
        "automatic_identity_selection": False,
        "scientific_d_unlocked": False,
    }
    records = [r for r in case_manifest.get("records", []) if str(r.get("case_id", "")).startswith("C")]
    executed_searches = 0
    for case in records:
        case_id = case["case_id"]
        if existing.get(case_id, {}).get("search_status") == "COMPLETE":
            output["records"].append(existing[case_id])
            continue
        if executed_searches and search_interval_seconds > 0:
            sleep(search_interval_seconds)
        query = f'{case.get("title", "")} {case.get("artist", "")} official music video'
        response = request(
            "search",
            {
                "part": "snippet",
                "q": query,
                "type": "video",
                "videoCategoryId": "10",
                "maxResults": max_results,
                "order": "relevance",
                "fields": "items(id/videoId,snippet(title,channelId,channelTitle,publishedAt))",
            },
            key,
        )
        executed_searches += 1
        candidates = []
        for rank, item in enumerate(response.get("items", []), start=1):
            video_id = (item.get("id") or {}).get("videoId")
            snippet = item.get("snippet") or {}
            if video_id:
                candidates.append({
                    "rank": rank,
                    "video_id": video_id,
                    "video_url": f"https://www.youtube.com/watch?v={video_id}",
                    "title": snippet.get("title"),
                    "channel_id": snippet.get("channelId"),
                    "channel_title": snippet.get("channelTitle"),
                    "published_at": snippet.get("publishedAt"),
                })
        output["records"].append({
            "case_id": case_id,
            "corpus_title": case.get("title"),
            "corpus_artist": case.get("artist"),
            "query": query,
            "search_status": "COMPLETE",
            "candidates": candidates,
        })
        output["updated_at"] = _utc_now()
        _atomic_json(output_path, output)

    all_ids = [candidate["video_id"] for row in output["records"] for candidate in row["candidates"]]
    details = _details(list(dict.fromkeys(all_ids)), key, request)
    for row in output["records"]:
        row["candidates"] = [{**candidate, **details.get(candidate["video_id"], {})} for candidate in row["candidates"]]
    output["updated_at"] = _utc_now()
    _atomic_json(output_path, output)
    return output


def collect_snapshots(identity_map: dict[str, Any], key: str, request: Callable = _request) -> dict[str, Any]:
    selected = [
        row for row in identity_map.get("records", [])
        if row.get("identity_review_status") == "VERIFIED" and row.get("video_id")
    ]
    details = _details([row["video_id"] for row in selected], key, request)
    captured_at = _utc_now()
    return {
        "schema": "HOOKLAB_YOUTUBE_PUBLIC_METRIC_SNAPSHOT_v0.1",
        "status": "PUBLIC_METRIC_SNAPSHOT_COMPLETE" if selected else "AUDIT_NO_VERIFIED_VIDEO_IDENTITIES",
        "captured_at": captured_at,
        "collector_version": COLLECTOR_VERSION,
        "provider": "YouTube Data API v3",
        "records": [
            {
                "case_id": row["case_id"],
                "identity_review_status": "VERIFIED",
                "captured_at": captured_at,
                **details.get(row["video_id"], {"video_id": row["video_id"], "metric_status": "VIDEO_NOT_RETURNED"}),
            }
            for row in selected
        ],
        "interpretation": "TIMESTAMPED_PUBLIC_SNAPSHOT_NOT_TRAFFIC_PEAK_OR_CAUSAL_EFFECT",
        "generation_class": "D0_EXPLORATORY",
        "scientific_d_unlocked": False,
    }


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="HookLab YouTube public metric collector")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init-map")
    init.add_argument("--case-manifest", required=True, type=Path)
    init.add_argument("--output", required=True, type=Path)
    search = sub.add_parser("search-candidates")
    search.add_argument("--case-manifest", required=True, type=Path)
    search.add_argument("--output", required=True, type=Path)
    search.add_argument("--max-results", type=int, default=5)
    search.add_argument(
        "--search-interval-seconds",
        type=float,
        default=DEFAULT_SEARCH_INTERVAL_SECONDS,
        help="Minimum pause between search.list calls to respect per-minute quota.",
    )
    snapshot = sub.add_parser("collect-snapshots")
    snapshot.add_argument("--identity-map", required=True, type=Path)
    snapshot.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        if args.command == "init-map":
            _atomic_json(args.output, initialize_map(_load(args.case_manifest)))
        elif args.command == "search-candidates":
            search_candidates(
                _load(args.case_manifest),
                args.output,
                _api_key(),
                args.max_results,
                search_interval_seconds=args.search_interval_seconds,
            )
        else:
            _atomic_json(args.output, collect_snapshots(_load(args.identity_map), _api_key()))
    except CollectorError as error:
        print(str(error))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
