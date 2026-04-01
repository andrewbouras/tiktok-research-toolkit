from __future__ import annotations

import argparse
import json
import threading
import webbrowser
from pathlib import Path
from typing import Any

from .config import load_runtime
from .dashboard.app import create_app
from .legacy import import_legacy_workspace
from .providers.judge import score_workspace
from .providers.tiktok_collector import collect_videos
from .providers.transcribe import transcribe_workspace
from .sample_replacement import (
    handle_inspect_slot,
    handle_list_reserve,
    handle_replace_slot,
    project_config_from_runtime,
)
from .snapshot import create_snapshot_archive, timestamp_slug
from .workspace import init_demo_workspace, init_study_workspace


def json_print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tiktok-research", description="TikTok Research Toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("init-demo", help="Create a demo workspace with synthetic data")
    demo.add_argument("workspace", help="Workspace directory to create")

    init = subparsers.add_parser("init-study", help="Create a new blank study workspace")
    init.add_argument("workspace", help="Workspace directory to create")
    init.add_argument("--study-name", default="TikTok Research Study", help="Study name to write into study_config.yaml")

    legacy = subparsers.add_parser("import-legacy", help="Import an existing workbook/json/transcript workflow")
    legacy.add_argument("workspace", help="Workspace directory to create")
    legacy.add_argument("--study-name", default="Imported TikTok Research Study")
    legacy.add_argument("--workbook", required=True)
    legacy.add_argument("--metadata-json")
    legacy.add_argument("--transcripts-dir")
    legacy.add_argument("--replacement-json")
    legacy.add_argument("--database")
    legacy.add_argument("--llm-scores-dir")

    run = subparsers.add_parser("run-dashboard", help="Run the Flask dashboard for a workspace")
    run.add_argument("workspace", help="Workspace directory containing study_config.yaml")
    run.add_argument("--host", default="127.0.0.1")
    run.add_argument("--port", type=int)
    run.add_argument("--no-browser", action="store_true")

    collect = subparsers.add_parser("collect", help="Run TikTok Research API collection")
    collect.add_argument("workspace")
    collect.add_argument("--start-date", required=True)
    collect.add_argument("--end-date", required=True)
    collect.add_argument("--region-code", default="US")
    collect.add_argument("--keyword", action="append", dest="keywords", required=True)

    transcribe = subparsers.add_parser("transcribe", help="Extract or generate transcripts for the workspace workbook")
    transcribe.add_argument("workspace")
    transcribe.add_argument("--whisper", action="store_true")
    transcribe.add_argument("--whisper-only", action="store_true")

    judge = subparsers.add_parser("judge", help="Run optional LLM scoring over workspace transcripts")
    judge.add_argument("workspace")
    judge.add_argument("--model", choices=["all", "gpt", "claude"], default="all")

    replacement = subparsers.add_parser("replace-sample", help="Inspect or replace sample slots")
    replacement.add_argument("workspace")
    replacement_sub = replacement.add_subparsers(dest="replace_command", required=True)
    inspect = replacement_sub.add_parser("inspect-slot")
    inspect.add_argument("slot_id")
    reserve = replacement_sub.add_parser("list-reserve")
    reserve.add_argument("--limit", type=int, default=20)
    replace = replacement_sub.add_parser("replace-slot")
    replace.add_argument("slot_id")
    replace.add_argument("candidate_numeric_id")
    replace.add_argument("--yes", action="store_true")
    replace.add_argument("--allow-existing-candidate", action="store_true")

    export = subparsers.add_parser("export", help="Write CSV export and a reproducible snapshot zip")
    export.add_argument("workspace")
    export.add_argument("--output-dir")

    return parser


def handle_init_demo(args: argparse.Namespace) -> int:
    runtime = init_demo_workspace(Path(args.workspace))
    json_print({"workspace": str(runtime.paths.root), "study": runtime.raw_config["study"]["name"], "mode": "demo"})
    return 0


def handle_init_study(args: argparse.Namespace) -> int:
    runtime = init_study_workspace(Path(args.workspace), args.study_name)
    json_print({"workspace": str(runtime.paths.root), "study": runtime.raw_config["study"]["name"], "mode": "blank"})
    return 0


def handle_import_legacy(args: argparse.Namespace) -> int:
    runtime = import_legacy_workspace(
        Path(args.workspace),
        workbook_path=Path(args.workbook),
        metadata_json_path=Path(args.metadata_json) if args.metadata_json else None,
        transcripts_dir=Path(args.transcripts_dir) if args.transcripts_dir else None,
        replacement_candidates_path=Path(args.replacement_json) if args.replacement_json else None,
        database_path=Path(args.database) if args.database else None,
        llm_scores_dir=Path(args.llm_scores_dir) if args.llm_scores_dir else None,
        study_name=args.study_name,
    )
    json_print({"workspace": str(runtime.paths.root), "study": runtime.raw_config["study"]["name"], "mode": "legacy-import"})
    return 0


def handle_run_dashboard(args: argparse.Namespace) -> int:
    runtime = load_runtime(Path(args.workspace))
    app = create_app(runtime)
    port = args.port or int(runtime.raw_config["study"].get("port", 5173))
    url = f"http://{args.host}:{port}"
    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    app.run(host=args.host, port=port, debug=False)
    return 0


def handle_collect(args: argparse.Namespace) -> int:
    runtime = load_runtime(Path(args.workspace))
    result = collect_videos(
        runtime,
        keywords=args.keywords,
        start_date=args.start_date,
        end_date=args.end_date,
        region_code=args.region_code,
    )
    json_print(result)
    return 0


def handle_transcribe(args: argparse.Namespace) -> int:
    runtime = load_runtime(Path(args.workspace))
    result = transcribe_workspace(runtime, use_whisper=args.whisper, whisper_only=args.whisper_only)
    json_print(result)
    return 0


def handle_judge(args: argparse.Namespace) -> int:
    runtime = load_runtime(Path(args.workspace))
    result = score_workspace(runtime, model=args.model)
    json_print(result)
    return 0


def handle_replace_sample(args: argparse.Namespace) -> int:
    runtime = load_runtime(Path(args.workspace))
    config = project_config_from_runtime(runtime)
    if args.replace_command == "inspect-slot":
        return handle_inspect_slot(args, config)
    if args.replace_command == "list-reserve":
        return handle_list_reserve(args, config)
    if args.replace_command == "replace-slot":
        return handle_replace_slot(args, config)
    raise ValueError(f"Unsupported replace-sample subcommand: {args.replace_command}")


def handle_export(args: argparse.Namespace) -> int:
    runtime = load_runtime(Path(args.workspace))
    output_dir = Path(args.output_dir) if args.output_dir else runtime.paths.exports_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    app = create_app(runtime)
    with app.app_context():
        from .dashboard.app import get_db, write_csv_snapshot

        conn = get_db()
        csv_path = output_dir / f"{runtime.raw_config['study']['slug']}_coding_export.csv"
        write_csv_snapshot(conn, csv_path)
    snapshot_path = output_dir / f"{runtime.raw_config['study']['slug']}_snapshot_{timestamp_slug()}.zip"
    create_snapshot_archive(runtime, snapshot_path)
    json_print({"csv_export": str(csv_path), "snapshot_zip": str(snapshot_path)})
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "init-demo":
        return handle_init_demo(args)
    if args.command == "init-study":
        return handle_init_study(args)
    if args.command == "import-legacy":
        return handle_import_legacy(args)
    if args.command == "run-dashboard":
        return handle_run_dashboard(args)
    if args.command == "collect":
        return handle_collect(args)
    if args.command == "transcribe":
        return handle_transcribe(args)
    if args.command == "judge":
        return handle_judge(args)
    if args.command == "replace-sample":
        return handle_replace_sample(args)
    if args.command == "export":
        return handle_export(args)
    parser.error(f"Unsupported command: {args.command}")
    return 1

