import numpy as np
import pytest

from backend.demo_selector import build_synthetic_training_data
from backend.neurospec.baselines.fisher_bs import compute_fisher_scores
from backend.selector_registry import METHODS, select_bands


def test_fisher_ranks_the_separable_band_first():
    X = np.array([[0.0, 1.0], [0.1, 2.0], [4.0, 1.5], [4.1, 2.5]])
    y = np.array([0, 0, 1, 1])
    scores = compute_fisher_scores(X, y)
    assert int(np.argmax(scores)) == 0


@pytest.mark.parametrize("method", METHODS)
def test_each_public_method_returns_unique_valid_indices(method):
    X, y = build_synthetic_training_data()
    labels = y if method in {"fisher", "mrmr"} else None
    result = select_bands(method, X, labels, k=5)
    assert result.indices.shape == (5,)
    assert np.unique(result.indices).size == 5
    assert int(result.indices.min()) >= 0
    assert int(result.indices.max()) < X.shape[1]


def test_random_selector_is_reproducible():
    X, _ = build_synthetic_training_data()
    first = select_bands("random", X, None, 10, {"random_state": 42})
    second = select_bands("random", X, None, 10, {"random_state": 42})
    np.testing.assert_array_equal(first.indices, second.indices)

