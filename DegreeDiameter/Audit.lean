import DegreeDiameter.All

/-!
This module records the complete transitive logical footprint of the external
prime-interval input, the exact counting results, Proposition 3.1, its two
actual-family limits, and the principal exported results.  Every line
below must use only Lean/Mathlib's standard axioms (in this project normally
`propext`, `Classical.choice`, and `Quot.sound`).
-/

#print axioms WeakPNT
#print axioms prime_between

#print axioms DegreeDiameter.oddEvenRoute
#print axioms DegreeDiameter.common_apartment
#print axioms DegreeDiameter.common_basis_orderings
#print axioms DegreeDiameter.alternating_route

#print axioms DegreeDiameter.nKD_le_mooreBound
#print axioms DegreeDiameter.halvedFlagGraph_ediam_le
#print axioms DegreeDiameter.halvedFlagGraph_ediam_eq_ofBasis
#print axioms DegreeDiameter.intermediateSubspaceEquivProjectiveLine
#print axioms DegreeDiameter.natCard_intermediate_eq
#print axioms DegreeDiameter.evenCompletionEquiv
#print axioms DegreeDiameter.oddCompletionEquiv
#print axioms DegreeDiameter.natCard_odd_compatible_eq
#print axioms DegreeDiameter.natCard_even_compatible_eq
#print axioms DegreeDiameter.natCard_completeFlag_of_finrank
#print axioms DegreeDiameter.completeFlagEquivCompatiblePartialFlagPair
#print axioms DegreeDiameter.natCard_evenPartialFlag_mul_completion_eq_qFactorial
#print axioms DegreeDiameter.natCard_evenPartialFlag_eq_qFactorial_div
#print axioms DegreeDiameter.halvedFlagGraph_natCard_neighborSet_le_sharp
#print axioms DegreeDiameter.natCard_evenPartialFlag_lower
#print axioms DegreeDiameter.proposition_3_1_over_finite_field
#print axioms DegreeDiameter.proposition_3_1_for_prime_power
#print axioms DegreeDiameter.proposition31_finite_claims
#print axioms DegreeDiameter.proposition31_degree_div_cap_tendsto_one
#print axioms DegreeDiameter.proposition31_order_div_degree_pow_tendsto_one
#print axioms DegreeDiameter.proposition31_order_div_cap_pow_tendsto_one
#print axioms DegreeDiameter.proposition31_order_div_cap_pow_tendsto_one_from_proposition_3_1
#print axioms DegreeDiameter.proposition_3_1
#print axioms DegreeDiameter.asymptoticHalvedWitnessHypothesis

#print axioms DegreeDiameter.lemma_4_1_le
#print axioms DegreeDiameter.lemma_4_1

#print axioms DegreeDiameter.theorem_1_1_from_proposition_3_1
#print axioms DegreeDiameter.corollary_1_2_from_proposition_3_1
#print axioms DegreeDiameter.theorem_1_1
#print axioms DegreeDiameter.corollary_1_2
#print axioms DegreeDiameter.theorem_1_1_via_big_cell
#print axioms DegreeDiameter.corollary_1_2_via_big_cell
