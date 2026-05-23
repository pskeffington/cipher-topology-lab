from __future__ import annotations

from typing import Any

import numpy as np
from scipy.spatial.distance import pdist, squareform


def persistence_entropy(lifetimes: np.ndarray) -> float:
    lifetimes = lifetimes[np.isfinite(lifetimes)]
    lifetimes = lifetimes[lifetimes > 0]
    if lifetimes.size == 0:
        return 0.0
    p = lifetimes / lifetimes.sum()
    return float(-(p * np.log(p)).sum())


def summarize_diagram(diagram: np.ndarray, homology_dim: int, backend: str) -> dict[str, Any]:
    if diagram.size == 0:
        lifetimes = np.array([])
    else:
        births = diagram[:, 0]
        deaths = diagram[:, 1]
        lifetimes = deaths - births
        lifetimes = lifetimes[np.isfinite(lifetimes)]

    return {
        "backend": backend,
        "homology_dim": homology_dim,
        "interval_count": int(diagram.shape[0]) if diagram.ndim == 2 else 0,
        "finite_count": int(lifetimes.size),
        "lifetime_mean": float(np.mean(lifetimes)) if lifetimes.size else 0.0,
        "lifetime_sd": float(np.std(lifetimes, ddof=1)) if lifetimes.size > 1 else 0.0,
        "lifetime_max": float(np.max(lifetimes)) if lifetimes.size else 0.0,
        "persistence_entropy": persistence_entropy(lifetimes),
    }


def _compute_development_fallback_features(
    points: np.ndarray,
    max_dimension: int,
    max_edge_length: float | None,
) -> list[dict[str, Any]]:
    """Return lightweight development diagnostics when ripser is unavailable."""
    threshold = 0.35 if max_edge_length is None else float(max_edge_length)
    if len(points) == 0:
        h0 = np.empty((0, 2), dtype=float)
    elif len(points) == 1:
        h0 = np.array([[0.0, np.inf]], dtype=float)
    else:
        distances = squareform(pdist(points))
        adjacency = distances <= threshold
        seen = np.zeros(len(points), dtype=bool)
        component_count = 0
        for start in range(len(points)):
            if seen[start]:
                continue
            component_count += 1
            stack = [start]
            seen[start] = True
            while stack:
                node = stack.pop()
                neighbors = np.flatnonzero(adjacency[node] & ~seen)
                seen[neighbors] = True
                stack.extend(neighbors.tolist())
        finite_components = max(component_count - 1, 0)
        h0 = np.vstack(
            [
                np.column_stack([np.zeros(finite_components), np.full(finite_components, threshold)]),
                np.array([[0.0, np.inf]]),
            ]
        )

    rows = [summarize_diagram(h0, 0, "fallback_threshold_graph")]
    if max_dimension >= 1:
        rows.append(summarize_diagram(np.empty((0, 2), dtype=float), 1, "fallback_threshold_graph"))
    return rows


def compute_ripser_features(
    points: np.ndarray,
    max_dimension: int = 1,
    max_edge_length: float | None = None,
) -> list[dict[str, Any]]:
    try:
        from ripser import ripser
    except ImportError:
        return _compute_development_fallback_features(points, max_dimension, max_edge_length)

    kwargs: dict[str, Any] = {"maxdim": max_dimension}
    if max_edge_length is not None:
        kwargs["thresh"] = max_edge_length

    result = ripser(points, **kwargs)
    diagrams = result["dgms"]
    return [summarize_diagram(diagram, dim, "ripser") for dim, diagram in enumerate(diagrams)]


def compute_cubical_features(image: np.ndarray) -> list[dict[str, Any]]:
    try:
        import gudhi as gd
    except ImportError as exc:
        raise RuntimeError("gudhi is required for cubical persistence computation.") from exc

    cubical = gd.CubicalComplex(top_dimensional_cells=image.astype(float))
    cubical.persistence()
    rows: list[dict[str, Any]] = []
    for dim in (0, 1):
        intervals = cubical.persistence_intervals_in_dimension(dim)
        if intervals.size == 0:
            diagram = np.empty((0, 2), dtype=float)
        else:
            diagram = np.asarray(intervals, dtype=float)
        rows.append(summarize_diagram(diagram, dim, "gudhi_cubical"))
    return rows
