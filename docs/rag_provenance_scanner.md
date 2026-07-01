# Cryptographic Provenance Scanner for RAG

## Purpose

The RAG provenance scanner adds a platform-facing control layer for retrieval-augmented generation workflows that ingest files, APIs, drives, PDFs, GIS layers, and databases. Its purpose is to create pre-ingestion source evidence before content is embedded, indexed, summarized, or used by an AI agent.

This module extends the repository's evidence-register posture. It does not change the scientific claim boundary of the cipher/TDA experiments and does not claim cryptanalysis, source truth, model safety, or security certification.

## Problem

RAG systems often treat source material as available context without preserving strong proof of origin. Common gaps include:

- no durable fingerprint for the original file;
- no chunk-level fingerprint for text used in embeddings;
- weak distinction between source files, derived chunks, generated answers, and review actions;
- stale or archived files entering retrieval indexes;
- GIS layers and infrastructure datasets moving into AI workflows without layer-level provenance;
- difficulty reproducing which source version supported a model answer.

## Initial deliverable

The first implementation creates:

- `src/ciphertopology/rag_provenance.py` — dependency-light scanner core;
- `scripts/13_rag_provenance_scan.py` — command-line runner;
- `results/provenance/rag_provenance_manifest.json` — default JSON manifest target;
- `results/provenance/rag_provenance_report.md` — default Markdown report target.

## What the manifest records

Each scanned file receives a deterministic asset record:

```json
{
  "asset_id": "asset-...",
  "path": "docs/example.md",
  "source_type": "document",
  "extension": ".md",
  "bytes": 1234,
  "sha256": "...",
  "modified_utc": "2026-07-01T00:00:00Z",
  "trust_flags": ["chunk_hashable"],
  "chunks": []
}
```

Text-like files also receive deterministic line-window chunk hashes. Binary files receive file-level fingerprints only until an extractor is registered.

## Source classes

The scanner currently classifies assets into conservative operational classes:

| Class | Examples | Initial handling |
|---|---|---|
| `document` | `.md`, `.txt`, `.pdf`, `.docx` | text chunks when readable; otherwise file hash |
| `dataset` | `.csv`, `.json`, `.xlsx`, `.sqlite`, `.db` | file hash; text chunks where readable |
| `gis_layer` | `.geojson`, `.gpkg`, `.shp`, `.tif`, `.tiff` | file hash and GIS candidate flag |
| `code_or_config` | `.py`, `.yaml`, `.yml`, config-named files | file and text chunk hashes |
| `unknown` | unregistered extensions | file hash and review flag |

## Run command

From a configured development environment:

```bash
python scripts/13_rag_provenance_scan.py --root .
```

Scan only Markdown and JSON files:

```bash
python scripts/13_rag_provenance_scan.py \
  --root . \
  --include-extension .md \
  --include-extension .json
```

Change chunk size:

```bash
python scripts/13_rag_provenance_scan.py --root . --lines-per-chunk 50
```

## Acceptance criteria

The scanner is ready for the next platform step when it can:

1. generate a stable manifest for a repository, document folder, or GIS source directory;
2. hash file-level assets deterministically;
3. hash text chunks deterministically;
4. flag unknown, stale, archived, draft, or GIS candidate material for review;
5. write a machine-readable JSON manifest and a human-readable report;
6. preserve clear claim-boundary language.

## Next development steps

1. Add extractor adapters for PDFs, spreadsheets, and GIS formats.
2. Add Google Drive and GitHub connector metadata fields.
3. Add a verifier that checks whether a RAG answer cites only manifest-approved source chunks.
4. Add signature support for manifests and selected source registries.
5. Add a GIS layer registry profile for town, utility, emergency, and critical-infrastructure overlays.
6. Add CI tests for deterministic output on a fixture directory.

## Product framing

This module can be productized as **Resilient Provenance** or **ProofLayer AI**:

> A cryptographic control layer for proving which source files and chunks entered an AI retrieval pipeline, which assets require review, and which outputs can be traced back to approved source material.
