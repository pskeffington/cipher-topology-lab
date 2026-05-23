from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
import pandas as pd

from ciphertopology.embeddings import make_embedding
from ciphertopology.utils import ensure_dirs, read_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = read_json(args.config)
    ensure_dirs("data/interim")
    manifest = pd.read_csv("data/raw/stream_manifest.csv")
    rows = []

    for _, stream_row in manifest.iterrows():
        data = Path(stream_row["path"]).read_bytes()
        for emb in config["embeddings"]:
            points = make_embedding(data, emb["name"], emb["dimension"], emb["stride"], emb["sample_points"])
            embedding_id = f"{stream_row['stream_id']}__{emb['name']}"
            out_path = Path("data/interim") / f"{embedding_id}.npy"
            np.save(out_path, points)
            rows.append({
                "embedding_id": embedding_id,
                "stream_id": stream_row["stream_id"],
                "condition": stream_row["condition"],
                "embedding_name": emb["name"],
                "dimension": emb["dimension"],
                "stride": emb["stride"],
                "sample_points": points.shape[0],
                "path": str(out_path),
            })

    out_manifest = Path("data/interim/embedding_manifest.csv")
    with out_manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} embeddings to data/interim")


if __name__ == "__main__":
    main()
