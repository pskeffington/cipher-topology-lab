import numpy as np

from ciphertopology.tda import compute_ripser_features, persistence_entropy


def test_persistence_entropy_zero_for_empty_lifetimes():
    assert persistence_entropy(np.array([])) == 0.0


def test_tda_feature_schema_returns_backend_field():
    points = np.array(
        [
            [0.0, 0.0],
            [0.1, 0.1],
            [0.9, 0.9],
        ]
    )
    rows = compute_ripser_features(points, max_dimension=1, max_edge_length=0.25)
    assert len(rows) >= 1
    assert "backend" in rows[0]
    assert "homology_dim" in rows[0]
    assert "persistence_entropy" in rows[0]
