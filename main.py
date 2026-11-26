#!/usr/bin/env python3
"""Render the 26 November 2026 world-news front page and hand it over.

Running this file executes the drawing program that lives beside it,
then places the finished picture where the grading harness expects it:
inside the folder named by MAKEFUN_OUTPUT_DIR (or /output when that
variable is absent). Only the standard library is used, and nothing
here depends on the time of day, the network, or chance, so repeated
runs produce the same bytes.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE_NAME = "entry.png"


def build_picture() -> Path:
    """Run the drawing program and return the finished picture's path.

    The drawing program leaves entry.png in MAKEFUN_OUTPUT_DIR when that
    variable is set (the grader's writable output folder; the repository
    itself is read-only there), or beside this file otherwise.
    """
    painter = HERE / "draw.py"
    subprocess.run([sys.executable, str(painter)], cwd=HERE, check=True)
    drop_folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    for candidate in (drop_folder / PICTURE_NAME, HERE / PICTURE_NAME):
        if candidate.is_file():
            return candidate
    raise SystemExit("drawing program finished without leaving entry.png behind")


def main() -> int:
    picture = build_picture()
    drop_folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    drop_folder.mkdir(parents=True, exist_ok=True)
    target = drop_folder / PICTURE_NAME
    if picture.resolve() != target.resolve():
        shutil.copyfile(picture, target)
        target.chmod(0o644)
    print(f"front page ready: {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
