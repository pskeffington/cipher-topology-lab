from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


CONDITIONS = [
    "aes128_ctr_random_plaintext",
    "aes128_ctr_zero_plaintext",
    "lcg_weak",
    "xorshift32_weak",
]
BASELINE = "os_csprng"


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
) -> pd.DataFrame:
    rows = []
    for group_key, group in data.groupby(grouping_cols):
        group_dict = dict(zip(grouping_cols, group_key if isinstance(group_key, tuple) else (group_key,)))
        baseline_values = group.loc[group["condition"] == BASELINE, value_col].to_numpy()
        if len(baseline_values) == 0:
            continue
        for condition in CONDITIONS:
            values = group.loc[group["condition"] == condition, value_col].to_numpy()
            if len(values) == 0:
                continue
            _, p_value = stats.mannwhitneyu(values, baseline_values, alternative="two-sided")
            rows.append(
                {
                    "table": table_name,
                    **group_dict,
                    "condition": condition,
                    "baseline_condition": BASELINE,
                    "n": int(len(values)),
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
    parser.add_argument("--features", default="data/processed/tda_features.csv")
    parser.add_argument("--distances", default="results/tables/tda_distance_to_os_csprng.csv")
    parser.add_argument("--out-dir", default="results/tables")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    features = pd.read_csv(args.features)
    distances = pd.read_csv(args.distances)

    entropy_effects = effect_rows(
        features,
        value_col="persistence_entropy",
        table_name="persistence_entropy",
        grouping_cols=["backend", "embedding_name", "homology_dim"],
    )
    distance_effects = effect_rows(
        distances,
        value_col="euclidean_feature_distance",
        table_name="distance_to_os_csprng",
        grouping_cols=["backend", "embedding_name", "homology_dim"],
    )

    entropy_effects.to_csv(out_dir / "tda_persistence_entropy_effects.csv", index=False)
    distance_effects.to_csv(out_dir / "tda_distance_effects.csv", index=False)

    combined = pd.concat([entropy_effects, distance_effects], ignore_index=True)
    combined.to_csv(out_dir / "tda_effects_combined.csv", index=False)

    print(f"Wrote {len(entropy_effects)} persistence-entropy effect rows.")
    print(f"Wrote {len(distance_effects)} distance effect rows.")
    print(f"Wrote combined effect table to {out_dir / 'tda_effects_combined.csv'}")


if __name__ == "__main__":
    main()
