# Lab Note — 2026-06-25 64-Replicate Evidence Reconciliation Pass

## Status

The 64-replicate internal evidence rebuild completed and passed the core evidence gates for `configs/experiment_64rep.json`.

This establishes the current registered internal evidence package. It does not establish a completed external randomness comparison because Dieharder is unavailable on the current machine.

## Configuration

- Config: `configs/experiment_64rep.json`
- Project version: `0.4.1-pre.0-64rep`
- Baseline condition: `sha256_seeded_baseline`
- Conditions: `aes128_ctr_xor_deterministic_plaintext`, `aes128_ctr_keystream_zero_plaintext`, `sha256_seeded_baseline`, `os_csprng`, `lcg_weak`, `xorshift32_weak`
- Replicates: `64`
- Embeddings: `byte_pair_2d`, `sliding_window_8d`
- TDA max dimension: `1`

## Validation result

Artifact coherence passed:

```text
Validated artifact coherence: conditions=6, embeddings=2, homology_dims=[0, 1], replicates=64, baseline=sha256_seeded_baseline.
```

Artifact consistency passed:

```text
Artifact consistency validation passed: baseline=sha256_seeded_baseline, distance_table=results/tables/tda_distance_to_sha256_seeded_baseline.csv.
```

Effect-size tables were generated:

```text
Wrote effect-size tables: baseline=sha256_seeded_baseline, comparisons=5, entropy_rows=20, distance_rows=20.
Wrote combined effect table to results/tables/tda_effects_combined.csv
```

## Registered artifacts

| Path | Status | Rows |
| --- | --- | --- |
| `data/raw/stream_manifest.csv` | present | 384 |
| `data/interim/embedding_manifest.csv` | present | 768 |
| `data/processed/tda_features.csv` | present | 1536 |
| `data/processed/randomness_tests_internal.csv` | present | 384 |
| `data/processed/external_randomness_tests.csv` | present | 0 |
| `results/tables/tda_backend_summary.csv` | present | 4 |
| `results/tables/tda_feature_summary.csv` | present | 24 |
| `results/tables/tda_distance_to_sha256_seeded_baseline.csv` | present | 1536 |

## Backend state

- Observed TDA backend: `ripser`
- Fallback backend detected: `False`

This satisfies the manuscript-grade backend rule for internal persistent-homology evidence.

## External randomness status

External randomness status is explicit but unavailable:

- External randomness table: `data/processed/external_randomness_tests.csv`
- Rows: `0`
- Populated: `False`
- Status report: `results/logs/external_randomness_status.md`
- External runner status: `UNAVAILABLE`
- External runner message: `Dieharder executable not found on PATH: dieharder`

This supports an availability/status claim only. It does not support completed external randomness comparison claims.

## Registered figures

The 64-replicate register includes persistence-entropy figures and distance-to-SHA-256 seeded baseline figures for `ripser`, `byte_pair_2d`, and `sliding_window_8d`, across H0 and H1 where generated.

## Interpretation

The internal evidence package is now coherent and registered at manuscript scale for the current design. Public and manuscript claims may describe the completed 64-replicate internal TDA workflow, registered artifact counts, `ripser` backend, no fallback backend, and distance-to-`sha256_seeded_baseline` tables.

Claims that remain withheld:

- completed Dieharder or external randomness-test comparison;
- external-test agreement or disagreement with TDA outputs;
- cryptanalytic break, security certification, or cipher vulnerability claim;
- Ascon, DES, or TDEA empirical results before those conditions are implemented and registered.

## Next reconciliation pass

1. Update README status language to match the regenerated evidence register.
2. Update `docs/publication_plan.md` to state that external randomness is unavailable on the current machine, not completed.
3. Review manuscript sections for claims that are unsupported by `docs/evidence_register.md`.
4. Add or update a claim-to-artifact table if manuscript language is being prepared.
5. Prepare a portfolio-safe project blurb that presents the work as reproducible computational diagnostics, not cryptanalysis.
