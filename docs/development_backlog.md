# Platform Development Backlog

## Priority order

This backlog converts `cipher-topology-lab` from a high-value research asset into a continuing platform. Tasks are ordered to preserve scientific claim control while improving demo, review, and productization readiness.

## P0 — Claim safety and platform control

### P0.1 Add platform report generator

Goal: create a compact report that can be read by a reviewer, sponsor, or portfolio system.

Expected output:

- `results/platform/platform_report.md`
- `results/platform/platform_object.json`

Report should include:

- repo purpose;
- current supported claim;
- evidence state;
- run configuration;
- generated artifacts;
- unavailable external dependencies;
- claim boundaries;
- next recommended run.

Acceptance criteria:

- Runs without changing the empirical pipeline.
- Does not claim cryptanalysis.
- Reads current evidence registers where available.
- Produces a stable JSON object for portfolio ingestion.

### P0.2 Add platform preflight check

Goal: detect whether the environment can support demo, full run, manuscript build, and external randomness testing.

Expected output:

- `results/logs/platform_preflight.md`

Checks:

- Python version;
- package import readiness;
- `ripser` availability;
- LaTeX availability;
- Dieharder availability;
- expected config files;
- expected evidence-register files.

Acceptance criteria:

- Missing optional dependencies are recorded as unavailable, not confused with failed analysis.
- Missing required dependencies return nonzero status.

### P0.3 Add claim-boundary validator

Goal: prevent platform reports and public docs from drifting into prohibited claims.

Flagged phrases:

- breaks AES;
- AES vulnerability;
- proves randomness;
- security certification;
- cryptanalysis result;
- Ascon result;
- DES result;
- TDEA result.

Acceptance criteria:

- Validator checks README, portfolio status, platform report, and manuscript discussion text.
- Validator allows explicit negative/avoidance language.

## P1 — Demo hardening

### P1.1 Add deterministic platform demo command

Goal: one command that runs a small deterministic workflow and generates a human-readable report.

Command target:

```bash
make platform-demo
```

Expected behavior:

- uses an existing smoke config or a new platform-demo config;
- runs generation, embedding, features, diagnostics, coherence, consistency, effects, and evidence if feasible;
- writes a compact report to `results/platform/platform_demo_report.md`.

Acceptance criteria:

- completes quickly on a clean dev machine after setup;
- preserves deterministic reproducibility;
- produces artifact inventory and claim boundary;
- does not require Dieharder.

### P1.2 Add buyer/sponsor walkthrough

Goal: explain the platform in non-specialist terms without overstating claims.

Output:

- `docs/platform_walkthrough.md`

Sections:

- What the platform does;
- What it does not do;
- Who would use it;
- What evidence exists today;
- What remains before a paid pilot or sponsored research package.

Acceptance criteria:

- suitable for portfolio review;
- suitable for foundation productization review;
- no unsupported security claims.

## P2 — Evidence expansion execution

### P2.1 Seed sweep 20260701

Command:

```bash
./scripts/run_segmented.sh full --strict --python .venv/bin/python --config configs/experiment_weak_controls_seed_sweep_20260701_64rep.json
```

Expected output:

- `docs/evidence_register_seed_sweep_20260701.md`

Acceptance criteria:

- weak controls remain top or near-top separators;
- AES-CTR, OS CSPRNG, and xorshift32 do not show comparable broad top-ranked separation;
- backend remains `ripser` without fallback.

### P2.2 Seed sweep 20260702

Expected output:

- `docs/evidence_register_seed_sweep_20260702.md`

Acceptance criteria:

- same as P2.1.

### P2.3 128-replicate scale check

Expected output:

- `docs/evidence_register_weak_controls_128rep.md`

Acceptance criteria:

- main weak-control pattern persists;
- ranking remains interpretable;
- backend remains manuscript-grade.

### P2.4 Embedding sample-size sensitivity

Expected output:

- `docs/evidence_register_embedding_sensitivity.md`

Acceptance criteria:

- periodic and biased controls remain separated;
- results do not degrade into indiscriminate separation;
- backend remains manuscript-grade.

## P3 — Productization and valuation integration

### P3.1 Export platform object for CV valuation

Goal: provide a stable object for the CV valuation tool.

Output:

- `results/platform/platform_object.json`

Required fields:

- `repo_full_name`;
- `platform_name`;
- `current_claim`;
- `market_segment`;
- `evidence_level`;
- `demo_status`;
- `claim_boundaries`;
- `packaging_gaps`;
- `next_milestone`.

### P3.2 Add productization status table

Goal: make development and market-readiness visible.

Output:

- `docs/productization_status.md`

Fields:

- feature;
- readiness;
- evidence;
- buyer value;
- gap;
- next action.

### P3.3 Add pilot package outline

Goal: define a paid/sponsored pilot without making unsupported security claims.

Output:

- `docs/pilot_package_outline.md`

Pilot shape:

- diagnostic workflow review;
- generated-data control analysis;
- reproducibility/evidence-register setup;
- claim-boundary audit;
- final report.

## P4 — External testing decision

### P4.1 Docker Dieharder path

Goal: support external randomness testing on systems without native Dieharder.

Potential outputs:

- `docker/dieharder/Dockerfile`
- `scripts/run_dieharder_docker.sh`
- `docs/external_randomness_docker.md`

Acceptance criteria:

- output files parse through existing parser;
- evidence register records completed external rows;
- manuscript language distinguishes internal TDA evidence from external randomness tests.

### P4.2 External comparison deferral note

Goal: preserve external comparison as future work if completion is out of scope.

Output:

- update manuscript discussion and portfolio status.

Acceptance criteria:

- no ambiguity between unavailable external infrastructure and completed external testing.

## Current recommended sprint

1. Add `scripts/13_build_platform_report.py`.
2. Add `make platform-report`.
3. Add `docs/platform_walkthrough.md`.
4. Add `docs/productization_status.md`.
5. Update README with the new platform continuation links.
