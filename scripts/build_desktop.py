from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"
APP_NAME = "TikTokResearchToolkit"


def release_archive_name() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower() or "unknown"
    return f"{APP_NAME}-{system}-{machine}"


def bundle_output() -> Path:
    executable_name = f"{APP_NAME}.exe" if sys.platform == "win32" else APP_NAME
    executable_path = DIST_DIR / executable_name
    if not executable_path.exists():
        raise FileNotFoundError(f"Expected PyInstaller output at {executable_path}")
    archive_path = shutil.make_archive(
        str(DIST_DIR / release_archive_name()),
        "zip",
        root_dir=DIST_DIR,
        base_dir=executable_name,
    )
    return Path(archive_path)


def main() -> int:
    pyinstaller = shutil.which("pyinstaller")
    if pyinstaller is None:
        print("pyinstaller is not installed. Install the desktop extra first.", file=sys.stderr)
        return 1
    command = [
        pyinstaller,
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name",
        APP_NAME,
        str(REPO_ROOT / "src" / "tiktok_research" / "desktop.py"),
    ]
    subprocess.run(command, check=True, cwd=REPO_ROOT)
    archive_path = bundle_output()
    print(f"Created desktop archive: {archive_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
