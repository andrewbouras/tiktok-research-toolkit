from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path
from typing import Iterable

from .config import build_default_config, load_runtime, write_config
from .models import Researcher, StudyRuntime
from .workspace import copy_path, ensure_workspace_directories


def discover_researchers_from_database(database_path: Path) -> list[Researcher]:
    if not database_path.exists():
        return []
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT slug, display_name
            FROM researchers
            ORDER BY display_name COLLATE NOCASE
            """
        ).fetchall()
    except sqlite3.Error:
        return []
    finally:
        conn.close()
    return [
        Researcher(slug=str(row["slug"]), display_name=str(row["display_name"]))
        for row in rows
        if row["slug"] and row["display_name"]
    ]


def import_legacy_workspace(
    workspace_root: Path,
    *,
    workbook_path: Path,
    metadata_json_path: Path | None = None,
    transcripts_dir: Path | None = None,
    replacement_candidates_path: Path | None = None,
    database_path: Path | None = None,
    llm_scores_dir: Path | None = None,
    study_name: str = "Imported TikTok Research Study",
    researchers: Iterable[Researcher] | None = None,
) -> StudyRuntime:
    inferred_researchers = list(researchers or [])
    if not inferred_researchers and database_path is not None:
        inferred_researchers = discover_researchers_from_database(database_path)

    config = build_default_config(study_name, researchers=inferred_researchers)
    write_config(workspace_root / "study_config.yaml", config)
    runtime = load_runtime(workspace_root)
    ensure_workspace_directories(runtime)

    copy_path(workbook_path, runtime.paths.workbook_path)
    if metadata_json_path is not None and metadata_json_path.exists():
        copy_path(metadata_json_path, runtime.paths.metadata_json_path)
    else:
        runtime.paths.metadata_json_path.write_text("[]\n", encoding="utf-8")

    if replacement_candidates_path is not None and replacement_candidates_path.exists():
        copy_path(replacement_candidates_path, runtime.paths.replacement_candidates_path)
    else:
        runtime.paths.replacement_candidates_path.write_text("[]\n", encoding="utf-8")

    if transcripts_dir is not None and transcripts_dir.exists():
        shutil.copytree(transcripts_dir, runtime.paths.transcripts_dir, dirs_exist_ok=True)
    else:
        runtime.paths.transcripts_dir.mkdir(parents=True, exist_ok=True)
        (runtime.paths.transcripts_dir / "index.json").write_text("{}\n", encoding="utf-8")

    if database_path is not None and database_path.exists():
        copy_path(database_path, runtime.paths.database_path)

    if llm_scores_dir is not None and llm_scores_dir.exists():
        shutil.copytree(llm_scores_dir, runtime.paths.llm_scores_dir, dirs_exist_ok=True)

    return runtime

