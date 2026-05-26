# Data Dictionary

## Stream manifest

| Field | Meaning |
|---|---|
| `stream_id` | unique stream identifier |
| `condition` | experimental condition |
| `replicate` | replicate number |
| `master_seed` | top-level seed |
| `algorithm` | AES, SHA-256 expansion, OS CSPRNG, LCG, xorshift, Ascon extension, or DES/TDEA legacy comparator |
| `mode` | cipher mode, expansion mode, or generator mode |
| `bytes` | stream length |
| `path` | stream path within the generated artifact tree |
| `sha256` | stream file digest |

## Active configured conditions

| Condition | Meaning |
|---|---|
| `aes128_ctr_xor_deterministic_plaintext` | AES-128 CTR output under deterministic plaintext generation |
| `aes128_ctr_keystream_zero_plaintext` | AES-128 CTR keystream condition generated from zero plaintext |
| `sha256_seeded_baseline` | deterministic SHA-256 expansion baseline used for reproducible baseline-distance calculations |
| `os_csprng` | operating-system cryptographic RNG output used as a non-deterministic sensitivity condition |
| `lcg_weak` | linear congruential generator weak-control output |
| `xorshift32_weak` | xorshift32 weak-control output |

## Manuscript evidence scale

The current manuscript evidence configuration is `configs/experiment_64rep.json`. It uses 64 replicates across six conditions, producing 384 streams. With two embeddings and H0/H1 summaries, the current evidence run produces 768 embeddings and 1,536 TDA feature rows.

## Embedding manifest

| Field | Meaning |
|---|---|
| `embedding_id` | unique embedding identifier |
| `stream_id` | source stream |
| `condition` | experimental condition |
| `embedding_name` | embedding transform, such as `byte_pair_2d`, `sliding_window_8d`, or explicitly configured `cubical_image_2d` |
| `dimension` | embedding dimension or cubical image side parameter, depending on embedding type |
| `stride` | byte stride where applicable |
| `sample_points` | number of points retained for point-cloud embeddings |
| `path` | local `.npy` path |

## TDA feature table

| Field | Meaning |
|---|---|
| `backend` | TDA backend used, such as `ripser`, `gudhi_cubical`, or development fallback |
| `embedding_id` | source embedding identifier |
| `stream_id` | source stream identifier |
| `condition` | experimental condition |
| `embedding_name` | embedding transform |
| `homology_dim` | homology dimension |
| `interval_count` | number of persistence intervals |
| `finite_count` | number of finite intervals |
| `lifetime_mean` | mean finite lifetime |
| `lifetime_sd` | standard deviation of finite lifetimes |
| `lifetime_max` | maximum finite lifetime |
| `persistence_entropy` | entropy of positive finite lifetimes |

## TDA backend summary table

| Field | Meaning |
|---|---|
| `backend` | TDA backend represented in the feature table |
| `embedding_name` | embedding transform |
| `homology_dim` | homology dimension |
| `row_count` | number of feature rows represented by the backend, embedding, and homology-dimension stratum |

## TDA feature summary table

| Field | Meaning |
|---|---|
| `condition` | experimental condition |
| `backend` | TDA backend |
| `embedding_name` | embedding transform |
| `homology_dim` | homology dimension |
| feature summary statistics | condition-level summaries of interval, lifetime, entropy, or related feature columns |

## TDA distance-to-baseline table

| Field | Meaning |
|---|---|
| `stream_id` | source stream identifier for stream-level distance row |
| `condition` | experimental condition |
| `baseline_condition` | reference condition used to compute centroid; `v0.4.1-pre.0` uses `sha256_seeded_baseline` |
| `backend` | TDA backend |
| `embedding_name` | embedding transform |
| `homology_dim` | homology dimension |
| `euclidean_feature_distance` | Euclidean distance between the stream feature vector and the baseline-condition centroid within the same backend, embedding, and homology dimension |

## Effect-size tables

| Field | Meaning |
|---|---|
| `table` | effect family, such as `persistence_entropy` or `distance_to_sha256_seeded_baseline` |
| `backend` | TDA backend |
| `embedding_name` | embedding transform |
| `homology_dim` | homology dimension |
| `condition` | comparison condition |
| `baseline_condition` | configured baseline condition |
| `n` | number of comparison rows |
| `baseline_n` | number of baseline rows |
| `median` | comparison-condition median |
| `baseline_median` | baseline-condition median |
| `mean` | comparison-condition mean |
| `baseline_mean` | baseline-condition mean |
| `cliffs_delta` | Cliff's delta effect size comparing condition against baseline |
| `mann_whitney_p` | two-sided Mann--Whitney p value |

## Internal randomness-test table

| Field | Meaning |
|---|---|
| `stream_id` | source stream identifier |
| `condition` | experimental condition |
| randomness-test columns | internal statistical diagnostics computed by `scripts/03_randomness_tests.py` |

## External randomness-test table

| Field | Meaning |
|---|---|
| `source_file` | source result file parsed from an external test suite |
| `suite` | external test suite, currently `dieharder` for parsed rows |
| `test_name` | external randomness-test name |
| `ntup` | Dieharder tuple parameter where reported |
| `tsamples` | test sample count where reported |
| `psamples` | p-value sample count where reported |
| `p_value` | reported p-value |
| `assessment` | external suite assessment label |

The external randomness-test table may be schema-only when external testing is unavailable. In that case, consult `results/logs/external_randomness_status.md` and the evidence register before making any claim about external randomness testing.

## External randomness status report

| Field or section | Meaning |
|---|---|
| `Status` | external runner status, such as `PASS`, `FAIL`, or `UNAVAILABLE` |
| `Message` | human-readable reason for the status |
| `Configuration` | manifest, input directory, result directory, parsed output path, executable, and test id |
| `Selected targets` | replicate-zero exported input files selected for the external-test subset |
| `Test results` | per-target command output status when tests are run |

## External export manifest

| Field | Meaning |
|---|---|
| `stream_id` | exported source stream identifier |
| `condition` | experimental condition |
| `bytes` | exported byte count |
| `export_path` | path to exported binary file |
| `sha256` | SHA-256 digest of exported binary file |
