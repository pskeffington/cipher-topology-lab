# External Randomness Test Status

Generated: `2026-05-26T03:01:50+00:00`
Status: `UNAVAILABLE`
Message: `Dieharder executable not found on PATH: dieharder`

## Configuration

- Manifest: `data/raw/stream_manifest.csv`
- Input directory: `external_tests/inputs`
- Result directory: `external_tests/results/dieharder`
- Parsed output: `data/processed/external_randomness_tests.csv`
- Dieharder executable: `dieharder`
- Dieharder test id: `0`

## Selected targets

| Condition | Replicate | Path | Exists | Bytes |
| --- | --- | --- | --- | --- |
| aes128_ctr_xor_deterministic_plaintext | 0 | `external_tests/inputs/aes128_ctr_xor_deterministic_plaintext_r000.bin` | True | 8388608 |
| aes128_ctr_keystream_zero_plaintext | 0 | `external_tests/inputs/aes128_ctr_keystream_zero_plaintext_r000.bin` | True | 8388608 |
| sha256_seeded_baseline | 0 | `external_tests/inputs/sha256_seeded_baseline_r000.bin` | True | 8388608 |
| os_csprng | 0 | `external_tests/inputs/os_csprng_r000.bin` | True | 8388608 |
| lcg_weak | 0 | `external_tests/inputs/lcg_weak_r000.bin` | True | 8388608 |
| xorshift32_weak | 0 | `external_tests/inputs/xorshift32_weak_r000.bin` | True | 8388608 |

## Test results

No external tests were run.

## Notes

This file is intentionally written even when Dieharder is unavailable or a test fails, so the evidence register can distinguish missing external infrastructure from absent analysis.
