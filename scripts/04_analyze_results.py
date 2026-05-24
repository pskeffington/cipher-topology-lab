from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ciphertopology.distances import distance_to_baseline
from ciphertopology.utils import ensure_dirs, read_json


def slug(value: object) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value)).strip("_")


def write_diagnostic_note(path: Path, message: str) -> None:
    path.write_text(message.strip() + "\n", encoding="utf-8")


def remove_stale_combined_plots() -> None:
    for stale in [
        Path("results/figures/h1_persistence_entropy_by_condition.png"),
        Path("results/figures/h0_persistence_entropy_by_condition.png"),
        Path("results/figures/tda_distance_to_os_csprng.png"),
    ]:
        if stale.exists():
            stale.unlink()


def plot_entropy_by_condition(features: pd.DataFrame, homology_dim: int) -> int:
    plot_count = 0
    subset = features[features["homology_dim"] == homology_dim].copy()
    if subset.empty:
        return 0

    for (backend, embedding_name), group in subset.groupby(["backend", "embedding_name"]):
        has_signal = bool(
            (group["finite_count"].sum() > 0) and (group["persistence_entropy"].abs().sum() > 0)
        )
        if not has_signal:
            continue
        plt.figure(figsize=(10, 6))
        group.boxplot(column="persistence_entropy", by="condition", rot=45)
        plt.title(f"H{homology_dim} Persistence Entropy by Condition: {backend} / {embedding_name}")
        plt.suptitle("")
        plt.ylabel("Persistence entropy")
        plt.tight_layout()
        out = (
            Path("results/figures")
            / f"h{homology_dim}_persistence_entropy__{slug(backend)}__{slug(embedding_name)}.png"
        )
        plt.savefig(out, dpi=300)
        plt.close()
        plot_count += 1
    return plot_count


def plot_distances_by_condition(distances: pd.DataFrame, baseline_condition: str) -> int:
    if distances.empty:
        return 0
    plot_count = 0
    skipped: list[str] = []
    baseline_slug = slug(baseline_condition)
    for (backend, embedding_name, homology_dim), group in distances.groupby(
        ["backend", "embedding_name", "homology_dim"]
    ):
        nonbaseline = group[group["condition"] != group["baseline_condition"]]
        has_distance_signal = bool(nonbaseline["euclidean_feature_distance"].abs().sum() > 0)
        if not has_distance_signal:
            skipped.append(f"{backend} / {embedding_name} / H{homology_dim}")
            continue
        plt.figure(figsize=(10, 6))
        group.boxplot(column="euclidean_feature_distance", by="condition", rot=45)
        plt.title(
            f"TDA Feature Distance to {baseline_condition}: "
            f"{backend} / {embedding_name} / H{homology_dim}"
        )
        plt.suptitle("")
        plt.ylabel("Euclidean feature distance")
        plt.tight_layout()
        out = (
            Path("results/figures")
            / f"tda_distance_to_{baseline_slug}__{slug(backend)}__{slug(embedding_name)}__h{homology_dim}.png"
        )
        plt.savefig(out, dpi=300)
        plt.close()
        plot_count += 1
    if skipped:
        write_diagnostic_note(
            Path("results/logs/distance_plots_skipped.txt"),
            "Skipped distance plots with no nonbaseline distance signal:\n" + "\n".join(skipped),
        )
    return plot_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config = read_json(args.config)
    baseline_condition = config.get("baseline_condition", "os_csprng")
    baseline_slug = slug(baseline_condition)

    ensure_dirs("results/figures", "results/tables", "results/logs")
    remove_stale_combined_plots()
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

    distances = distance_to_baseline(features, baseline_condition=baseline_condition)
    distances.to_csv(f"results/tables/tda_distance_to_{baseline_slug}.csv", index=False)
    if baseline_condition == "os_csprng":
        distances.to_csv("results/tables/tda_distance_to_os_csprng.csv", index=False)

    fallback_used = features["backend"].astype(str).str.contains("fallback", case=False).any()
    h1_plot_count = plot_entropy_by_condition(features, homology_dim=1)
    h0_plot_count = plot_entropy_by_condition(features, homology_dim=0)
    distance_plot_count = plot_distances_by_condition(distances, baseline_condition)

    if fallback_used:
        write_diagnostic_note(
            Path("results/logs/fallback_backend_used.txt"),
            "A fallback TDA backend was used. Figures from this run are diagnostic only and are not manuscript-grade evidence.",
        )
    if h1_plot_count == 0:
        write_diagnostic_note(
            Path("results/logs/h1_plot_skipped.txt"),
            "No stratified H1 persistence-entropy plot was produced because no backend/embedding group had finite H1 signal.",
        )

    print(
        "Wrote analysis summaries, backend diagnostics, distances, and stratified figures: "
        f"baseline={baseline_condition}, H0={h0_plot_count}, H1={h1_plot_count}, "
        f"distances={distance_plot_count}."
    )


if __name__ == "__main__":
    main()
