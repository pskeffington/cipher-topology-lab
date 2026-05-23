from __future__ import annotations

import math

import numpy as np


def bytes_to_uint8_array(data: bytes) -> np.ndarray:
    return np.frombuffer(data, dtype=np.uint8)


def byte_pair_embedding(data: bytes, sample_points: int | None = None) -> np.ndarray:
    arr = bytes_to_uint8_array(data)
    n = (len(arr) // 2) * 2
    pts = arr[:n].reshape(-1, 2).astype(float) / 255.0
    if sample_points is not None:
        pts = pts[:sample_points]
    return pts


def sliding_window_embedding(
    data: bytes,
    dimension: int = 8,
    stride: int = 1,
    sample_points: int | None = None,
) -> np.ndarray:
    arr = bytes_to_uint8_array(data).astype(float) / 255.0
    if len(arr) < dimension:
        raise ValueError("Data length is shorter than embedding dimension.")
    starts = np.arange(0, len(arr) - dimension + 1, stride)
    if sample_points is not None:
        starts = starts[:sample_points]
    return np.vstack([arr[i : i + dimension] for i in starts])


def cubical_image_embedding(data: bytes, side: int | None = None) -> np.ndarray:
    arr = bytes_to_uint8_array(data).astype(float) / 255.0
    if side is None:
        side = int(math.floor(math.sqrt(len(arr))))
    if side <= 1:
        raise ValueError("Cubical image side length must exceed 1.")
    n = side * side
    if len(arr) < n:
        raise ValueError("Data length is too short for requested cubical image side length.")
    return arr[:n].reshape(side, side)


def make_embedding(data: bytes, name: str, dimension: int, stride: int, sample_points: int):
    if name == "byte_pair_2d":
        return byte_pair_embedding(data, sample_points=sample_points)
    if name == "sliding_window_8d":
        return sliding_window_embedding(data, dimension=dimension, stride=stride, sample_points=sample_points)
    if name == "cubical_image_2d":
        return cubical_image_embedding(data, side=dimension)
    raise ValueError(f"Unknown embedding: {name}")
