from __future__ import annotations

import argparse

import numpy as np
import pandas as pd
from tqdm import tqdm

from ciphertopology.tda import compute_cubical_features, compute_ripser_features
from ciphertopology.utils import ensure_dirs, read_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_json(args.config)
    ensure_dirs("data/processed", "results/tables")
    manifest = pd.read_csv("data/interim/embedding_manifest.csv")
    rows = []

    for _, row in tqdm(manifest.iterrows(), total=len(manifest)):
        embedding = np.load(row["path"])
        if row["embedding_name"] == "cubical_image_2d":
            feature_rows = compute_cubical_features(embedding)
        else:
            feature_rows = compute_ripser_features(
                embedding,
                max_dimension=config["tda"]["max_dimension"],
                max_edge_length=config["tda"]["max_edge_length"],
            )
        for feat in feature_rows:
            rows.append({
                "embedding_id": row["embedding_id"],
                "stream_id": row["stream_id"],
                "condition": row["condition"],
                "embedding_name": row["embedding_name"],
                **feat,
            })

    features = pd.DataFrame(rows)
    features.to_csv("data/processed/tda_features.csv", index=False)
    features.to_csv("results/tables/tda_features.csv", index=False)
    print("Wrote TDA features to data/processed/tda_features.csv")


if __name__ == "__main__":
    main()
