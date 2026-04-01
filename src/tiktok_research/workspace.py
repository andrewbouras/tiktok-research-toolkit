from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Iterable

from .config import build_default_config, load_runtime, write_config
from .demo_data import DEMO_MAIN_VIDEOS, DEMO_REPLACEMENT_CANDIDATES, DEMO_RESEARCHERS
from .models import Researcher, StudyRuntime
from .workbook import create_template_workbook


def ensure_workspace_directories(runtime: StudyRuntime) -> None:
    for directory in (
        runtime.paths.root,
        runtime.paths.inputs_dir,
        runtime.paths.data_dir,
        runtime.paths.exports_dir,
        runtime.paths.cache_dir,
        runtime.paths.logs_dir,
        runtime.paths.transcripts_dir,
        runtime.paths.backups_dir,
        runtime.paths.llm_scores_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)


def init_study_workspace(
    workspace_root: Path,
    study_name: str,
    *,
    researchers: Iterable[Researcher] | None = None,
) -> StudyRuntime:
    workspace_root = workspace_root.resolve()
    config = build_default_config(study_name, researchers=list(researchers or []))
    write_config(workspace_root / "study_config.yaml", config)
    runtime = load_runtime(workspace_root)
    ensure_workspace_directories(runtime)
    create_template_workbook(runtime.paths.workbook_path, videos=[])
    runtime.paths.metadata_json_path.write_text("[]\n", encoding="utf-8")
    runtime.paths.replacement_candidates_path.write_text("[]\n", encoding="utf-8")
    (runtime.paths.transcripts_dir / "index.json").write_text("{}\n", encoding="utf-8")
    return runtime


def init_demo_workspace(workspace_root: Path) -> StudyRuntime:
    runtime = init_study_workspace(
        workspace_root,
        "TikTok Research Toolkit Demo",
        researchers=DEMO_RESEARCHERS,
    )
    create_template_workbook(runtime.paths.workbook_path, videos=DEMO_MAIN_VIDEOS)
    runtime.paths.metadata_json_path.write_text(
        json.dumps(
            [
                {
                    "id": item["id"],
                    "username": item["username"],
                    "view_count": item["view_count"],
                    "like_count": item["like_count"],
                    "comment_count": item["comment_count"],
                    "share_count": item["share_count"],
                    "create_time": item["create_time"],
                    "region_code": "US",
                    "video_description": item["video_description"],
                    "voice_to_text": item["transcript"],
                }
                for item in DEMO_MAIN_VIDEOS
            ],
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    runtime.paths.replacement_candidates_path.write_text(
        json.dumps(DEMO_REPLACEMENT_CANDIDATES, indent=2) + "\n",
        encoding="utf-8",
    )
    transcript_index: dict[str, dict[str, str | int]] = {}
    for item in DEMO_MAIN_VIDEOS:
        transcript_path = runtime.paths.transcripts_dir / f"{item['video_id']}.txt"
        transcript_path.write_text(item["transcript"], encoding="utf-8")
        transcript_index[item["video_id"]] = {
            "url": f"https://www.tiktok.com/@{item['username']}/video/{item['id']}",
            "status": "demo",
            "chars": len(item["transcript"]),
        }
    (runtime.paths.transcripts_dir / "index.json").write_text(
        json.dumps(transcript_index, indent=2) + "\n",
        encoding="utf-8",
    )
    return runtime


def copy_path(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        shutil.copy2(source, destination)

