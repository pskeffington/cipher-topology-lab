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
    """Compute stream-level distance to the baseline centroid.

    Distances are computed within each backend, embedding, and homology dimension.
    The baseline centroid is the mean feature vector among streams whose condition
    equals `baseline_condition`. Each stream is then compared with that centroid.
    This yields replicate-level distance distributions rather than one aggregate
    distance per condition.
    """
    required = {
        "stream_id",
        "condition",
        "backend",
        "embedding_name",
        "homology_dim",
        *DISTANCE_FEATURES,
    }
    missing = required - set(features.columns)
    if missing:
        raise ValueError(f"Missing required distance feature columns: {sorted(missing)}")

    baseline = (
        features[features["condition"] == baseline_condition]
        .groupby(["backend", "embedding_name", "homology_dim"], as_index=False)[DISTANCE_FEATURES]
        .mean()
    )

    rows = []
    for _, row in features.iterrows():
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
                "stream_id": row["stream_id"],
                "condition": row["condition"],
                "baseline_condition": baseline_condition,
                "backend": row["backend"],
                "embedding_name": row["embedding_name"],
                "homology_dim": row["homology_dim"],
                "euclidean_feature_distance": squared_sum ** 0.5,
            }
        )
    return pd.DataFrame(rows)
