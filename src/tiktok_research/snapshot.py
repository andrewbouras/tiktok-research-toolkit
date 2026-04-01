from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from .models import StudyRuntime


def timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def create_snapshot_archive(runtime: StudyRuntime, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for path in (
            runtime.paths.config_path,
            runtime.paths.workbook_path,
            runtime.paths.metadata_json_path,
            runtime.paths.replacement_candidates_path,
            runtime.paths.database_path,
        ):
            if path.exists():
                archive.write(path, arcname=path.relative_to(runtime.paths.root))
        if runtime.paths.transcripts_dir.exists():
            for item in sorted(runtime.paths.transcripts_dir.rglob("*")):
                if item.is_file():
                    archive.write(item, arcname=item.relative_to(runtime.paths.root))
        if runtime.paths.llm_scores_dir.exists():
            for item in sorted(runtime.paths.llm_scores_dir.rglob("*")):
                if item.is_file():
                    archive.write(item, arcname=item.relative_to(runtime.paths.root))
    return destination
