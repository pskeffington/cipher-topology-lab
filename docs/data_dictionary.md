# Data Dictionary

## Stream manifest

| Field | Meaning |
|---|---|
| `stream_id` | unique stream identifier |
| `condition` | experimental condition |
| `replicate` | replicate number |
| `master_seed` | top-level seed |
| `algorithm` | AES, Ascon, OS CSPRNG, LCG, xorshift, or DES/TDEA legacy |
| `mode` | cipher mode or generator mode |
| `bytes` | stream length |
| `path` | local stream path |
| `sha256` | stream file digest |

## Embedding manifest

| Field | Meaning |
|---|---|
| `embedding_id` | unique embedding identifier |
| `stream_id` | source stream |
| `condition` | experimental condition |
| `embedding_name` | embedding transform |
| `dimension` | embedding dimension |
| `stride` | byte stride |
| `sample_points` | number of points retained |
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

## TDA distance-to-baseline table

| Field | Meaning |
|---|---|
| `stream_id` | source stream identifier for stream-level distance row |
| `condition` | experimental condition |
| `baseline_condition` | reference condition used to compute centroid, usually `os_csprng` |
| `backend` | TDA backend |
| `embedding_name` | embedding transform |
| `homology_dim` | homology dimension |
| `euclidean_feature_distance` | Euclidean distance between the stream feature vector and the baseline-condition centroid within the same backend, embedding, and homology dimension |

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

## External export manifest

| Field | Meaning |
|---|---|
| `stream_id` | exported source stream identifier |
| `condition` | experimental condition |
| `bytes` | exported byte count |
| `export_path` | path to exported binary file |
| `sha256` | SHA-256 digest of exported binary file |
