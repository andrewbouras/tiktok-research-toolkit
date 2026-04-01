from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


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
        "TikTokResearchToolkit",
        str(REPO_ROOT / "src" / "tiktok_research" / "desktop.py"),
    ]
    subprocess.run(command, check=True, cwd=REPO_ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

