"""Seeded random band selection without replacement."""

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
    """Select k original bands using a reproducible sampling order."""
    start = perf_counter()
    X, _, k = validate_inputs(X_train, y_train, k)
    options = {} if config is None else dict(config)
    random_state = int(options.get("random_state", 42))
    indices = np.random.default_rng(random_state).choice(X.shape[1], size=k, replace=False)
    result = BandSelectionResult(
        indices=np.asarray(indices, dtype=np.int64),
        scores=None,
        metadata={
            "method": "random",
            "version": "1.0",
            "random_state": random_state,
            "sampling": "without_replacement",
            "rng_api": "numpy.random.default_rng(seed).choice",
            "selection_seconds": perf_counter() - start,
        },
    )
    return validate_result(result, X.shape[1], k)
