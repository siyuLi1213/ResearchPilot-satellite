"""Maximum-variance PCA band prioritization from Chang et al. (1999)."""

from __future__ import annotations

from time import perf_counter

import numpy as np

from .base import BandSelectionResult, validate_inputs, validate_result


def compute_mvpca_scores(
    X_train: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    """Return paper-defined band powers, descending eigenvalues, and tolerance.

    Chang et al. define the loading factor for component ``i`` and original
    band ``l`` as ``sqrt(lambda_i) * v_il``.  Summing its square over all
    components gives the MVPCA priority ``p_l``, equal to that band's variance.
    """
    X, _, _ = validate_inputs(X_train, None, 1)
    values = np.asarray(X, dtype=np.float64)
    centered = values - np.mean(values, axis=0, dtype=np.float64)
    covariance = (centered.T @ centered) / float(values.shape[0])
    covariance = (covariance + covariance.T) * 0.5

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(-eigenvalues, kind="stable")
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    scale = max(float(np.max(np.abs(eigenvalues))), 1.0)
    tolerance = np.finfo(np.float64).eps * max(values.shape[1], 1) * scale * 10.0
    if float(np.min(eigenvalues)) < -tolerance:
        raise ValueError("MVPCA covariance has a materially negative eigenvalue")
    nonnegative_eigenvalues = np.maximum(eigenvalues, 0.0)

    loading_factors = eigenvectors * np.sqrt(nonnegative_eigenvalues)[None, :]
    loading_scores = np.sum(np.square(loading_factors), axis=1, dtype=np.float64)
    scores = np.diag(covariance).copy()
    scores[np.ptp(values, axis=0) == 0.0] = 0.0
    if not np.all(np.isfinite(scores)):
        raise ValueError("MVPCA produced NaN or Inf scores")
    reconstruction_error = float(np.max(np.abs(loading_scores - scores)))
    return scores, nonnegative_eigenvalues, tolerance, reconstruction_error


def select_bands(
    X_train: np.ndarray,
    y_train: np.ndarray | None,
    k: int,
    config: dict | None = None,
) -> BandSelectionResult:
    """Select top-priority original bands using verified MVPCA equations (1)-(4)."""
    start = perf_counter()
    X, _, k = validate_inputs(X_train, None, k)
    options = {} if config is None else dict(config)
    if options:
        unknown = ", ".join(sorted(map(str, options)))
        raise ValueError(f"MVPCA has no configurable parameters; received: {unknown}")

    scores, eigenvalues, tolerance, reconstruction_error = compute_mvpca_scores(X)
    indices = np.argsort(-scores, kind="stable")[:k].astype(np.int64)
    result = BandSelectionResult(
        indices=indices,
        scores=scores,
        metadata={
            "method": "mvpca",
            "version": "1.0",
            "fidelity_status": "verified_original",
            "source": "Chang et al., IEEE TGRS 37(6), 1999",
            "doi": "10.1109/36.803411",
            "source_section": "II-A, equations (1)-(4)",
            "covariance_normalization": "1/N",
            "eigendecomposition": "numpy.linalg.eigh_real_symmetric",
            "eigenvalue_order": "descending",
            "eigenvalue_negative_tolerance": float(tolerance),
            "eigenvalues": eigenvalues.tolist(),
            "priority": "sum_i((sqrt(lambda_i)*v_il)^2)",
            "priority_equivalence": "original_band_population_variance",
            "priority_roundoff_canonicalization": "covariance_diagonal",
            "tie_break": "original_index_ascending",
            "output": "original_band_indices",
            "uses_labels": False,
            "divergence_decorrelation": "not_applied",
            "variance_reconstruction_max_abs_error": reconstruction_error,
            "selection_seconds": perf_counter() - start,
        },
    )
    return validate_result(result, X.shape[1], k)

