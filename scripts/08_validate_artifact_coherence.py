from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from ciphertopology.utils import read_json


ARTIFACTS = [
    Path("data/raw/stream_manifest.csv"),
    Path("data/interim/embedding_manifest.csv"),
    Path("data/processed/tda_features.csv"),
    Path("data/processed/randomness_tests_internal.csv"),
    Path("results/tables/tda_feature_summary.csv"),
    Path("results/tables/tda_backend_summary.csv"),
]


def read_conditions(path: Path) -> set[str]:
    if not path.exists():
        raise SystemExit(f"Missing required artifact: {path}")
    frame = pd.read_csv(path)
    if "condition" not in frame.columns:
        return set()
    return set(frame["condition"].dropna().astype(str))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_json(args.config)
    expected_conditions = set(config["conditions"])
    baseline_condition = config.get("baseline_condition")
    if baseline_condition and baseline_condition not in expected_conditions:
        raise SystemExit(
            f"Configured baseline_condition is not present in conditions: {baseline_condition}"
        )

    mismatches: list[str] = []
    for artifact in ARTIFACTS:
        observed = read_conditions(artifact)
        if observed and observed != expected_conditions:
            mismatches.append(
                f"{artifact}: observed={sorted(observed)} expected={sorted(expected_conditions)}"
            )

    if baseline_condition:
        distance_path = Path(f"results/tables/tda_distance_to_{baseline_condition}.csv")
        observed = read_conditions(distance_path)
        if observed and observed != expected_conditions:
            mismatches.append(
                f"{distance_path}: observed={sorted(observed)} expected={sorted(expected_conditions)}"
            )

    if mismatches:
        raise SystemExit("Artifact condition mismatch detected:\n" + "\n".join(mismatches))

    print(f"Validated artifact coherence for {len(expected_conditions)} conditions.")


if __name__ == "__main__":
    main()
