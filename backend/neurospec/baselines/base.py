"""Shared contracts and validation for band-selection algorithms."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class BandSelectionResult:
    """Selected original band indices, optional candidate scores, and diagnostics."""

    indices: np.ndarray
    scores: np.ndarray | None
    metadata: dict[str, Any]


def validate_inputs(
    X_train: np.ndarray,
    y_train: np.ndarray | None,
    k: int,
) -> tuple[np.ndarray, np.ndarray | None, int]:
    """Validate common selector inputs without fitting or transforming them."""
    X = np.asarray(X_train)
    if X.ndim != 2 or X.shape[0] == 0 or X.shape[1] == 0:
        raise ValueError("X_train must be a nonempty two-dimensional matrix")
    if not np.issubdtype(X.dtype, np.number) or not np.all(np.isfinite(X)):
        raise ValueError("X_train must contain only finite numeric values")
    if isinstance(k, bool) or not isinstance(k, (int, np.integer)):
        raise TypeError("k must be an integer")
    k = int(k)
    if k < 1 or k > X.shape[1]:
        raise ValueError(f"k must satisfy 1 <= k <= {X.shape[1]}")
    if y_train is None:
        y = None
    else:
        y = np.asarray(y_train)
        if y.ndim != 1 or y.size != X.shape[0]:
            raise ValueError("y_train must be one-dimensional and align with X_train")
        if not np.issubdtype(y.dtype, np.number) or not np.all(np.isfinite(y)):
            raise ValueError("y_train must contain only finite numeric values")
    return X, y, k


def validate_result(
    result: BandSelectionResult,
    band_count: int,
    k: int,
) -> BandSelectionResult:
    """Enforce the shared zero-based, unique, finite result contract."""
    if not isinstance(result, BandSelectionResult):
        raise TypeError("Selector must return BandSelectionResult")
    indices = np.asarray(result.indices)
    if indices.ndim != 1 or indices.size != k or not np.issubdtype(indices.dtype, np.integer):
        raise ValueError("Selected indices must be a one-dimensional integer array of length k")
    indices = indices.astype(np.int64, copy=False)
    if np.unique(indices).size != k or indices.min() < 0 or indices.max() >= band_count:
        raise ValueError("Selected indices must be unique and within the original band range")
    scores = result.scores
    if scores is not None:
        scores = np.asarray(scores, dtype=np.float64)
        if scores.shape != (band_count,) or not np.all(np.isfinite(scores)):
            raise ValueError("Candidate scores must be a finite length-B vector")
    if not isinstance(result.metadata, dict):
        raise TypeError("metadata must be a dictionary")
    return BandSelectionResult(indices=indices, scores=scores, metadata=dict(result.metadata))
