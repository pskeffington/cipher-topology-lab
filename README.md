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
| AES-128 | Primary modern block-cipher baseline |
| Ascon | Lightweight-cryptography comparison |
| OS CSPRNG | Random baseline |
| LCG / xorshift | Weak-generator positive controls |
| DES / TDEA | Deprecated legacy comparator only |

DES and TDEA are not treated as modern security targets.

## Why this project is data-accessible

No restricted datasets are required. The complete dataset is generated locally from documented seeds, keys, nonces, plaintext patterns, and generator settings.

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
│   └── 04_analyze_results.py
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
make features
make analysis
make manuscript
```

## Initial publication frame

This project is suitable for an applied cryptography, cybersecurity engineering, computational topology, or reproducible research venue. The paper should be framed as a diagnostic and reproducibility contribution, not as cryptanalysis.

## Status

`v0.1.0-pre.0`: repository scaffold and pre-analysis protocol.
