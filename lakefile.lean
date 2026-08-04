import Lake

open Lake DSL

package «DegreeDiameterFormalization» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

require LeanArchitect from git
  "https://github.com/hanwenzhu/LeanArchitect.git" @
  "d9013cc08bd2b5483e837368dfa4cc7ead92a5c2"
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @
  "905b95818eb32af7874a58b427f50c1711a5e96c"

lean_lib PrimeNumberTheoremAnd

@[default_target]
lean_lib DegreeDiameter where
  roots := #[
    `DegreeDiameter.All,
    `DegreeDiameter.Asymptotics,
    `DegreeDiameter.AsymptoticsLimits,
    `DegreeDiameter.Audit,
    `DegreeDiameter.CommonBasis,
    `DegreeDiameter.CompletionCount,
    `DegreeDiameter.Construction,
    `DegreeDiameter.DependencyAudit,
    `DegreeDiameter.EdgeReduction,
    `DegreeDiameter.ExactDiameter,
    `DegreeDiameter.ExactOrder,
    `DegreeDiameter.FiniteFieldModels,
    `DegreeDiameter.FlagSpace,
    `DegreeDiameter.FlagEnumeration,
    `DegreeDiameter.Framework,
    `DegreeDiameter.HalvedFlags,
    `DegreeDiameter.Lemma21,
    `DegreeDiameter.LowerBound,
    `DegreeDiameter.MooreBound,
    `DegreeDiameter.OddEvenRoute,
    `DegreeDiameter.PrimeIntervals,
    `DegreeDiameter.Proposition31,
    `DegreeDiameter.Proposition31Asymptotics,
    `DegreeDiameter.Proposition31Full,
    `DegreeDiameter.Theorem11FromProposition31,
    `DegreeDiameter.Corollary12FromProposition31,
    `DegreeDiameter.Results,
    `DegreeDiameter.Symmetry
  ]
