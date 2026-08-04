#!/usr/bin/env python3
"""Enforce completeness of the generated declaration-dependency report."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_TARGETS = {
    "DegreeDiameter.theorem_1_1_from_proposition_3_1",
    "DegreeDiameter.corollary_1_2_from_proposition_3_1",
    "DegreeDiameter.theorem_1_1",
    "DegreeDiameter.corollary_1_2",
}

PASS_RECORD = re.compile(
    r"dependency audit PASS:\s*([A-Za-z0-9_'.]+)\s*$", re.MULTILINE
)
LEAN_ERROR = re.compile(r"(?:^|\s)error:", re.MULTILINE | re.IGNORECASE)


class PolicyError(ValueError):
    pass


def validate_report(text: str) -> None:
    if LEAN_ERROR.search(text):
        raise PolicyError("report contains a Lean error")

    records = PASS_RECORD.findall(text)
    if len(records) != len(set(records)):
        duplicates = sorted(
            target for target in set(records) if records.count(target) > 1
        )
        raise PolicyError("duplicate PASS targets: " + ", ".join(duplicates))

    found = set(records)
    missing = sorted(REQUIRED_TARGETS - found)
    unexpected = sorted(found - REQUIRED_TARGETS)
    problems: list[str] = []
    if missing:
        problems.append("missing targets: " + ", ".join(missing))
    if unexpected:
        problems.append("unexpected targets: " + ", ".join(unexpected))
    if problems:
        raise PolicyError("; ".join(problems))


def self_test() -> None:
    def report(targets: list[str]) -> str:
        return "".join(
            f"DependencyAudit.lean:1:0: info: dependency audit PASS: {target}\n"
            for target in targets
        )

    valid = sorted(REQUIRED_TARGETS)
    validate_report(report(valid))

    invalid_reports = (
        report(valid[:-1]),
        report(valid + [valid[0]]),
        report(valid + ["DegreeDiameter.unregistered_result"]),
        report(valid) + "DependencyAudit.lean:1:0: error: synthetic failure\n",
    )
    for invalid in invalid_reports:
        try:
            validate_report(invalid)
        except PolicyError:
            continue
        raise AssertionError("dependency-report policy accepted an invalid regression fixture")
    print("dependency-report policy self-test PASS")


def main() -> None:
    arguments = sys.argv[1:]
    ran_self_test = False
    if arguments and arguments[0] == "--self-test":
        self_test()
        ran_self_test = True
        arguments = arguments[1:]
    if ran_self_test and not arguments:
        return
    if len(arguments) != 1:
        raise SystemExit(
            "usage: check_dependency_report.py [--self-test] DEPENDENCY_REPORT"
        )

    report = Path(arguments[0])
    try:
        text = report.read_text(encoding="utf-8")
        validate_report(text)
    except (OSError, UnicodeError, PolicyError) as error:
        print(f"dependency-report policy failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(
        f"dependency-report policy PASS: {len(REQUIRED_TARGETS)} exact required targets"
    )


if __name__ == "__main__":
    main()
