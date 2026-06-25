# Run Plan — Weak-Control Seed-Robustness Experiment

## Purpose

Run the completed eight-condition weak-control sensitivity design under an alternate deterministic master seed. This tests whether the observed separation of deliberately periodic and biased controls is stable to a seed change rather than tied to the original `20260523` seed.

## Claim boundary

This is a robustness check for internal TDA diagnostics only.

Supported if successful:

- The same registered workflow can be rerun under a new deterministic master seed.
- Deliberately structured weak controls can be compared against the SHA-256 seeded baseline under the same embeddings and effect-size summaries.
- Results can be compared with the original weak-control evidence register.

Not supported by this run alone:

- Cipher break.
- AES vulnerability.
- Security certification.
- Completed external randomness comparison if Dieharder is unavailable.
- Any Ascon, DES, or TDEA empirical result.

## Configs

Smoke config:

```text
configs/experiment_weak_controls_seed_robustness_smoke.json
```

64-replicate config:

```text
configs/experiment_weak_controls_seed_robustness_64rep.json
```

Both configs use:

- `master_seed`: `20260625`
- `baseline_condition`: `sha256_seeded_baseline`
- Conditions: AES-CTR deterministic plaintext, AES-CTR zero plaintext, SHA-256 seeded baseline, OS CSPRNG, LCG weak, xorshift32 weak, periodic byte weak, biased byte weak
- Embeddings: `byte_pair_2d`, `sliding_window_8d`
- Homology dimensions: H0/H1 through `max_dimension: 1`
- Backend requirement: strict `ripser`, no fallback for evidence claims

## Step 1 — Sync local repository

```bash
git fetch origin
git pull --ff-only origin main
git status --short --branch
```

## Step 2 — Smoke run

```bash
./scripts/run_segmented.sh full --strict --python .venv/bin/python --config configs/experiment_weak_controls_seed_robustness_smoke.json
.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/experiment_weak_controls_seed_robustness_smoke.json
.venv/bin/python scripts/09_validate_artifact_consistency.py --config configs/experiment_weak_controls_seed_robustness_smoke.json
.venv/bin/python scripts/10_effect_size_tables.py --config configs/experiment_weak_controls_seed_robustness_smoke.json
.venv/bin/python scripts/12_run_external_randomness.py --allow-missing-dieharder
.venv/bin/python scripts/09_build_evidence_register.py --config configs/experiment_weak_controls_seed_robustness_smoke.json --output docs/evidence_register_weak_controls_seed_robustness_smoke.md
```

Expected smoke scale:

- Streams: 16
- Embeddings: 32
- TDA feature rows: 64
- Internal randomness rows: 16
- Distance-to-baseline rows: 64

## Step 3 — 64-replicate run

```bash
./scripts/run_segmented.sh full --strict --python .venv/bin/python --config configs/experiment_weak_controls_seed_robustness_64rep.json
.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/experiment_weak_controls_seed_robustness_64rep.json
.venv/bin/python scripts/09_validate_artifact_consistency.py --config configs/experiment_weak_controls_seed_robustness_64rep.json
.venv/bin/python scripts/10_effect_size_tables.py --config configs/experiment_weak_controls_seed_robustness_64rep.json
.venv/bin/python scripts/12_run_external_randomness.py --allow-missing-dieharder
.venv/bin/python scripts/09_build_evidence_register.py --config configs/experiment_weak_controls_seed_robustness_64rep.json --output docs/evidence_register_weak_controls_seed_robustness.md
```

Expected 64-replicate scale:

- Streams: 512
- Embeddings: 1024
- TDA feature rows: 2048
- Internal randomness rows: 512
- Distance-to-baseline rows: 2048

## Step 4 — Review effect-size table

```bash
.venv/bin/python - <<'PY'
import pandas as pd
from pathlib import Path

path = Path("results/tables/tda_effects_combined.csv")
df = pd.read_csv(path)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 220)

print("Shape:", df.shape)
print("Columns:", list(df.columns))
print()

sort_col = "cliffs_delta" if "cliffs_delta" in df.columns else None
if sort_col:
    out = df.copy()
    out["_abs_sort"] = out[sort_col].abs()
    out = out.sort_values("_abs_sort", ascending=False)
    print(out.head(40).to_string(index=False))
else:
    print(df.head(40).to_string(index=False))
PY
```

## Step 5 — Evidence language

Use this wording only if the 64-replicate run passes coherence, consistency, effect-size generation, and evidence-register generation:

> The weak-control sensitivity pattern was reproduced under an alternate deterministic master seed: deliberately periodic and biased byte-stream controls separated strongly from the SHA-256 seeded baseline under the registered internal TDA summaries, while no cryptanalytic or security-certification claim is made.

If external testing remains unavailable, also state:

> External randomness testing was explicitly recorded as unavailable because Dieharder was not installed; no completed external randomness comparison is claimed.
