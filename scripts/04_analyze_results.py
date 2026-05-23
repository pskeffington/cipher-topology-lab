from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ciphertopology.utils import ensure_dirs, read_json


def write_diagnostic_note(path: Path, message: str) -> None:
    path.write_text(message.strip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    _ = read_json(args.config)

    ensure_dirs("results/figures", "results/tables", "results/logs")
    features = pd.read_csv("data/processed/tda_features.csv")

    backend_summary = (
        features.groupby(["backend", "embedding_name", "homology_dim"], as_index=False)
        .size()
        .rename(columns={"size": "row_count"})
    )
    backend_summary.to_csv("results/tables/tda_backend_summary.csv", index=False)

    summary = (
        features.groupby(["backend", "condition", "embedding_name", "homology_dim"], as_index=False)
        .agg(
            interval_count_mean=("interval_count", "mean"),
            finite_count_mean=("finite_count", "mean"),
            lifetime_mean=("lifetime_mean", "mean"),
            lifetime_max_mean=("lifetime_max", "mean"),
            persistence_entropy_mean=("persistence_entropy", "mean"),
        )
    )
    summary.to_csv("results/tables/tda_feature_summary.csv", index=False)

    fallback_used = features["backend"].astype(str).str.contains("fallback", case=False).any()
    h1 = features[features["homology_dim"] == 1].copy()
    h1_has_signal = bool((h1["finite_count"].sum() > 0) and (h1["persistence_entropy"].abs().sum() > 0))

    if not fallback_used and h1_has_signal:
        plt.figure(figsize=(10, 6))
        h1.boxplot(column="persistence_entropy", by="condition", rot=45)
        plt.title("H1 Persistence Entropy by Condition")
        plt.suptitle("")
        plt.ylabel("Persistence entropy")
        plt.tight_layout()
        plt.savefig("results/figures/h1_persistence_entropy_by_condition.png", dpi=300)
        plt.close()
    else:
        write_diagnostic_note(
            Path("results/logs/h1_plot_skipped.txt"),
            "H1 persistence-entropy plot skipped because the run used a fallback backend or produced no finite H1 intervals. Manuscript-grade H1 figures require ripser or GUDHI output with finite H1 intervals.",
        )

    h0 = features[features["homology_dim"] == 0].copy()
    if not h0.empty:
        plt.figure(figsize=(10, 6))
        h0.boxplot(column="persistence_entropy", by="condition", rot=45)
        plt.title("H0 Persistence Entropy by Condition")
        plt.suptitle("")
        plt.ylabel("Persistence entropy")
        plt.tight_layout()
        plt.savefig("results/figures/h0_persistence_entropy_by_condition.png", dpi=300)
        plt.close()

    print("Wrote analysis summaries, backend diagnostics, and eligible figures.")


if __name__ == "__main__":
    main()
