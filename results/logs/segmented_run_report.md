# Segmented Run Report

Generated: `2026-05-26T01:50:00+00:00`
Status: `final`
Config: `configs/smoke_test.json`
Baseline condition: `sha256_seeded_baseline`
Continue on failure: `True`

## Stage results

| Stage | Status | Return code | Command | Message |
| --- | --- | --- | --- | --- |
| clean | PASS | 0 | clean generated directories |  |
| generate | PASS | 0 | /Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/00_generate_streams.py --config configs/smoke_test.json |  |
| embed | PASS | 0 | /Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/01_embed_ciphertext.py --config configs/smoke_test.json |  |
| features | PASS | 0 | /Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/02_compute_tda_features.py --config configs/smoke_test.json |  |
| randomness | PASS | 0 | /Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/03_randomness_tests.py --config configs/smoke_test.json |  |
| analysis | PASS | 0 | /Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/04_analyze_results.py --config configs/smoke_test.json |  |
| export | PASS | 0 | /Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/05_export_randomness_inputs.py --manifest data/raw/stream_manifest.csv |  |
| external-parse | SKIP | 0 |  | Skipped; pass --parse-external to enable. |
| coherence | PASS | 0 | /Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/08_validate_artifact_coherence.py --config configs/smoke_test.json |  |
| consistency | PASS | 0 | /Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/09_validate_artifact_consistency.py --config configs/smoke_test.json |  |
| effects | PASS | 0 | /Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/10_effect_size_tables.py --config configs/smoke_test.json |  |
| evidence | PASS | 0 | /Users/null/Documents/GitHub/cipher-topology-lab/.venv/bin/python scripts/09_build_evidence_register.py --config configs/smoke_test.json --output docs/evidence_register.md |  |
| manuscript | SKIP | 0 |  | Skipped; pass --build-manuscript to enable. |

## Artifact availability

| Artifact | Status | Size or count |
| --- | --- | --- |
| data/raw/stream_manifest.csv | present | 2914 |
| data/interim/embedding_manifest.csv | present | 4361 |
| data/processed/tda_features.csv | present | 9141 |
| data/processed/randomness_tests_internal.csv | present | 1691 |
| data/processed/external_randomness_tests.csv | missing | 0 |
| results/tables/tda_backend_summary.csv | present | 156 |
| results/tables/tda_feature_summary.csv | present | 2621 |
| results/tables/tda_persistence_entropy_effects.csv | present | 3554 |
| results/tables/tda_distance_effects.csv | present | 3779 |
| results/tables/tda_effects_combined.csv | present | 7179 |
| docs/evidence_register.md | present | 2987 |
| results/figures | present | 9 files |
| results/logs | present | 3 files |
| external_tests/inputs | present | 15 files |

## Notes

This report is written after every stage, so a failed segmented run should still leave partial diagnostics and artifact availability information for debugging.
