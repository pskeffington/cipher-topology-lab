# cipher-topology-lab

**Formal project title:** *Topological Diagnostics of Symmetric-Cipher Output Randomness*

This repository is a reproducible research workspace for evaluating whether topological data analysis (TDA), especially persistent homology, can serve as an auxiliary diagnostic for symmetric-cipher output randomness.

The project does **not** claim to break AES, Ascon, DES, or any standardized cipher. It evaluates whether ciphertext-derived point clouds produce topological summaries that distinguish standard cipher output from structured, weak, or intentionally biased controls.

## Research question

Can persistent-homology features distinguish structured or weakened ciphertext-generation conditions from standard AES and Ascon ciphertext outputs, and how do these topological diagnostics compare with conventional statistical randomness-test batteries?

## Primary contribution

A reproducible pipeline that:

1. Generates ciphertext streams under controlled conditions.
2. Converts bitstreams and byte streams into point clouds or cubical-complex inputs.
3. Computes persistent-homology features.
4. Benchmarks topological summaries against conventional randomness diagnostics.
5. Produces manuscript-ready tables, figures, and audit logs.

## Cipher scope

| Class | Role |
|---|---|
| AES-128 CTR | Primary modern block-cipher stream baseline |
| SHA-256 expansion | Deterministic reproducibility baseline |
| OS CSPRNG | Non-deterministic sensitivity baseline |
| LCG / xorshift | Weak-generator positive controls |
| Ascon | Planned lightweight-cryptography comparison |
| DES / TDEA | Planned deprecated legacy comparator only |

DES and TDEA are not treated as modern security targets.

## Why this project is data-accessible

No restricted datasets are required. The complete primary dataset is generated locally from documented seeds, keys, CTR initial values, plaintext patterns, and generator settings. The OS CSPRNG condition is retained as a non-deterministic sensitivity condition, not as the primary reproducibility baseline.

## Repository structure

```text
cipher-topology-lab/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── docs/
│   ├── protocol.md
│   ├── data_dictionary.md
│   └── publication_plan.md
├── manuscript/
│   ├── main.tex
│   ├── references.bib
│   └── sections/
├── results/
│   ├── figures/
│   ├── tables/
│   └── logs/
├── scripts/
│   ├── 00_generate_streams.py
│   ├── 01_embed_ciphertext.py
│   ├── 02_compute_tda_features.py
│   ├── 03_randomness_tests.py
│   ├── 04_analyze_results.py
│   ├── 05_export_randomness_inputs.py
│   ├── 06_parse_external_results.py
│   └── 07_validate_tda_backend.py
├── src/
│   └── ciphertopology/
├── tests/
├── .github/workflows/
├── pyproject.toml
├── environment.yml
├── Makefile
└── README.md
```

## Minimal workflow

```bash
make setup
make data
make embed
make features
make analysis
make manuscript
```

## Smoke workflow

```bash
make setup
make smoke
```

## Initial publication frame

This project is suitable for an applied cryptography, cybersecurity engineering, computational topology, or reproducible research venue. The paper should be framed as a diagnostic and reproducibility contribution, not as cryptanalysis.

## Status

`v0.4.1-pre.0`: execution-repair pre-release with deterministic baseline, corrected AES-CTR metadata language, stratified TDA outputs, and standardized distance metrics.
