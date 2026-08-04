import DegreeDiameter.AsymptoticsLimits
import PrimeNumberTheoremAnd.Consequences

/-!
# Main degree--diameter consequences

These wrappers discharge the abstract prime-interval premise of the analytic reduction using the
proved prime-number-theorem consequence `prime_between`.  Thus the only remaining hypothesis of
the exported results is the finite-geometry construction
`AsymptoticHalvedWitnessHypothesis`.
-/

open Filter

namespace DegreeDiameter

lemma primeIntervalHypothesis_of_primeNumberTheorem : PrimeIntervalHypothesis := by
  intro η hη
  exact prime_between hη

/-- Theorem 1.1 reduced to the halved-flag construction. -/
theorem theorem_1_1_of_asymptoticHalvedWitness
    (hw : AsymptoticHalvedWitnessHypothesis) {k : ℕ} (hk : 0 < k) :
    Tendsto (fun d : ℕ ↦ (nKD k d : ℝ) / (d : ℝ) ^ k) atTop (nhds 1) :=
  theorem_1_1_of_prime_intervals primeIntervalHypothesis_of_primeNumberTheorem hw hk

/-- Corollary 1.2 reduced to the halved-flag construction. -/
theorem corollary_1_2_of_asymptoticHalvedWitness
    (hw : AsymptoticHalvedWitnessHypothesis)
    {ell : ℕ} (hell : 2 ≤ ell) :
    1 ≤ liminf (fun d : ℕ ↦ (h ell d : ℝ) / (d : ℝ) ^ ell) atTop :=
  corollary_1_2_of_prime_intervals primeIntervalHypothesis_of_primeNumberTheorem hw hell

end DegreeDiameter
