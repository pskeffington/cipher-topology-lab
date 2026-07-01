# 2026-07-01 RAG Provenance Scanner Development Note

## Development action

Added the first implementation slice for a **Cryptographic Provenance Scanner for RAG** inside `cipher-topology-lab`.

## Why this belongs in the lab

The existing lab already maintains a strict evidence-register and claim-boundary discipline for cryptographic diagnostics. The RAG provenance scanner reuses that discipline for AI-security workflows where files, reports, APIs, GIS layers, and datasets may be embedded or retrieved by AI systems without durable proof of origin.

## Added files

- `src/ciphertopology/rag_provenance.py`
- `scripts/13_rag_provenance_scan.py`
- `docs/rag_provenance_scanner.md`
- `tests/test_rag_provenance.py`

## Make target

Added:

```bash
make rag-provenance
```

Default outputs:

- `results/provenance/rag_provenance_manifest.json`
- `results/provenance/rag_provenance_report.md`

## Current capability

The scanner can:

1. scan a repository, document folder, data folder, or GIS source directory;
2. generate file-level SHA-256 fingerprints;
3. generate deterministic line-window chunk hashes for readable text files;
4. classify assets as documents, datasets, GIS layers, code/config, or unknown;
5. flag draft, archived, stale-looking, unknown-extension, and GIS candidate assets;
6. write a JSON manifest and Markdown report.

## Claim boundary

This module provides provenance evidence only. It does not certify source truth, data completeness, model safety, cryptographic security, or regulatory compliance. It also does not alter the repository's existing cipher/TDA research claims.

## Next build step

Add a verifier that takes a RAG answer object and checks whether each cited chunk maps to an approved manifest asset and chunk hash.
