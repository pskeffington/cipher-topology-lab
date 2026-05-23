from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd

from ciphertopology.utils import ensure_dirs, read_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    _ = read_json(args.config)

    ensure_dirs("results/figures", "results/tables")
    features = pd.read_csv("data/processed/tda_features.csv")
    summary = (
        features.groupby(["condition", "embedding_name", "homology_dim"], as_index=False)
        .agg(
            interval_count_mean=("interval_count", "mean"),
            finite_count_mean=("finite_count", "mean"),
            lifetime_mean=("lifetime_mean", "mean"),
            lifetime_max_mean=("lifetime_max", "mean"),
            persistence_entropy_mean=("persistence_entropy", "mean"),
        )
    )
    summary.to_csv("results/tables/tda_feature_summary.csv", index=False)

    plot_df = features[features["homology_dim"] == 1].copy()
    if not plot_df.empty:
        plt.figure(figsize=(10, 6))
        plot_df.boxplot(column="persistence_entropy", by="condition", rot=45)
        plt.title("H1 Persistence Entropy by Condition")
        plt.suptitle("")
        plt.ylabel("Persistence entropy")
        plt.tight_layout()
        plt.savefig("results/figures/h1_persistence_entropy_by_condition.png", dpi=300)
        plt.close()

    print("Wrote analysis summaries and figures.")


if __name__ == "__main__":
    main()
