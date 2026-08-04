#!/usr/bin/env python3
"""Check the transitive project import closure of the direct paper route."""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path


IMPORT = re.compile(
    r"^[ \t]*(?:public\s+)?(?:meta\s+)?import\s+"
    r"(?:all\s+)?([^\s]+)",
    re.MULTILINE,
)
ROOTS = (
    "DegreeDiameter.Theorem11FromProposition31",
    "DegreeDiameter.Corollary12FromProposition31",
)
FORBIDDEN = {
    "DegreeDiameter.LowerBound",
    "DegreeDiameter.Construction",
}


def module_path(root: Path, module: str) -> Path:
    return root / (module.replace(".", "/") + ".lean")


def blank_comments_and_strings(source: str) -> str:
    """Replace Lean comments/strings by whitespace while preserving newlines."""
    output = list(source)
    state = "code"
    depth = 0
    index = 0
    while index < len(source):
        pair = source[index : index + 2]
        char = source[index]
        if state == "code":
            if pair == "--":
                output[index] = output[index + 1] = " "
                state = "line-comment"
                index += 2
                continue
            if pair == "/-":
                output[index] = output[index + 1] = " "
                state = "block-comment"
                depth = 1
                index += 2
                continue
            if char == '"':
                output[index] = " "
                state = "string"
                index += 1
                continue
            index += 1
            continue
        if state == "line-comment":
            if char == "\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "block-comment":
            if pair == "/-":
                output[index] = output[index + 1] = " "
                depth += 1
                index += 2
                continue
            if pair == "-/":
                output[index] = output[index + 1] = " "
                depth -= 1
                index += 2
                if depth == 0:
                    state = "code"
                continue
            if char != "\n":
                output[index] = " "
            index += 1
            continue
        if state == "string":
            if char == "\\" and index + 1 < len(source):
                output[index] = output[index + 1] = " "
                index += 2
                continue
            if char == '"':
                output[index] = " "
                state = "code"
            elif char != "\n":
                output[index] = " "
            index += 1
    return "".join(output)


def direct_imports(root: Path, module: str) -> list[str]:
    path = module_path(root, module)
    if not path.is_file():
        raise RuntimeError(f"missing local module {module} at {path}")
    source = blank_comments_and_strings(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for imported in IMPORT.findall(source):
        if "«" in imported or "»" in imported:
            raise RuntimeError(
                f"quoted module segment is forbidden by the import audit: {imported}"
            )
        imports.append(imported)
    return imports


def closure(root: Path, start: str) -> set[str]:
    if not module_path(root, start).is_file():
        raise RuntimeError(f"missing audit-root module {start}")
    seen: set[str] = set()
    work = [start]
    while work:
        module = work.pop()
        if module in seen:
            continue
        seen.add(module)
        for imported in direct_imports(root, module):
            # Follow every module supplied by this source tree, even if it is
            # placed outside the `DegreeDiameter` namespace. Missing paths are
            # dependencies supplied externally by Lean/Lake.
            if module_path(root, imported).is_file():
                work.append(imported)
    return seen


def self_test() -> None:
    fixture_parent = Path.cwd() / ".audit-tmp"
    fixture_parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="import-isolation-", dir=fixture_parent
    ) as fixture_name:
        fixture = Path(fixture_name)
        (fixture / "DegreeDiameter").mkdir()
        (fixture / "Root.lean").write_text(
            "import Bridge\nimport Mathlib.Data.Nat.Basic\n", encoding="utf-8"
        )
        (fixture / "RootQuoted.lean").write_text(
            "import DegreeDiameter.«LowerBound»\n", encoding="utf-8"
        )
        (fixture / "RootMeta.lean").write_text("meta import Bridge\n", encoding="utf-8")
        (fixture / "RootSplit.lean").write_text(
            "import /-\nsplit import token\n-/ DegreeDiameter.LowerBound\n",
            encoding="utf-8",
        )
        (fixture / "RootNested.lean").write_text(
            "import /- outer /- nested -/ comment -/ Bridge\n", encoding="utf-8"
        )
        (fixture / "RootLineComment.lean").write_text(
            "import -- split by a line comment\n  Bridge\n", encoding="utf-8"
        )
        (fixture / "Bridge.lean").write_text(
            "import DegreeDiameter.LowerBound\n", encoding="utf-8"
        )
        (fixture / "DegreeDiameter/LowerBound.lean").write_text("", encoding="utf-8")
        modules = closure(fixture, "Root")
        if "Bridge" not in modules or "DegreeDiameter.LowerBound" not in modules:
            raise AssertionError(
                "local cross-namespace Bridge failed to expose forbidden LowerBound import"
            )
        if not modules & FORBIDDEN:
            raise AssertionError("Bridge fixture should fail the production forbidden-module test")
        meta_modules = closure(fixture, "RootMeta")
        if "Bridge" not in meta_modules or not meta_modules & FORBIDDEN:
            raise AssertionError("meta import fixture failed to expose the Bridge route")
        for split_root in ("RootSplit", "RootNested", "RootLineComment"):
            split_modules = closure(fixture, split_root)
            if not split_modules & FORBIDDEN:
                raise AssertionError(
                    f"comment-split import fixture {split_root} failed to expose LowerBound"
                )
        try:
            closure(fixture, "RootQuoted")
        except RuntimeError as error:
            if "quoted module segment" not in str(error):
                raise
        else:
            raise AssertionError(
                "quoted import fixture should be rejected before it can alias LowerBound"
            )
    try:
        fixture_parent.rmdir()
    except OSError:
        pass
    print(
        "import-isolation ordinary/Bridge/meta/quoted/comment-split regression "
        "self-test PASS"
    )


def main() -> None:
    arguments = sys.argv[1:]
    if arguments and arguments[0] == "--self-test":
        self_test()
        arguments = arguments[1:]
    if len(arguments) != 1:
        raise SystemExit(
            "usage: check_import_isolation.py [--self-test] REPOSITORY_ROOT"
        )
    root = Path(arguments[0]).resolve()
    for start in ROOTS:
        try:
            modules = closure(root, start)
        except (OSError, UnicodeError, RuntimeError) as error:
            print(f"import-isolation check failed: {error}", file=sys.stderr)
            raise SystemExit(1) from error
        bad = sorted(modules & FORBIDDEN)
        if bad:
            print(
                f"import-isolation check failed: {start} transitively imports "
                + ", ".join(bad),
                file=sys.stderr,
            )
            raise SystemExit(1)
        print(
            f"import-isolation PASS: {start} closure has {len(modules)} local modules "
            "and excludes LowerBound/Construction"
        )


if __name__ == "__main__":
    main()
