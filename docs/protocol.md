# Protocol v0.1.0-pre.0

## Objective

Evaluate whether persistent-homology summaries of ciphertext-derived point clouds provide an auxiliary diagnostic for distinguishing standard symmetric-cipher output from structured or weak control outputs.

## Primary research question

Can persistent-homology features distinguish structured or weakened ciphertext-generation conditions from standard AES and Ascon ciphertext outputs, and how do these topological diagnostics compare with conventional statistical randomness-test batteries?

## Initial conditions

| Condition | Description | Role |
|---|---|---|
| `aes128_ctr_random_plaintext` | AES-128 in CTR mode over random plaintext | modern cipher baseline |
| `aes128_ctr_zero_plaintext` | AES-128 in CTR mode over zero plaintext | controlled AES keystream condition |
| `os_csprng` | operating-system cryptographic RNG output | random baseline |
| `lcg_weak` | linear congruential generator output | weak positive control |
| `xorshift32_weak` | xorshift32 output | weak positive control |

Ascon should be added in `v0.2.0` using a pinned reference implementation or reproducible package. DES/TDEA should be added only as a deprecated legacy control.

## Data-generation principle

Every stream must be reproducible from condition name, replicate index, master seed, key, nonce, plaintext pattern, generator parameters, and software version.

## Embedding methods

The initial release uses byte-pair embedding and sliding-window embedding. Later extensions should add cubical encodings from ciphertext reshaped as grayscale arrays.

## TDA features

Initial features include H0/H1 interval counts, finite interval counts, finite lifetime mean, finite lifetime maximum, and persistence entropy.

## Interpretation rule

This project does not certify cipher security. It tests whether topological summaries add diagnostic information relative to conventional tests and known weak controls.
