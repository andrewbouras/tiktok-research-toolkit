from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BLOCKED_GLOBS = [
    "*.sqlite3",
    "*.db",
    "*.mp3",
    "*.mp4",
    "*.m4a",
]
BLOCKED_PATH_PARTS = {
    "audio_cache",
    "transcripts",
    "llm_scores",
    "sample_replacement_archives",
}
ALLOWED_PREFIXES = {
    REPO_ROOT / "src",
    REPO_ROOT / "tests",
    REPO_ROOT / "docs",
    REPO_ROOT / ".github",
    REPO_ROOT / "scripts",
}
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"client_secret\s*=\s*[\"'][^\"']+[\"']", re.IGNORECASE),
    re.compile(r"client_key\s*=\s*[\"'][^\"']+[\"']", re.IGNORECASE),
]


def path_is_allowed(path: Path) -> bool:
    return any(path.is_relative_to(prefix) for prefix in ALLOWED_PREFIXES)


def main() -> int:
    violations: list[str] = []

    for pattern in BLOCKED_GLOBS:
        for path in REPO_ROOT.rglob(pattern):
            if ".git" in path.parts:
                continue
            violations.append(f"Blocked artifact type found: {path.relative_to(REPO_ROOT)}")

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in BLOCKED_PATH_PARTS for part in path.parts):
            if not path_is_allowed(path):
                violations.append(f"Blocked study artifact path found: {path.relative_to(REPO_ROOT)}")
        if path.suffix in {".png", ".jpg", ".jpeg", ".gif", ".svg"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                violations.append(f"Possible secret found in {path.relative_to(REPO_ROOT)}")

    if violations:
        for violation in violations:
            print(violation, file=sys.stderr)
        return 1

    print("publish_check: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

