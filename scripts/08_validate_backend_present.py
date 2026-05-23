from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default="data/processed/tda_features.csv")
    parser.add_argument("--require-backend", required=True)
    args = parser.parse_args()

    path = Path(args.features)
    if not path.exists():
        raise SystemExit(f"Missing TDA feature file: {path}")

    features = pd.read_csv(path)
    if "backend" not in features.columns:
        raise SystemExit("TDA feature table has no backend column.")

    backends = set(features["backend"].dropna().astype(str))
    if args.require_backend not in backends:
        raise SystemExit(f"Required backend not found: {args.require_backend}. Observed: {sorted(backends)}")

    print(f"Validated backend presence: {args.require_backend}")


if __name__ == "__main__":
    main()
