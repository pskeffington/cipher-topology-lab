from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ciphertopology.distances import distance_to_baseline
from ciphertopology.utils import ensure_dirs, read_json


def slug(value: object) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value)).strip("_")


def label_condition(value: object) -> str:
    labels = {
        "aes128_ctr_xor_deterministic_plaintext": "AES-CTR\ndeterministic PT",
        "aes128_ctr_keystream_zero_plaintext": "AES-CTR\nzero PT",
        "sha256_seeded_baseline": "SHA-256\nseeded baseline",
        "os_csprng": "OS\nCSPRNG",
        "lcg_weak": "LCG\nweak",
        "xorshift32_weak": "xorshift32\nweak",
        "aes128_ctr_random_plaintext": "AES-CTR\nlegacy random PT",
        "aes128_ctr_zero_plaintext": "AES-CTR\nlegacy zero PT",
    }
    return labels.get(str(value), "\n".join(textwrap.wrap(str(value), width=16)))


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


def save_boxplot(
    data: pd.DataFrame,
    value_column: str,
    title: str,
    ylabel: str,
    out_path: Path,
) -> None:
    plot_data = data.copy()
    plot_data["condition_label"] = plot_data["condition"].map(label_condition)
    ax = plot_data.boxplot(column=value_column, by="condition_label", rot=0, figsize=(12, 7))
    ax.set_title(title, fontsize=12)
    ax.set_xlabel("Condition")
    ax.set_ylabel(ylabel)
    plt.suptitle("")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()


def write_figure_notes(
    baseline_condition: str,
    include_baseline_distance_plots: bool,
) -> None:
    baseline_display = label_condition(baseline_condition).replace("\n", " ")
    note = f"""
# Figure notes

Distance figures show stream-level Euclidean distances to the {baseline_display} condition centroid.
The distance CSV retains all streams, including the baseline condition. If the baseline is displayed,
its values represent within-baseline dispersion around the baseline centroid rather than zero distance.

Displayed distance plots exclude the baseline condition by default to emphasize nonbaseline separation.
Set `--include-baseline-distance-plots` to display baseline dispersion in distance figures.

Persistence-entropy figures are not distance-to-baseline figures and therefore retain all configured
conditions.

Current distance-plot baseline inclusion: {include_baseline_distance_plots}.
"""
    write_diagnostic_note(Path("results/logs/figure_notes.md"), note)


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
        out = (
            Path("results/figures")
            / f"h{homology_dim}_persistence_entropy__{slug(backend)}__{slug(embedding_name)}.png"
        )
        save_boxplot(
            group,
            "persistence_entropy",
            f"H{homology_dim} Persistence Entropy: {backend} / {embedding_name}",
            "Persistence entropy",
            out,
        )
        plot_count += 1
    return plot_count


def plot_distances_by_condition(
    distances: pd.DataFrame,
    baseline_condition: str,
    include_baseline: bool = False,
) -> int:
    if distances.empty:
        return 0
    plot_count = 0
    skipped: list[str] = []
    baseline_slug = slug(baseline_condition)
    distance_specs = [
        ("euclidean_feature_distance", "Raw Euclidean feature distance", "raw"),
        ("z_scored_euclidean_feature_distance", "Z-scored Euclidean feature distance", "zscored"),
    ]
    for (backend, embedding_name, homology_dim), group in distances.groupby(
        ["backend", "embedding_name", "homology_dim"]
    ):
        nonbaseline = group[group["condition"] != group["baseline_condition"]]
        plot_group = group if include_baseline else nonbaseline
        if plot_group.empty:
            skipped.append(f"{backend} / {embedding_name} / H{homology_dim}")
            continue
        has_distance_signal = bool(nonbaseline["euclidean_feature_distance"].abs().sum() > 0)
        if not has_distance_signal:
            skipped.append(f"{backend} / {embedding_name} / H{homology_dim}")
            continue
        for column, ylabel, suffix in distance_specs:
            if column not in group.columns:
                continue
            baseline_suffix = "with_baseline" if include_baseline else "nonbaseline"
            out = (
                Path("results/figures")
                / f"tda_distance_to_{baseline_slug}__{slug(backend)}__{slug(embedding_name)}__h{homology_dim}__{suffix}__{baseline_suffix}.png"
            )
            title_suffix = "with baseline" if include_baseline else "nonbaseline only"
            save_boxplot(
                plot_group,
                column,
                f"TDA Distance to {baseline_condition}: {backend} / {embedding_name} / H{homology_dim} ({title_suffix})",
                ylabel,
                out,
            )
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
    parser.add_argument(
        "--include-baseline-distance-plots",
        action="store_true",
        help="Display baseline-condition dispersion in distance figures. CSV outputs always retain baseline rows.",
    )
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
    distance_plot_count = plot_distances_by_condition(
        distances,
        baseline_condition,
        include_baseline=args.include_baseline_distance_plots,
    )
    write_figure_notes(baseline_condition, args.include_baseline_distance_plots)

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
