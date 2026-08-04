#!/usr/bin/env python3
"""Lexically scan Lean source for project-forbidden trust mechanisms.

Comments and string literals are blanked before matching, so mathematical
prose may discuss words such as "constant" without causing false positives.
The lexer handles Lean's nested block comments.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


PROOF_HOLE_OR_BYPASS = re.compile(
    r"\b(?:sorry|admit|native_decide|implemented_by)\b|trustCompiler|by\?"
)

ASSUMPTION_DECLARATION = re.compile(
    r"\b(?:axiom|constants?|postulates?|opaque|unsafe|extern)\b"
)

IGNORED_SOURCE_TREES = {
    ".git",
    ".lake",
    ".audit-tmp",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}


def blank_comments_and_strings(source: str) -> str:
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
            continue

    return "".join(output)


def violations(source: str) -> list[tuple[int, int, str]]:
    clean = blank_comments_and_strings(source)
    found: list[tuple[int, int, str]] = []
    for pattern in (PROOF_HOLE_OR_BYPASS, ASSUMPTION_DECLARATION):
        for match in pattern.finditer(clean):
            line = clean.count("\n", 0, match.start()) + 1
            line_start = clean.rfind("\n", 0, match.start()) + 1
            column = match.start() - line_start + 1
            found.append((line, column, match.group(0).strip()))
    return sorted(found)


def self_test() -> None:
    forbidden = (
        "axiom bad : False\n",
        "private constant bad : False\n",
        "public postulate bad : False\n",
        "@[irreducible] opaque bad : Nat\n",
        "unsafe def bad := 1\n",
        "extern \"bad\" bad : Nat\n",
        "example : True := by sorry\n",
        "example : True := by admit\n",
        "example : True := by native_decide\n",
        "example : True := by?\n",
        "@[implemented_by bad] def x := 1\n",
    )
    wrapped_declarations = (
        "axiom bad : False",
        "constant bad : False",
        "postulate bad : False",
        "unsafe def bad := 1",
        "opaque bad : Nat",
        'extern "bad" bad : Nat',
    )
    forbidden += tuple(
        f"set_option autoImplicit false in {declaration}\n"
        for declaration in wrapped_declarations
    )
    for sample in forbidden:
        if not violations(sample):
            raise AssertionError(f"scanner failed to reject {sample!r}")

    permitted = (
        "/- nested /- axiom hidden : False -/ comment -/\nexample : True := by trivial\n",
        "-- constant hidden : False\nexample : True := by trivial\n",
        'def prose := "postulate hidden : False; by?; sorry"\n',
        "/-- A constant map. -/\ndef constantMap := 1\n",
    )
    for sample in permitted:
        if violations(sample):
            raise AssertionError(f"scanner falsely rejected {sample!r}")
    print("Lean trust-source scanner self-test PASS")


def lean_files(arguments: list[str]) -> list[Path]:
    files: list[Path] = []
    for argument in arguments:
        path = Path(argument)
        if path.is_dir():
            for current, directories, names in os.walk(path, topdown=True, followlinks=False):
                directories[:] = [
                    name for name in directories if name not in IGNORED_SOURCE_TREES
                ]
                current_path = Path(current)
                files.extend(
                    current_path / name for name in names if name.endswith(".lean")
                )
        elif path.suffix == ".lean":
            files.append(path)
        else:
            raise ValueError(f"not a Lean file or directory: {path}")
    return sorted(set(files))


def main() -> None:
    arguments = sys.argv[1:]
    expected_count: int | None = None
    if arguments and arguments[0] == "--self-test":
        self_test()
        arguments = arguments[1:]
    if arguments and arguments[0] == "--expect-count":
        if len(arguments) < 2:
            raise SystemExit("--expect-count requires a nonnegative integer")
        try:
            expected_count = int(arguments[1])
        except ValueError as error:
            raise SystemExit("--expect-count requires a nonnegative integer") from error
        if expected_count < 0:
            raise SystemExit("--expect-count requires a nonnegative integer")
        arguments = arguments[2:]
    if not arguments:
        if sys.argv[1:]:
            return
        raise SystemExit(
            "usage: scan_lean_trust.py [--self-test] [--expect-count N] PATH ..."
        )

    any_violation = False
    try:
        files = lean_files(arguments)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    if expected_count is not None and len(files) != expected_count:
        print(
            f"Lean trust-source inventory failed: expected {expected_count} files, "
            f"discovered {len(files)}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    for path in files:
        try:
            source = path.read_text(encoding="utf-8")
        except OSError as error:
            print(f"cannot read {path}: {error}", file=sys.stderr)
            any_violation = True
            continue
        for line, column, marker in violations(source):
            print(f"{path}:{line}:{column}: forbidden trust marker: {marker}")
            any_violation = True
    if any_violation:
        raise SystemExit(1)
    print(f"Lean trust-source scan PASS: {len(files)} files")


if __name__ == "__main__":
    main()
