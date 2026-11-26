"""Public API adapter around the unmodified research baseline modules."""

from __future__ import annotations

import numpy as np

from .neurospec.baselines.base import BandSelectionResult

METHODS = ("fisher", "mrmr", "mvpca", "ie", "random", "uniform")


def select_bands(
    method: str,
    X_train: np.ndarray,
    y_train: np.ndarray | None,
    k: int,
    config: dict | None = None,
) -> BandSelectionResult:
    if method == "fisher":
        from .neurospec.baselines.fisher_bs import select_bands as selector
    elif method == "mrmr":
        from .neurospec.baselines.mrmr_bs import select_bands as selector
    elif method == "mvpca":
        from .neurospec.baselines.mvpca_bs import select_bands as selector
    elif method == "ie":
        from .neurospec.baselines.entropy_bs import select_bands as selector
    elif method == "random":
        from .neurospec.baselines.random_bs import select_bands as selector
    elif method == "uniform":
        from .neurospec.baselines.uniform_bs import select_bands as selector
    else:
        raise ValueError(f"Unsupported band-selection method: {method!r}")
    return selector(X_train, y_train, k, config)

