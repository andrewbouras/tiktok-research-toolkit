from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml

from .models import Researcher, StudyRuntime, WorkspacePaths


DEFAULT_PORT = 5173
DEFAULT_BACKUP_MIN_INTERVAL_SECONDS = 300
DEFAULT_BACKUP_MAX_FILES = 96
DEFAULT_RESEARCHERS = (
    Researcher(slug="reviewer-a", display_name="Reviewer A"),
    Researcher(slug="reviewer-b", display_name="Reviewer B"),
)
TOP_LEVEL_KEYS = ("study", "researchers", "paths", "providers")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "study"


def build_default_config(
    study_name: str,
    *,
    researchers: list[Researcher] | None = None,
    port: int = DEFAULT_PORT,
) -> dict[str, Any]:
    selected_researchers = tuple(researchers or DEFAULT_RESEARCHERS)
    return {
        "study": {
            "name": study_name,
            "slug": slugify(study_name),
            "description": "Reusable workspace for coding short-form health videos.",
            "port": port,
            "backup_min_interval_seconds": DEFAULT_BACKUP_MIN_INTERVAL_SECONDS,
            "backup_max_files": DEFAULT_BACKUP_MAX_FILES,
        },
        "researchers": [
            {"slug": researcher.slug, "display_name": researcher.display_name}
            for researcher in selected_researchers
        ],
        "paths": {
            "workbook": "inputs/coding_template.xlsx",
            "metadata_json": "inputs/collected_videos.json",
            "replacement_candidates_json": "inputs/replacement_candidates.json",
            "transcripts_dir": "inputs/transcripts",
            "database": "data/research_dashboard.sqlite3",
            "backups_dir": "data/backups",
            "llm_scores_dir": "data/llm_scores",
            "replacement_log": "logs/sample_replacement_log.jsonl",
        },
        "providers": {
            "tiktok": {
                "enabled": False,
                "client_key_env": "TIKTOK_CLIENT_KEY",
                "client_secret_env": "TIKTOK_CLIENT_SECRET",
            },
            "openai": {
                "enabled": False,
                "api_key_env": "OPENAI_API_KEY",
                "whisper_model": "whisper-1",
                "judge_model": "gpt-5.2-2025-12-11",
            },
            "anthropic": {
                "enabled": False,
                "api_key_env": "ANTHROPIC_API_KEY",
                "judge_model": "claude-sonnet-4-6",
            },
        },
    }


def write_config(path: Path, config: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing study configuration: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError("study_config.yaml must contain a mapping at the top level")
    missing = [key for key in TOP_LEVEL_KEYS if key not in payload]
    if missing:
        raise ValueError(f"study_config.yaml is missing top-level sections: {', '.join(missing)}")
    return payload


def resolve_workspace_paths(root: Path, config: dict[str, Any]) -> WorkspacePaths:
    root = root.resolve()
    paths = config["paths"]
    return WorkspacePaths(
        root=root,
        config_path=root / "study_config.yaml",
        inputs_dir=root / "inputs",
        data_dir=root / "data",
        exports_dir=root / "exports",
        cache_dir=root / "cache",
        logs_dir=root / "logs",
        workbook_path=root / paths["workbook"],
        metadata_json_path=root / paths["metadata_json"],
        replacement_candidates_path=root / paths["replacement_candidates_json"],
        transcripts_dir=root / paths["transcripts_dir"],
        database_path=root / paths["database"],
        backups_dir=root / paths["backups_dir"],
        llm_scores_dir=root / paths["llm_scores_dir"],
        replacement_log_path=root / paths["replacement_log"],
    )


def resolve_researchers(config: dict[str, Any]) -> tuple[Researcher, ...]:
    researchers = []
    for item in config.get("researchers", []):
        if not isinstance(item, dict):
            continue
        slug = str(item.get("slug") or "").strip()
        display_name = str(item.get("display_name") or "").strip()
        if slug and display_name:
            researchers.append(Researcher(slug=slug, display_name=display_name))
    return tuple(researchers) or DEFAULT_RESEARCHERS


def load_runtime(workspace_root: Path) -> StudyRuntime:
    config_path = workspace_root / "study_config.yaml"
    config = load_config(config_path)
    return StudyRuntime(
        raw_config=config,
        paths=resolve_workspace_paths(workspace_root, config),
        researchers=resolve_researchers(config),
    )


def get_provider_config(runtime: StudyRuntime, provider_name: str) -> dict[str, Any]:
    providers = runtime.raw_config.get("providers", {})
    provider = providers.get(provider_name, {})
    return provider if isinstance(provider, dict) else {}


def get_env_value(variable_name: str | None) -> str:
    if not variable_name:
        return ""
    return os.environ.get(variable_name, "").strip()


def get_provider_secret(runtime: StudyRuntime, provider_name: str, env_key_field: str) -> str:
    provider = get_provider_config(runtime, provider_name)
    env_name = provider.get(env_key_field)
    return get_env_value(env_name if isinstance(env_name, str) else None)

