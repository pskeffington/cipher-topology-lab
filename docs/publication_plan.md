# Publication Plan

## Working title

Topological Diagnostics of Symmetric-Cipher Output Randomness

## Contribution type

This is a reproducible computational-diagnostics paper. It does not propose a new cipher, new attack, proof of security, or practical cryptanalytic break.

## Defensible contribution

The defensible contribution is a transparent pipeline for comparing persistent-homology summaries against conventional randomness diagnostics under controlled deterministic cipher-output conditions, a deterministic SHA-256 reproducibility baseline, an OS CSPRNG sensitivity condition, and weak-generator positive controls.

## Current manuscript evidence package

The current manuscript evidence package uses `configs/experiment_64rep.json` with 64 replicates. It produces 384 streams, 768 embeddings, 1,536 TDA feature rows, 384 internal randomness-diagnostic rows, and 1,536 distance-to-baseline rows. Artifact coherence and artifact consistency pass, the observed TDA backend is `ripser`, and no fallback backend is detected.

The central internal result is LCG weak-control separation from the SHA-256 seeded baseline under byte-pair H0 summaries. AES-CTR deterministic-output conditions, OS CSPRNG output, and xorshift32 do not show comparable separation under the current embeddings and feature set.

## Minimum publishable package

- Reproducible stream generation with manifests and SHA-256 digests
- AES-128 CTR deterministic-output conditions
- SHA-256 seeded deterministic reproducibility baseline
- OS CSPRNG non-deterministic sensitivity condition
- Weak generator controls using LCG and xorshift32
- At least two embedding methods, currently `byte_pair_2d` and `sliding_window_8d`
- Optional cubical-image experiments when enabled by config
- Persistent-homology features for H0 and H1 using manuscript-grade backends
- Internal randomness diagnostics
- External randomness-test support and explicit external-test availability status
- Artifact coherence validation, artifact consistency validation, and evidence-register generation
- Replication instructions and cautious manuscript framing

## Evidence control

Every manuscript claim should trace to a registered table, figure, validation log, or external-test status report. Fallback or development TDA backends are diagnostic only and should not support publication claims. External randomness rows must not be described as populated unless `data/processed/external_randomness_tests.csv` contains parsed rows and the evidence register reports the external runner as populated.

## External randomness-testing status

Dieharder is not assumed to be available on every local development machine. The repository therefore includes a failure-safe external-randomness runner that records an explicit status report when Dieharder is unavailable. This is an honest evidence state, not a completed external-test comparison. A stronger submission package should include completed external Dieharder or NIST SP 800-22 results.

## Extension path

Ascon should be added as the next lightweight-cryptography comparator after the v0.4.1 execution-repair baseline is stable. DES/TDEA may be added later as deprecated legacy comparators only. Additional embedding experiments should include explicitly configured cubical-complex runs and additional weak-generator controls.

## Venue fit

Likely targets include applied cryptography workshops, cybersecurity engineering venues, computational topology workshops, reproducibility tracks, and preprint release through IACR Cryptology ePrint or arXiv. The strongest near-term framing is a reproducible diagnostic pipeline paper with a stable positive-control result and transparent limits around external randomness testing.
