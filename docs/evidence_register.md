# Evidence Register

Generated: `2026-05-26T03:01:50+00:00`

## Configuration

- Config: `configs/experiment_64rep.json`
- Project version: `0.4.1-pre.0-64rep`
- Baseline condition: `sha256_seeded_baseline`
- Conditions: `aes128_ctr_xor_deterministic_plaintext, aes128_ctr_keystream_zero_plaintext, sha256_seeded_baseline, os_csprng, lcg_weak, xorshift32_weak`
- Replicates: `64`
- Embeddings: `byte_pair_2d, sliding_window_8d`
- TDA max dimension: `1`

## Validation

- Command: `/Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/experiment_64rep.json`
- Status: `FAIL`

```text
Missing required artifact: data/interim/embedding_manifest.csv
```

## Registered artifacts

| Path | Status | Rows |
| --- | --- | --- |
| `data/raw/stream_manifest.csv` | present | 6 |
| `data/interim/embedding_manifest.csv` | missing | NA |
| `data/processed/tda_features.csv` | missing | NA |
| `data/processed/randomness_tests_internal.csv` | missing | NA |
| `data/processed/external_randomness_tests.csv` | present | 0 |
| `results/tables/tda_backend_summary.csv` | missing | NA |
| `results/tables/tda_feature_summary.csv` | missing | NA |
| `results/tables/tda_distance_to_sha256_seeded_baseline.csv` | missing | NA |

## Backend status

- Observed TDA backends: `none detected`
- Fallback backend detected: `unknown`
- Manuscript-grade rule: use only true persistent-homology backend outputs for evidentiary claims. Fallback outputs are diagnostic only.

## External randomness status

- External randomness table: `data/processed/external_randomness_tests.csv`
- Rows: `0`
- Populated: `False`
- Status report: `results/logs/external_randomness_status.md`
- External runner status: `UNAVAILABLE`
- External runner message: `Dieharder executable not found on PATH: dieharder`

## Registered figures

No figures detected.

## Registered logs

| Log path |
| --- |
| `results/logs/external_randomness_status.md` |
| `results/logs/segmented_run_report.md` |

## Claim-control rule

Every result claim in `manuscript/main.tex` or `manuscript/sections/` must trace to one registered table, figure, or validation log in this file.
