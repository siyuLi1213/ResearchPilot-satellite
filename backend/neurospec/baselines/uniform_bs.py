"""Deterministic uniformly spaced band selection."""

from __future__ import annotations

from time import perf_counter

import numpy as np

from .base import BandSelectionResult, validate_inputs, validate_result


def select_bands(
    X_train: np.ndarray,
    y_train: np.ndarray | None,
    k: int,
    config: dict | None = None,
) -> BandSelectionResult:
    """Select endpoint-inclusive, approximately uniform original indices."""
    start = perf_counter()
    X, _, k = validate_inputs(X_train, y_train, k)
    band_count = X.shape[1]
    if k == 1:
        indices = np.array([(band_count - 1) // 2], dtype=np.int64)
    elif k == band_count:
        indices = np.arange(band_count, dtype=np.int64)
    else:
        indices = np.rint(np.linspace(0, band_count - 1, num=k)).astype(np.int64)
    result = BandSelectionResult(
        indices=indices,
        scores=None,
        metadata={
            "method": "uniform",
            "version": "1.0",
            "rounding": "numpy.rint_nearest_even",
            "k1_policy": "lower_center",
            "selection_seconds": perf_counter() - start,
        },
    )
    return validate_result(result, band_count, k)
