import DegreeDiameter.Results
import DegreeDiameter.FlagSpace
import DegreeDiameter.Proposition31
import DegreeDiameter.Proposition31Asymptotics
import DegreeDiameter.Proposition31Full
import DegreeDiameter.Theorem11FromProposition31
import DegreeDiameter.Corollary12FromProposition31

/-!
# Formalization of the fixed-diameter degree--diameter theorem

The exported results are:

* `DegreeDiameter.alternating_route` — Lemma 2.1;
* `DegreeDiameter.proposition_3_1` — the complete formal statement of
  Proposition 3.1, including equations (6)--(9), with the finite clauses
  exposed through the named fields of `DegreeDiameter.Proposition31FiniteClaims`;
* `DegreeDiameter.proposition_3_1_over_finite_field` — its finite-field
  finite-claims theorem;
* `DegreeDiameter.proposition_3_1_for_prime_power` — its all-prime-power
  instance;
* `DegreeDiameter.proposition31_degree_div_cap_tendsto_one` and
  `DegreeDiameter.proposition31_order_div_degree_pow_tendsto_one` — equation
  (9) for the actual graph family;
* `DegreeDiameter.proposition31_order_div_cap_pow_tendsto_one_from_proposition_3_1`
  — the order/cap bridge derived from the two bundled equation-(9) limits;
* `DegreeDiameter.theorem_1_1` — Theorem 1.1;
* `DegreeDiameter.corollary_1_2` — Corollary 1.2.
-/
