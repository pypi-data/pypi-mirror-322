import pytest
import numpy as np
from Moral88.regression import (
                                mean_absolute_error,
                                mean_absolute_error,
                                mean_squared_error,
                                r2_score,
                                mean_bias_deviation,
                                adjusted_r2_score,
                                root_mean_squared_error,
                                mean_absolute_percentage_error,
                                explained_variance_score
)
import warnings
from Moral88.utils import DataValidator

validator = DataValidator()

def test_is_1d_array():
    validator = DataValidator()
    array = [[1], [2], [3]]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        result = validator.is_1d_array(array, warn=True)
    assert result.ndim == 1
    assert np.array_equal(result, np.array([1, 2, 3]))

def test_check_samples():
    validator = DataValidator()
    array = [[1, 2], [3, 4], [5, 6]]
    result = validator.check_samples(array)
    assert result == 3

def test_check_consistent_length():
    validator = DataValidator()
    array1 = [1, 2, 3]
    array2 = [4, 5, 6]
    validator.check_consistent_length(array1, array2)  # Should not raise an error

    array3 = [7, 8]
    with pytest.raises(ValueError):
        validator.check_consistent_length(array1, array3)

def test_mean_absolute_error():

    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = mean_absolute_error(y_true, y_pred)
    assert result == pytest.approx(0.5, rel=1e-2)

def test_mean_squared_error():

    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = mean_squared_error(y_true, y_pred)
    assert result == pytest.approx(0.375, rel=1e-2)

def test_r2_score():

    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = r2_score(y_true, y_pred)
    assert result == pytest.approx(0.948, rel=1e-2)

def test_mean_bias_deviation():

    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = mean_bias_deviation(y_true, y_pred)
    assert result == pytest.approx(0.25, rel=1e-2)

def test_explained_variance_score():

    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = explained_variance_score(y_true, y_pred)
    assert result == pytest.approx(0.957, rel=1e-2)

def test_mean_absolute_percentage_error():
 
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = mean_absolute_percentage_error(y_true, y_pred)
    assert result == pytest.approx(32.738095, rel=1e-2)

def test_root_mean_squared_error():

    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    result = root_mean_squared_error(y_true, y_pred)
    assert result == pytest.approx(0.612, rel=1e-2)

def test_adjusted_r2_score():

    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    n_features = 2
    result = adjusted_r2_score(y_true, y_pred, n_features)
    assert result == pytest.approx(0.8458, rel=1e-2)

