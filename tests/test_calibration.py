import shutil
import tempfile
import unittest
from pathlib import Path

import tiktok_research.dashboard.app as dashboard_app
from tiktok_research.workspace import init_demo_workspace

from test_persistence import build_complete_payload


class CalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = Path(tempfile.mkdtemp(prefix="research-dashboard-calibration-tests-"))
        init_demo_workspace(cls.temp_dir)
        cls.app = dashboard_app.create_app(cls.temp_dir)
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def setUp(self) -> None:
        with self.app.app_context():
            conn = dashboard_app.get_db()
            conn.execute("DELETE FROM ratings")
            conn.execute("DELETE FROM calibration_ratings")
            conn.commit()

    def test_calibration_dataset_is_separate_from_main_study_sample(self) -> None:
        with self.app.app_context():
            conn = dashboard_app.get_db()
            overlap_count = conn.execute(
                """
                SELECT COUNT(*)
                FROM calibration_videos cv
                JOIN videos v
                  ON v.tiktok_numeric_id = cv.tiktok_numeric_id
                """
            ).fetchone()[0]
            calibration_count = conn.execute(
                "SELECT COUNT(*) FROM calibration_videos"
            ).fetchone()[0]

        self.assertEqual(overlap_count, 0)
        self.assertEqual(calibration_count, dashboard_app.CALIBRATION_VIDEO_COUNT)

    def test_calibration_route_uses_first_calibration_video(self) -> None:
        response = self.client.get("/calibration/reviewer-a", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/calibration/reviewer-a/videos/CAL001")

    def test_calibration_route_advances_to_next_calibration_video(self) -> None:
        self.client.post(
            "/api/calibration/reviewer-a/videos/CAL001",
            json={"responses": build_complete_payload()},
        )
        response = self.client.get("/calibration/reviewer-a", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/calibration/reviewer-a/videos/CAL002")

    def test_calibration_save_is_persisted_separately_from_main_ratings(self) -> None:
        self.client.post(
            "/api/calibration/reviewer-a/videos/CAL001",
            json={"responses": build_complete_payload("4")},
        )

        with self.app.app_context():
            conn = dashboard_app.get_db()
            main_count = conn.execute("SELECT COUNT(*) AS count FROM ratings").fetchone()["count"]
            calibration_count = conn.execute(
                "SELECT COUNT(*) AS count FROM calibration_ratings"
            ).fetchone()["count"]
            self.assertEqual(main_count, 0)
            self.assertEqual(calibration_count, 1)

        response = self.client.get("/researchers/reviewer-a", follow_redirects=False)
        self.assertEqual(response.headers["Location"], "/researchers/reviewer-a/videos/VID001")

    def test_calibration_dashboard_flags_discussion_for_score_mismatch(self) -> None:
        self.client.post(
            "/api/calibration/reviewer-a/videos/CAL001",
            json={"responses": build_complete_payload("2")},
        )
        self.client.post(
            "/api/calibration/reviewer-b/videos/CAL001",
            json={"responses": build_complete_payload("5")},
        )

        response = self.client.get("/calibration")
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("Needs discussion", body)
        self.assertIn("CAL001", body)
