"""Greedy minimum-Redundancy Maximum-Relevance selection using MID."""

from __future__ import annotations

from time import perf_counter

import numpy as np
from sklearn.metrics import mutual_info_score

from .base import BandSelectionResult, validate_inputs, validate_result


def discretize_equal_width(X_train: np.ndarray, bins: int = 16) -> np.ndarray:
    """Fit deterministic per-band equal-width bins on the provided training rows."""
    X, _, _ = validate_inputs(X_train, None, 1)
    if isinstance(bins, bool) or not isinstance(bins, (int, np.integer)):
        raise TypeError("bins must be an integer")
    bins = int(bins)
    if bins < 2:
        raise ValueError("bins must be at least 2")

    values = np.asarray(X, dtype=np.float64)
    discrete = np.zeros(values.shape, dtype=np.int64)
    for band_index in range(values.shape[1]):
        band = values[:, band_index]
        minimum = float(np.min(band))
        maximum = float(np.max(band))
        if minimum == maximum:
            continue
        edges = np.linspace(minimum, maximum, bins + 1, dtype=np.float64)
        discrete[:, band_index] = np.searchsorted(
            edges[1:-1], band, side="right"
        )
    return discrete


def compute_relevance(discrete_bands: np.ndarray, y_train: np.ndarray) -> np.ndarray:
    """Compute discrete mutual information between every band and the labels."""
    discrete = np.asarray(discrete_bands)
    y = np.asarray(y_train)
    if discrete.ndim != 2 or y.ndim != 1 or discrete.shape[0] != y.size:
        raise ValueError("discrete_bands and y_train must align by sample")
    scores = np.array(
        [mutual_info_score(discrete[:, index], y) for index in range(discrete.shape[1])],
        dtype=np.float64,
    )
    if not np.all(np.isfinite(scores)):
        raise ValueError("mRMR relevance produced NaN or Inf")
    return scores


def select_bands(
    X_train: np.ndarray,
    y_train: np.ndarray | None,
    k: int,
    config: dict | None = None,
) -> BandSelectionResult:
    """Greedily select k original bands with the classic mRMR-MID criterion."""
    start = perf_counter()
    X, y, k = validate_inputs(X_train, y_train, k)
    if y is None:
        raise ValueError("mRMR requires y_train")
    if np.unique(y).size < 2:
        raise ValueError("mRMR requires at least two training classes")
    options = {} if config is None else dict(config)
    bins = options.get("bins", 16)
    discrete = discretize_equal_width(X, bins=bins)
    relevance = compute_relevance(discrete, y)

    band_count = X.shape[1]
    selected: list[int] = []
    remaining = list(range(band_count))
    redundancy_sums = np.zeros(band_count, dtype=np.float64)
    pair_cache: dict[tuple[int, int], float] = {}
    selection_log: list[dict[str, object]] = []

    def pair_mutual_information(left: int, right: int) -> float:
        key = (left, right) if left < right else (right, left)
        if key not in pair_cache:
            pair_cache[key] = float(
                mutual_info_score(discrete[:, key[0]], discrete[:, key[1]])
            )
        return pair_cache[key]

    for round_index in range(k):
        selected_count = len(selected)
        candidates: list[dict[str, float | int]] = []
        candidate_scores = np.empty(len(remaining), dtype=np.float64)
        for position, band_index in enumerate(remaining):
            redundancy = (
                0.0
                if selected_count == 0
                else float(redundancy_sums[band_index] / selected_count)
            )
            score = float(relevance[band_index] - redundancy)
            candidate_scores[position] = score
            candidates.append(
                {
                    "band": int(band_index),
                    "relevance": float(relevance[band_index]),
                    "redundancy": redundancy,
                    "score": score,
                }
            )
        if not np.all(np.isfinite(candidate_scores)):
            raise ValueError("mRMR MID produced NaN or Inf scores")
        best_position = int(np.argmax(candidate_scores))
        chosen = int(remaining.pop(best_position))
        chosen_record = candidates[best_position]
        selected.append(chosen)
        selection_log.append(
            {
                "round": round_index + 1,
                "selected_band": chosen,
                "selected_relevance": chosen_record["relevance"],
                "selected_redundancy": chosen_record["redundancy"],
                "selected_score": chosen_record["score"],
                "candidates": candidates,
            }
        )
        if round_index + 1 < k:
            for band_index in remaining:
                redundancy_sums[band_index] += pair_mutual_information(
                    band_index, chosen
                )

    result = BandSelectionResult(
        indices=np.asarray(selected, dtype=np.int64),
        scores=relevance,
        metadata={
            "method": "mrmr",
            "version": "1.0",
            "criterion": "MID",
            "bins": int(bins),
            "discretization": "per_band_training_min_max_equal_width",
            "constant_band_bin": 0,
            "mutual_information": "sklearn.metrics.mutual_info_score",
            "log_base": "natural",
            "score_payload": "label_relevance_I(B_i;Y)",
            "tie_break": "original_index_ascending",
            "pairwise_cache_entries": len(pair_cache),
            "selection_log": selection_log,
            "selection_seconds": perf_counter() - start,
        },
    )
    return validate_result(result, band_count, k)
