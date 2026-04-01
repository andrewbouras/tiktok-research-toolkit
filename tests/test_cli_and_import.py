import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tiktok_research.cli import main as cli_main
from tiktok_research.config import load_runtime
from tiktok_research.legacy import import_legacy_workspace
from tiktok_research.workspace import init_demo_workspace
from tiktok_research.workbook import create_template_workbook


class CliAndImportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="tiktok-toolkit-cli-tests-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_demo_cli_creates_workspace(self) -> None:
        workspace = self.temp_dir / "demo"
        code = cli_main(["init-demo", str(workspace)])
        self.assertEqual(code, 0)
        runtime = load_runtime(workspace)
        self.assertEqual(runtime.raw_config["study"]["name"], "TikTok Research Toolkit Demo")
        self.assertTrue(runtime.paths.workbook_path.exists())
        self.assertTrue(runtime.paths.metadata_json_path.exists())

    def test_import_legacy_copies_core_inputs(self) -> None:
        legacy_root = self.temp_dir / "legacy"
        legacy_root.mkdir()
        workbook = legacy_root / "legacy.xlsx"
        create_template_workbook(
            workbook,
            videos=[
                {
                    "video_id": "VID001",
                    "id": "9999999999999999991",
                    "username": "legacydemo",
                    "view_count": 10,
                    "like_count": 2,
                    "comment_count": 1,
                    "share_count": 0,
                    "post_date": "2025-01-01",
                }
            ],
        )
        metadata_json = legacy_root / "collected_videos.json"
        metadata_json.write_text(
            json.dumps(
                [
                    {
                        "id": "9999999999999999991",
                        "username": "legacydemo",
                        "view_count": 10,
                        "like_count": 2,
                        "comment_count": 1,
                        "share_count": 0,
                        "create_time": 1735689600,
                        "video_description": "legacy import smoke test",
                    }
                ]
            ),
            encoding="utf-8",
        )
        transcripts_dir = legacy_root / "transcripts"
        transcripts_dir.mkdir()
        (transcripts_dir / "VID001.txt").write_text("legacy transcript", encoding="utf-8")

        imported = self.temp_dir / "imported"
        runtime = import_legacy_workspace(
            imported,
            workbook_path=workbook,
            metadata_json_path=metadata_json,
            transcripts_dir=transcripts_dir,
        )
        self.assertTrue(runtime.paths.workbook_path.exists())
        self.assertTrue(runtime.paths.metadata_json_path.exists())
        self.assertTrue((runtime.paths.transcripts_dir / "VID001.txt").exists())

