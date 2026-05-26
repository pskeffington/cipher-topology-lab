# Release Notes: v0.4.1-pre.1

## Summary

`v0.4.1-pre.1` is a reproducibility and evidence checkpoint for *Topological Diagnostics of Symmetric-Cipher Output Randomness*. It converts the project from an execution-repair pre-release into a manuscript-ready internal evidence package with a validated 64-replicate `ripser` run, segmented workflow tooling, related-work manuscript expansion, and explicit external-randomness-test status reporting.

## Current evidence run

The manuscript evidence configuration is:

```text
configs/experiment_64rep.json
```

The run produced:

```text
384 streams
768 embeddings
1,536 persistent-homology feature rows
384 internal randomness-diagnostic rows
1,536 distance-to-baseline rows
```

The evidence register reports:

```text
Observed TDA backend: ripser
Fallback backend detected: False
Baseline condition: sha256_seeded_baseline
```

## Primary result

The strongest and most stable internal result is the separation of the LCG weak-control condition from the SHA-256 seeded baseline under byte-pair H0 summaries. The 64-replicate run supports this finding in both persistence entropy and Euclidean distance-to-baseline.

AES-CTR deterministic-output conditions, OS CSPRNG output, and xorshift32 did not show comparable separation under the current embeddings and feature set.

## External randomness status

External randomness testing is implemented but not populated in the current local evidence run because Dieharder was unavailable on the local execution path.

The current evidence register records:

```text
External runner status: UNAVAILABLE
External runner message: Dieharder executable not found on PATH: dieharder
```

This is an audited infrastructure limitation, not a completed external-test comparison.

## Key files

```text
configs/experiment_64rep.json
scripts/11_run_micro_workflow.py
scripts/run_segmented.sh
scripts/12_run_external_randomness.py
docs/evidence_register.md
results/logs/segmented_run_report.md
results/logs/external_randomness_status.md
manuscript/sections/related_work.tex
manuscript/sections/results.tex
manuscript/sections/discussion.tex
manuscript/sections/conclusion.tex
```

## Reproduction commands

Set up the project:

```bash
make setup
```

Run the 64-replicate internal evidence workflow:

```bash
./scripts/run_segmented.sh full --strict --python .venv/bin/python --config configs/experiment_64rep.json
```

Run failure-safe external randomness status capture:

```bash
python scripts/12_run_external_randomness.py --allow-missing-dieharder
```

Rebuild the evidence register:

```bash
python scripts/09_build_evidence_register.py \
  --config configs/experiment_64rep.json \
  --output docs/evidence_register.md
```

Build the manuscript:

```bash
cd manuscript
latexmk -pdf main.tex
cd ..
```

## Remaining work before submission

- Run Dieharder or NIST SP 800-22 in an environment where those tools are available.
- Import external randomness-test outputs through the parser.
- Add explicitly configured cubical-complex experiments when ready.
- Consider additional weak-generator controls beyond LCG and xorshift32.
- Decide whether to archive generated figure/table artifacts in a release asset rather than tracking them directly in Git.
