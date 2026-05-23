# Roadmap

## Project aim

Build a reproducible research package for testing whether persistent-homology summaries of ciphertext-derived point clouds provide useful auxiliary diagnostics for symmetric-cipher output randomness.

The project is not a cipher-breaking claim. It is a reproducible diagnostics and measurement study.

## Version sequence

### v0.1.0-pre.0 — Repository scaffold and runnable baseline

Status: active.

Exit criteria:

- Repository has installable Python package metadata.
- Stream generation runs for AES-128, OS CSPRNG, and weak controls.
- Embedding scripts create byte-pair and sliding-window point-cloud inputs.
- TDA feature script computes H0/H1 features.
- Internal randomness diagnostics run.
- Python CI passes unit tests and lint checks.
- Manuscript scaffold compiles locally.

### v0.2.0-pre.0 — Ascon integration

Exit criteria:

- Add a pinned Ascon implementation path.
- Add Ascon stream-generation condition.
- Record implementation source and version in manifest.
- Add tests verifying deterministic Ascon-stream generation where applicable.
- Update manuscript background and methods.

### v0.3.0-pre.0 — External randomness batteries

Exit criteria:

- Add NIST SP 800-22 execution notes or wrapper.
- Add Dieharder/TestU01-compatible export format.
- Store randomness-test outputs in `results/tables/`.
- Add parser into unified result tables.
- Add manuscript table shell for conventional diagnostics.

### v0.4.0-pre.0 — Topological analysis expansion

Exit criteria:

- Add cubical-complex image encoding.
- Add persistence-diagram export.
- Add bottleneck or Wasserstein distance comparisons to random baseline.
- Add effect-size reporting across conditions.
- Add reproducible figure scripts.

### v0.5.0-pre.0 — Manuscript evidence package

Exit criteria:

- Complete results section from generated tables.
- Complete discussion with restrained claims.
- Verify all citations against official pages, DOI records, or publisher pages.
- Add replication appendix.
- Create release candidate tag.

## Immediate execution order

1. Harden package metadata and tests.
2. Fix internal monobit test numeric behavior.
3. Add local smoke-test config for fast runs.
4. Add issue-tracked work units for Ascon, external randomness tests, TDA expansion, and manuscript evidence.
5. Run and inspect CI after the next push.
