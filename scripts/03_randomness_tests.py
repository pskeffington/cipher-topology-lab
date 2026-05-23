from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from ciphertopology.stats import monobit_frequency_test
from ciphertopology.utils import ensure_dirs, read_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    _ = read_json(args.config)

    ensure_dirs("data/processed", "results/tables")
    manifest = pd.read_csv("data/raw/stream_manifest.csv")
    rows = []

    for _, row in manifest.iterrows():
        data = Path(row["path"]).read_bytes()
        result = monobit_frequency_test(data)
        rows.append({
            "stream_id": row["stream_id"],
            "condition": row["condition"],
            "test": "monobit_frequency_internal",
            **result,
        })

    out = pd.DataFrame(rows)
    out.to_csv("data/processed/randomness_tests_internal.csv", index=False)
    out.to_csv("results/tables/randomness_tests_internal.csv", index=False)
    print("Wrote internal randomness-test diagnostics.")


if __name__ == "__main__":
    main()
