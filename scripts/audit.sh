#!/bin/sh
set -eu

python3 scripts/scan_lean_trust.py --self-test --expect-count 38 .
python3 scripts/check_import_isolation.py --self-test .

if rg -n \
    'AsymptoticHalvedWitness|asymptoticHalvedWitnessHypothesis|natCard_evenPartialFlag_lower|import DegreeDiameter\.(LowerBound|Construction)' \
    DegreeDiameter/Theorem11FromProposition31.lean \
    DegreeDiameter/Corollary12FromProposition31.lean; then
  echo "principal Proposition 3.1 derivation depends on the alternative witness" >&2
  exit 1
fi

lake build
lake env lean DegreeDiameter/Audit.lean >axiom-audit.txt 2>&1
cat axiom-audit.txt
python3 scripts/check_axiom_allowlist.py axiom-audit.txt

lake env lean DegreeDiameter/DependencyAudit.lean >dependency-audit.txt 2>&1
cat dependency-audit.txt
python3 scripts/check_dependency_report.py --self-test dependency-audit.txt
