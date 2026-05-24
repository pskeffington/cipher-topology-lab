import pandas as pd

from ciphertopology.distances import distance_to_baseline


def test_distance_to_baseline_returns_stream_level_distances():
    features = pd.DataFrame(
        [
            {
                "stream_id": "os_001",
                "condition": "os_csprng",
                "backend": "ripser",
                "embedding_name": "byte_pair_2d",
                "homology_dim": 0,
                "interval_count": 1,
                "finite_count": 1,
                "lifetime_mean": 0.1,
                "lifetime_sd": 0.0,
                "lifetime_max": 0.1,
                "persistence_entropy": 0.0,
            },
            {
                "stream_id": "weak_001",
                "condition": "lcg_weak",
                "backend": "ripser",
                "embedding_name": "byte_pair_2d",
                "homology_dim": 0,
                "interval_count": 2,
                "finite_count": 1,
                "lifetime_mean": 0.1,
                "lifetime_sd": 0.0,
                "lifetime_max": 0.1,
                "persistence_entropy": 0.0,
            },
        ]
    )
    distances = distance_to_baseline(features)
    assert "stream_id" in distances.columns
    assert len(distances) == 2
    control_distance = distances.loc[
        distances["condition"] == "os_csprng", "euclidean_feature_distance"
    ].iloc[0]
    weak_distance = distances.loc[
        distances["condition"] == "lcg_weak", "euclidean_feature_distance"
    ].iloc[0]
    assert control_distance == 0.0
    assert weak_distance > 0.0
