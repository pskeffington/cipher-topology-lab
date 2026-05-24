from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from ciphertopology.utils import read_json


def read_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"Missing required artifact: {path}")
    return pd.read_csv(path)


def read_conditions(path: Path) -> set[str]:
    frame = read_frame(path)
    if "condition" not in frame.columns:
        return set()
    return set(frame["condition"].dropna().astype(str))


def check_condition_set(
    path: Path,
    expected_conditions: set[str],
    mismatches: list[str],
) -> None:
    observed = read_conditions(path)
    if observed and observed != expected_conditions:
        mismatches.append(
            f"{path}: observed_conditions={sorted(observed)} "
            f"expected_conditions={sorted(expected_conditions)}"
        )


def check_group_counts(
    frame: pd.DataFrame,
    path: Path,
    group_columns: list[str],
    expected_count: int,
    mismatches: list[str],
    count_column: str | None = None,
) -> None:
    missing = [column for column in group_columns if column not in frame.columns]
    if missing:
        mismatches.append(f"{path}: missing columns for grouped count check: {missing}")
        return

    if count_column is not None and count_column in frame.columns:
        counts = frame.groupby(group_columns)[count_column].nunique(dropna=True)
        count_label = f"unique {count_column}"
    else:
        counts = frame.groupby(group_columns).size()
        count_label = "rows"

    bad = counts[counts != expected_count]
    if not bad.empty:
        examples = bad.head(12).to_dict()
        mismatches.append(
            f"{path}: expected {expected_count} {count_label} per {group_columns}; "
            f"found mismatches={examples}"
        )


def check_expected_categories(
    frame: pd.DataFrame,
    path: Path,
    column: str,
    expected_values: set[str] | set[int],
    mismatches: list[str],
) -> None:
    if column not in frame.columns:
        return
    observed = set(frame[column].dropna().tolist())
    if observed and not observed.issubset(expected_values):
        mismatches.append(
            f"{path}: unexpected {column} values={sorted(observed - expected_values)} "
            f"expected_subset={sorted(expected_values)}"
        )


def check_stream_manifest(
    path: Path,
    expected_conditions: set[str],
    replicates: int,
    mismatches: list[str],
) -> None:
    frame = read_frame(path)
    check_condition_set(path, expected_conditions, mismatches)
    if "replicate" in frame.columns:
        check_group_counts(frame, path, ["condition"], replicates, mismatches, "replicate")
    elif "stream_id" in frame.columns:
        check_group_counts(frame, path, ["condition"], replicates, mismatches, "stream_id")


def check_embedding_manifest(
    path: Path,
    expected_conditions: set[str],
    expected_embeddings: set[str],
    replicates: int,
    mismatches: list[str],
) -> None:
    frame = read_frame(path)
    check_condition_set(path, expected_conditions, mismatches)
    check_expected_categories(frame, path, "embedding_name", expected_embeddings, mismatches)
    if "embedding_name" in frame.columns:
        count_column = "stream_id" if "stream_id" in frame.columns else None
        check_group_counts(
            frame,
            path,
            ["embedding_name", "condition"],
            replicates,
            mismatches,
            count_column,
        )


def check_tda_features(
    path: Path,
    expected_conditions: set[str],
    expected_embeddings: set[str],
    expected_homology_dims: set[int],
    replicates: int,
    mismatches: list[str],
) -> None:
    frame = read_frame(path)
    check_condition_set(path, expected_conditions, mismatches)
    check_expected_categories(frame, path, "embedding_name", expected_embeddings, mismatches)
    check_expected_categories(frame, path, "homology_dim", expected_homology_dims, mismatches)
    required = ["backend", "embedding_name", "homology_dim", "condition"]
    if all(column in frame.columns for column in required):
        check_group_counts(frame, path, required, replicates, mismatches)


def check_randomness_tests(
    path: Path,
    expected_conditions: set[str],
    replicates: int,
    mismatches: list[str],
) -> None:
    frame = read_frame(path)
    check_condition_set(path, expected_conditions, mismatches)
    if "stream_id" in frame.columns:
        check_group_counts(frame, path, ["condition"], replicates, mismatches, "stream_id")


def check_backend_summary(
    path: Path,
    expected_conditions: set[str],
    expected_embeddings: set[str],
    expected_homology_dims: set[int],
    replicates: int,
    mismatches: list[str],
) -> None:
    frame = read_frame(path)
    # Backend summary is grouped above condition, so it normally lacks a condition column.
    check_expected_categories(frame, path, "embedding_name", expected_embeddings, mismatches)
    check_expected_categories(frame, path, "homology_dim", expected_homology_dims, mismatches)
    if "row_count" in frame.columns:
        expected_rows = replicates * len(expected_conditions)
        bad = frame[frame["row_count"] != expected_rows]
        if not bad.empty:
            mismatches.append(
                f"{path}: expected row_count={expected_rows} per backend/embedding/H; "
                f"found={bad.head(12).to_dict(orient='records')}"
            )


def check_feature_summary(
    path: Path,
    expected_conditions: set[str],
    expected_embeddings: set[str],
    expected_homology_dims: set[int],
    mismatches: list[str],
) -> None:
    frame = read_frame(path)
    check_condition_set(path, expected_conditions, mismatches)
    check_expected_categories(frame, path, "embedding_name", expected_embeddings, mismatches)
    check_expected_categories(frame, path, "homology_dim", expected_homology_dims, mismatches)


def check_distance_table(
    path: Path,
    expected_conditions: set[str],
    expected_embeddings: set[str],
    expected_homology_dims: set[int],
    baseline_condition: str,
    replicates: int,
    mismatches: list[str],
) -> None:
    frame = read_frame(path)
    check_condition_set(path, expected_conditions, mismatches)
    check_expected_categories(frame, path, "embedding_name", expected_embeddings, mismatches)
    check_expected_categories(frame, path, "homology_dim", expected_homology_dims, mismatches)
    if "baseline_condition" in frame.columns:
        observed_baselines = set(frame["baseline_condition"].dropna().astype(str))
        if observed_baselines != {baseline_condition}:
            mismatches.append(
                f"{path}: observed_baseline_condition={sorted(observed_baselines)} "
                f"expected_baseline_condition={[baseline_condition]}"
            )
    required = ["backend", "embedding_name", "homology_dim", "condition"]
    if all(column in frame.columns for column in required):
        count_column = "stream_id" if "stream_id" in frame.columns else None
        check_group_counts(frame, path, required, replicates, mismatches, count_column)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_json(args.config)
    expected_conditions = set(config["conditions"])
    expected_embeddings = {item["name"] for item in config.get("embeddings", [])}
    expected_homology_dims = set(range(int(config.get("tda", {}).get("max_dimension", 1)) + 1))
    replicates = int(config["replicates"])
    baseline_condition = config.get("baseline_condition")
    if baseline_condition and baseline_condition not in expected_conditions:
        raise SystemExit(
            f"Configured baseline_condition is not present in conditions: {baseline_condition}"
        )

    mismatches: list[str] = []

    check_stream_manifest(
        Path("data/raw/stream_manifest.csv"), expected_conditions, replicates, mismatches
    )
    check_embedding_manifest(
        Path("data/interim/embedding_manifest.csv"),
        expected_conditions,
        expected_embeddings,
        replicates,
        mismatches,
    )
    check_tda_features(
        Path("data/processed/tda_features.csv"),
        expected_conditions,
        expected_embeddings,
        expected_homology_dims,
        replicates,
        mismatches,
    )
    check_randomness_tests(
        Path("data/processed/randomness_tests_internal.csv"),
        expected_conditions,
        replicates,
        mismatches,
    )
    check_feature_summary(
        Path("results/tables/tda_feature_summary.csv"),
        expected_conditions,
        expected_embeddings,
        expected_homology_dims,
        mismatches,
    )
    check_backend_summary(
        Path("results/tables/tda_backend_summary.csv"),
        expected_conditions,
        expected_embeddings,
        expected_homology_dims,
        replicates,
        mismatches,
    )

    if baseline_condition:
        distance_path = Path(f"results/tables/tda_distance_to_{baseline_condition}.csv")
        check_distance_table(
            distance_path,
            expected_conditions,
            expected_embeddings,
            expected_homology_dims,
            baseline_condition,
            replicates,
            mismatches,
        )

    if mismatches:
        raise SystemExit("Artifact coherence validation failed:\n" + "\n".join(mismatches))

    print(
        "Validated artifact coherence: "
        f"conditions={len(expected_conditions)}, embeddings={len(expected_embeddings)}, "
        f"homology_dims={sorted(expected_homology_dims)}, replicates={replicates}, "
        f"baseline={baseline_condition}."
    )


if __name__ == "__main__":
    main()
