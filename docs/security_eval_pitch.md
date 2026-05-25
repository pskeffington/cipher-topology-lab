# Security Evaluation Pitch

## Project Title

**Topological Diagnostics of Symmetric-Cipher Output Randomness**

## Strategic Frame

This project is a reproducible AI/cybersecurity evaluation benchmark. It evaluates whether topological summaries of ciphertext-derived data can serve as auxiliary diagnostics for distinguishing standard cryptographic output from structured, weak, biased, or intentionally degraded controls.

The project does not claim to break AES, Ascon, DES, or any standardized cipher. It is an evaluation-infrastructure project: controlled inputs, reproducible generation, baseline randomness diagnostics, topological feature extraction, weak-control comparisons, audit logs, and manuscript-ready outputs.

## Frontier AI Security Relevance

Frontier AI security and preparedness teams need evaluation systems that can measure technical risk under controlled conditions. This project demonstrates the same core pattern required for AI cyber evaluations:

```text
threat model -> controlled tasks -> reproducible generation -> diagnostic metrics -> weak/positive controls -> audit logs -> result tables -> figures -> white paper
```

The immediate technical object is cryptographic randomness diagnostics. The broader portfolio object is a reusable template for cyber/security evaluation systems.

## Research Question

Can persistent-homology features and related topological summaries distinguish structured or weakened ciphertext-generation conditions from standard AES/SHA/CSPRNG baselines, and how do these summaries compare with conventional statistical randomness diagnostics?

## Evaluation Hypothesis

Topological summaries should not distinguish properly generated modern cipher outputs from strong pseudorandom baselines at useful rates. They may, however, detect structured or intentionally weakened controls such as LCG, xorshift, repeated plaintext patterns, biased streams, or malformed generation settings.

A useful result is not “TDA breaks encryption.” A useful result is a calibrated diagnostic profile showing where topological methods fail, where they detect trivial structure, and whether they add anything beyond standard randomness tests.

## Controlled Conditions

| Condition | Role |
|---|---|
| AES-128 CTR | Primary modern block-cipher stream baseline |
| SHA-256 expansion | Deterministic reproducibility baseline |
| OS CSPRNG | Non-deterministic sensitivity baseline |
| LCG | Weak-generator positive control |
| xorshift | Weak-generator positive control |
| Repeated plaintext under controlled settings | Structure-control condition |
| Biased bitstream | Positive control for trivial structure |
| DES/TDEA | Legacy comparator only, not modern target |
| Ascon | Planned lightweight-cryptography comparator |

## Diagnostic Families

### Conventional Diagnostics

```text
monobit frequency
block frequency
runs
serial tests
entropy estimates
autocorrelation
compression ratio
basic NIST-style summary placeholders
```

### Topological Diagnostics

```text
point-cloud embeddings
sliding-window embeddings
cubical-complex summaries
persistence diagrams
Betti curve summaries
persistence entropy
landscape statistics
summary vector comparisons
```

## Expected Outputs

```text
results/tables/baseline_randomness_tests.csv
results/tables/tda_feature_summary.csv
results/tables/control_condition_comparison.csv
results/figures/persistence_diagram_baseline.png
results/figures/persistence_diagram_weak_control.png
results/figures/randomness_vs_tda_summary.png
results/logs/run_manifest.json
manuscript/cipher_topology_whitepaper.pdf
```

## Technical Acceptance Criteria

The first benchmark release should satisfy:

```text
1. All generated streams are documented with seeds, keys, IVs, generator settings, and condition labels.
2. Baseline diagnostic results are written to CSV.
3. TDA features are written to CSV with stable schema.
4. At least one persistence diagram or summary figure is generated.
5. A run manifest records timestamp, parameters, code version, and output paths.
6. A smoke command can execute a small end-to-end version.
```

## Security Boundaries

This project is diagnostic and defensive. It does not provide exploit instructions, operational attack procedures, unauthorized access methods, or claims of practical cryptanalytic compromise.

The project deliberately uses controlled, locally generated streams and transparent weak controls. The purpose is to evaluate diagnostic methods, not to weaken or attack deployed systems.

## Role Alignment

### Frontier Cybersecurity / Preparedness

This project demonstrates capacity to build a controlled technical evaluation system for cyber-risk measurement.

### Agentic Cyber Evaluation

The same architecture can support agentic cyber-eval tasks by replacing stream conditions with sandboxed tool-use tasks, scoring functions, audit logs, and failure-mode reports.

### AI Safety Infrastructure

The project models a broader safety-infrastructure pattern: every claim should trace to reproducible data, executable code, metrics, and logged artifacts.

### Research Engineering

The project is structured for Makefile execution, CI hardening, tests, result artifacts, figures, and manuscript production.

## Portfolio Message

This repo is the technical lead object for a portfolio aimed at frontier AI security, preparedness, agentic cyber evaluation, and principal research engineering roles. It converts abstract cyber-risk interest into an executable evaluation pipeline.

## Next Build Steps

```text
1. Add or verify stream-generation smoke path.
2. Add baseline randomness diagnostics table.
3. Add TDA feature schema.
4. Add one persistence figure.
5. Add run manifest.
6. Draft short white paper.
```
