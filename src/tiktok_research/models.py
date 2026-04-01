from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Researcher:
    slug: str
    display_name: str


@dataclass(frozen=True)
class WorkspacePaths:
    root: Path
    config_path: Path
    inputs_dir: Path
    data_dir: Path
    exports_dir: Path
    cache_dir: Path
    logs_dir: Path
    workbook_path: Path
    metadata_json_path: Path
    replacement_candidates_path: Path
    transcripts_dir: Path
    database_path: Path
    backups_dir: Path
    llm_scores_dir: Path
    replacement_log_path: Path


@dataclass(frozen=True)
class StudyRuntime:
    raw_config: dict[str, Any]
    paths: WorkspacePaths
    researchers: tuple[Researcher, ...]


@dataclass(frozen=True)
class NormalizedVideoRecord:
    record_id: str
    video_url: str
    numeric_id: str
    creator_handle: str
    username: str
    description: str
    transcript: str
    metrics: dict[str, int]
    post_date: str
    extra: dict[str, Any]


@dataclass(frozen=True)
class ProviderStatus:
    name: str
    enabled: bool
    reason: str = ""

