#!/usr/bin/env python3
"""Compare the vendored PrimeNumberTheoremAnd closure with its pinned source."""

from __future__ import annotations

import difflib
import hashlib
import sys
from pathlib import Path


VENDORED_FILES = (
    "PrimeNumberTheoremAnd/Consequences.lean",
    "PrimeNumberTheoremAnd/Defs.lean",
    "PrimeNumberTheoremAnd/Fourier.lean",
    "PrimeNumberTheoremAnd/Mathlib/Algebra/Notation/Support.lean",
    "PrimeNumberTheoremAnd/Mathlib/Analysis/Asymptotics/Asymptotics.lean",
    "PrimeNumberTheoremAnd/Mathlib/Analysis/SpecialFunctions/Log/Basic.lean",
    "PrimeNumberTheoremAnd/SmoothExistence.lean",
    "PrimeNumberTheoremAnd/Sobolev.lean",
    "PrimeNumberTheoremAnd/Wiener.lean",
)

MODIFICATION_NOTICE = """/-
MODIFICATION NOTICE (2026-08-02): this derivative omits the unused declaration
block consisting of `prelim_decay_2`, `AbsolutelyContinuous`, `prelim_decay_3`,
and `decay_alt`. The block is outside the transitive declaration-dependency
footprint of `WeakPNT` and `prime_between`; no retained declaration was changed.
See `THIRD_PARTY.md`.
-/

"""

OMITTED_BLOCK_START = '@[blueprint "prelim-decay-2"'
OMITTED_BLOCK_END = "lemma decay_bounds_key"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(message: str) -> None:
    print(f"third-party provenance check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        fail(f"cannot read {path}: {error}")


def inventory_difference(discovered: set[str]) -> tuple[set[str], set[str]]:
    registered = set(VENDORED_FILES)
    return registered - discovered, discovered - registered


def inventory_self_test() -> None:
    registered = set(VENDORED_FILES)
    extra_name = "PrimeNumberTheoremAnd/Unregistered.lean"
    missing_name = VENDORED_FILES[0]
    missing, extra = inventory_difference(registered | {extra_name})
    if missing or extra != {extra_name}:
        raise AssertionError("inventory check failed to reject an unregistered Lean file")
    missing, extra = inventory_difference(registered - {missing_name})
    if missing != {missing_name} or extra:
        raise AssertionError("inventory check failed to reject a missing registered Lean file")
    print("third-party Lean-source inventory self-test PASS")


def main() -> None:
    if len(sys.argv) not in (3, 4) or (len(sys.argv) == 4 and sys.argv[3] != "--show-diff"):
        fail("usage: verify_third_party.py VENDORED_ROOT UPSTREAM_ROOT [--show-diff]")

    vendored_root = Path(sys.argv[1]).resolve()
    upstream_root = Path(sys.argv[2]).resolve()
    show_diff = len(sys.argv) == 4

    inventory_self_test()
    source_root = vendored_root / "PrimeNumberTheoremAnd"
    try:
        symlinks = [path for path in source_root.rglob("*") if path.is_symlink()]
        if symlinks:
            fail(
                "symbolic links are forbidden in vendored sources: "
                + ", ".join(
                    sorted(path.relative_to(vendored_root).as_posix() for path in symlinks)
                )
            )
        discovered = {
            path.relative_to(vendored_root).as_posix()
            for path in source_root.rglob("*.lean")
            if path.is_file()
        }
    except OSError as error:
        fail(f"cannot enumerate vendored Lean sources: {error}")
    missing, extra = inventory_difference(discovered)
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append("missing registered files: " + ", ".join(sorted(missing)))
        if extra:
            details.append("unregistered files: " + ", ".join(sorted(extra)))
        fail("; ".join(details))
    print(f"vendored Lean-source inventory PASS: {len(discovered)} registered files")

    for relative in VENDORED_FILES[:-1]:
        local = read(vendored_root / relative)
        upstream = read(upstream_root / relative)
        if local != upstream:
            fail(f"undocumented difference in {relative}")
        print(f"exact upstream match: {relative} sha256={digest(local)}")

    relative = VENDORED_FILES[-1]
    local_bytes = read(vendored_root / relative)
    upstream_bytes = read(upstream_root / relative)
    try:
        local = local_bytes.decode("utf-8")
        upstream = upstream_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        fail(f"non-UTF-8 Lean source: {error}")

    if not local.startswith(MODIFICATION_NOTICE):
        fail(f"{relative} does not have the exact recorded modification notice")
    if upstream.count(OMITTED_BLOCK_START) != 1 or upstream.count(OMITTED_BLOCK_END) != 1:
        fail("the pinned upstream omission markers are not unique")
    start = upstream.index(OMITTED_BLOCK_START)
    end = upstream.index(OMITTED_BLOCK_END, start)
    expected_local = MODIFICATION_NOTICE + upstream[:start] + upstream[end:]
    if local != expected_local:
        fail(
            f"{relative} differs by more than the exact documented declaration-block omission"
        )

    print(
        "documented derivative match: "
        f"{relative} sha256={digest(local_bytes)}; omitted declarations = "
        "prelim_decay_2, AbsolutelyContinuous, prelim_decay_3, decay_alt"
    )

    local_license = read(vendored_root / "LICENSE-PrimeNumberTheoremAnd")
    upstream_license = read(upstream_root / "LICENSE")
    if local_license != upstream_license:
        fail("LICENSE-PrimeNumberTheoremAnd differs from the pinned upstream LICENSE")
    print(f"exact upstream match: LICENSE sha256={digest(local_license)}")

    if show_diff:
        print("--- transparent documented upstream-to-vendored diff ---")
        sys.stdout.writelines(
            difflib.unified_diff(
                upstream.splitlines(keepends=True),
                local.splitlines(keepends=True),
                fromfile=f"upstream/{relative}",
                tofile=f"vendored/{relative}",
            )
        )

    print("third-party provenance PASS")


if __name__ == "__main__":
    main()
