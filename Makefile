.PHONY: setup setup-smoke data embed features analysis export-randomness external-randomness evidence-register rag-provenance rag-verify platform-report platform-artifact-check platform-demo claim-check platform-validate manuscript clean clean-generated test smoke micro micro-smoke micro-full micro-stage segmented-smoke segmented-full segmented-stage segmented-list

CONFIG ?= configs/experiment_v0.json
SMOKE_CONFIG ?= configs/smoke_test.json
PYTHON ?= .venv/bin/python
STAGE ?= all
ANSWER ?= examples/rag_answer_citation_example.json

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev,tda]"

setup-smoke:
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

data:
	$(PYTHON) scripts/00_generate_streams.py --config $(CONFIG)

embed:
	$(PYTHON) scripts/01_embed_ciphertext.py --config $(CONFIG)

features:
	$(PYTHON) scripts/02_compute_tda_features.py --config $(CONFIG)

analysis:
	$(PYTHON) scripts/03_randomness_tests.py --config $(CONFIG)
	$(PYTHON) scripts/04_analyze_results.py --config $(CONFIG)

export-randomness:
	$(PYTHON) scripts/05_export_randomness_inputs.py --manifest data/raw/stream_manifest.csv

external-randomness:
	$(PYTHON) scripts/12_run_external_randomness.py --allow-missing-dieharder

evidence-register:
	$(PYTHON) scripts/09_build_evidence_register.py --config $(CONFIG) --output docs/evidence_register.md

rag-provenance:
	$(PYTHON) scripts/13_rag_provenance_scan.py --root .

rag-verify:
	$(PYTHON) scripts/16_verify_rag_answer.py --answer $(ANSWER)

platform-report:
	$(PYTHON) scripts/13_build_platform_report.py

platform-artifact-check:
	$(PYTHON) scripts/15_validate_platform_artifacts.py

claim-check:
	$(PYTHON) scripts/14_validate_claim_boundaries.py

platform-validate: platform-report platform-artifact-check claim-check

platform-demo: segmented-smoke platform-report platform-artifact-check claim-check

micro:
	$(PYTHON) scripts/11_run_micro_workflow.py --config $(CONFIG)

micro-smoke:
	$(PYTHON) scripts/11_run_micro_workflow.py --config $(SMOKE_CONFIG) --allow-fallback

micro-full:
	$(PYTHON) scripts/11_run_micro_workflow.py --config $(CONFIG)

micro-stage:
	$(PYTHON) scripts/11_run_micro_workflow.py --config $(CONFIG) --stage $(STAGE)

segmented-smoke:
	PYTHON=$(PYTHON) bash scripts/run_segmented.sh smoke

segmented-full:
	PYTHON=$(PYTHON) bash scripts/run_segmented.sh full

segmented-stage:
	PYTHON=$(PYTHON) bash scripts/run_segmented.sh --config $(CONFIG) stage $(STAGE)

segmented-list:
	bash scripts/run_segmented.sh list

clean-generated:
	rm -rf data/raw/* data/interim/* data/processed/* results/figures/* results/tables/* results/logs/* results/platform/* results/provenance/* external_tests/inputs/* external_tests/results/*

smoke: clean-generated
	$(PYTHON) scripts/00_generate_streams.py --config $(SMOKE_CONFIG)
	$(PYTHON) scripts/01_embed_ciphertext.py --config $(SMOKE_CONFIG)
	$(PYTHON) scripts/02_compute_tda_features.py --config $(SMOKE_CONFIG)
	$(PYTHON) scripts/03_randomness_tests.py --config $(SMOKE_CONFIG)
	$(PYTHON) scripts/04_analyze_results.py --config $(SMOKE_CONFIG)
	$(PYTHON) scripts/05_export_randomness_inputs.py --manifest data/raw/stream_manifest.csv
	$(PYTHON) scripts/08_validate_artifact_coherence.py --config $(SMOKE_CONFIG)
	$(PYTHON) scripts/09_build_evidence_register.py --config $(SMOKE_CONFIG) --output docs/evidence_register.md

manuscript:
	cd manuscript && latexmk -pdf main.tex

test:
	$(PYTHON) -m pytest -q

clean: clean-generated
	cd manuscript && latexmk -C || true
