# Lab Note — 2026-06-25 Smoke Evidence Reconciliation Pass

## Status

Smoke workflow completed and the internal evidence gates passed for `configs/smoke_test.json`. External randomness status is now closed as explicitly unavailable on the current machine because Dieharder is not installed.

## Configuration

- Config: `configs/smoke_test.json`
- Project version: `0.4.1-pre.0-smoke`
- Baseline condition: `sha256_seeded_baseline`
- Conditions: `aes128_ctr_xor_deterministic_plaintext`, `aes128_ctr_keystream_zero_plaintext`, `sha256_seeded_baseline`, `os_csprng`, `lcg_weak`, `xorshift32_weak`
- Replicates: `2`
- Embeddings: `byte_pair_2d`, `sliding_window_8d`
- TDA max dimension: `1`

## Validation result

Artifact coherence passed:

```text
Validated artifact coherence: conditions=6, embeddings=2, homology_dims=[0, 1], replicates=2, baseline=sha256_seeded_baseline.
```

Artifact consistency passed:

```text
Artifact consistency validation passed: baseline=sha256_seeded_baseline, distance_table=results/tables/tda_distance_to_sha256_seeded_baseline.csv.
```

## Registered smoke artifacts

| Path | Status | Rows |
| --- | --- | --- |
| `data/raw/stream_manifest.csv` | present | 12 |
| `data/interim/embedding_manifest.csv` | present | 24 |
| `data/processed/tda_features.csv` | present | 48 |
| `data/processed/randomness_tests_internal.csv` | present | 12 |
| `data/processed/external_randomness_tests.csv` | present | 0 |
| `results/tables/tda_backend_summary.csv` | present | 4 |
| `results/tables/tda_feature_summary.csv` | present | 24 |
| `results/tables/tda_distance_to_sha256_seeded_baseline.csv` | present | 48 |

## Backend state

- Observed TDA backend: `ripser`
- Fallback backend detected: `False`

This is sufficient for the smoke-stage internal TDA gate. It does not yet promote 64-replicate claims.

## External randomness status

External randomness evidence is now closed as an explicit unavailable-status state for this machine:

- External randomness table: `data/processed/external_randomness_tests.csv`
- Rows: `0`
- Populated: `False`
- Status report: `results/logs/external_randomness_status.md`
- External runner status: `UNAVAILABLE`
- External runner message: `Dieharder executable not found on PATH: dieharder`

This is an acceptable evidence-register state for honest reporting. It does not support claims that external randomness testing was completed. It supports the more limited claim that external randomness testing infrastructure was checked and recorded as unavailable.

## Registered smoke figures

The smoke register includes persistence-entropy and distance-to-baseline figures for `ripser`, `byte_pair_2d`, and `sliding_window_8d` outputs. Some distance plots are intentionally skipped where a figure is not applicable, with notes captured in `results/logs/distance_plots_skipped.txt` and `results/logs/figure_notes.md`.

## Interpretation

The smoke pass demonstrates that the internal pipeline can generate coherent artifacts for six conditions, two embeddings, H0/H1 summaries, and a SHA-256 seeded baseline-distance table under a two-replicate test configuration.

External randomness is unavailable on the current machine because Dieharder is not installed, so external comparison claims remain withheld.

This supports proceeding to the 64-replicate internal rebuild, but it does not by itself support manuscript-scale result claims.

## Next commands

```bash
./scripts/run_segmented.sh full --strict --python .venv/bin/python --config configs/experiment_64rep.json
.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/experiment_64rep.json
.venv/bin/python scripts/09_validate_artifact_consistency.py --config configs/experiment_64rep.json
.venv/bin/python scripts/10_effect_size_tables.py --config configs/experiment_64rep.json
.venv/bin/python scripts/12_run_external_randomness.py --allow-missing-dieharder
.venv/bin/python scripts/09_build_evidence_register.py --config configs/experiment_64rep.json --output docs/evidence_register.md
```

If the regenerated 64-replicate register passes coherence and consistency with `ripser` and no fallback backend, then README, publication plan, manuscript, CV, and LinkedIn language can be reconciled against the registered artifacts.
