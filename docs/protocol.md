# Protocol v0.4.1-pre.0

## Objective

Evaluate whether persistent-homology summaries of ciphertext-derived point clouds provide an auxiliary diagnostic for distinguishing standard symmetric-cipher output from structured deterministic controls and weak-generator positive controls.

## Primary research question

Can persistent-homology features distinguish structured or weakened ciphertext-generation conditions from standard deterministic cipher-output baselines, and how do these topological diagnostics compare with conventional statistical randomness-test batteries?

## Configured conditions

| Condition | Description | Role |
|---|---|---|
| `aes128_ctr_xor_deterministic_plaintext` | AES-128 CTR output produced under deterministic plaintext generation | modern cipher condition with reproducible structured plaintext input |
| `aes128_ctr_keystream_zero_plaintext` | AES-128 CTR keystream obtained by encrypting zero plaintext | controlled AES keystream condition |
| `sha256_seeded_baseline` | deterministic SHA-256 expansion from seeded inputs | primary reproducibility baseline |
| `os_csprng` | operating-system cryptographic RNG output | non-deterministic sensitivity baseline |
| `lcg_weak` | linear congruential generator output | weak positive control |
| `xorshift32_weak` | xorshift32 output | weak positive control |

Ascon remains a planned lightweight-cryptography comparator. DES/TDEA should be added only as a deprecated legacy control, not as a modern security target.

## Data-generation principle

Every reproducible stream must be traceable from condition name, replicate index, master seed, key or seed material, nonce or counter initialization where applicable, plaintext pattern or generator parameters, output byte count, software version, and SHA-256 digest. The OS CSPRNG condition is retained as a sensitivity condition and is not the primary reproducibility baseline.

## Embedding methods

The current configured embeddings are `byte_pair_2d` and `sliding_window_8d`. The codebase also contains a `cubical_image_2d` embedding path for GUDHI cubical-complex experiments when explicitly included in a config.

## TDA features

Core features include interval counts, finite interval counts, finite lifetime mean, finite lifetime standard deviation, finite lifetime maximum, and persistence entropy for configured homology dimensions.

## Backend rule

Publication-grade evidence must use true persistent-homology backends such as ripser or GUDHI. Any fallback or development backend is diagnostic only and must not be used as manuscript evidence.

## Baseline-distance rule

Distance-to-baseline tables must identify the configured `baseline_condition`. For `v0.4.1-pre.0`, that baseline is `sha256_seeded_baseline`; OS CSPRNG is a separate non-deterministic sensitivity condition.

## Interpretation rule

This project does not certify cipher security and does not claim to break AES, Ascon, DES, or any standardized cipher. It tests whether topological summaries add diagnostic information relative to conventional tests and known weak controls.
