from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default="data/processed/tda_features.csv")
    parser.add_argument("--require-backend", default="ripser")
    parser.add_argument("--require-finite-h1", action="store_true")
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

    if any("fallback" in backend.lower() for backend in backends):
        raise SystemExit(f"Fallback backend present in manuscript-grade run: {sorted(backends)}")

    if args.require_finite_h1:
        h1 = features[features["homology_dim"] == 1]
        if h1.empty:
            raise SystemExit("No H1 rows found in TDA feature table.")
        if h1["finite_count"].sum() <= 0:
            raise SystemExit("No finite H1 intervals found; H1 figure is not eligible.")

    print(f"Validated TDA backend. Observed backends: {sorted(backends)}")


if __name__ == "__main__":
    main()
