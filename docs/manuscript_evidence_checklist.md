# Manuscript Evidence Checklist

## Purpose

This checklist defines which outputs can be promoted from diagnostic workflow artifacts into manuscript evidence.

## Required analysis scale

Manuscript evidence should use `configs/manuscript_30rep.json` or a later configuration with at least 30 replicates per condition. Smoke-test artifacts are acceptable for engineering validation but not for manuscript claims.

## Required backends

A manuscript evidence package must include both:

- `ripser` for point-cloud embeddings
- `gudhi_cubical` for cubical image embeddings

Any run containing `fallback_threshold_graph` is diagnostic only and must not be used for publication claims.

## Required tables

| Table | Required file | Use |
|---|---|---|
| Stream manifest | `data/raw/stream_manifest.csv` | reproducibility and audit trail |
| Embedding manifest | `data/interim/embedding_manifest.csv` | embedding audit trail |
| Backend summary | `results/tables/tda_backend_summary.csv` | confirms backend eligibility |
| TDA features | `results/tables/tda_features.csv` | primary TDA feature table |
| TDA feature summary | `results/tables/tda_feature_summary.csv` | manuscript descriptive/result table |
| Distance-to-baseline | `results/tables/tda_distance_to_os_csprng.csv` | comparison against random baseline |
| Internal randomness diagnostics | `results/tables/randomness_tests_internal.csv` | preliminary conventional diagnostic |
| External randomness diagnostics | `results/tables/external_randomness_tests.csv` | external-suite results when imported |

## Candidate figure rules

A figure may be promoted only if all conditions below hold:

- backend is `ripser` or `gudhi_cubical`
- no fallback backend is present in the run
- figure is stratified by backend and embedding
- figure is not pooled across embeddings
- H1 figure has finite H1 intervals
- distance figure has nonzero nonbaseline distance signal
- source table comes from a 30-replicate or larger run

## Current candidate figure classes

After a 30-replicate rerun, likely candidate classes are:

- `h1_persistence_entropy__ripser__byte_pair_2d.png`
- `h1_persistence_entropy__gudhi_cubical__cubical_image_2d.png`
- `h0_persistence_entropy__gudhi_cubical__cubical_image_2d.png`
- nonzero-signal `tda_distance_to_os_csprng__*` figures

## Exclusion rules

Do not use:

- flat H1 plots from fallback or no-signal groups
- pooled condition-level plots that mix embeddings
- zero-signal distance plots
- smoke-test figures as manuscript evidence
- any result interpreted as proof that AES or Ascon is secure or insecure

## Claim rule

Acceptable claim form:

The selected topological features distinguish some controlled weak-generator or structured-output conditions from an OS CSPRNG baseline under specified embeddings and backends.

Unacceptable claim form:

The selected topological features break AES, prove AES security, replace cryptanalysis, or certify cryptographic randomness.
