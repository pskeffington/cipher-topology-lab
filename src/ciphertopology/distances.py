from __future__ import annotations

import pandas as pd


DISTANCE_FEATURES = [
    "interval_count",
    "finite_count",
    "lifetime_mean",
    "lifetime_sd",
    "lifetime_max",
    "persistence_entropy",
]


def distance_to_baseline(
    features: pd.DataFrame,
    baseline_condition: str = "os_csprng",
) -> pd.DataFrame:
    grouped = (
        features.groupby(["condition", "backend", "embedding_name", "homology_dim"], as_index=False)[
            DISTANCE_FEATURES
        ]
        .mean()
    )
    baseline = grouped[grouped["condition"] == baseline_condition].copy()
    rows = []
    for _, row in grouped.iterrows():
        match = baseline[
            (baseline["backend"] == row["backend"])
            & (baseline["embedding_name"] == row["embedding_name"])
            & (baseline["homology_dim"] == row["homology_dim"])
        ]
        if match.empty:
            continue
        base = match.iloc[0]
        squared_sum = 0.0
        for feature in DISTANCE_FEATURES:
            squared_sum += float(row[feature] - base[feature]) ** 2
        rows.append(
            {
                "condition": row["condition"],
                "baseline_condition": baseline_condition,
                "backend": row["backend"],
                "embedding_name": row["embedding_name"],
                "homology_dim": row["homology_dim"],
                "euclidean_feature_distance": squared_sum ** 0.5,
            }
        )
    return pd.DataFrame(rows)
