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
    assert "euclidean_feature_distance" in distances.columns
    assert "z_scored_euclidean_feature_distance" in distances.columns
    assert len(distances) == 2
    control_distance = distances.loc[
        distances["condition"] == "os_csprng", "euclidean_feature_distance"
    ].iloc[0]
    weak_distance = distances.loc[
        distances["condition"] == "lcg_weak", "euclidean_feature_distance"
    ].iloc[0]
    weak_standardized_distance = distances.loc[
        distances["condition"] == "lcg_weak", "z_scored_euclidean_feature_distance"
    ].iloc[0]
    assert control_distance == 0.0
    assert weak_distance > 0.0
    assert weak_standardized_distance > 0.0


def test_distance_to_baseline_accepts_deterministic_baseline():
    features = pd.DataFrame(
        [
            {
                "stream_id": "det_001",
                "condition": "sha256_seeded_baseline",
                "backend": "ripser",
                "embedding_name": "byte_pair_2d",
                "homology_dim": 1,
                "interval_count": 10,
                "finite_count": 4,
                "lifetime_mean": 0.2,
                "lifetime_sd": 0.01,
                "lifetime_max": 0.3,
                "persistence_entropy": 1.2,
            },
            {
                "stream_id": "aes_001",
                "condition": "aes128_ctr_keystream_zero_plaintext",
                "backend": "ripser",
                "embedding_name": "byte_pair_2d",
                "homology_dim": 1,
                "interval_count": 11,
                "finite_count": 5,
                "lifetime_mean": 0.25,
                "lifetime_sd": 0.02,
                "lifetime_max": 0.35,
                "persistence_entropy": 1.5,
            },
        ]
    )
    distances = distance_to_baseline(features, baseline_condition="sha256_seeded_baseline")
    assert set(distances["condition"]) == {
        "sha256_seeded_baseline",
        "aes128_ctr_keystream_zero_plaintext",
    }
