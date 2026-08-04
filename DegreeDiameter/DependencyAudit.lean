import DegreeDiameter.Results
import Lean.Util.FoldConsts

/-!
Declaration-level dependency audit for the principal results.

Unlike a source-text search, this command recursively traverses the type and
kernel value of every referenced declaration.  Consequently, putting a
forbidden construction behind a newly introduced alias does not evade the
check.
-/

open Lean Elab Command

namespace DegreeDiameter.DependencyAudit

private partial def transitiveDependencies (env : Environment)
    (work : List Name) (seen : NameSet) : NameSet :=
  match work with
  | [] => seen
  | declName :: rest =>
      if seen.contains declName then
        transitiveDependencies env rest seen
      else
        let seen := seen.insert declName
        match env.checked.get.find? declName with
        | none => transitiveDependencies env rest seen
        | some info =>
            let direct := info.getUsedConstantsAsSet.toArray.toList
            transitiveDependencies env (direct ++ rest) seen

private def auditDeclaration (env : Environment) (target : Name)
    (required forbidden : List Name) : CommandElabM Unit := do
  unless (env.find? target).isSome do
    throwError m!"dependency audit target is missing: {target}"
  let deps := transitiveDependencies env [target] {}
  for requiredName in required do
    unless deps.contains requiredName do
      throwError m!"{target} does not depend on required declaration {requiredName}"
  for forbiddenName in forbidden do
    if deps.contains forbiddenName then
      throwError m!"{target} depends on forbidden declaration {forbiddenName}"
  logInfo m!"dependency audit PASS: {target}"

private def forbiddenAlternativeRoute : List Name := [
  ``DegreeDiameter.AsymptoticHalvedWitness,
  ``DegreeDiameter.AsymptoticHalvedWitnessHypothesis,
  ``DegreeDiameter.asymptoticHalvedWitnessHypothesis,
  ``DegreeDiameter.natCard_evenPartialFlag_lower,
  ``DegreeDiameter.theorem_1_1_of_asymptoticHalvedWitness,
  ``DegreeDiameter.corollary_1_2_of_asymptoticHalvedWitness,
  ``DegreeDiameter.theorem_1_1_of_prime_intervals,
  ``DegreeDiameter.corollary_1_2_of_prime_intervals,
  ``DegreeDiameter.theorem_1_1_via_big_cell,
  ``DegreeDiameter.corollary_1_2_via_big_cell
]

run_cmd do
  let env ← getEnv
  auditDeclaration env
    ``DegreeDiameter.theorem_1_1_from_proposition_3_1
    [``DegreeDiameter.proposition_3_1,
      ``DegreeDiameter.proposition31_order_div_cap_pow_tendsto_one_from_proposition_3_1,
      ``DegreeDiameter.nKD_le_mooreBound]
    forbiddenAlternativeRoute
  auditDeclaration env
    ``DegreeDiameter.corollary_1_2_from_proposition_3_1
    [``DegreeDiameter.proposition_3_1,
      ``DegreeDiameter.lemma_4_1_le]
    forbiddenAlternativeRoute
  auditDeclaration env
    ``DegreeDiameter.theorem_1_1
    [``DegreeDiameter.theorem_1_1_from_proposition_3_1,
      ``DegreeDiameter.proposition_3_1,
      ``DegreeDiameter.nKD_le_mooreBound]
    forbiddenAlternativeRoute
  auditDeclaration env
    ``DegreeDiameter.corollary_1_2
    [``DegreeDiameter.corollary_1_2_from_proposition_3_1,
      ``DegreeDiameter.proposition_3_1,
      ``DegreeDiameter.lemma_4_1_le]
    forbiddenAlternativeRoute

end DegreeDiameter.DependencyAudit
