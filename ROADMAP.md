# Roadmap

## Project aim

Build a reproducible research package for testing whether persistent-homology summaries of ciphertext-derived point clouds provide useful auxiliary diagnostics for symmetric-cipher output randomness.

The project is not a cipher-breaking claim. It is a reproducible diagnostics and measurement study.

## Current checkpoint

### v0.4.1-pre.1 — 64-replicate `ripser` evidence and ERT status

Status: completed and tagged.

Evidence state:

- Manuscript evidence configuration: `configs/experiment_64rep.json`
- Streams: 384
- Embeddings: 768
- TDA feature rows: 1,536
- Internal randomness-diagnostic rows: 384
- Distance-to-baseline rows: 1,536
- TDA backend: `ripser`
- Fallback backend detected: `False`
- Baseline condition: `sha256_seeded_baseline`
- External randomness status: implemented and audited; Dieharder unavailable on the local execution path

Central internal result:

- LCG weak-control output separates strongly from the SHA-256 seeded baseline under byte-pair H0 persistence-entropy and distance-to-baseline summaries.
- AES-CTR deterministic-output conditions, OS CSPRNG output, and xorshift32 do not show comparable separation under the current embeddings and feature set.

Completed scope:

- Object-oriented segmented workflow runner
- Executable terminal wrapper
- Failure-safe segmented run report
- Failure-safe external-randomness runner
- Evidence register with external-runner status
- Related Work manuscript section
- 64-replicate Results, Discussion, Conclusion, and replication appendix updates
- Release notes and changelog for `v0.4.1-pre.1`

## Version sequence

### v0.4.1-pre.2 — External randomness execution package

Status: next.

Goal: complete the external randomness-testing pathway with actual imported rows instead of only audited unavailability status.

Exit criteria:

- Run Dieharder in a supported environment against the selected 8 MiB replicate-zero exports.
- Capture stdout and stderr into non-empty `external_tests/results/dieharder/*.txt` files.
- Parse results into `data/processed/external_randomness_tests.csv`.
- Rebuild `docs/evidence_register.md` with `External runner status: PASS` and populated external rows.
- Add a manuscript Results subsection comparing external randomness-test results against the TDA positive-control result.
- Preserve external-test outputs in a release artifact bundle, not as tracked bulk Git files.

Candidate commands:

```bash
./scripts/run_segmented.sh \
  --config configs/external_dieharder_8mb.json \
  stage clean generate export \
  --python .venv/bin/python

python scripts/12_run_external_randomness.py

python scripts/09_build_evidence_register.py \
  --config configs/experiment_64rep.json \
  --output docs/evidence_register.md
```

### v0.4.2-pre.0 — Release artifact bundle and archival package

Status: open.

Goal: package generated evidence tables, logs, figures, and the manuscript PDF as a GitHub release asset while keeping the repository itself source-focused.

Exit criteria:

- Create `release_artifacts/v0.4.1-pre.1_artifacts.zip` or successor bundle.
- Include evidence register, segmented run report, external randomness status, effect tables, backend summary, feature summary, distance tables, and selected figures.
- Attach the ZIP to the GitHub release.
- Confirm `release_artifacts/` is ignored by Git.
- Add release-asset checksum file.

### v0.4.3-pre.0 — Cubical/GUDHI extension

Status: open.

Goal: add a configured cubical-complex evidence run rather than relying only on point-cloud embeddings.

Exit criteria:

- Add a dedicated config enabling `cubical_image_2d`.
- Run GUDHI cubical persistence with manuscript-grade backend status.
- Generate backend summary showing `gudhi_cubical`.
- Compare cubical H0/H1 summaries against the existing `ripser` byte-pair and sliding-window results.
- Add a manuscript subsection only if cubical features add interpretable evidence.

### v0.4.4-pre.0 — Additional weak-generator controls

Status: open.

Goal: test whether the current feature set detects more than one weak generator class.

Candidate controls:

- PCG or Mersenne Twister as non-cryptographic comparators
- Biased-bit generator
- Repeating-block or low-period synthetic generator
- Counter or ramp-pattern byte stream
- RC4 legacy stream as a historically relevant but clearly caveated comparator

Exit criteria:

- Add each control with manifest metadata and deterministic seeds.
- Run at 64 replicates or greater.
- Compare against the SHA-256 seeded baseline using the same effect-table pipeline.
- Update manuscript claims only if effects are stable and interpretable.

### v0.5.0-pre.0 — Manuscript submission candidate

Status: open.

Goal: prepare a submission-ready preprint or workshop manuscript.

Exit criteria:

- External randomness tests are either completed and interpreted, or explicitly scoped out with a strong limitation statement.
- All manuscript claims trace to `docs/evidence_register.md`, release assets, or cited sources.
- Related Work citations are verified against DOI, publisher, or official project pages.
- Results section contains only evidence-backed claims.
- Tables are compact and publication-ready.
- Replication appendix lists exact commands and configs.
- Release asset bundle contains all tables/logs/figures needed to reproduce the manuscript claims.
- GitHub release exists for the manuscript evidence tag.

## Immediate execution order

1. Keep `v0.4.1-pre.1` as the current source/evidence checkpoint.
2. Complete the external randomness execution path in a Linux/Docker/VM environment where Dieharder is available.
3. Rebuild the evidence register after external rows are populated.
4. Patch manuscript Results and Discussion with external randomness-test comparison.
5. Create and attach a release artifact bundle.
6. Decide whether the next empirical extension should be cubical/GUDHI or additional weak controls.

## Claim-control rule

No manuscript claim should be made unless it traces to one of the following:

- `docs/evidence_register.md`
- generated tables in the release artifact bundle
- generated figures in the release artifact bundle
- validation or external-test status logs
- cited external sources

Statistical and topological diagnostics must not be described as proofs of cipher security or randomness certification.
