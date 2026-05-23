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
| `homology_dim` | homology dimension |
| `interval_count` | number of persistence intervals |
| `finite_count` | number of finite intervals |
| `lifetime_mean` | mean finite lifetime |
| `lifetime_sd` | standard deviation of finite lifetimes |
| `lifetime_max` | maximum finite lifetime |
| `persistence_entropy` | entropy of positive finite lifetimes |
