# Experiment Expansion Plan

## Purpose

The current evidence base supports a defensible diagnostic and reproducibility thesis. The next experiment expansion should strengthen footing without changing the claim boundary. The goal is not to pursue cryptanalysis; it is to test whether the registered weak-control sensitivity pattern is stable across seeds, replicate scale, and representation sampling choices.

## Current footing

Completed evidence:

- Primary six-condition 64-replicate run.
- Eight-condition weak-control sensitivity run.
- Alternate-seed eight-condition robustness run.
- Evidence registers for validation status, artifact scale, backend status, external-test status, registered figures, and logs.

Current supported claim:

> Registered persistent-homology summaries reproducibly distinguish deliberately structured weak-control byte streams from a SHA-256 seeded deterministic baseline under configured byte-pair and sliding-window embeddings. The result is diagnostic and reproducibility evidence, not cryptanalysis or security certification.

## Expansion ladder

### Tier 1 — Seed sweep

Purpose: test whether the weak-control sensitivity pattern is stable across additional deterministic master seeds.

Configs:

- `configs/experiment_weak_controls_seed_sweep_20260701_64rep.json`
- `configs/experiment_weak_controls_seed_sweep_20260702_64rep.json`

Design:

- Conditions: same eight-condition weak-control design.
- Replicates: 64.
- Stream bytes: 1 MiB.
- Embeddings: `byte_pair_2d` and `sliding_window_8d` with the current registered sample sizes.
- Baseline: `sha256_seeded_baseline`.

Pass criterion:

- Deliberately biased and periodic controls remain top-ranked or near-top-ranked separators from the SHA-256 seeded baseline.
- AES-CTR, OS CSPRNG, and xorshift32 do not produce comparable broad top-ranked separation.
- Backend remains `ripser` with no fallback detected.

### Tier 2 — Replicate-scale check

Purpose: test whether the weak-control pattern persists at a larger replicate scale.

Config:

- `configs/experiment_weak_controls_replication_128rep.json`

Design:

- Conditions: same eight-condition weak-control design.
- Replicates: 128.
- Stream bytes: 1 MiB.
- Embeddings: current registered sample sizes.
- Baseline: `sha256_seeded_baseline`.

Pass criterion:

- The main weak-control sensitivity pattern persists at 128 replicates.
- Effect direction and ranking remain interpretable.
- No fallback backend is used.

### Tier 3 — Embedding sample-size sensitivity

Purpose: test whether the weak-control pattern persists when point-cloud sample sizes are increased.

Config:

- `configs/experiment_weak_controls_embedding_sensitivity_64rep.json`

Design:

- Conditions: same eight-condition weak-control design.
- Replicates: 64.
- Stream bytes: 1 MiB.
- Byte-pair sample points: 8,192.
- Sliding-window sample points: 4,096.
- Baseline: `sha256_seeded_baseline`.

Pass criterion:

- Periodic and biased controls remain strongly separated from the SHA-256 seeded baseline.
- Results do not invert into indiscriminate separation of every non-baseline condition.
- Backend remains manuscript-grade.

### Tier 4 — External randomness completion

Purpose: complete the conventional randomness-test comparison in an environment where Dieharder or an equivalent battery is available.

Plan:

- Run Dieharder through Docker or Linux if local macOS installation is unavailable.
- Parse output through the existing parser.
- Rebuild the evidence register with populated external rows.

Pass criterion:

- External randomness table is populated from an actual external run.
- Status is no longer `UNAVAILABLE` for the completed run.
- Any manuscript comparison between TDA and external randomness tests is explicitly scoped to the populated external table.

## Recommended run order

1. Run seed-sweep seed `20260701`.
2. Inspect effect-size table and evidence register.
3. Run seed-sweep seed `20260702`.
4. Inspect effect-size table and evidence register.
5. Run 128-replicate scale check.
6. Run embedding sample-size sensitivity check.
7. Decide whether external randomness completion is required for the thesis or deferred to future work.

## Standard run command

```bash
./scripts/run_segmented.sh full --strict --python .venv/bin/python --config <CONFIG_PATH>
```

## Standard post-run inspection

```bash
.venv/bin/python - <<'PY'
import pandas as pd
from pathlib import Path

path = Path('results/tables/tda_effects_combined.csv')
df = pd.read_csv(path)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 220)

out = df.copy()
out['_abs_sort'] = out['cliffs_delta'].abs()
out = out.sort_values('_abs_sort', ascending=False)
print(out.head(40).to_string(index=False))
PY
```

## Evidence-register naming

Use one evidence register per expansion run:

- `docs/evidence_register_seed_sweep_20260701.md`
- `docs/evidence_register_seed_sweep_20260702.md`
- `docs/evidence_register_weak_controls_128rep.md`
- `docs/evidence_register_embedding_sensitivity.md`

## Claim boundary

Allowed after successful expansion:

- Additional deterministic-seed robustness.
- Replicate-scale robustness.
- Embedding sample-size sensitivity.
- Completed external randomness comparison only if external rows are populated by a real run.

Still not allowed:

- Cipher break.
- AES vulnerability.
- Security certification.
- Ascon, DES, or TDEA empirical claims unless separately implemented and registered.
- Claims that TDA proves cryptographic randomness.
