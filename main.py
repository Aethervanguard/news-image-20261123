#!/usr/bin/env python3
"""news-image-20261123: place the pre-rendered front page at /output/entry.png.

The front page (entry.png, 1024x1024) was drawn with PIL and verified
locally: it sums up the world's news of Monday 23 November 2026, led by
the Papua forest fires. This program copies it into place using only the
standard library, so it runs in the grader's bare Python image (no PIL,
no fonts installed) and always writes byte-identical output.
"""
import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(here / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
