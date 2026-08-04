#!/usr/bin/env python3
"""Idempotently append source-integrity metadata to GitHub release notes."""

from __future__ import annotations

import re
import sys
from pathlib import Path


START = "<!-- degree-diameter-source-integrity:start -->"
END = "<!-- degree-diameter-source-integrity:end -->"


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: append_release_integrity.py NOTES_FILE ARCHIVE_NAME SHA256"
        )

    notes_path = Path(sys.argv[1])
    archive_name = sys.argv[2]
    digest = sys.argv[3]
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise SystemExit("invalid SHA-256 digest")

    notes = notes_path.read_text(encoding="utf-8")
    old_block = re.compile(
        rf"\n*{re.escape(START)}.*?{re.escape(END)}\n*", re.DOTALL
    )
    notes = old_block.sub("\n", notes).rstrip()
    block = (
        f"{START}\n"
        "## Formalization source integrity\n\n"
        f"- Archive: `{archive_name}`\n"
        f"- SHA-256: `{digest}`\n"
        "- The attached `.sha256` file contains the same digest.\n"
        f"{END}\n"
    )
    notes_path.write_text(notes + "\n\n" + block, encoding="utf-8")


if __name__ == "__main__":
    main()
