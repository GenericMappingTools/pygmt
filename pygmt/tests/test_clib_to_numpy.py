"""
Tests for the _to_numpy function in the clib.conversion module.
"""

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt.clib.conversion import _to_numpy
from pygmt.clib.session import DTYPES


def _check_result(result, supported):
    """
    Check the result of the _to_numpy function.
    """
    # Check that the result is a NumPy array and is C-contiguous.
    assert isinstance(result, np.ndarray)
    assert result.flags.c_contiguous
    # Check that the dtype is supported by PyGMT (or the GMT C API).
    assert (result.dtype.type in DTYPES) == supported


########################################################################################
# Test the _to_numpy function with NumPy arrays.
#
# There are 24 fundamental dtypes in NumPy. Not all of them are supported by PyGMT.
# Reference: https://numpy.org/doc/2.1/reference/arrays.scalars.html
#
# - Numeric dtypes:
#   - int8, int16, int32, int64, longlong
#   - uint8, uint16, uint32, uint64, ulonglong
#   - float16, float32, float64, longdouble
#   - complex64, complex128, clongdouble
# - bool
# - datetime64, timedelta64
# - str_
# - bytes_
# - object_
# - void
########################################################################################
@pytest.mark.parametrize(
    ("dtype", "supported"),
    [
        (np.int8, True),
        (np.int16, True),
        (np.int32, True),
        (np.int64, True),
        (np.longlong, True),
        (np.uint8, True),
        (np.uint16, True),
        (np.uint32, True),
        (np.uint64, True),
        (np.ulonglong, True),
        (np.float16, False),
        (np.float32, True),
        (np.float64, True),
        (np.longdouble, False),
        (np.complex64, False),
        (np.complex128, False),
        (np.clongdouble, False),
    ],
)
def test_to_numpy_ndarray_numpy_dtypes_numeric(dtype, supported):
    """
    Test the _to_numpy function with NumPy arrays of NumPy numeric dtypes.

    "dtype" is the NumPy dtype to be tested and "supported" is a boolean value
    indicating whether the dtype is supported by PyGMT (or the GMT C API).
    """
    # 1-D array
    array = np.array([1, 2, 3], dtype=dtype)
    assert array.dtype == dtype
    result = _to_numpy(array)
    _check_result(result, supported)
    npt.assert_array_equal(result, array)

    # 2-D array
    array = np.array([[1, 2, 3], [4, 5, 6]], dtype=dtype)
    assert array.dtype == dtype
    result = _to_numpy(array)
    _check_result(result, supported)
    npt.assert_array_equal(result, array)


########################################################################################
# Test the _to_numpy function with pandas.Series.
#
# In pandas, dtype can be specified by
#
# 1. NumPy dtypes (see above)
# 2. pandas dtypes
# 3. PyArrow dtypes
#
# Reference: https://pandas.pydata.org/docs/reference/arrays.html
########################################################################################
@pytest.mark.parametrize(
    ("dtype", "supported"),
    [
        (np.int8, True),
        (np.int16, True),
        (np.int32, True),
        (np.int64, True),
        (np.longlong, True),
        (np.uint8, True),
        (np.uint16, True),
        (np.uint32, True),
        (np.uint64, True),
        (np.ulonglong, True),
        (np.float16, False),
        (np.float32, True),
        (np.float64, True),
        (np.longdouble, False),
        (np.complex64, False),
        (np.complex128, False),
        (np.clongdouble, False),
    ],
)
def test_to_numpy_pandas_series_numpy_dtypes_numeric(dtype, supported):
    """
    Test the _to_numpy function with pandas.Series of NumPy numeric dtypes.
    """
    series = pd.Series([1, 2, 3], dtype=dtype)
    assert series.dtype == dtype
    result = _to_numpy(series)
    _check_result(result, supported)
    npt.assert_array_equal(result, series)
