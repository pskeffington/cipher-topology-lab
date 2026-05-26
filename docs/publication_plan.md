# Publication Plan

## Working title

Topological Diagnostics of Symmetric-Cipher Output Randomness

## Contribution type

This is a reproducible computational-diagnostics paper. It does not propose a new cipher, new attack, proof of security, or practical cryptanalytic break.

## Defensible contribution

The defensible contribution is a transparent pipeline for comparing persistent-homology summaries against conventional randomness diagnostics under controlled deterministic cipher-output conditions, a deterministic SHA-256 reproducibility baseline, an OS CSPRNG sensitivity baseline, and weak-generator positive controls.

## Minimum publishable package

- Reproducible stream generation with manifests and SHA-256 digests
- AES-128 CTR deterministic-output conditions
- SHA-256 seeded deterministic reproducibility baseline
- OS CSPRNG non-deterministic sensitivity condition
- Weak generator controls using LCG and xorshift32
- At least two embedding methods, currently `byte_pair_2d` and `sliding_window_8d`
- Optional cubical-image experiments when enabled by config
- Persistent-homology features for H0 and H1 using manuscript-grade backends
- Internal randomness diagnostics and external randomness-test comparison where available
- Artifact coherence validation and evidence-register generation
- Replication instructions and cautious manuscript framing

## Evidence control

Every manuscript claim should trace to a registered table, figure, or validation log. Fallback or development TDA backends are diagnostic only and should not support publication claims.

## Extension path

Ascon should be added as the next lightweight-cryptography comparator after the v0.4.1 execution-repair baseline is stable. DES/TDEA may be added later as deprecated legacy comparators only.

## Venue fit

Likely targets include applied cryptography workshops, cybersecurity engineering venues, computational topology workshops, reproducibility tracks, and preprint release through IACR Cryptology ePrint or arXiv.
