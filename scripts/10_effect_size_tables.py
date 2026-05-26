from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from ciphertopology.utils import read_json


def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    greater = 0
    lesser = 0
    for value in x:
        greater += int(np.sum(value > y))
        lesser += int(np.sum(value < y))
    return float((greater - lesser) / (len(x) * len(y)))


def effect_rows(
    data: pd.DataFrame,
    value_col: str,
    table_name: str,
    grouping_cols: list[str],
    baseline_condition: str,
    comparison_conditions: list[str],
) -> pd.DataFrame:
    rows = []
    for group_key, group in data.groupby(grouping_cols):
        group_dict = dict(zip(grouping_cols, group_key if isinstance(group_key, tuple) else (group_key,)))
        baseline_values = group.loc[group["condition"] == baseline_condition, value_col].to_numpy()
        if len(baseline_values) == 0:
            continue
        for condition in comparison_conditions:
            values = group.loc[group["condition"] == condition, value_col].to_numpy()
            if len(values) == 0:
                continue
            _, p_value = stats.mannwhitneyu(values, baseline_values, alternative="two-sided")
            rows.append(
                {
                    "table": table_name,
                    **group_dict,
                    "condition": condition,
                    "baseline_condition": baseline_condition,
                    "n": int(len(values)),
                    "baseline_n": int(len(baseline_values)),
                    "median": float(np.median(values)),
                    "baseline_median": float(np.median(baseline_values)),
                    "mean": float(np.mean(values)),
                    "baseline_mean": float(np.mean(baseline_values)),
                    "cliffs_delta": cliffs_delta(values, baseline_values),
                    "mann_whitney_p": float(p_value),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/experiment_v0.json")
    parser.add_argument("--features", default="data/processed/tda_features.csv")
    parser.add_argument("--distances", default=None)
    parser.add_argument("--out-dir", default="results/tables")
    args = parser.parse_args()

    config = read_json(args.config)
    baseline_condition = config.get("baseline_condition")
    if not baseline_condition:
        raise SystemExit(f"Config has no baseline_condition: {args.config}")
    comparison_conditions = [
        condition for condition in config.get("conditions", []) if condition != baseline_condition
    ]
    if not comparison_conditions:
        raise SystemExit(f"Config has no nonbaseline comparison conditions: {args.config}")

    distance_path = args.distances or f"results/tables/tda_distance_to_{baseline_condition}.csv"

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    features = pd.read_csv(args.features)
    distances = pd.read_csv(distance_path)

    entropy_effects = effect_rows(
        features,
        value_col="persistence_entropy",
        table_name="persistence_entropy",
        grouping_cols=["backend", "embedding_name", "homology_dim"],
        baseline_condition=baseline_condition,
        comparison_conditions=comparison_conditions,
    )
    distance_effects = effect_rows(
        distances,
        value_col="euclidean_feature_distance",
        table_name=f"distance_to_{baseline_condition}",
        grouping_cols=["backend", "embedding_name", "homology_dim"],
        baseline_condition=baseline_condition,
        comparison_conditions=comparison_conditions,
    )

    entropy_effects.to_csv(out_dir / "tda_persistence_entropy_effects.csv", index=False)
    distance_effects.to_csv(out_dir / "tda_distance_effects.csv", index=False)

    combined = pd.concat([entropy_effects, distance_effects], ignore_index=True)
    combined.to_csv(out_dir / "tda_effects_combined.csv", index=False)

    print(
        "Wrote effect-size tables: "
        f"baseline={baseline_condition}, comparisons={len(comparison_conditions)}, "
        f"entropy_rows={len(entropy_effects)}, distance_rows={len(distance_effects)}."
    )
    print(f"Wrote combined effect table to {out_dir / 'tda_effects_combined.csv'}")


if __name__ == "__main__":
    main()
