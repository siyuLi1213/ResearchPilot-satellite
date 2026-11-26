"""Synthetic-data adapter for demonstrating the real selector implementations."""

from __future__ import annotations

import numpy as np

from .selector_registry import select_bands
from .schemas import BandSelectionRequest, BandSelectionResponse


def build_synthetic_training_data() -> tuple[np.ndarray, np.ndarray]:
    """Create deterministic labeled data with 103 bands and no research samples."""
    rng = np.random.default_rng(2026)
    y_train = np.repeat(np.arange(3, dtype=np.int64), 30)
    X_train = rng.normal(size=(y_train.size, 103))
    for class_id, band in enumerate((7, 31, 76)):
        X_train[y_train == class_id, band] += 4.0
    return X_train, y_train


def run_demo_selection(request: BandSelectionRequest) -> BandSelectionResponse:
    X_train, y_train = build_synthetic_training_data()
    labels = y_train if request.method in {"fisher", "mrmr"} else None
    result = select_bands(request.method, X_train, labels, request.k)
    return BandSelectionResponse(
        method=request.method,
        k=request.k,
        selected_bands=result.indices.tolist(),
        note=(
            "The selector implementation is real, but it ran on deterministic synthetic "
            "data. This response is not a PaviaU experiment result."
        ),
    )

