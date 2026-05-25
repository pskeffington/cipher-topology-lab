# Benchmark Roadmap

## Purpose

This roadmap converts `cipher-topology-lab` from a research scaffold into an executable AI/cybersecurity evaluation benchmark.

The benchmark evaluates whether conventional randomness diagnostics and topological summaries can distinguish strong cryptographic or pseudorandom baselines from structured, weak, biased, or intentionally degraded controls.

## Core Rule

No scaffolded values should be treated as empirical results. Placeholder CSVs and figures define schemas only. All manuscript-weight claims require generated outputs from the executable pipeline.

## Benchmark Thesis

The project should demonstrate evaluation discipline rather than cryptanalytic overclaiming.

A strong result is one of the following:

```text
1. Topological diagnostics fail to distinguish strong baselines from each other, as expected.
2. Topological diagnostics distinguish weak or biased controls from strong baselines.
3. Topological diagnostics add no measurable value beyond conventional randomness tests.
4. Topological diagnostics add limited value in specific structured-control settings.
```

Any of these outcomes is publishable if the benchmark is reproducible, well-controlled, and honestly interpreted.

## Benchmark Families

### Family A: Strong Baselines

| Condition | Generator | Purpose |
|---|---|---|
| `AES_128_CTR_baseline` | AES-128 CTR | Primary modern block-cipher stream baseline |
| `SHA256_expansion_baseline` | SHA-256 expansion | Deterministic reproducibility baseline |
| `OS_CSPRNG_sensitivity` | OS random source | Non-deterministic sensitivity baseline |

### Family B: Weak Positive Controls

| Condition | Generator | Purpose |
|---|---|---|
| `LCG_weak_control` | Linear congruential generator | Obvious weak generator |
| `xorshift_weak_control` | xorshift | Simple weak generator with less trivial structure |
| `biased_bitstream_control` | Biased Bernoulli bitstream | Sanity check for diagnostic sensitivity |

### Family C: Structured Controls

| Condition | Generator | Purpose |
|---|---|---|
| `repeated_plaintext_control` | AES-CTR over repeated plaintext | Detect effect of structured input if implementation exposes pattern risk |
| `low_entropy_plaintext_control` | AES-CTR over low-entropy plaintext | Verify strong cipher output remains indistinguishable under proper mode use |
| `truncated_counter_control` | intentionally malformed counter behavior | Detect implementation-level degradation |

### Family D: Legacy / Comparator Conditions

| Condition | Generator | Purpose |
|---|---|---|
| `DES_legacy_comparator` | DES-like legacy condition | Historical comparator only; not a modern target |
| `Ascon_lightweight_comparator` | Ascon | Planned lightweight-cryptography comparator |

## Diagnostic Layer 1: Conventional Randomness Metrics

Minimum v0.1 metrics:

```text
monobit frequency
byte entropy
serial correlation
runs count
compression ratio
byte chi-square statistic
```

Later metrics:

```text
block frequency
approximate entropy
serial test variants
autocorrelation by lag
NIST STS export format
PractRand/TestU01 export hooks
```

## Diagnostic Layer 2: Embedding Methods

Minimum v0.1 embeddings:

```text
byte sliding windows
bit sliding windows
byte-pair point clouds
fixed-length chunk vectors
```

Later embeddings:

```text
frequency-domain embeddings
ordinal-pattern embeddings
cubical-complex image embeddings
multi-scale delay embeddings
```

## Diagnostic Layer 3: Topological Features

Minimum v0.1 features:

```text
H0 total persistence
H0 max lifetime
H0 persistence entropy
H1 total persistence
H1 max lifetime
H1 persistence entropy
Betti curve summaries
landscape norm summaries
```

Later features:

```text
persistence images
bottleneck distance matrix
Wasserstein distance matrix
bootstrap confidence intervals
condition-level classifier diagnostics
```

## Required Output Artifacts

### Tables

```text
results/tables/baseline_randomness_tests.csv
results/tables/tda_feature_summary.csv
results/tables/control_condition_comparison.csv
results/tables/reproducibility_audit.csv
```

### Figures

```text
results/figures/persistence_diagram_baseline.svg
results/figures/persistence_diagram_weak_control.svg
results/figures/randomness_vs_tda_summary.svg
results/figures/condition_distance_heatmap.svg
```

### Logs

```text
results/logs/run_manifest.json
results/logs/output_checksums.json
```

### Manuscript Artifacts

```text
manuscript/cipher_topology_whitepaper.md
manuscript/cipher_topology_whitepaper.pdf
```

## v0.1 Execution Plan

### Step 1: Stream Generation

Build:

```text
src/ciphertopology/streams.py
scripts/run_generate_streams.py
tests/test_stream_generation.py
```

Acceptance:

```text
- Generates deterministic AES, SHA, LCG, xorshift, and biased streams.
- Writes streams or summaries to data/interim/.
- Records seed, key, IV, generator family, stream length, and condition label.
```

### Step 2: Conventional Diagnostics

Build:

```text
src/ciphertopology/randomness_tests.py
scripts/run_randomness_tests.py
tests/test_randomness_report_schema.py
```

Acceptance:

```text
- Produces `results/tables/baseline_randomness_tests.csv` from generated streams.
- No placeholder values remain.
- Every row has condition, generator_family, seed_id, n_bytes, metric fields, and diagnostic label.
```

### Step 3: Embeddings

Build:

```text
src/ciphertopology/embeddings.py
tests/test_embedding_shapes.py
```

Acceptance:

```text
- Byte sliding-window embeddings return stable shapes.
- Embedding functions validate input sizes.
- Embedding metadata is preserved for downstream TDA.
```

### Step 4: TDA Feature Extraction

Build:

```text
src/ciphertopology/tda_features.py
scripts/run_tda_features.py
tests/test_tda_feature_schema.py
```

Acceptance:

```text
- Produces `results/tables/tda_feature_summary.csv` from generated embeddings.
- Writes at least H0/H1 summaries or a documented fallback if backend unavailable.
- Schema remains stable for manuscript tables.
```

### Step 5: Figures

Build:

```text
src/ciphertopology/plotting.py
scripts/run_figures.py
```

Acceptance:

```text
- Replaces scaffold SVG with computed baseline diagram or documented schematic generated from real feature output.
- Produces at least one baseline and one weak-control figure.
```

### Step 6: Audit and Manifest

Build:

```text
src/ciphertopology/reporting.py
scripts/run_baseline_eval.py
```

Acceptance:

```text
- `run_manifest.json` records commit ref, timestamp, parameters, output paths, and placeholder-free status.
- Output checksum file exists.
```

## v0.1 Make Targets

```makefile
smoke:
	python scripts/run_baseline_eval.py --profile smoke

data:
	python scripts/run_generate_streams.py --profile baseline

analysis:
	python scripts/run_randomness_tests.py --profile baseline
	python scripts/run_tda_features.py --profile baseline

figures:
	python scripts/run_figures.py --profile baseline

manifest:
	python scripts/run_baseline_eval.py --profile baseline --manifest-only
```

## v0.1 Definition of Done

```text
1. `make smoke` runs without error.
2. Placeholder tables are replaced by generated outputs.
3. At least one real table and one real figure exist.
4. Run manifest confirms generated status.
5. Tests cover stream generation and output schema.
6. White paper has methods and limitations sections.
```

## v0.2 Extension

```text
add structured controls
add bootstrap replicates
add condition-distance heatmap
add classifier-free separability summary
add external randomness-test export format
add GitHub Actions workflow
```

## v0.3 Extension

```text
add Ascon comparator
add DES/TDEA legacy comparator
add persistence-image features
add reproducibility release packet
add manuscript PDF build
```

## Manuscript Claim Policy

Allowed claims after v0.1:

```text
The benchmark generated controlled stream conditions and compared conventional randomness diagnostics with topological feature summaries.
```

Disallowed claims unless directly supported:

```text
TDA breaks AES.
TDA detects cryptographic weakness in modern ciphers.
The method is superior to established randomness batteries.
The method is operationally useful for cryptanalysis.
```

Preferred claim style:

```text
Topological summaries are evaluated as auxiliary diagnostic features under controlled synthetic conditions, with explicit weak positive controls and strong cryptographic baselines.
```
