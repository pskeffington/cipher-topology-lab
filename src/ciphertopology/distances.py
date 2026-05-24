from __future__ import annotations

import math

import pandas as pd


DISTANCE_FEATURES = [
    "interval_count",
    "finite_count",
    "lifetime_mean",
    "lifetime_sd",
    "lifetime_max",
    "persistence_entropy",
]

STRATA_COLUMNS = ["backend", "embedding_name", "homology_dim"]


def _validate_feature_table(features: pd.DataFrame) -> None:
    required = {
        "stream_id",
        "condition",
        *STRATA_COLUMNS,
        *DISTANCE_FEATURES,
    }
    missing = required - set(features.columns)
    if missing:
        raise ValueError(f"Missing required distance feature columns: {sorted(missing)}")


def _safe_scale(value: float) -> float:
    if math.isnan(value) or value == 0.0:
        return 1.0
    return value


def distance_to_baseline(
    features: pd.DataFrame,
    baseline_condition: str = "os_csprng",
) -> pd.DataFrame:
    """Compute stream-level raw and standardized distance to a baseline centroid.

    Distances are computed within each backend, embedding, and homology dimension.
    The raw Euclidean distance preserves the original feature units. The standardized
    distance z-scores each feature within its backend x embedding x H-dimension stratum
    before comparing streams with the baseline centroid, preventing count features from
    automatically dominating entropy or lifetime features.
    """
    _validate_feature_table(features)

    baseline = (
        features[features["condition"] == baseline_condition]
        .groupby(STRATA_COLUMNS, as_index=False)[DISTANCE_FEATURES]
        .mean()
    )
    if baseline.empty:
        raise ValueError(f"Baseline condition not found: {baseline_condition}")

    scales = (
        features.groupby(STRATA_COLUMNS, as_index=False)[DISTANCE_FEATURES]
        .std(ddof=1)
        .rename(columns={feature: f"{feature}_sd_scale" for feature in DISTANCE_FEATURES})
    )

    rows = []
    for _, row in features.iterrows():
        match = baseline[
            (baseline["backend"] == row["backend"])
            & (baseline["embedding_name"] == row["embedding_name"])
            & (baseline["homology_dim"] == row["homology_dim"])
        ]
        scale_match = scales[
            (scales["backend"] == row["backend"])
            & (scales["embedding_name"] == row["embedding_name"])
            & (scales["homology_dim"] == row["homology_dim"])
        ]
        if match.empty or scale_match.empty:
            continue

        base = match.iloc[0]
        scale = scale_match.iloc[0]
        raw_squared_sum = 0.0
        standardized_squared_sum = 0.0
        for feature in DISTANCE_FEATURES:
            diff = float(row[feature] - base[feature])
            raw_squared_sum += diff**2
            sd_scale = _safe_scale(float(scale[f"{feature}_sd_scale"]))
            standardized_squared_sum += (diff / sd_scale) ** 2

        rows.append(
            {
                "stream_id": row["stream_id"],
                "condition": row["condition"],
                "baseline_condition": baseline_condition,
                "backend": row["backend"],
                "embedding_name": row["embedding_name"],
                "homology_dim": row["homology_dim"],
                "euclidean_feature_distance": raw_squared_sum**0.5,
                "z_scored_euclidean_feature_distance": standardized_squared_sum**0.5,
            }
        )
    return pd.DataFrame(rows)
