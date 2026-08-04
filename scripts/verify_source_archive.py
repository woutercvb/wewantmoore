#!/usr/bin/env python3
"""Validate a ZIP source release without extracting it."""

from __future__ import annotations

import collections
import re
import stat
import sys
import zipfile
from pathlib import PurePosixPath


FORBIDDEN_CACHE_PARTS = {
    ".git",
    ".lake",
    ".audit-tmp",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}
FORBIDDEN_COMPILED_SUFFIXES = {".olean", ".ilean", ".pyc", ".pyo"}


def fail(message: str) -> None:
    print(f"source-archive check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: verify_source_archive.py SOURCE.zip")

    archive = sys.argv[1]
    try:
        with zipfile.ZipFile(archive, "r") as source_zip:
            infos = source_zip.infolist()
            if not infos:
                fail("archive is empty")

            names = [info.filename for info in infos]
            duplicates = sorted(
                name for name, count in collections.Counter(names).items() if count > 1
            )
            if duplicates:
                fail("duplicate entries: " + ", ".join(duplicates))

            canonical_names: dict[str, str] = {}
            for info in infos:
                name = info.filename
                if not name or "\x00" in name:
                    fail("empty or NUL-containing archive path")
                if "\\" in name:
                    fail(f"backslash path separator in {name!r}")
                if re.match(r"^[A-Za-z]:", name):
                    fail(f"Windows absolute path in {name!r}")

                raw_name = name[:-1] if name.endswith("/") else name
                raw_parts = raw_name.split("/")
                if any(part in ("", ".", "..") for part in raw_parts):
                    fail(f"non-canonical or traversing path in {name!r}")

                path = PurePosixPath(name)
                if path.is_absolute():
                    fail(f"absolute path in {name!r}")

                canonical = "/".join(path.parts).casefold()
                if canonical in canonical_names:
                    fail(
                        "case-insensitive/canonical path collision: "
                        f"{canonical_names[canonical]!r} and {name!r}"
                    )
                canonical_names[canonical] = name

                if any(part.casefold() in FORBIDDEN_CACHE_PARTS for part in path.parts):
                    fail(f"build/VCS cache path included: {name!r}")
                if path.suffix.casefold() in FORBIDDEN_COMPILED_SUFFIXES:
                    fail(f"compiled/cache artifact included: {name!r}")
                if info.flag_bits & 0x1:
                    fail(f"encrypted entry included: {name!r}")

                mode = (info.external_attr >> 16) & 0o177777
                if mode and stat.S_ISLNK(mode):
                    fail(f"symbolic link included: {name!r}")
                if mode and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                    fail(f"non-regular filesystem entry included: {name!r}")

            bad_crc = source_zip.testzip()
            if bad_crc is not None:
                fail(f"ZIP CRC/integrity failure at {bad_crc!r}")
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as error:
        fail(f"cannot validate {archive}: {error}")

    print(
        f"source-archive PASS: {len(infos)} entries; no duplicate, traversing, "
        "absolute, symlink, cache, .olean, .ilean, .pyc, or .pyo entries; ZIP CRC valid"
    )


if __name__ == "__main__":
    main()
