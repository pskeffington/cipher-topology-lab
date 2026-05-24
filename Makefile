.PHONY: setup setup-smoke data embed features analysis export-randomness manuscript clean clean-generated test smoke

CONFIG ?= configs/experiment_v0.json
SMOKE_CONFIG ?= configs/smoke_test.json

setup:
	python -m pip install -e ".[dev,tda]"

setup-smoke:
	python -m pip install -e ".[dev]"

data:
	python scripts/00_generate_streams.py --config $(CONFIG)

embed:
	python scripts/01_embed_ciphertext.py --config $(CONFIG)

features:
	python scripts/02_compute_tda_features.py --config $(CONFIG)

analysis:
	python scripts/03_randomness_tests.py --config $(CONFIG)
	python scripts/04_analyze_results.py --config $(CONFIG)

export-randomness:
	python scripts/05_export_randomness_inputs.py --manifest data/raw/stream_manifest.csv

clean-generated:
	rm -rf data/raw/* data/interim/* data/processed/* results/figures/* results/tables/* results/logs/* external_tests/inputs/* external_tests/results/*

smoke: clean-generated
	python scripts/00_generate_streams.py --config $(SMOKE_CONFIG)
	python scripts/01_embed_ciphertext.py --config $(SMOKE_CONFIG)
	python scripts/02_compute_tda_features.py --config $(SMOKE_CONFIG)
	python scripts/03_randomness_tests.py --config $(SMOKE_CONFIG)
	python scripts/04_analyze_results.py --config $(SMOKE_CONFIG)
	python scripts/05_export_randomness_inputs.py --manifest data/raw/stream_manifest.csv
	python scripts/08_validate_artifact_coherence.py --config $(SMOKE_CONFIG)

manuscript:
	cd manuscript && latexmk -pdf main.tex

test:
	pytest -q

clean: clean-generated
	cd manuscript && latexmk -C || true
