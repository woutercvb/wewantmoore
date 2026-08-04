# Write-up alignment

This document maps the 3 August 2026 draft *Asymptotically attaining the Moore
bound* by W. Cames van Batenburg and S. Korsky to kernel-checked declarations
in this project.  The project formalizes the central theorem chain—Lemma 2.1,
Proposition 3.1, Theorem 1.1, Lemma 4.1, and Corollary 1.2—and records the
remaining scope boundaries explicitly.

## Exact final statements

The paper's `n_k(d)` is `DegreeDiameter.nKD k d`.  `OrderAdmissible` requires
a finite simple graph of exactly the stated order, maximum degree at most `d`,
and extended diameter at most `k`; `nKD_isGreatest` proves the maximum
specification.  The convention `h_ell(d)-1 = maximum edge count` is encoded by
`DegreeDiameter.h`, and `h_sub_one_isGreatest` proves that specification.

```lean
theorem theorem_1_1 {k : ℕ} (hk : 0 < k) :
    Tendsto (fun d : ℕ ↦ (nKD k d : ℝ) / (d : ℝ) ^ k) atTop (nhds 1)

theorem corollary_1_2 {ell : ℕ} (hell : 2 ≤ ell) :
    1 ≤ liminf (fun d : ℕ ↦ (h ell d : ℝ) / (d : ℝ) ^ ell) atTop
```

Both principal exports call the direct Proposition 3.1 derivations.  The
independent big-cell/witness derivations remain available under explicitly
alternative names.

## Lemma 2.1 and the common-basis step

`CommonBasis.lean` proves the standard fact used at the beginning of the
write-up's argument; it is not postulated as a building axiom.  Its
principal statement is:

```lean
theorem common_basis_orderings {n : ℕ}
    (F F' : CompleteFlag K V n) :
    ∃ (b : Basis (Fin n) K V) (π : Equiv.Perm (Fin n)),
      (∀ i, F i = Submodule.span K (b '' {j | j.castSucc < i})) ∧
      (∀ i, F' i = Submodule.span K (b '' PrefixSet π i))
```

The proof constructs the common basis from successive
intersection-dimension jumps, proves its linear independence, obtains the
permutation, and verifies both prefix-span identities.  `alternating_route`
then invokes `common_basis_orderings`, invokes the separately proved
`n`-round odd--even transposition route, and takes prefix spans.  This is the
formal Lemma 2.1.

## Proposition 3.1 and equations (6)--(9)

For fixed positive `k`, `Proposition31Graph K k` is the compatibility graph on
even partial flags in the `(2k+1)`-dimensional `FlagSpace K k`.
`proposition31Degree K k` is the actual neighbor-set cardinality at a fixed
coordinate flag; transitivity proves that it is the common degree.  The cap
`proposition31DegreeCap q k` remains an upper bound, never an asserted degree
equality.

The equation map is:

| Write-up equation | Content | Principal Lean declarations |
|---|---|---|
| (6) | `N_q = [2k+1]_q!/(q+1)^k` | `natCard_evenPartialFlag_mul_completion_eq_qFactorial`, then `natCard_evenPartialFlag_eq_qFactorial_div` |
| (7) | `Δ_q ≤ (q+1)^k((q+1)^k-1)` | `halvedFlagGraph_natCard_neighborSet_le_sharp` |
| (8) | `diam H_{k,q}=k` | `halvedFlagGraph_ediam_eq_ofBasis` |
| (9) | `Δ_q/K_q → 1` and `N_q/Δ_q^k → 1` | `proposition31_degree_div_cap_tendsto_one`, `proposition31_order_div_degree_pow_tendsto_one` |

The exact finite counting used in equation (6) is exposed in independently
auditable stages:

| Finite-geometric step | Lean declaration | Content |
|---|---|---|
| A rank-two interval has `q+1` choices | `intermediateSubspaceEquivProjectiveLine`, `natCard_intermediate_eq` | Genuine quotient/pullback equivalence |
| Every even flag has `(q+1)^k` odd completions | `evenCompletionEquiv`, `natCard_odd_compatible_eq` | Explicit assembly map with both inverse laws |
| Every odd flag has `(q+1)^k` even completions | `oddCompletionEquiv`, `natCard_even_compatible_eq` | Dual explicit equivalence |
| Complete flags number `[2k+1]_q!` | `natCard_completeFlag_of_finrank` | Adapted-basis equivalence and exact tuple count |
| Complete flags correspond to compatible parity pairs | `completeFlagEquivCompatiblePartialFlagPair` | Exact finite-fibre double count |

`proposition_3_1_over_finite_field` packages the finite assertions over an
arbitrary finite field.  `proposition_3_1_for_prime_power` instantiates them
over a field whose cardinality is exactly any `q : PrimePowerIndex`.
`tendsto_primePowerIndex_val` makes the all-prime-power asymptotic index
literal and cofinal.  Finally, `Proposition31Full.lean` defines
`Proposition31FiniteClaims` and proves:

```lean
theorem proposition_3_1 (k : ℕ) (hk : 0 < k) :
    (∀ q : PrimePowerIndex, Proposition31FiniteClaims q k) ∧
    Tendsto
      (fun q ↦ (proposition31PrimePowerDegree k q : ℝ) /
        (proposition31DegreeCap q.1 k : ℝ)) atTop (nhds 1) ∧
    Tendsto
      (fun q ↦ (proposition31PrimePowerOrder k q : ℝ) /
        (proposition31PrimePowerDegree k q : ℝ) ^ k) atTop (nhds 1)
```

Thus one declaration contains all of Proposition 3.1, and both asymptotic
clauses refer to the same concrete graphs and their actual degree.

`Proposition31Full.lean` represents the finite clauses as a structure with the
named fields `regularity`, `order_mul`, `order_eq`, `degree_le_cap`, and
`ediam_eq`. The theorem
`proposition31_order_div_cap_pow_tendsto_one_from_proposition_3_1` obtains both
equation-(9) limits from `proposition_3_1` and proves

```text
N_q / K_q^k = (N_q / Delta_q^k) * (Delta_q / K_q)^k
```

with the necessary denominator nonzero facts. It is the order/cap bridge used
by Theorem 1.1.

## Theorem 1.1

Neutral ambient-space infrastructure is defined in `FlagSpace.lean` rather
than `LowerBound.lean`. Consequently, the transitive import closure of
`Theorem11FromProposition31.lean` does not contain `LowerBound.lean` or
`Construction.lean`. Its `theorem_1_1_from_proposition_3_1` follows the
write-up's principal dependency chain in mathematical substance: it binds
`proposition_3_1 k hk`, uses its finite claims and the named order/cap bridge,
uses the sharp cap and exact diameter, interpolates with primes in short
multiplicative intervals, and applies the Moore upper bound. The prime is
explicitly regarded as a `PrimePowerIndex`, and the interpolation proves the
needed comparison between its cap and the ambient degree.

There are two presentational differences. The write-up handles `k = 1` by a
complete graph, while this declaration applies the Proposition 3.1 route for
every positive `k`. The write-up selects the largest prime below its threshold,
while Lean selects an arbitrary prime in a sufficiently short multiplicative
interval. Both choices yield the stated limit.

`Results.theorem_1_1` is defined from this direct theorem.  The separate
`theorem_1_1_via_big_cell` provides an alternative coefficient-one big-cell
derivation; it is not the formal counterpart of the write-up's dependency
chain.

## Lemma 4.1 and Corollary 1.2

`EdgeReduction.lean` defines the bipartite expansion `bipartiteExpansion`,
proves its exact edge and regular-degree counts, and proves the line-graph
extended-diameter statement `lemma_4_1`.

`Corollary12FromProposition31.lean` proves
`corollary_1_2_from_proposition_3_1` directly from the same concrete graph's
actual order `N_q`, actual degree `Δ_q`, cap `K_q`, and a bound
`hP31 := proposition_3_1 k hk`. The edge-factor limit is constructed from the
two clauses `Δ_q/K_q → 1` and `N_q/Δ_q^k → 1` obtained from that same bundled
proof. The bipartite expansion has its exact edge count, and
`lemma_4_1_le` is the directly used inequality form of Lemma 4.1. The proof
retains the paper's `h_ell(d)-1` convention and handles the additive ones
formally. `Results.corollary_1_2` calls this direct theorem;
`corollary_1_2_via_big_cell` is the independent alternative.

## Formalization structure

Short export wrappers are consolidated, while the mathematically substantive
steps remain separate. In particular, the common-basis theorem,
projective-line equivalence, completion bijections, flag enumeration, exact
double count, and actual-degree squeeze are kept as named declarations so that
they can be inspected independently.

The formal proofs are faithful in mathematical substance but are not intended
to be line-by-line transcriptions. Some asymptotic calculations are
implemented through polynomial leading terms rather than explicit `O_k`
notation, and the Lean representation of partial flags is extensionally
equivalent to the tuple notation used in the paper.

## Scope

Fully formalized central statements:

- Lemma 2.1;
- Proposition 3.1, equations (6)--(9);
- Theorem 1.1;
- Lemma 4.1;
- Corollary 1.2.

Present as alternative proofs or supporting lemmas:

- the exact big-cell lower bound;
- the weak `AsymptoticHalvedWitness` route.

Not yet formalized:

- the explicit `O_k(q⁻¹)` and `O_k(q⁻²)` rates in the prose and
  quantitative remark;
- the bipartite-restricted exact limit obtained using the cited external
  odd-cycle-free upper bound, along with its restricted extremal-function API;
- broader bibliographical assertions unnecessary for the central chain.

No unformalized external theorem is counted as kernel-checked here.

## Trust and reproducibility

`scripts/audit.sh` scans proof sources for proof holes, assumption declarations,
and prohibited trust mechanisms; builds the pinned project; regenerates
`axiom-audit.txt`; and validates every printed axiom name against the exact
allowlist `propext`, `Classical.choice`, and `Quot.sound`. `Audit.lean` names
all critical targets explicitly, so a missing declaration is an elaboration
error. `DependencyAudit.lean` recursively traverses declaration bodies: the
two direct proofs and public exports must depend on the bundled Proposition
3.1, the theorem must depend on the Moore bound, the corollary must depend on
the inequality form of Lemma 4.1, and none may depend on the weak witness,
big-cell lower bound, or alternative final theorems—even behind an alias.

The SHA-pinned workflow records the clean-checkout build-and-audit procedure
and verifies the committed manifest and reports. This source tree does not
claim that a hosted workflow has already run; public immutable-revision and CI
evidence is an external publication step described in
`RELEASE_AND_REPRODUCIBILITY.md`.
