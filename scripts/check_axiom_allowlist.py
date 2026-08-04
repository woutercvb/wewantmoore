#!/usr/bin/env python3
"""Validate the generated `#print axioms` report against a fixed policy.

This check is intentionally independent of the committed report.  Updating
`axiom-audit.txt` therefore cannot hide a new axiom or the disappearance of a
required audit target.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

REQUIRED_TARGETS = {
    "WeakPNT",
    "prime_between",
    "DegreeDiameter.oddEvenRoute",
    "DegreeDiameter.common_apartment",
    "DegreeDiameter.common_basis_orderings",
    "DegreeDiameter.alternating_route",
    "DegreeDiameter.nKD_le_mooreBound",
    "DegreeDiameter.halvedFlagGraph_ediam_le",
    "DegreeDiameter.halvedFlagGraph_ediam_eq_ofBasis",
    "DegreeDiameter.intermediateSubspaceEquivProjectiveLine",
    "DegreeDiameter.natCard_intermediate_eq",
    "DegreeDiameter.evenCompletionEquiv",
    "DegreeDiameter.oddCompletionEquiv",
    "DegreeDiameter.natCard_odd_compatible_eq",
    "DegreeDiameter.natCard_even_compatible_eq",
    "DegreeDiameter.natCard_completeFlag_of_finrank",
    "DegreeDiameter.completeFlagEquivCompatiblePartialFlagPair",
    "DegreeDiameter.natCard_evenPartialFlag_mul_completion_eq_qFactorial",
    "DegreeDiameter.natCard_evenPartialFlag_eq_qFactorial_div",
    "DegreeDiameter.halvedFlagGraph_natCard_neighborSet_le_sharp",
    "DegreeDiameter.natCard_evenPartialFlag_lower",
    "DegreeDiameter.proposition_3_1_over_finite_field",
    "DegreeDiameter.proposition_3_1_for_prime_power",
    "DegreeDiameter.proposition31_finite_claims",
    "DegreeDiameter.proposition31_degree_div_cap_tendsto_one",
    "DegreeDiameter.proposition31_order_div_degree_pow_tendsto_one",
    "DegreeDiameter.proposition31_order_div_cap_pow_tendsto_one",
    "DegreeDiameter.proposition31_order_div_cap_pow_tendsto_one_from_proposition_3_1",
    "DegreeDiameter.proposition_3_1",
    "DegreeDiameter.asymptoticHalvedWitnessHypothesis",
    "DegreeDiameter.lemma_4_1_le",
    "DegreeDiameter.lemma_4_1",
    "DegreeDiameter.theorem_1_1_from_proposition_3_1",
    "DegreeDiameter.corollary_1_2_from_proposition_3_1",
    "DegreeDiameter.theorem_1_1",
    "DegreeDiameter.corollary_1_2",
    "DegreeDiameter.theorem_1_1_via_big_cell",
    "DegreeDiameter.corollary_1_2_via_big_cell",
}

RECORD = re.compile(
    r"^'([^'\n]+)' depends on axioms:\s*\[(.*?)\]\s*$",
    re.MULTILINE | re.DOTALL,
)


def fail(message: str) -> None:
    print(f"axiom allowlist check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: check_axiom_allowlist.py AXIOM_REPORT")

    report = Path(sys.argv[1])
    try:
        text = report.read_text(encoding="utf-8")
    except OSError as error:
        fail(f"cannot read {report}: {error}")

    records: dict[str, set[str]] = {}
    for target, body in RECORD.findall(text):
        if target in records:
            fail(f"duplicate report entry for {target}")
        names = {item.strip() for item in body.split(",") if item.strip()}
        records[target] = names

    missing = sorted(REQUIRED_TARGETS - records.keys())
    if missing:
        fail("missing required targets: " + ", ".join(missing))

    unexpected_targets = sorted(records.keys() - REQUIRED_TARGETS)
    if unexpected_targets:
        fail(
            "unregistered targets (update the policy deliberately): "
            + ", ".join(unexpected_targets)
        )

    violations = {
        target: sorted(axioms - ALLOWED_AXIOMS)
        for target, axioms in records.items()
        if axioms - ALLOWED_AXIOMS
    }
    if violations:
        detail = "; ".join(
            f"{target}: {', '.join(names)}"
            for target, names in sorted(violations.items())
        )
        fail("unexpected axioms: " + detail)

    print(
        f"axiom allowlist PASS: {len(records)} required declarations; "
        f"allowed set = {sorted(ALLOWED_AXIOMS)}"
    )


if __name__ == "__main__":
    main()
