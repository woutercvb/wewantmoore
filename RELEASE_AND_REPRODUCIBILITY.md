# Release and reproducibility procedure

## What this source tree establishes

The toolchain and direct dependencies are pinned in `lean-toolchain`,
`lakefile.lean`, and `lake-manifest.json`. The checked-in workflows and scripts
define the source, kernel-axiom, declaration-dependency, third-party
provenance, and archive-integrity checks. Once the repository is public, the
release record should link both the immutable revision and its successful
hosted workflow run.

## Clean-checkout verification

Run from a fresh checkout of the intended release commit:

```sh
cat lean-toolchain
lake build
sh scripts/audit.sh
sh scripts/verify_third_party.sh
git ls-files --error-unmatch lake-manifest.json axiom-audit.txt dependency-audit.txt
git diff --exit-code -- lake-manifest.json axiom-audit.txt dependency-audit.txt
git rev-parse HEAD
lean --version
lake --version
```

The trust audit has independent safeguards:

1. `scripts/audit.sh` rejects proof holes, assumption declarations, unsafe
   declarations, external implementations, and native-decision shortcuts in
   project and vendored Lean sources.
2. `DegreeDiameter/Audit.lean` names every required theorem explicitly.
3. `scripts/check_axiom_allowlist.py` requires every target and permits only
   `propext`, `Classical.choice`, and `Quot.sound`; changing the committed
   report cannot expand this allowlist.
4. `DegreeDiameter/DependencyAudit.lean` traverses kernel declaration types
   and values transitively. It requires the bundled Proposition 3.1 and the
   relevant Moore/Lemma 4.1 dependencies and rejects the weak witness,
   big-cell lower bound, and alternative final results even through aliases.
5. `scripts/check_dependency_report.py` independently requires exactly the
   four direct/public dependency PASS records and rejects missing, duplicate,
   unexpected, or error-bearing reports.

## Hosted build record

`.github/workflows/lean.yml` pins every action by its full official commit SHA:

| Action | Pinned release | Commit |
|---|---|---|
| `actions/checkout` | v4.4.0 | `11d5960a326750d5838078e36cf38b85af677262` |
| `leanprover/lean-action` | v1.5.0 | `38fbc41a8c28c4cbaec22d7f7de508ec2e7c0dd9` |
| `actions/upload-artifact` | v4.6.2 | `ea165f8d65b6e75b540449e92b4886f43607fa02` |

The workflow records the source SHA, toolchain text, Lean and Lake versions,
Mathlib and LeanArchitect revisions, and generated trust reports. A release
should link its successful run.

## Source release

For a local release candidate in a clean Git checkout:

```sh
sh scripts/make_source_archive.sh /absolute/output/ReleaseName.zip
python3 scripts/verify_source_archive.py /absolute/output/ReleaseName.zip
cat /absolute/output/ReleaseName.zip.sha256
cd /absolute/output && sha256sum -c ReleaseName.zip.sha256
```

The archive maker refuses to overwrite an existing archive or hash and uses
`git archive` on the exact `HEAD` commit. The `.sha256` sidecar records only
the archive basename, not the machine-specific absolute output path, so the
downloaded pair can be verified in any directory with `sha256sum -c`. The
validator reads the ZIP without extracting it and rejects:

- duplicate or case-colliding paths;
- `..` traversal, absolute paths, and backslash/drive-letter paths;
- symbolic links and encrypted entries;
- `.git`, `.lake`, cache directories, `.olean`, `.ilean`, `.pyc`, and `.pyo`
  entries;
- CRC or general ZIP-format failures.

`.github/workflows/source-release.yml` repeats the pinned build, trust audit,
and provenance comparison on a published release tag; performs the archive
checks; attaches the ZIP, `.sha256`, both trust reports, and a metadata record
containing the exact source/toolchain/dependency/report revisions; and records
the digest in the release notes.

## Third-party provenance

`sh scripts/verify_third_party.sh` fetches only the recorded
PrimeNumberTheoremAnd commit and makes an exact comparison. Details, file
hashes, the one documented declaration-block omission, and licensing are in
`THIRD_PARTY.md`.
