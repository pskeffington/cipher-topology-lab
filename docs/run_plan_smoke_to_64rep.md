# Smoke-to-64rep Run Plan

## Purpose

This run plan defines the controlled path from basic execution repair to a defensible 64-replicate evidence package. It is intentionally staged so that manuscript-scale runs are not treated as evidence until smoke-stage artifact generation and validation pass.

## Operating rule

Do not strengthen public claims after a partial run. A run becomes evidence only when expected artifacts are present, validations pass, and `docs/evidence_register.md` is regenerated from current outputs.

## Stage 0 — environment check

From repository root:

```bash
make setup
```

Record:

- Python version
- package install status
- availability of `ripser` or GUDHI
- availability of Dieharder or other external randomness-test tools

If Dieharder is unavailable, continue only with explicit unavailable-status reporting.

## Stage 1 — smoke workflow

Run:

```bash
./scripts/run_segmented.sh smoke --python .venv/bin/python
```

Expected output:

- segmented run report exists at `results/logs/segmented_run_report.md`
- stream manifest is generated
- embeddings are generated
- TDA feature table is generated with a manuscript-grade backend or clearly marked diagnostic backend
- internal randomness diagnostics are generated
- evidence register can be generated

If smoke fails, stop and repair the failed stage before proceeding.

## Stage 2 — smoke validation

Run targeted validation scripts after smoke output exists:

```bash
.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/smoke_test.json
.venv/bin/python scripts/09_validate_artifact_consistency.py --config configs/smoke_test.json
.venv/bin/python scripts/09_build_evidence_register.py --config configs/smoke_test.json
```

Do not proceed to 64 replicates until smoke artifact coherence and consistency are understood.

## Stage 3 — 64-replicate internal run

Run:

```bash
./scripts/run_segmented.sh full --strict --python .venv/bin/python --config configs/experiment_64rep.json
```

Expected design:

- 64 replicates
- configured conditions from `configs/experiment_64rep.json`
- `byte_pair_2d` and `sliding_window_8d` embeddings
- H0/H1 persistent-homology summaries
- manuscript-grade backend such as `ripser` or GUDHI

## Stage 4 — 64-replicate validation

Run:

```bash
.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/experiment_64rep.json
.venv/bin/python scripts/09_validate_artifact_consistency.py --config configs/experiment_64rep.json
.venv/bin/python scripts/10_effect_size_tables.py --config configs/experiment_64rep.json
.venv/bin/python scripts/09_build_evidence_register.py --config configs/experiment_64rep.json
```

The exact script names should be checked against the current CLI options before execution. If script names or flags differ, update this plan rather than improvising untracked commands.

## Stage 5 — external randomness status

Run:

```bash
.venv/bin/python scripts/12_run_external_randomness.py --allow-missing-dieharder
```

If Dieharder is installed, preserve parsed external rows and logs. If Dieharder is missing, preserve the explicit unavailable status and do not claim external testing is completed.

## Stage 6 — reconciliation

After validation and evidence-register generation:

1. Review `docs/evidence_register.md`.
2. Compare registered artifact counts against README and `docs/publication_plan.md`.
3. Update README/status language if needed.
4. Update manuscript claims only when the relevant evidence is registered.
5. Add a dated lab note summarizing the run.

## Evidence promotion rule

A result may be promoted into README, publication plan, or manuscript prose only when it names:

- active config;
- condition;
- baseline;
- embedding;
- homology dimension;
- feature family or metric;
- replicate count;
- registered artifact path.

## Stop conditions

Stop and do not promote claims if:

- artifact coherence fails;
- artifact consistency fails;
- backend summary reports fallback outputs for manuscript evidence;
- TDA feature rows are missing;
- baseline-distance rows are missing;
- the evidence register cannot be regenerated;
- external randomness rows are unavailable but prose describes external testing as completed.
