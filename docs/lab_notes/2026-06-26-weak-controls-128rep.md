# Weak-Control 128-Replicate Interpretation

## Run status

The `128rep` weak-control scale check supports the planned replicate-scale pass criterion. The effect table uses 128 non-baseline samples and 128 baseline samples per comparison row, and the strongest absolute Cliff's delta rows are again dominated by deliberately structured weak controls.

## Effect-size interpretation

The dominant pattern remains stable at 128 replicates:

- `biased_byte_weak` reaches maximum separation in sliding-window H1 distance-to-baseline, sliding-window H0 distance-to-baseline, byte-pair H1 distance-to-baseline, byte-pair H0 distance-to-baseline, sliding-window H1 persistence entropy, sliding-window H0 persistence entropy, byte-pair H1 persistence entropy, and byte-pair H0 persistence entropy.
- `periodic_byte_weak` reaches maximum or near-maximum separation in byte-pair H1 persistence entropy, byte-pair H1 distance-to-baseline, byte-pair H0 distance-to-baseline, sliding-window H0 distance-to-baseline, byte-pair H0 persistence entropy, sliding-window H1 distance-to-baseline, sliding-window H0 persistence entropy, and sliding-window H1 persistence entropy.
- `lcg_weak` remains a strong positive-control signal, especially under byte-pair H0 distance-to-baseline and byte-pair H0 persistence entropy.

AES-CTR, OS CSPRNG, and xorshift32 appear only in smaller effect rows in the reviewed top-50 table. They do not show the repeated, broad, top-ranked separation pattern shown by deliberately biased and periodic controls.

## Supported incremental claim

The 128-replicate run strengthens replicate-scale footing for the internal TDA diagnostic thesis. The registered workflow continues to distinguish deliberately structured weak controls from the SHA-256 seeded baseline when the replicate count is doubled from 64 to 128.

The claim remains bounded: this is diagnostic and reproducibility evidence, not cryptanalysis, a cipher-vulnerability finding, or security certification.

## Required next actions

1. Confirm `docs/evidence_register_weak_controls_128rep.md` is built and committed.
2. Archive the 128rep effect and distance tables if needed before running another config.
3. Update manuscript and portfolio evidence maps after the evidence register is present.
4. Proceed to the embedding sample-size sensitivity run only after the 128rep register is committed.
