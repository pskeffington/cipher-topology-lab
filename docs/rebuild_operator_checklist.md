# Evidence Rebuild Operator Checklist

## Purpose

This is the short operator-facing checklist for rebuilding the evidence state after documentation drift or stale artifacts. It complements `docs/run_plan_smoke_to_64rep.md` and `docs/evidence_reconciliation_checklist.md`.

## Core principle

Treat the current evidence register as stale until it is regenerated from the current artifacts. Treat README, publication plan, and manuscript prose as provisional until they match the regenerated register.

## Step 1 — start clean enough to reason

From repository root, confirm the current branch and inspect changed files:

```bash
git status
```

Do not delete generated artifacts unless you intentionally want a full rebuild. If you do remove generated artifacts, record that action in the lab note.

## Step 2 — setup environment

```bash
make setup
```

Confirm that the selected Python path is the one used for all later commands:

```bash
.venv/bin/python --version
```

## Step 3 — smoke rebuild

```bash
./scripts/run_segmented.sh smoke --python .venv/bin/python
```

Expected minimum outputs:

- `data/raw/stream_manifest.csv`
- `data/interim/embedding_manifest.csv`
- `data/processed/tda_features.csv`
- `data/processed/randomness_tests_internal.csv`
- `results/tables/tda_backend_summary.csv`
- `results/tables/tda_feature_summary.csv`
- `results/logs/segmented_run_report.md`

## Step 4 — smoke validation and smoke register

```bash
.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/smoke_test.json
.venv/bin/python scripts/09_validate_artifact_consistency.py --config configs/smoke_test.json
.venv/bin/python scripts/09_build_evidence_register.py --config configs/smoke_test.json --output docs/evidence_register_smoke.md
```

If smoke validation fails, stop and repair the failing stage. Do not run the 64-replicate workflow until smoke is understood.

## Step 5 — full 64-replicate rebuild

```bash
./scripts/run_segmented.sh full --strict --python .venv/bin/python --config configs/experiment_64rep.json
```

This should rebuild the manuscript-scale internal artifacts.

## Step 6 — full validation

```bash
.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/experiment_64rep.json
.venv/bin/python scripts/09_validate_artifact_consistency.py --config configs/experiment_64rep.json
.venv/bin/python scripts/10_effect_size_tables.py --config configs/experiment_64rep.json
```

The coherence validator checks expected condition, replicate, embedding, homology-dimension, backend-summary, feature-summary, and distance-table structure. The consistency validator checks feature/backend-summary agreement, fallback backend exclusion, distance-table backend keys, and baseline condition.

## Step 7 — external randomness status

```bash
.venv/bin/python scripts/12_run_external_randomness.py --allow-missing-dieharder
```

If Dieharder is unavailable, preserve the unavailable-status log. Do not describe external randomness testing as completed unless parsed external rows are populated.

## Step 8 — regenerate final evidence register

```bash
.venv/bin/python scripts/09_build_evidence_register.py --config configs/experiment_64rep.json --output docs/evidence_register.md
```

Open `docs/evidence_register.md` and verify:

- validation status is `PASS`;
- required artifacts are present;
- row counts match expected scale;
- backend is manuscript-grade and not fallback;
- external randomness status is accurately described;
- figures and logs are registered.

## Step 9 — reconcile prose

Compare regenerated `docs/evidence_register.md` against:

- `README.md`
- `docs/protocol.md`
- `docs/publication_plan.md`
- `manuscript/main.tex`
- `manuscript/sections/`

Weaken or update any sentence that describes evidence not present in the register.

## Step 10 — lab note

Create a dated lab note under `docs/lab_notes/` with:

- branch and commit context;
- commands run;
- config used;
- artifact counts;
- validation status;
- external randomness status;
- claims promoted;
- claims withheld;
- next repair task if any gate failed.

## Immediate repair targets if validation fails

1. Missing `embedding_manifest.csv`: inspect embedding stage and stage ordering.
2. Missing `tda_features.csv`: inspect TDA backend availability and feature stage logs.
3. Missing backend summary: inspect analysis/effects stage outputs.
4. Distance-table baseline mismatch: inspect config `baseline_condition` and distance-table generation.
5. Fallback backend detected: install manuscript-grade backend or mark outputs diagnostic only.
6. External randomness unavailable: preserve the status log and do not claim completed external comparison.

## Promotion gate

Only after this checklist passes should README, publication plan, manuscript, CV, or LinkedIn language describe a completed evidence package.
