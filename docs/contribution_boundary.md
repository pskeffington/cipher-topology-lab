# Contribution Boundary

## Project identity

`cipher-topology-lab` is an evaluation-science and reproducible computational-diagnostics project. It studies whether topological data analysis, especially persistent homology, can provide auxiliary diagnostic summaries for cipher-output randomness experiments.

## What the project contributes

The defensible contribution is a transparent pipeline for:

1. Generating deterministic and controlled output streams.
2. Embedding bitstreams or byte streams into configured point-cloud or complex representations.
3. Computing persistent-homology features with manuscript-grade backends.
4. Comparing topological summaries against internal and external randomness diagnostics.
5. Registering artifacts, tables, figures, logs, and claim boundaries for reproducible review.

## What the project does not claim

This project does not claim to:

- break AES, Ascon, DES, TDEA, or any standardized cipher;
- certify cipher security;
- propose a new cryptanalytic attack;
- replace established statistical randomness-test batteries;
- prove that persistent homology is a universal randomness detector;
- treat DES or TDEA as modern security targets;
- treat missing external randomness rows as completed external evidence.

## Public-facing language

Preferred public-facing description:

> Reproducible computational-diagnostics project evaluating whether persistent-homology summaries can distinguish structured or weak generator controls from deterministic cryptographic baselines under controlled cipher-output experiments.

Avoid language such as:

- "breaking AES"
- "detecting insecure encryption"
- "proving cipher randomness"
- "cryptanalysis result"
- "security certification"

## Manuscript claim hierarchy

### Allowed design-level claims

These may be stated when supported by repository design and documentation:

- The repository implements a reproducible pipeline for stream generation, embedding, persistent-homology feature extraction, randomness diagnostics, and evidence registration.
- The experiment includes deterministic reproducibility baselines, modern cipher-output conditions, non-deterministic sensitivity conditions, and weak-generator positive controls.
- The project is framed as diagnostic and reproducibility work, not cryptanalysis.

### Allowed evidence-level claims

These require current registered artifacts:

- A condition separates from the baseline under a specific embedding, homology dimension, feature family, and replicate configuration.
- Artifact coherence or consistency passes.
- External randomness testing is populated.
- Manuscript figures or tables support a specific result.

### Not allowed unless explicitly implemented and registered

- Claims about Ascon, DES, or TDEA results before those conditions are implemented and registered.
- Claims that external randomness tests support or contradict TDA results when external rows are unavailable.
- Claims based on fallback or development TDA backends.

## Evidence reconciliation requirement

Before public manuscript claims are strengthened, reconcile the repository documentation with the current evidence register. If the README or publication plan describes completed 64-replicate evidence while `docs/evidence_register.md` reports missing artifacts or failed validation, the evidence register should be treated as the stricter source of truth until regenerated.

## Portfolio positioning

For portfolio purposes, describe the project as:

- applied cryptography adjacent;
- computational topology / TDA;
- reproducible evaluation science;
- evidence governance for technical claims;
- diagnostic pipeline development.

Do not position the project as operational cyber defense, offensive security, or a practical cipher-breaking system.
