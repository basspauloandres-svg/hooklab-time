"""Open, quota-free public metadata lane for HookLab.

Candidate discovery uses yt-dlp only as a public metadata extractor. Scheduled
metric snapshots use the open Return YouTube Dislike public API and retain only
its cached public ``viewCount`` and ``likes`` fields. Dislikes, raw votes,
ratings, audio, video, captions, descriptions, and lyrics are never persisted.
Candidate search cannot promote an identity; scheduled snapshots include
VERIFIED identities only and remain descriptive/D0.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable


COLLECTOR_VERSION = "hooklab-open-metadata-stack-v1.1"
GENERATION_CLASS = "D0_EXPLORATORY"
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
RYD_API_BASE = "https://returnyoutubedislikeapi.com"
RYD_PROVIDER = "Return YouTube Dislike public votes API"
RYD_PROVIDER_VERSION = "public-votes-endpoint-v1"
RYD_CACHE_POLICY = "PROVIDER_DOCUMENTED_APPROXIMATELY_2_TO_3_DAYS"
RYD_DATA_LINEAGE = "GOOGLE_API_AND_SCRAPED_PUBLIC_DATA_CACHED_BY_PROVIDER"


class OpenMetadataError(RuntimeError):
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


def _yt_dlp_session() -> tuple[Callable[[str], dict[str, Any]], str]:
    try:
        import yt_dlp
    except ImportError as error:
        raise OpenMetadataError("YT_DLP_NOT_INSTALLED") from error

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
        "cachedir": False,
        "socket_timeout": 30,
        "retries": 2,
        "extract_flat": False,
    }
    client = yt_dlp.YoutubeDL(options)

    def extract(url: str) -> dict[str, Any]:
        return client.extract_info(url, download=False)

    return extract, yt_dlp.version.__version__


def _ryd_session(
    timeout_seconds: int = 30,
    retries: int = 2,
) -> tuple[Callable[[str], dict[str, Any]], str]:
    """Return a quota-free metric fetcher with bounded retries.

    The endpoint response contains reconstructed dislike fields. They are never
    returned by the whitelist adapter and therefore cannot enter HookLab data.
    """

    def extract(video_id: str) -> dict[str, Any]:
        if not VIDEO_ID_RE.fullmatch(video_id):
            raise OpenMetadataError("INVALID_VIDEO_ID")
        query = urllib.parse.urlencode({"videoId": video_id})
        request = urllib.request.Request(
            f"{RYD_API_BASE}/votes?{query}",
            headers={
                "Accept": "application/json",
                "User-Agent": f"HookLab/{COLLECTOR_VERSION}",
            },
        )
        last_error: Exception | None = None
        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                if not isinstance(payload, dict):
                    raise OpenMetadataError("PROVIDER_RESPONSE_NOT_OBJECT")
                return payload
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
                last_error = error
                if attempt < retries:
                    time.sleep(2**attempt)
        raise OpenMetadataError("RYD_PROVIDER_FETCH_FAILED") from last_error

    return extract, RYD_PROVIDER_VERSION


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _safe_error(error: Exception) -> str:
    return type(error).__name__


def _whitelisted_video_metadata(info: dict[str, Any]) -> dict[str, Any]:
    video_id = str(info.get("id") or "")
    return {
        "video_id": video_id if VIDEO_ID_RE.fullmatch(video_id) else None,
        "video_url": f"https://www.youtube.com/watch?v={video_id}" if VIDEO_ID_RE.fullmatch(video_id) else None,
        "title": info.get("title"),
        "channel_id": info.get("channel_id"),
        "channel": info.get("channel") or info.get("uploader"),
        "channel_is_verified": info.get("channel_is_verified"),
        "upload_date": info.get("upload_date"),
        "release_date": info.get("release_date"),
        "duration_seconds": _int_or_none(info.get("duration")),
        "view_count": _int_or_none(info.get("view_count")),
        "like_count": _int_or_none(info.get("like_count")),
        "comment_count": _int_or_none(info.get("comment_count")),
        "availability": info.get("availability"),
        "live_status": info.get("live_status"),
    }


def _whitelisted_ryd_metrics(info: dict[str, Any]) -> dict[str, Any]:
    """Retain only non-estimated public fields needed by HookLab.

    ``dislikes``, ``rawDislikes``, ``rawLikes`` and ``rating`` are deliberately
    absent because the provider may estimate/reconstruct them.
    """

    video_id = str(info.get("id") or "")
    return {
        "video_id": video_id if VIDEO_ID_RE.fullmatch(video_id) else None,
        "video_url": f"https://www.youtube.com/watch?v={video_id}" if VIDEO_ID_RE.fullmatch(video_id) else None,
        "view_count": _int_or_none(info.get("viewCount")),
        "like_count": _int_or_none(info.get("likes")),
        "provider_record_created_at": info.get("dateCreated"),
        "provider_deleted": info.get("deleted"),
    }


def discover_candidates(
    case_manifest: dict[str, Any],
    extractor: Callable[[str], dict[str, Any]],
    provider_version: str,
    max_results: int = 5,
) -> dict[str, Any]:
    records = []
    for case in case_manifest.get("records", []):
        if not str(case.get("case_id", "")).startswith("C"):
            continue
        query = f'{case.get("title", "")} {case.get("artist", "")} official music video'
        try:
            result = extractor(f"ytsearch{max_results}:{query}")
            entries = result.get("entries") or []
            candidates = [
                {"rank": rank, **_whitelisted_video_metadata(entry or {})}
                for rank, entry in enumerate(entries, start=1)
            ]
            status = "CANDIDATES_FOUND" if candidates else "NO_CANDIDATES_FOUND"
            error_class = None
        except Exception as error:  # provider failures must remain case-local
            candidates = []
            status = "PROVIDER_QUERY_FAILED"
            error_class = _safe_error(error)
        records.append({
            "case_id": case.get("case_id"),
            "corpus_title": case.get("title"),
            "corpus_artist": case.get("artist"),
            "query": query,
            "status": status,
            "error_class": error_class,
            "candidates": candidates,
            "identity_promotion": "FORBIDDEN_AUTOMATICALLY",
        })
    return {
        "schema": "HOOKLAB_OPEN_YOUTUBE_CANDIDATES_v1",
        "created_at": _utc_now(),
        "collector_version": COLLECTOR_VERSION,
        "provider": "yt-dlp public metadata extractor",
        "provider_version": provider_version,
        "records": records,
        "automatic_identity_selection": False,
        "downloads_media": False,
        "scientific_d_unlocked": False,
    }


def collect_verified_snapshot(
    identity_map: dict[str, Any],
    extractor: Callable[[str], dict[str, Any]],
    provider_version: str,
    captured_at: str | None = None,
    *,
    provider: str = "yt-dlp public metadata extractor",
    metadata_adapter: Callable[[dict[str, Any]], dict[str, Any]] = _whitelisted_video_metadata,
    provider_cache_policy: str | None = None,
    provider_data_lineage: str | None = None,
) -> dict[str, Any]:
    captured_at = captured_at or _utc_now()
    records = []
    for row in identity_map.get("records", []):
        if row.get("identity_review_status") != "VERIFIED" or not row.get("video_id"):
            continue
        video_id = str(row["video_id"])
        if not VIDEO_ID_RE.fullmatch(video_id):
            records.append({
                "case_id": row.get("case_id"),
                "video_id": None,
                "snapshot_status": "AUDIT_INVALID_VERIFIED_VIDEO_ID",
            })
            continue
        try:
            provider_input = video_id if provider == RYD_PROVIDER else f"https://www.youtube.com/watch?v={video_id}"
            info = extractor(provider_input)
            metadata = metadata_adapter(info)
            returned_id = metadata.get("video_id")
            valid_public_metrics = (
                metadata.get("view_count") is not None
                and metadata.get("view_count") >= 0
                and metadata.get("provider_deleted") is not True
            )
            if returned_id != video_id:
                status = "AUDIT_IDENTITY_MISMATCH"
            elif not valid_public_metrics:
                status = "AUDIT_PUBLIC_METRICS_NOT_VALID"
            else:
                status = "SNAPSHOT_COMPLETE"
            records.append({
                "case_id": row.get("case_id"),
                "identity_review_status": "VERIFIED",
                "snapshot_status": status,
                "captured_at": captured_at,
                **metadata,
            })
        except Exception as error:
            records.append({
                "case_id": row.get("case_id"),
                "video_id": video_id,
                "video_url": f"https://www.youtube.com/watch?v={video_id}",
                "identity_review_status": "VERIFIED",
                "snapshot_status": "PROVIDER_FETCH_FAILED",
                "error_class": _safe_error(error),
                "captured_at": captured_at,
            })

    complete = sum(row.get("snapshot_status") == "SNAPSHOT_COMPLETE" for row in records)
    return {
        "schema": "HOOKLAB_AUTOMATED_PUBLIC_METRIC_SNAPSHOT_v1",
        "status": "SNAPSHOT_COMPLETE" if records and complete == len(records) else "SNAPSHOT_PARTIAL_OR_AUDIT",
        "captured_at": captured_at,
        "collector_version": COLLECTOR_VERSION,
        "provider": provider,
        "provider_version": provider_version,
        "provider_cache_policy": provider_cache_policy,
        "provider_data_lineage": provider_data_lineage,
        "retained_metric_fields": ["view_count", "like_count"],
        "explicitly_forbidden_provider_fields": ["dislikes", "rawDislikes", "rawLikes", "rating"],
        "verified_identity_count": len(records),
        "complete_snapshot_count": complete,
        "records": records,
        "interpretation": "TIMESTAMPED_PUBLIC_SNAPSHOT_NOT_RETROSPECTIVE_TRAFFIC_PEAK_OR_CAUSAL_EFFECT",
        "generation_class": GENERATION_CLASS,
        "downloads_media": False,
        "scientific_d_unlocked": False,
    }


def snapshot_filename(captured_at: str) -> str:
    stamp = re.sub(r"[^0-9]", "", captured_at)[:14]
    return f"youtube_public_snapshot_{stamp}Z.json"


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="HookLab open public metadata collector")
    sub = parser.add_subparsers(dest="command", required=True)
    discover = sub.add_parser("discover-candidates")
    discover.add_argument("--case-manifest", required=True, type=Path)
    discover.add_argument("--output", required=True, type=Path)
    discover.add_argument("--max-results", type=int, default=5)
    snapshot = sub.add_parser("collect-verified-snapshot")
    snapshot.add_argument("--identity-map", required=True, type=Path)
    snapshot.add_argument("--snapshot-dir", required=True, type=Path)
    args = parser.parse_args()

    try:
        if args.command == "discover-candidates":
            extractor, provider_version = _yt_dlp_session()
            result = discover_candidates(_load(args.case_manifest), extractor, provider_version, args.max_results)
            _atomic_json(args.output, result)
            print(args.output)
        else:
            extractor, provider_version = _ryd_session()
            captured_at = _utc_now()
            result = collect_verified_snapshot(
                _load(args.identity_map),
                extractor,
                provider_version,
                captured_at,
                provider=RYD_PROVIDER,
                metadata_adapter=_whitelisted_ryd_metrics,
                provider_cache_policy=RYD_CACHE_POLICY,
                provider_data_lineage=RYD_DATA_LINEAGE,
            )
            output = args.snapshot_dir / snapshot_filename(captured_at)
            _atomic_json(output, result)
            _atomic_json(args.snapshot_dir / "latest.json", result)
            print(output)
    except OpenMetadataError as error:
        print(str(error))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
