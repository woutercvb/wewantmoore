# Third-party source

The files under `PrimeNumberTheoremAnd/` are the minimal import closure needed
for the proved theorem `prime_between`. They are derived from Alex Kontorovich
et al., [*PrimeNumberTheoremAnd*](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd),
commit `0c7abf7be7765dc5ffd21afc1c37b018199ec3c9`, under Apache-2.0; see
`LICENSE-PrimeNumberTheoremAnd`.

Four declarations in the upstream snapshot lie outside the dependency closure
of `WeakPNT` and `prime_between`. This distribution omits those declarations:
`prelim_decay_2`, `AbsolutelyContinuous`, `prelim_decay_3`, and `decay_alt`.
No retained declaration was changed.
`DegreeDiameter/Audit.lean` checks that `WeakPNT` and `prime_between` depend
only on Lean's standard axioms.

The provenance check is executable rather than documentary only:

```sh
sh scripts/verify_third_party.sh
```

It fetches exactly the commit above and checks all nine vendored Lean source
files. The following eight files must be byte-for-byte identical to upstream:

- `Consequences.lean`;
- `Defs.lean`;
- `Fourier.lean`;
- `Mathlib/Algebra/Notation/Support.lean`;
- `Mathlib/Analysis/Asymptotics/Asymptotics.lean`;
- `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean`;
- `SmoothExistence.lean`;
- `Sobolev.lean`.

The checker also verifies that the vendored license equals the upstream
license and that `Wiener.lean` is exactly the upstream file after the four
named declarations are removed and the recorded modification notice is
prepended. Before comparing contents, it requires the complete discovered
`PrimeNumberTheoremAnd/**/*.lean` inventory to equal this nine-file registry;
an added unregistered or missing registered Lean file fails the check. Built-in
negative regression tests exercise both inventory failures on every run. The
checker prints the complete upstream-to-vendored diff.

Current vendored SHA-256 values are:

| File | SHA-256 |
|---|---|
| `Consequences.lean` | `b6c3ce0377e08884af9ead61b19c028635a0226c375af55460f6e41143657c6a` |
| `Defs.lean` | `64137811210c81187151a3d48ef170195cf36d58ea07a67ee61d1dc3212c82d0` |
| `Fourier.lean` | `e9db3c235cabf356d2b4aed528d0ceca6ad3e23c7a150d7049fd9ac796315823` |
| `Mathlib/Algebra/Notation/Support.lean` | `e688bf925c2130b291c536d3b93b72c20e41ae95d530c90915921d75a6f52504` |
| `Mathlib/Analysis/Asymptotics/Asymptotics.lean` | `c1cdb6bb509c6178bf17868c57e5b53721b87fb2774ef8562bc5945ffe5b11ae` |
| `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` | `7e3e2b8f84e6c170051a6474272455bed2432e6fddac5660072318b9b4eda7ec` |
| `SmoothExistence.lean` | `e689045a2d7f92c71c68fda6aa69a89d4a8692187475ba432ed010f453110ea0` |
| `Sobolev.lean` | `fe06e13fad5b47dbd324307ba246110515c4cb50f4c41d6cb15764fd53b1b8ef` |
| `Wiener.lean` (documented derivative) | `65c1d4a173b26cd96d67449e572eda61ea43abe97c0f0f758f5986d0e02291f6` |
| `LICENSE-PrimeNumberTheoremAnd` | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
