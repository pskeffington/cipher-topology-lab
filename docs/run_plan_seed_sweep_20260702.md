# Run Plan — Seed Sweep 20260702

## Purpose

Run the second deterministic seed-sweep expansion after the `20260701` seed-sweep result. The objective is to test whether the weak-control sensitivity pattern remains stable across another deterministic master seed.

This run strengthens the diagnostic and reproducibility footing. It does not change the project claim boundary: no cryptanalysis, no AES vulnerability claim, and no security certification.

## Config

`configs/experiment_weak_controls_seed_sweep_20260702_64rep.json`

Expected design:

- Conditions: 8
- Replicates: 64
- Stream bytes: 1 MiB
- Baseline: `sha256_seeded_baseline`
- Embeddings: `byte_pair_2d`, `sliding_window_8d`
- Homology dimensions: H0, H1
- Backend requirement: `ripser`
- Fallback allowed for evidence claims: false

## Pre-run checklist

Before starting this run:

1. Commit `docs/evidence_register_seed_sweep_20260701.md`.
2. Confirm `20260701` external randomness status is either `UNAVAILABLE` or populated, not `missing`.
3. Archive or preserve the `20260701` effect table and distance table if they need to be retained separately.
4. Confirm local working tree is clean except intentional untracked runtime artifacts.

Suggested check:

```bash
git status --short --branch
```

## Run command

```bash
./scripts/run_segmented.sh full --strict --python .venv/bin/python \
  --config configs/experiment_weak_controls_seed_sweep_20260702_64rep.json
```

## External randomness status normalization

After the segmented run completes, run:

```bash
.venv/bin/python scripts/12_run_external_randomness.py --allow-missing-dieharder
```

This ensures the evidence register records external randomness as unavailable if Dieharder is missing, rather than recording a missing status file.

## Build evidence register

```bash
.venv/bin/python scripts/09_build_evidence_register.py \
  --config configs/experiment_weak_controls_seed_sweep_20260702_64rep.json \
  --output docs/evidence_register_seed_sweep_20260702.md
```

Confirm:

```bash
grep -A12 "External randomness status" docs/evidence_register_seed_sweep_20260702.md
```

## Inspect effects

```bash
.venv/bin/python - <<'PY'
import pandas as pd

path = "results/tables/tda_effects_combined.csv"
df = pd.read_csv(path)
df["_abs_sort"] = df["cliffs_delta"].abs()
df = df.sort_values("_abs_sort", ascending=False)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 220)

print(df.head(40).to_string(index=False))
PY
```

## Pass criterion

The run supports the expansion if:

- `biased_byte_weak` and `periodic_byte_weak` remain top-ranked or near-top-ranked separators from the SHA-256 seeded baseline.
- `lcg_weak` remains an interpretable positive-control signal, especially under byte-pair H0 summaries.
- AES-CTR, OS CSPRNG, and xorshift32 do not show comparable broad top-ranked separation.
- Backend is `ripser` with fallback detected as `False`.
- External randomness status is explicitly unavailable or populated, not silently missing.

## Commit command

```bash
git add docs/evidence_register_seed_sweep_20260702.md
git commit -m "Record seed-sweep 20260702 evidence"
git push origin main
```

## Next step after pass

If the `20260702` top-40 effect table matches the pass criterion, move to the 128-replicate scale check:

`configs/experiment_weak_controls_replication_128rep.json`
