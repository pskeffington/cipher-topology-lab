# Evidence Register

Generated: `2026-05-26T01:48:47+00:00`

## Configuration

- Config: `configs/smoke_test.json`
- Project version: `0.4.1-pre.0-smoke`
- Baseline condition: `sha256_seeded_baseline`
- Conditions: `aes128_ctr_xor_deterministic_plaintext, aes128_ctr_keystream_zero_plaintext, sha256_seeded_baseline, os_csprng, lcg_weak, xorshift32_weak`
- Replicates: `2`
- Embeddings: `byte_pair_2d, sliding_window_8d`
- TDA max dimension: `1`

## Validation

- Command: `/Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/smoke_test.json`
- Status: `PASS`

```text
Validated artifact coherence: conditions=6, embeddings=2, homology_dims=[0, 1], replicates=2, baseline=sha256_seeded_baseline.
```

## Registered artifacts

| Path | Status | Rows |
| --- | --- | --- |
| `data/raw/stream_manifest.csv` | present | 12 |
| `data/interim/embedding_manifest.csv` | present | 24 |
| `data/processed/tda_features.csv` | present | 48 |
| `data/processed/randomness_tests_internal.csv` | present | 12 |
| `data/processed/external_randomness_tests.csv` | missing | NA |
| `results/tables/tda_backend_summary.csv` | present | 4 |
| `results/tables/tda_feature_summary.csv` | present | 24 |
| `results/tables/tda_distance_to_sha256_seeded_baseline.csv` | present | 48 |

## Backend status

- Observed TDA backends: `fallback_threshold_graph`
- Fallback backend detected: `True`
- Manuscript-grade rule: use only true persistent-homology backend outputs for evidentiary claims. Fallback outputs are diagnostic only.

## External randomness status

- External randomness table: `data/processed/external_randomness_tests.csv`
- Rows: `missing`
- Populated: `False`

## Registered figures

| Figure path |
| --- |
| `results/figures/h0_persistence_entropy__fallback_threshold_graph__sliding_window_8d.png` |
| `results/figures/tda_distance_to_sha256_seeded_baseline__fallback_threshold_graph__sliding_window_8d__h0__raw__nonbaseline.png` |
| `results/figures/tda_distance_to_sha256_seeded_baseline__fallback_threshold_graph__sliding_window_8d__h0__zscored__nonbaseline.png` |

## Registered logs

| Log path |
| --- |
| `results/logs/distance_plots_skipped.txt` |
| `results/logs/fallback_backend_used.txt` |
| `results/logs/figure_notes.md` |
| `results/logs/h1_plot_skipped.txt` |
| `results/logs/segmented_run_report.md` |

## Claim-control rule

Every result claim in `manuscript/main.tex` or `manuscript/sections/` must trace to one registered table, figure, or validation log in this file.
