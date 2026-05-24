from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from ciphertopology.utils import ensure_dirs, read_json


ARTIFACT_PATHS = [
    Path("data/raw/stream_manifest.csv"),
    Path("data/interim/embedding_manifest.csv"),
    Path("data/processed/tda_features.csv"),
    Path("data/processed/randomness_tests_internal.csv"),
    Path("data/processed/external_randomness_tests.csv"),
    Path("results/tables/tda_backend_summary.csv"),
    Path("results/tables/tda_feature_summary.csv"),
]


def csv_row_count(path: Path) -> int | None:
    if not path.exists():
        return None
    return len(pd.read_csv(path))


def csv_columns(path: Path) -> list[str]:
    if not path.exists():
        return []
    return list(pd.read_csv(path, nrows=0).columns)


def validation_status(config_path: str) -> tuple[str, str]:
    command = [
        sys.executable,
        "scripts/08_validate_artifact_coherence.py",
        "--config",
        config_path,
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    output = (completed.stdout + completed.stderr).strip()
    if completed.returncode == 0:
        return "PASS", output
    return "FAIL", output


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return "\n".join(lines)


def sorted_paths(pattern: str) -> list[Path]:
    return sorted(Path().glob(pattern), key=lambda item: str(item))


def build_register(config_path: str, output_path: Path) -> str:
    config = read_json(config_path)
    baseline_condition = config.get("baseline_condition", "")
    distance_path = Path(f"results/tables/tda_distance_to_{baseline_condition}.csv")
    artifact_paths = ARTIFACT_PATHS + [distance_path]

    validation_result, validation_output = validation_status(config_path)
    generated_at = datetime.now(UTC).isoformat(timespec="seconds")

    artifact_rows: list[list[object]] = []
    for path in artifact_paths:
        row_count = csv_row_count(path)
        artifact_rows.append(
            [
                f"`{path}`",
                "present" if path.exists() else "missing",
                "NA" if row_count is None else row_count,
            ]
        )

    figure_rows = []
    for path in sorted_paths("results/figures/*"):
        if path.is_file():
            figure_rows.append([f"`{path}`"])

    log_rows = []
    for path in sorted_paths("results/logs/*"):
        if path.is_file():
            log_rows.append([f"`{path}`"])

    tda_features_path = Path("data/processed/tda_features.csv")
    backends: list[str] = []
    fallback_detected = "unknown"
    if tda_features_path.exists():
        features = pd.read_csv(tda_features_path)
        if "backend" in features.columns:
            backends = sorted(features["backend"].dropna().astype(str).unique().tolist())
            fallback_detected = str(
                features["backend"].astype(str).str.contains("fallback", case=False).any()
            )

    external_path = Path("data/processed/external_randomness_tests.csv")
    external_rows = csv_row_count(external_path)
    external_populated = external_rows is not None and external_rows > 0

    content = f"""# Evidence Register

Generated: `{generated_at}`

## Configuration

- Config: `{config_path}`
- Project version: `{config.get('version', 'unknown')}`
- Baseline condition: `{baseline_condition}`
- Conditions: `{', '.join(config.get('conditions', []))}`
- Replicates: `{config.get('replicates', 'unknown')}`
- Embeddings: `{', '.join(item.get('name', '') for item in config.get('embeddings', []))}`
- TDA max dimension: `{config.get('tda', {}).get('max_dimension', 'unknown')}`

## Validation

- Command: `{sys.executable} scripts/08_validate_artifact_coherence.py --config {config_path}`
- Status: `{validation_result}`

```text
{validation_output}
```

## Registered artifacts

{markdown_table(['Path', 'Status', 'Rows'], artifact_rows)}

## Backend status

- Observed TDA backends: `{', '.join(backends) if backends else 'none detected'}`
- Fallback backend detected: `{fallback_detected}`
- Manuscript-grade rule: use only true persistent-homology backend outputs for evidentiary claims. Fallback outputs are diagnostic only.

## External randomness status

- External randomness table: `{external_path}`
- Rows: `{external_rows if external_rows is not None else 'missing'}`
- Populated: `{external_populated}`

## Registered figures

{markdown_table(['Figure path'], figure_rows) if figure_rows else 'No figures detected.'}

## Registered logs

{markdown_table(['Log path'], log_rows) if log_rows else 'No logs detected.'}

## Claim-control rule

Every result claim in `manuscript/main.tex` or `manuscript/sections/` must trace to one registered table, figure, or validation log in this file.
"""

    ensure_dirs(output_path.parent)
    output_path.write_text(content, encoding="utf-8")
    return content


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/experiment_v0.json")
    parser.add_argument("--output", default="docs/evidence_register.md")
    args = parser.parse_args()

    content = build_register(args.config, Path(args.output))
    print(f"Wrote {args.output}")
    print(content)


if __name__ == "__main__":
    main()
