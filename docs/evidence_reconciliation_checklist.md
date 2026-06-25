# Evidence Reconciliation Checklist

## Purpose

This checklist controls the transition from documented workflow design to public-facing evidence claims. It should be completed whenever README, publication-plan, manuscript, or portfolio language describes results from the 64-replicate evidence package.

## Source-of-truth order

When documentation disagrees, use this order:

1. Current generated artifacts on disk.
2. `docs/evidence_register.md` generated from those artifacts.
3. Validation logs in `results/logs/`.
4. README, publication plan, manuscript prose, and portfolio descriptions.

If the evidence register reports missing artifacts or failed validation, prose claims must be weakened until the evidence register is regenerated and passing.

## Required artifact families

Before describing a run as manuscript-grade, verify that these artifacts are present and registered:

- `data/raw/stream_manifest.csv`
- `data/interim/embedding_manifest.csv`
- `data/processed/tda_features.csv`
- `data/processed/randomness_tests_internal.csv`
- `data/processed/external_randomness_tests.csv` or explicit unavailable-status report
- `results/tables/tda_backend_summary.csv`
- `results/tables/tda_feature_summary.csv`
- `results/tables/tda_distance_to_sha256_seeded_baseline.csv`
- `results/logs/segmented_run_report.md`
- `results/logs/external_randomness_status.md`
- `docs/evidence_register.md`

## Validation gates

### Gate 1 — stream manifest

- All configured conditions are present.
- Replicate counts match the active config.
- Byte counts are consistent with the config.
- SHA-256 digests are populated.
- Deterministic conditions are traceable to seed/key/nonce/plaintext metadata.

### Gate 2 — embedding manifest

- Every stream has each configured embedding.
- Embedding labels match the active config.
- Point-cloud or complex dimensions are documented.
- No unregistered embedding method appears in manuscript tables.

### Gate 3 — TDA backend

- Backend summary reports a manuscript-grade backend such as `ripser` or GUDHI.
- No fallback backend is detected for manuscript evidence.
- H0 and H1 feature rows are present for configured embeddings.

### Gate 4 — internal randomness diagnostics

- Internal randomness rows exist for every configured stream.
- Diagnostics are described as auxiliary comparisons, not as security certification.

### Gate 5 — distance-to-baseline tables

- Baseline condition is explicitly `sha256_seeded_baseline` unless the config says otherwise.
- OS CSPRNG is described as a non-deterministic sensitivity condition, not the primary baseline.
- Any separation claim names condition, embedding, homology dimension, feature family, and replicate configuration.

### Gate 6 — external randomness status

- If external rows are populated, document the runner and parsed output source.
- If Dieharder or another external battery is unavailable, report it as unavailable rather than completed.
- Do not compare TDA results to external tests unless external rows are populated.

### Gate 7 — evidence register

- `docs/evidence_register.md` is regenerated after the current run.
- Artifact coherence passes.
- Artifact consistency passes.
- Registered figures and tables match manuscript references.

## Claim language after reconciliation

Use strong evidence language only after all relevant gates pass.

Acceptable after passing gates:

> In the 64-replicate registered evidence package, the LCG weak-control condition separates from the SHA-256 seeded baseline under byte-pair H0 summaries, while AES-CTR deterministic-output conditions, OS CSPRNG, and xorshift32 do not show comparable separation under the current embeddings and feature set.

Acceptable before passing gates:

> The repository implements a reproducible workflow intended to test whether persistent-homology summaries can distinguish weak or structured controls from deterministic cryptographic baselines. Current documentation should be reconciled against the evidence register before treating results as manuscript-grade.

## Completion record

When reconciliation is complete, add a dated note to `docs/lab_notes/` summarizing:

- active config;
- commands run;
- artifact counts;
- validation status;
- external randomness status;
- claims promoted;
- claims withheld.
