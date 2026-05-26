# Changelog

## v0.4.1-pre.1

### Evidence package

- Added the 64-replicate manuscript evidence configuration at `configs/experiment_64rep.json`.
- Produced manuscript-scale internal evidence with 384 streams, 768 embeddings, 1,536 persistent-homology feature rows, 384 internal randomness-diagnostic rows, and 1,536 distance-to-baseline rows.
- Confirmed manuscript-grade `ripser` backend output with no fallback backend detected.
- Established the central internal finding: LCG weak-control separation from the SHA-256 seeded baseline under byte-pair H0 persistence-entropy and distance-to-baseline summaries.
- Preserved cautious interpretation for AES-CTR, OS CSPRNG, and xorshift32, which did not show comparable separation under the current embeddings and feature set.

### Workflow

- Added an object-oriented segmented workflow runner in `scripts/11_run_micro_workflow.py`.
- Added the executable terminal wrapper `scripts/run_segmented.sh`.
- Added partial/final segmented run reporting at `results/logs/segmented_run_report.md`.
- Added Makefile shortcuts for segmented smoke, full, stage-specific, and external-randomness workflows.

### External randomness testing

- Added failure-safe external randomness runner `scripts/12_run_external_randomness.py`.
- Added explicit external-test availability reporting at `results/logs/external_randomness_status.md`.
- Updated the evidence register to distinguish unavailable external infrastructure from completed external randomness-test results.
- Removed stale zero-byte Dieharder placeholder outputs from tracked evidence.

### Manuscript

- Added a Related Work section covering statistical randomness testing, persistent homology/TDA, TDA on generated structures, and limits of empirical diagnostics.
- Updated Results with the 64-replicate `ripser` findings.
- Updated Discussion and Conclusion to reflect completed internal evidence and the audited but unavailable Dieharder status.
- Updated the replication appendix to use `configs/experiment_64rep.json` as the manuscript evidence configuration.

### Documentation

- Updated README, protocol, publication plan, and data dictionary for the current 64-replicate evidence package and ERT status workflow.
