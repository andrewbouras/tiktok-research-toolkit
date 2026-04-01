from __future__ import annotations

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests

from ..config import get_provider_secret
from ..models import StudyRuntime


def get_access_token(client_key: str, client_secret: str) -> str:
    response = requests.post(
        "https://open.tiktokapis.com/v2/oauth/token/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "client_key": client_key,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def date_chunks(start_str: str, end_str: str, chunk_days: int = 20) -> list[tuple[str, str]]:
    start = datetime.strptime(start_str, "%Y%m%d")
    end = datetime.strptime(end_str, "%Y%m%d")
    chunks = []
    cursor = start
    while cursor <= end:
        chunk_end = min(cursor + timedelta(days=chunk_days - 1), end)
        chunks.append((cursor.strftime("%Y%m%d"), chunk_end.strftime("%Y%m%d")))
        cursor = chunk_end + timedelta(days=1)
    return chunks


def search_videos(
    token: str,
    *,
    keywords: list[str],
    start_date: str,
    end_date: str,
    region_code: str,
    cursor: int | None = None,
    search_id: str | None = None,
) -> dict[str, Any]:
    response = requests.post(
        "https://open.tiktokapis.com/v2/research/video/query/",
        params={
            "fields": (
                "id,video_description,voice_to_text,create_time,region_code,"
                "share_count,view_count,like_count,comment_count,username"
            )
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        json={
            "query": {
                "and": [
                    {
                        "operation": "IN",
                        "field_name": "region_code",
                        "field_values": [region_code],
                    },
                    {
                        "operation": "IN",
                        "field_name": "keyword",
                        "field_values": keywords,
                    },
                ]
            },
            "max_count": 100,
            "start_date": start_date,
            "end_date": end_date,
            "cursor": cursor or 0,
            **({"search_id": search_id} if search_id else {}),
        },
        timeout=30,
    )
    if response.status_code == 429:
        time.sleep(20)
        return search_videos(
            token,
            keywords=keywords,
            start_date=start_date,
            end_date=end_date,
            region_code=region_code,
            cursor=cursor,
            search_id=search_id,
        )
    response.raise_for_status()
    return response.json()


def collect_videos(
    runtime: StudyRuntime,
    *,
    keywords: list[str],
    start_date: str,
    end_date: str,
    region_code: str = "US",
) -> dict[str, Any]:
    client_key = get_provider_secret(runtime, "tiktok", "client_key_env")
    client_secret = get_provider_secret(runtime, "tiktok", "client_secret_env")
    if not client_key or not client_secret:
        raise RuntimeError(
            "TikTok collection is not configured. Set the env vars named in providers.tiktok.client_key_env and providers.tiktok.client_secret_env."
        )
    token = get_access_token(client_key, client_secret)
    collected: dict[str, dict[str, Any]] = {}
    fetched = 0
    for chunk_start, chunk_end in date_chunks(start_date, end_date):
        cursor = 0
        search_id = None
        while True:
            payload = search_videos(
                token,
                keywords=keywords,
                start_date=chunk_start,
                end_date=chunk_end,
                region_code=region_code,
                cursor=cursor,
                search_id=search_id,
            ).get("data", {})
            videos = payload.get("videos", [])
            fetched += len(videos)
            for item in videos:
                record_id = str(item.get("id") or "").strip()
                if record_id:
                    collected[record_id] = item
            if not payload.get("has_more"):
                break
            cursor = int(payload.get("cursor") or 0)
            search_id = payload.get("search_id") or search_id
            time.sleep(0.5)
    rows = sorted(
        collected.values(),
        key=lambda item: int(item.get("view_count") or 0),
        reverse=True,
    )
    runtime.paths.metadata_json_path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return {
        "output_path": str(runtime.paths.metadata_json_path),
        "keywords": keywords,
        "date_range": [start_date, end_date],
        "fetched_from_api": fetched,
        "saved_unique_rows": len(rows),
    }


def write_collection_csv(rows: list[dict[str, Any]], destination: Path) -> None:
    import csv

    fieldnames = [
        "id",
        "create_time",
        "username",
        "region_code",
        "view_count",
        "like_count",
        "share_count",
        "comment_count",
        "video_description",
        "voice_to_text",
    ]
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in rows:
            writer.writerow({field: item.get(field, "") for field in fieldnames})

