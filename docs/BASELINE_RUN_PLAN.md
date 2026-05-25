# Baseline Run Plan

## Purpose

Define the first reproducible benchmark run for the cipher-topology diagnostic project.

## Run inputs

| Input | Status | Notes |
|---|---|---|
| Standard cipher stream corpus | Pending freeze | Define algorithms and parameters |
| Weak or biased controls | Pending freeze | Define controlled deviations |
| Random baseline | Pending freeze | Define seed and generator |
| Embedding method | Pending | Define dimensionality and windowing |
| Randomness tests | Pending | Define tests and output schema |
| Topological features | Pending | Define persistence or summary features |

## Output targets

- `results/tables/baseline_randomness_tests.csv`
- `results/tables/tda_feature_summary.csv`
- `results/tables/control_condition_comparison.csv`
- `results/logs/run_manifest.json`
- `results/figures/randomness_vs_tda_summary.png`

## Reproducibility rules

- Record seeds and software versions.
- Write a run manifest for each benchmark run.
- Do not overwrite prior result tables without archiving the run manifest.
- Keep baseline and control-condition outputs separate.
