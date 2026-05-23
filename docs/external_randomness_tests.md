# External Randomness-Test Integration

## Purpose

This document defines how generated cipher and control streams are exported for external randomness-test suites. These tests are diagnostic tools only. They do not establish cryptographic security and do not replace cryptanalysis.

## Export command

Use the repository target:

```bash
make export-randomness
```

The command copies generated binary streams from `data/raw/` into `external_tests/inputs/` and creates an export manifest with SHA-256 digests.

## Exported files

| Path | Purpose |
|---|---|
| `external_tests/inputs/*.bin` | binary input files for external suites |
| `external_tests/inputs/export_manifest.csv` | stream identifiers, conditions, sizes, paths, and hashes |
| `external_tests/inputs/run_dieharder.sh` | convenience script for Dieharder |
| `external_tests/inputs/README_NIST_STS.md` | local notes for NIST STS execution |

## Dieharder

Dieharder can consume binary files using file-input mode. The generated helper script runs the full battery over each exported stream and writes text output under `external_tests/results/dieharder/`.

Record the Dieharder version before reporting results.

## NIST SP 800-22 STS

NIST STS usually requires local compilation and local path configuration. Use the exported binary files as input material, then archive the exact STS version, compiler, selected tests, bitstream length, number of bitstreams, and output directory structure.

## Reporting rule

External randomness-test results should be reported as conventional diagnostics. They should be compared with TDA features, not treated as proof that a cipher is secure or insecure.
