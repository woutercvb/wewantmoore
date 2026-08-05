# Asymptotically attaining the Moore bound — Lean 4 formalization

This repository formalizes the central theorem chain of the 4 August 2026
preprint *Asymptotically attaining the Moore bound* by W. Cames van Batenburg and
S. Korsky, available at https://arxiv.org/abs/2608.03965 

The AI-assisted formalization was carried out in the final phase of the project,
based on the 3 August 2026 version of the draft. No mathematically relevant changes where made between then and submission.

The formalized chain consists of Lemma 2.1, Proposition 3.1 including equations
(6)--(9), Theorem 1.1, Lemma 4.1, and Corollary 1.2. The graph extrema and
constructions use `SimpleGraph.ediam`.

## Main declarations

The principal exports are:

1. `DegreeDiameter.common_basis_orderings`, the common-basis/permutation step
   used in Lemma 2.1;
2. `DegreeDiameter.alternating_route`, Lemma 2.1;
3. `DegreeDiameter.proposition_3_1`, containing the finite claims in equations
   (6)--(8) and both actual-degree limits in equation (9), for one concrete
   graph family over every prime-power field order;
4. `DegreeDiameter.theorem_1_1`;
5. `DegreeDiameter.lemma_4_1` and its bounded form
   `DegreeDiameter.lemma_4_1_le`; and
6. `DegreeDiameter.corollary_1_2`.

The public versions of Theorem 1.1 and Corollary 1.2 use the concrete
Proposition 3.1 family. Separate big-cell proofs remain available as
`theorem_1_1_via_big_cell` and `corollary_1_2_via_big_cell`.

## Build and verification

The project is pinned to Lean `v4.32.2`, Mathlib commit
`905b95818eb32af7874a58b427f50c1711a5e96c`, and LeanArchitect commit
`d9013cc08bd2b5483e837368dfa4cc7ead92a5c2`.

From a clean checkout, run:

```sh
lake build
sh scripts/audit.sh
```

The separate provenance check uses the network to compare the vendored
PrimeNumberTheoremAnd files with their recorded upstream commit:

```sh
sh scripts/verify_third_party.sh
```

The audit scans the Lean sources for proof holes and prohibited trust
mechanisms, rebuilds the project, regenerates `axiom-audit.txt`, checks the
standard-axiom allowlist, and verifies the dependency route of the public final
theorems. See `RELEASE_AND_REPRODUCIBILITY.md` for the full clean-checkout and
release procedure.

## Proof organization

- `CommonBasis.lean`, `OddEvenRoute.lean`, and `Lemma21.lean` contain the
  common-basis argument and odd--even route for Lemma 2.1.
- `CompletionCount.lean`, `FlagEnumeration.lean`, and `ExactOrder.lean` prove
  the completion multiplicities and exact order formula.
- `Symmetry.lean`, `ExactDiameter.lean`, and `Proposition31.lean` establish
  regularity, the degree cap, and exact diameter for the concrete graph.
- `FiniteFieldModels.lean`, `Proposition31Asymptotics.lean`, and
  `Proposition31Full.lean` establish and package equations (6)--(9) over all
  prime-power field orders.
- `Theorem11FromProposition31.lean` proves Theorem 1.1 from that package, prime
  interpolation, and the Moore bound.
- `EdgeReduction.lean` and `Corollary12FromProposition31.lean` contain Lemma
  4.1 and the proof of Corollary 1.2.
- `LowerBound.lean`, `Construction.lean`, and `AsymptoticsLimits.lean` contain
  the independent big-cell proof route.

`WRITEUP_ALIGNMENT.md` gives a declaration-by-declaration map between the
formalization and the draft.

## Proof correspondence and scope

The formalization follows the paper's principal construction and most of its
proof architecture, but it is not a line-by-line transcription. In particular:

- the paper treats `k = 1` in Theorem 1.1 using the complete graph, whereas the
  Lean proof applies the Proposition 3.1 construction uniformly for every
  positive `k`;
- Lean proves the order/cap asymptotic through polynomial leading terms rather
  than formalizing the displayed `O_k(q⁻¹)` estimates; and
- prime interpolation chooses a suitably close prime rather than defining the
  largest prime below the paper's threshold.

These differences do not change the exported statements. The Lean
representation of partial flags is also extensionally equivalent, rather than
definitionally identical, to the tuple notation in the draft.

The following are outside the kernel-checked scope:

- the explicit `O_k(q⁻¹)` and `O_k(q⁻²)` error rates and the quantitative
  remark;
- the bipartite-restricted exact limit that uses a separately cited external
  odd-cycle-free upper bound; and
- historical and bibliographical assertions not needed for the central
  theorem chain.

## Third-party source and license

The project source is distributed under Apache-2.0. The vendored
PrimeNumberTheoremAnd material is separately identified and licensed; see
`THIRD_PARTY.md` and `LICENSE-PrimeNumberTheoremAnd`.
