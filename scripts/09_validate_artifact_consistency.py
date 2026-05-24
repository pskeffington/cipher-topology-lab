from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def require_file(path: str) -> Path:
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"Missing required artifact: {p}")
    return p


def compare_backend_summary(features: pd.DataFrame, backend_summary: pd.DataFrame) -> None:
    expected = (
        features.groupby(["backend", "embedding_name", "homology_dim"], as_index=False)
        .size()
        .rename(columns={"size": "row_count"})
        .sort_values(["backend", "embedding_name", "homology_dim"])
        .reset_index(drop=True)
    )
    observed = (
        backend_summary.sort_values(["backend", "embedding_name", "homology_dim"])
        .reset_index(drop=True)
    )
    if not expected.equals(observed):
        raise SystemExit(
            "Backend summary does not match TDA feature table. "
            "Artifacts are stale, mixed across runs, or generated from different inputs."
        )


def validate_no_fallback_for_manuscript(features: pd.DataFrame, allow_fallback: bool) -> None:
    if allow_fallback:
        return
    backends = set(features["backend"].dropna().astype(str))
    fallback = [backend for backend in backends if "fallback" in backend.lower()]
    if fallback:
        raise SystemExit(f"Fallback backend present in manuscript artifact set: {fallback}")


def validate_distance_backends(features: pd.DataFrame, distances: pd.DataFrame) -> None:
    feature_keys = set(
        tuple(row)
        for row in features[["backend", "embedding_name", "homology_dim"]]
        .drop_duplicates()
        .itertuples(index=False, name=None)
    )
    distance_keys = set(
        tuple(row)
        for row in distances[["backend", "embedding_name", "homology_dim"]]
        .drop_duplicates()
        .itertuples(index=False, name=None)
    )
    missing = distance_keys - feature_keys
    if missing:
        raise SystemExit(f"Distance table contains backend/embedding keys absent from features: {missing}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default="data/processed/tda_features.csv")
    parser.add_argument("--backend-summary", default="results/tables/tda_backend_summary.csv")
    parser.add_argument("--distances", default="results/tables/tda_distance_to_os_csprng.csv")
    parser.add_argument("--allow-fallback", action="store_true")
    args = parser.parse_args()

    features = pd.read_csv(require_file(args.features))
    backend_summary = pd.read_csv(require_file(args.backend_summary))
    distances = pd.read_csv(require_file(args.distances))

    compare_backend_summary(features, backend_summary)
    validate_no_fallback_for_manuscript(features, args.allow_fallback)
    validate_distance_backends(features, distances)

    print("Artifact consistency validation passed.")


if __name__ == "__main__":
    main()
