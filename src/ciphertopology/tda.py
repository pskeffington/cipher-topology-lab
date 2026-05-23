from __future__ import annotations

from typing import Any

import numpy as np


def persistence_entropy(lifetimes: np.ndarray) -> float:
    lifetimes = lifetimes[np.isfinite(lifetimes)]
    lifetimes = lifetimes[lifetimes > 0]
    if lifetimes.size == 0:
        return 0.0
    p = lifetimes / lifetimes.sum()
    return float(-(p * np.log(p)).sum())


def summarize_diagram(diagram: np.ndarray, homology_dim: int) -> dict[str, Any]:
    if diagram.size == 0:
        lifetimes = np.array([])
    else:
        births = diagram[:, 0]
        deaths = diagram[:, 1]
        lifetimes = deaths - births
        lifetimes = lifetimes[np.isfinite(lifetimes)]

    return {
        "homology_dim": homology_dim,
        "interval_count": int(diagram.shape[0]) if diagram.ndim == 2 else 0,
        "finite_count": int(lifetimes.size),
        "lifetime_mean": float(np.mean(lifetimes)) if lifetimes.size else 0.0,
        "lifetime_sd": float(np.std(lifetimes, ddof=1)) if lifetimes.size > 1 else 0.0,
        "lifetime_max": float(np.max(lifetimes)) if lifetimes.size else 0.0,
        "persistence_entropy": persistence_entropy(lifetimes),
    }


def compute_ripser_features(
    points: np.ndarray,
    max_dimension: int = 1,
    max_edge_length: float | None = None,
) -> list[dict[str, Any]]:
    try:
        from ripser import ripser
    except ImportError as exc:
        raise RuntimeError("ripser is required for persistent-homology computation.") from exc

    kwargs: dict[str, Any] = {"maxdim": max_dimension}
    if max_edge_length is not None:
        kwargs["thresh"] = max_edge_length

    result = ripser(points, **kwargs)
    diagrams = result["dgms"]
    return [summarize_diagram(diagram, dim) for dim, diagram in enumerate(diagrams)]
