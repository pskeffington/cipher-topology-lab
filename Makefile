.PHONY: setup data embed features analysis manuscript clean test

setup:
	python -m pip install -e ".[dev,tda]"

data:
	python scripts/00_generate_streams.py --config configs/experiment_v0.json

embed:
	python scripts/01_embed_ciphertext.py --config configs/experiment_v0.json

features:
	python scripts/02_compute_tda_features.py --config configs/experiment_v0.json

analysis:
	python scripts/03_randomness_tests.py --config configs/experiment_v0.json
	python scripts/04_analyze_results.py --config configs/experiment_v0.json

manuscript:
	cd manuscript && latexmk -pdf main.tex

test:
	pytest -q

clean:
	rm -rf data/interim/* data/processed/* results/figures/* results/tables/* results/logs/*
	cd manuscript && latexmk -C || true
