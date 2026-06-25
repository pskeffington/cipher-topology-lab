# Lab Note — 2026-06-25 Weak-Control Sensitivity Experiment

## Status

The weak-control sensitivity extension completed at 64 replicates and passed internal evidence gates.

## Configuration

- Config: `configs/experiment_weak_controls_64rep.json`
- Project version: `0.4.1-pre.0-weak-controls-64rep`
- Baseline condition: `sha256_seeded_baseline`
- Conditions: 8
- Replicates: 64
- Embeddings: `byte_pair_2d`, `sliding_window_8d`
- TDA max dimension: 1

## Registered artifact scale

- Streams: 512
- Embeddings: 1024
- TDA feature rows: 2048
- Internal randomness rows: 512
- Distance-to-baseline rows: 2048
- Backend: `ripser`
- Fallback backend detected: `False`

## External randomness status

External randomness testing is unavailable on the current machine because Dieharder is not installed.

No completed external randomness comparison is claimed.

## Effect-size interpretation

The added `biased_byte_weak` and `periodic_byte_weak` controls show strong separation from `sha256_seeded_baseline` across registered TDA distance and persistence-entropy summaries.

The original `lcg_weak` condition remains a strong positive-control signal.

The reviewed top-ranked effects do not support claims that AES-CTR, OS CSPRNG, or xorshift32 conditions show comparable separation.

## Claim boundary

Supported: the registered TDA workflow detects deliberately structured weak-control streams under the current embeddings and features.

Not supported: cipher break, AES vulnerability, security certification, completed Dieharder comparison, or claims about Ascon/DES/TDEA.
