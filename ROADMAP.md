# Roadmap

## Project aim

Build a reproducible research package for testing whether persistent-homology summaries of ciphertext-derived point clouds provide useful auxiliary diagnostics for symmetric-cipher output randomness.

The project is not a cipher-breaking claim. It is a reproducible diagnostics and measurement study.

## Version sequence

### v0.1.0-pre.0 — Repository scaffold and runnable baseline

Status: completed.

Exit criteria:

- Repository has installable Python package metadata.
- Stream generation runs for AES-128, OS CSPRNG, and weak controls.
- Embedding scripts create byte-pair and sliding-window point-cloud inputs.
- TDA feature script computes H0/H1 features.
- Internal randomness diagnostics run.
- Python CI passes unit tests and lint checks.
- Manuscript scaffold compiles locally.

### v0.2.0-pre.0 — Ascon integration

Status: open.

Exit criteria:

- Add a pinned Ascon implementation path.
- Add Ascon stream-generation condition.
- Record implementation source and version in manifest.
- Add tests verifying deterministic Ascon-stream generation where applicable.
- Update manuscript background and methods.

### v0.3.0-pre.0 — External randomness batteries

Status: completed for export and parser scaffold; pending imported external-suite outputs.

Exit criteria:

- Add NIST SP 800-22 execution notes or wrapper.
- Add Dieharder/TestU01-compatible export format.
- Store randomness-test outputs in `results/tables/`.
- Add parser into unified result tables.
- Add manuscript table shell for conventional diagnostics.

### v0.4.0-pre.0 — Topological analysis expansion

Status: implementation complete; manuscript-scale verification pending.

Exit criteria:

- Add cubical-complex image encoding.
- Add GUDHI cubical persistence features.
- Add distance-to-OS-CSPRNG baseline comparisons.
- Add effect-size reporting across conditions.
- Add reproducible stratified figure scripts.

### v0.5.0-pre.0 — Manuscript evidence package

Status: active.

Exit criteria:

- Run `configs/manuscript_30rep.json` through the manual manuscript-analysis workflow.
- Confirm `ripser` and `gudhi_cubical` backends are present.
- Confirm H1 figures are generated only for backend/embedding groups with finite H1 signal.
- Complete results section from generated tables.
- Complete discussion with restrained claims.
- Verify all citations against official pages, DOI records, or publisher pages.
- Add replication appendix.
- Create release candidate tag.

## Immediate execution order

1. Trigger `Manuscript Analysis` workflow with `configs/manuscript_30rep.json`.
2. Inspect `tda_backend_summary.csv`, `tda_feature_summary.csv`, and `tda_distance_to_os_csprng.csv`.
3. Promote only nonzero-signal stratified figures into manuscript candidates.
4. Add Ascon only after selecting a pinned implementation path.
5. Draft results from 30-replicate tables, not smoke-test artifacts.
