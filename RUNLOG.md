# Run Log

## 2026-05-23 — v0.1.0 smoke validation

### Scope

Validated the initial repository scaffold against the smoke-test configuration.

### Configuration

- Config: `configs/smoke_test.json`
- Conditions: AES-128 CTR random plaintext, AES-128 CTR zero plaintext, OS CSPRNG, LCG weak control, xorshift32 weak control
- Replicates: 2
- Stream size: 4,096 bytes
- Embeddings: byte-pair 2D, sliding-window 8D

### Local validation result

- Unit tests passed.
- Ruff passed after removing unused-import defects.
- Stream generation completed.
- Embedding generation completed.
- Internal randomness diagnostics completed.
- TDA feature computation completed using the development fallback backend when `ripser` was unavailable.
- Analysis summary and figure generation completed.

### Limitation

The fallback threshold-graph backend is for development execution only. It is not manuscript-grade persistent homology and must not be used for publication claims. Manuscript evidence must be generated with `ripser` or GUDHI.

### Resulting hardening commits

- Fixed signed-bit arithmetic in the internal monobit-frequency test.
- Added explicit `src/` package build metadata.
- Added smoke-test configuration.
- Added TDA fallback backend.
- Added TDA schema tests.
- Added `make smoke` command.
