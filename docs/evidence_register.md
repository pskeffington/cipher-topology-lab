# Evidence Register

Generated: `2026-05-24T03:07:23+00:00`

## Configuration

- Config: `configs/experiment_v0.json`
- Project version: `0.4.1-pre.0`
- Baseline condition: `sha256_seeded_baseline`
- Conditions: `aes128_ctr_xor_deterministic_plaintext, aes128_ctr_keystream_zero_plaintext, sha256_seeded_baseline, os_csprng, lcg_weak, xorshift32_weak`
- Replicates: `8`
- Embeddings: `byte_pair_2d, sliding_window_8d`
- TDA max dimension: `1`

## Validation

- Command: `/Users/null/cipher-topology-lab/.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/experiment_v0.json`
- Status: `PASS`

```text
Validated artifact coherence: conditions=6, embeddings=2, homology_dims=[0, 1], replicates=8, baseline=sha256_seeded_baseline.
```

## Registered artifacts

| Path | Status | Rows |
| --- | --- | --- |
| `data/raw/stream_manifest.csv` | present | 48 |
| `data/interim/embedding_manifest.csv` | present | 96 |
| `data/processed/tda_features.csv` | present | 192 |
| `data/processed/randomness_tests_internal.csv` | present | 48 |
| `data/processed/external_randomness_tests.csv` | missing | NA |
| `results/tables/tda_backend_summary.csv` | present | 4 |
| `results/tables/tda_feature_summary.csv` | present | 24 |
| `results/tables/tda_distance_to_sha256_seeded_baseline.csv` | present | 192 |

## Backend status

- Observed TDA backends: `ripser`
- Fallback backend detected: `False`
- Manuscript-grade rule: use only true persistent-homology backend outputs for evidentiary claims. Fallback outputs are diagnostic only.

## External randomness status

- External randomness table: `data/processed/external_randomness_tests.csv`
- Rows: `missing`
- Populated: `False`

## Registered figures

| Figure path |
| --- |
| `results/figures/h0_persistence_entropy__ripser__byte_pair_2d.png` |
| `results/figures/h0_persistence_entropy__ripser__sliding_window_8d.png` |
| `results/figures/h1_persistence_entropy__ripser__byte_pair_2d.png` |
| `results/figures/h1_persistence_entropy__ripser__sliding_window_8d.png` |
| `results/figures/tda_distance_to_sha256_seeded_baseline__ripser__byte_pair_2d__h0__raw__nonbaseline.png` |
| `results/figures/tda_distance_to_sha256_seeded_baseline__ripser__byte_pair_2d__h0__zscored__nonbaseline.png` |
| `results/figures/tda_distance_to_sha256_seeded_baseline__ripser__byte_pair_2d__h1__raw__nonbaseline.png` |
| `results/figures/tda_distance_to_sha256_seeded_baseline__ripser__byte_pair_2d__h1__zscored__nonbaseline.png` |
| `results/figures/tda_distance_to_sha256_seeded_baseline__ripser__sliding_window_8d__h0__raw__nonbaseline.png` |
| `results/figures/tda_distance_to_sha256_seeded_baseline__ripser__sliding_window_8d__h0__zscored__nonbaseline.png` |
| `results/figures/tda_distance_to_sha256_seeded_baseline__ripser__sliding_window_8d__h1__raw__nonbaseline.png` |
| `results/figures/tda_distance_to_sha256_seeded_baseline__ripser__sliding_window_8d__h1__zscored__nonbaseline.png` |

## Registered logs

| Log path |
| --- |
| `results/logs/figure_notes.md` |

## Claim-control rule

Every result claim in `manuscript/main.tex` or `manuscript/sections/` must trace to one registered table, figure, or validation log in this file.
