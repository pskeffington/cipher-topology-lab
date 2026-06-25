# Lab Note — 2026-06-25 Seed-Robustness Pass and Thesis Status

## Status

The weak-control seed-robustness experiment completed at smoke and 64-replicate scale.

The 64-replicate run used an alternate deterministic master seed and passed internal evidence gates:

- Config: `configs/experiment_weak_controls_seed_robustness_64rep.json`
- Project version: `0.4.1-pre.0-weak-controls-seed-robustness-64rep`
- Baseline condition: `sha256_seeded_baseline`
- Conditions: 8
- Replicates: 64
- Embeddings: `byte_pair_2d`, `sliding_window_8d`
- Homology dimensions: H0/H1
- Backend: `ripser`
- Fallback backend detected: `False`

Registered artifact scale:

- Streams: 512
- Embeddings: 1024
- TDA feature rows: 2048
- Internal randomness rows: 512
- External randomness rows: 0
- Backend summary rows: 4
- Feature summary rows: 32
- Distance-to-baseline rows: 2048

External randomness testing was recorded as `UNAVAILABLE` because Dieharder was not installed. No completed external randomness comparison is claimed.

## Interpretation

The alternate-seed run reproduces the main weak-control sensitivity pattern observed in the original weak-control experiment.

Deliberately structured controls, especially `biased_byte_weak` and `periodic_byte_weak`, remain the strongest separators from the SHA-256 seeded baseline under the registered internal TDA summaries. The LCG condition remains a meaningful positive-control signal. AES-CTR, OS CSPRNG, and xorshift32 do not show comparable top-ranked separation in the reviewed effect-size table.

## Supported thesis claim

A conservative thesis-ready claim is now supported:

> Under registered byte-pair and sliding-window embeddings, persistent-homology summaries reproducibly distinguish deliberately structured weak-control byte streams from a SHA-256 seeded deterministic baseline across two deterministic master seeds. In the same internal analyses, AES-CTR, OS CSPRNG, and xorshift32 conditions do not show comparable top-ranked separation. These results support TDA as an auxiliary diagnostic for control-condition structure, not as a cryptanalytic attack or security certification.

## Claim boundary

Supported:

- Registered internal TDA workflow execution at 64 replicates.
- Reproduction of the weak-control sensitivity pattern under an alternate deterministic seed.
- Deliberately periodic and biased weak controls separating from the SHA-256 seeded baseline.
- Evidence-register traceability for artifact counts, backend status, validation status, and external-test availability.

Not supported:

- Cipher break.
- AES vulnerability.
- Practical cryptanalytic attack.
- Security certification.
- Completed Dieharder comparison on the local run.
- Ascon, DES, or TDEA empirical results.

## Thesis readiness assessment

The project is now past the minimum threshold for a defensible methods/results thesis centered on reproducible diagnostics.

Ready thesis components:

- Research question and contribution boundary.
- Deterministic data-generation protocol.
- Six-condition registered 64-replicate evidence run.
- Eight-condition weak-control sensitivity extension.
- Alternate-seed robustness check.
- Evidence registers for traceability.
- Backend/fallback status checks.
- Internal randomness diagnostics.
- Explicit external randomness availability status.

Remaining thesis work:

1. Freeze the empirical scope.
2. Write the methods chapter around stream generation, embeddings, persistent homology, validation gates, and effect-size summaries.
3. Write the results chapter around the six-condition run, weak-control extension, and seed-robustness check.
4. Add a limitations section that clearly states no cipher break, no AES vulnerability claim, no security certification, and no completed local Dieharder comparison.
5. Decide whether to run external randomness testing in Docker/Linux or explicitly keep it as future work.
6. Produce final manuscript tables/figures from registered artifacts only.

## Recommended next step

Freeze the current empirical scope unless external randomness testing is added in a controlled environment. The next highest-value work is thesis writing and figure/table curation, not another internal TDA run.
