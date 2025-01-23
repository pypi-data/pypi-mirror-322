import numpy as np
import warnings
from typing import Union, List, Tuple
from scipy import sparse

class DataValidator:
    def __init__(self):
        pass

    def check_device_cpu(self, device):
        if device not in {"cpu", None}:
            raise ValueError(f"Unsupported device: {device!r}. Only 'cpu' is supported.")

    def is_1d_array(self, array: Union[np.ndarray, list], warn: bool = False) -> np.ndarray:
        """
        Ensures input is a 1D array. Raises an error if it's not 1D or convertible to 1D.
        """
        array = np.asarray(array)
        shape = array.shape

        if len(shape) == 1:
            return array
        elif len(shape) == 2 and shape[1] == 1:
            if warn:
                warnings.warn("Input is 2D but will be converted to 1D.", UserWarning)
            return array.ravel()
        else:
            raise ValueError(f"Input must be 1D. Found shape {shape}.")

    def check_samples(self, array: Union[np.ndarray, list]) -> int:
        """
        Returns the number of samples in the array.
        """
        array = np.asarray(array)
        if hasattr(array, 'shape') and len(array.shape) > 0:
            return array.shape[0]
        else:
            raise TypeError("Input must be an array-like object with at least one dimension.")

    def check_consistent_length(self, *arrays: Union[np.ndarray, list]):
        """
        Ensures all input arrays have the same length.
        """
        lengths = [self.check_samples(arr) for arr in arrays]
        if len(set(lengths)) > 1:
            raise ValueError(f"Inconsistent lengths: {lengths}")

    def validate_regression_targets(self, y_true, y_pred, dtype=np.float64):
        """
        Ensures regression target values are consistent and converted to the specified dtype.
        """
        y_true = np.asarray(y_true, dtype=dtype)
        y_pred = np.asarray(y_pred, dtype=dtype)

        if y_true.shape != y_pred.shape:
            raise ValueError(f"Shapes of y_true {y_true.shape} and y_pred {y_pred.shape} do not match.")

        return y_true, y_pred

    def validate_segmentation_inputs(self, y_true, y_pred):
        """
        Ensures segmentation inputs are valid, checking dimensions and consistency.
        """
        y_true = np.asarray(y_true, dtype=np.int32)
        y_pred = np.asarray(y_pred, dtype=np.int32)

        if y_true.shape != y_pred.shape:
            raise ValueError(f"Shapes of y_true {y_true.shape} and y_pred {y_pred.shape} do not match.")

        if y_true.ndim < 2 or y_pred.ndim < 2:
            raise ValueError("Segmentation inputs must have at least two dimensions.")

        return y_true, y_pred

    def check_array(self, array, ensure_2d: bool = True, dtype=np.float64, allow_nan: bool = False):
        """
        Validates input array and converts it to specified dtype.
        """
        array = np.asarray(array, dtype=dtype)

        if ensure_2d and array.ndim == 1:
            array = array.reshape(-1, 1)

        if not allow_nan and np.isnan(array).any():
            raise ValueError("Input contains NaN values, which are not allowed.")

        return array

    def check_sparse(self, array, accept_sparse: Tuple[str] = ('csr', 'csc')):
        """
        Validates sparse matrices and converts to an acceptable format.
        """
        if sparse.issparse(array):
            if array.format not in accept_sparse:
                return array.asformat(accept_sparse[0])
            return array
        else:
            raise ValueError("Input is not a sparse matrix.")

    def validate_r2_score_inputs(self, y_true, y_pred, sample_weight=None):
        """
        Ensures inputs for R2 score computation are valid.
        """
        y_true, y_pred = self.validate_regression_targets(y_true, y_pred)
        if sample_weight is not None:
            sample_weight = self.is_1d_array(sample_weight)
        return y_true, y_pred, sample_weight

    def validate_mae_mse_inputs(self, y_true, y_pred, library=None):
        """
        Ensures inputs for MAE and MSE computation are valid.
        """
        y_true, y_pred = self.validate_regression_targets(y_true, y_pred)
        if library not in {None, 'sklearn', 'torch', 'tensorflow', 'Moral88'}:
            raise ValueError(f"Invalid library: {library}. Choose from {{'Moral88', 'sklearn', 'torch', 'tensorflow'}}.")
        return y_true, y_pred
