# Null and Control Design

## Purpose

This document freezes the evaluation roles for the cipher-topology laboratory workstream. The project evaluates whether persistent-homology summaries of ciphertext-derived point clouds can act as auxiliary diagnostics for structured or weakened output conditions. It does not claim to break AES, Ascon, DES, TDEA, or any standardized cipher.

## Primary null frame

The primary null frame is that topological summaries should not produce stable, interpretable separation between modern cipher-output conditions and the deterministic reproducibility baseline under the configured embedding and feature set.

The current deterministic baseline is:

- `sha256_seeded_baseline`

This baseline is used for reproducibility and distance-to-baseline comparisons. It is not a security target and should not be described as a superior or inferior cipher.

## Sensitivity baseline

The non-deterministic sensitivity baseline is:

- `os_csprng`

This condition helps assess whether observed summaries are robust to non-deterministic cryptographic RNG output. Because it is not deterministic across machines or reruns, it should not be treated as the primary reproducibility baseline.

## Standard cipher-output conditions

The currently configured AES conditions are:

- `aes128_ctr_xor_deterministic_plaintext`
- `aes128_ctr_keystream_zero_plaintext`

These are modern block-cipher stream conditions used for diagnostic comparison. They must not be framed as broken or weakened unless the experiment explicitly introduces a weakened condition and the evidence supports that claim.

## Positive controls

The weak-generator positive controls are:

- `lcg_weak`
- `xorshift32_weak`

Positive controls are included to test whether the pipeline can detect known structured or weak output mechanisms. The current internal evidence frame treats LCG weak-control separation from the SHA-256 seeded baseline under byte-pair H0 summaries as the strongest stable internal result. Xorshift32 has not shown comparable separation under the current feature set.

## Planned comparators

Planned comparators should remain clearly labeled as future or extension work until implemented and registered:

- Ascon: planned lightweight-cryptography comparator.
- DES/TDEA: planned deprecated legacy comparator only, not a modern security target.

DES and TDEA should never be presented as current modern security baselines.

## Embedding and feature controls

Current manuscript-grade work uses:

- `byte_pair_2d`
- `sliding_window_8d`
- H0 and H1 persistent-homology summaries
- manuscript-grade persistent-homology backends such as `ripser` or GUDHI

Fallback or development TDA backends are diagnostic only and must not support manuscript claims.

## Evidence-registration rule

A claim is eligible for manuscript or public-facing use only when it traces to at least one registered table, figure, validation log, or external-test status report in `docs/evidence_register.md`.

If the evidence register reports missing artifacts, failed coherence, unavailable external testing, or no detected TDA backend, the project may describe the workflow and design but must not describe the run as a completed manuscript-grade evidence package.

## External randomness rule

External randomness testing is tracked separately from internal TDA evidence. If Dieharder or other external randomness-test infrastructure is unavailable, the project should report that status explicitly rather than treating missing rows as completed external evidence.

A stronger submission package should include populated external randomness rows from Dieharder, NIST SP 800-22, or another documented external test battery.
