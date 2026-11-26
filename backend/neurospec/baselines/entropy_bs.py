"""Information Entropy (IE) single-band ranking."""

from __future__ import annotations

from time import perf_counter

import numpy as np

from .base import BandSelectionResult, validate_inputs, validate_result


def compute_entropy_scores(X_train: np.ndarray, bins: int = 64) -> np.ndarray:
    """Compute per-band Shannon entropy from independent finite-range histograms."""
    X, _, _ = validate_inputs(X_train, None, 1)
    if isinstance(bins, bool) or not isinstance(bins, (int, np.integer)) or int(bins) < 1:
        raise ValueError("bins must be a positive integer")
    bins = int(bins)
    scores = np.zeros(X.shape[1], dtype=np.float64)
    values = np.asarray(X, dtype=np.float64)
    for band_index in range(values.shape[1]):
        band = values[:, band_index]
        minimum = float(np.min(band))
        maximum = float(np.max(band))
        if minimum == maximum:
            continue
        counts, _ = np.histogram(band, bins=bins, range=(minimum, maximum))
        probabilities = counts[counts > 0].astype(np.float64) / band.size
        scores[band_index] = -np.sum(probabilities * np.log2(probabilities))
    if not np.all(np.isfinite(scores)):
        raise ValueError("Information entropy produced NaN or Inf scores")
    return scores


def select_bands(
    X_train: np.ndarray,
    y_train: np.ndarray | None,
    k: int,
    config: dict | None = None,
) -> BandSelectionResult:
    """Rank original bands by descending entropy with index-stable ties."""
    start = perf_counter()
    X, _, k = validate_inputs(X_train, y_train, k)
    options = {} if config is None else dict(config)
    bins = options.get("bins", 64)
    scores = compute_entropy_scores(X, bins=bins)
    indices = np.argsort(-scores, kind="stable")[:k].astype(np.int64)
    result = BandSelectionResult(
        indices=indices,
        scores=scores,
        metadata={
            "method": "ie",
            "version": "1.0",
            "bins": int(bins),
            "histogram_range": "per_band_training_min_max",
            "histogram_bins": "equal_width",
            "histogram_boundaries": "left_inclusive_right_exclusive_except_final_right_inclusive",
            "log_base": 2,
            "tie_break": "original_index_ascending",
            "selection_seconds": perf_counter() - start,
        },
    )
    return validate_result(result, X.shape[1], k)
