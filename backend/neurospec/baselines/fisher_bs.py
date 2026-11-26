"""Multiclass Fisher Score band ranking."""

from __future__ import annotations

from time import perf_counter

import numpy as np

from .base import BandSelectionResult, validate_inputs, validate_result


def compute_fisher_scores(
    X_train: np.ndarray,
    y_train: np.ndarray,
    epsilon: float = 1e-12,
) -> np.ndarray:
    """Compute between-class scatter divided by pooled within-class scatter."""
    X, y, _ = validate_inputs(X_train, y_train, 1)
    if y is None:
        raise ValueError("Fisher Score requires y_train")
    if isinstance(epsilon, bool) or not np.isscalar(epsilon):
        raise TypeError("epsilon must be a positive finite scalar")
    epsilon = float(epsilon)
    if not np.isfinite(epsilon) or epsilon <= 0.0:
        raise ValueError("epsilon must be a positive finite scalar")

    classes = np.unique(y)
    if classes.size < 2:
        raise ValueError("Fisher Score requires at least two training classes")

    values = np.asarray(X, dtype=np.float64)
    overall_mean = np.mean(values, axis=0, dtype=np.float64)
    between = np.zeros(values.shape[1], dtype=np.float64)
    within = np.zeros(values.shape[1], dtype=np.float64)
    for label in classes:
        class_values = values[y == label]
        class_mean = np.mean(class_values, axis=0, dtype=np.float64)
        between += class_values.shape[0] * np.square(class_mean - overall_mean)
        within += np.sum(np.square(class_values - class_mean), axis=0, dtype=np.float64)

    scores = between / (within + epsilon)
    constant_bands = np.ptp(values, axis=0) == 0.0
    scores[constant_bands] = 0.0
    if not np.all(np.isfinite(scores)):
        raise ValueError("Fisher Score produced NaN or Inf scores")
    return scores


def select_bands(
    X_train: np.ndarray,
    y_train: np.ndarray | None,
    k: int,
    config: dict | None = None,
) -> BandSelectionResult:
    """Select original bands by descending Fisher Score and stable index ties."""
    start = perf_counter()
    X, y, k = validate_inputs(X_train, y_train, k)
    if y is None:
        raise ValueError("Fisher Score requires y_train")
    options = {} if config is None else dict(config)
    epsilon = options.get("epsilon", 1e-12)
    scores = compute_fisher_scores(X, y, epsilon=epsilon)
    indices = np.argsort(-scores, kind="stable")[:k].astype(np.int64)
    result = BandSelectionResult(
        indices=indices,
        scores=scores,
        metadata={
            "method": "fisher",
            "version": "1.0",
            "epsilon": float(epsilon),
            "score": "multiclass_between_scatter_over_pooled_within_scatter",
            "tie_break": "original_index_ascending",
            "redundancy_filter": "none",
            "selection_seconds": perf_counter() - start,
        },
    )
    return validate_result(result, X.shape[1], k)
