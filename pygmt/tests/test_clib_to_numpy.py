"""
Tests for the _to_numpy function in the clib.conversion module.
"""

import sys

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from packaging.version import Version
from pygmt.clib.conversion import _to_numpy

try:
    import pyarrow as pa

    _HAS_PYARROW = True
except ImportError:
    _HAS_PYARROW = False


def _check_result(result, expected_dtype):
    """
    A helper function to check if the result of the _to_numpy function is a C-contiguous
    NumPy array with the expected dtype.
    """
    assert isinstance(result, np.ndarray)
    assert result.flags.c_contiguous
    assert result.dtype.type == expected_dtype


########################################################################################
# Test the _to_numpy function with Python built-in types.
########################################################################################
@pytest.mark.parametrize(
    ("data", "expected_dtype"),
    [
        pytest.param(
            [1, 2, 3],
            np.int32
            if sys.platform == "win32" and Version(np.__version__) < Version("2.0")
            else np.int64,
            id="int",
        ),
        pytest.param([1.0, 2.0, 3.0], np.float64, id="float"),
        pytest.param(
            [complex(+1), complex(-2j), complex("-Infinity+NaNj")],
            np.complex128,
            id="complex",
        ),
    ],
)
def test_to_numpy_python_types_numeric(data, expected_dtype):
    """
    Test the _to_numpy function with Python built-in numeric types.
    """
    result = _to_numpy(data)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, data)


########################################################################################
# Test the _to_numpy function with NumPy arrays.
#
# There are 24 fundamental dtypes in NumPy. Not all of them are supported by PyGMT.
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
#
# Reference: https://numpy.org/doc/2.1/reference/arrays.scalars.html
########################################################################################
np_dtype_params = [
    pytest.param(np.int8, np.int8, id="int8"),
    pytest.param(np.int16, np.int16, id="int16"),
    pytest.param(np.int32, np.int32, id="int32"),
    pytest.param(np.int64, np.int64, id="int64"),
    pytest.param(np.longlong, np.longlong, id="longlong"),
    pytest.param(np.uint8, np.uint8, id="uint8"),
    pytest.param(np.uint16, np.uint16, id="uint16"),
    pytest.param(np.uint32, np.uint32, id="uint32"),
    pytest.param(np.uint64, np.uint64, id="uint64"),
    pytest.param(np.ulonglong, np.ulonglong, id="ulonglong"),
    pytest.param(np.float16, np.float16, id="float16"),
    pytest.param(np.float32, np.float32, id="float32"),
    pytest.param(np.float64, np.float64, id="float64"),
    pytest.param(np.longdouble, np.longdouble, id="longdouble"),
    pytest.param(np.complex64, np.complex64, id="complex64"),
    pytest.param(np.complex128, np.complex128, id="complex128"),
    pytest.param(np.clongdouble, np.clongdouble, id="clongdouble"),
]


@pytest.mark.parametrize(("dtype", "expected_dtype"), np_dtype_params)
def test_to_numpy_ndarray_numpy_dtypes_numeric(dtype, expected_dtype):
    """
    Test the _to_numpy function with NumPy arrays of NumPy numeric dtypes.

    Test both 1-D and 2-D arrays which are not C-contiguous.
    """
    # 1-D array that is not C-contiguous
    array = np.array([1, 2, 3, 4, 5, 6], dtype=dtype)[::2]
    assert array.flags.c_contiguous is False
    result = _to_numpy(array)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, array, strict=True)

    # 2-D array that is not C-contiguous
    array = np.array([[1, 2, 3, 4], [5, 6, 7, 8]], dtype=dtype)[::2, ::2]
    assert array.flags.c_contiguous is False
    result = _to_numpy(array)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, array, strict=True)


########################################################################################
# Test the _to_numpy function with pandas.Series.
#
# In pandas, dtype can be specified by
#
# 1. NumPy dtypes (see above)
# 2. pandas dtypes
# 3. PyArrow dtypes
#
# pandas provides following dtypes:
#
# - Numeric dtypes:
#   - Int8, Int16, Int32, Int64
#   - UInt8, UInt16, UInt32, UInt64
#   - Float32, Float64
# - DatetimeTZDtype
# - PeriodDtype
# - IntervalDtype
# - StringDtype
# - CategoricalDtype
# - SparseDtype
# - BooleanDtype
# - ArrowDtype: a special dtype used to store data in the PyArrow format.
#
# References:
# 1. https://pandas.pydata.org/docs/reference/arrays.html
# 2. https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes
# 3. https://pandas.pydata.org/docs/user_guide/pyarrow.html
########################################################################################
@pytest.mark.parametrize(("dtype", "expected_dtype"), np_dtype_params)
def test_to_numpy_pandas_series_numpy_dtypes_numeric(dtype, expected_dtype):
    """
    Test the _to_numpy function with pandas.Series of NumPy numeric dtypes.
    """
    series = pd.Series([1, 2, 3, 4, 5, 6], dtype=dtype)[::2]  # Not C-contiguous
    result = _to_numpy(series)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, series)


########################################################################################
# Test the _to_numpy function with PyArrow arrays.
#
# PyArrow provides the following dtypes:
#
# - Numeric dtypes:
#   - int8, int16, int32, int64
#   - uint8, uint16, uint32, uint64
#   - float16, float32, float64
#
# In PyArrow, array types can be specified in two ways:
#
# - Using string aliases (e.g., "int8")
# - Using pyarrow.DataType (e.g., ``pa.int8()``)
#
# Reference: https://arrow.apache.org/docs/python/api/datatypes.html
########################################################################################
@pytest.mark.skipif(not _HAS_PYARROW, reason="pyarrow is not installed")
@pytest.mark.parametrize(
    ("dtype", "expected_dtype"),
    [
        pytest.param("int8", np.int8, id="int8"),
        pytest.param("int16", np.int16, id="int16"),
        pytest.param("int32", np.int32, id="int32"),
        pytest.param("int64", np.int64, id="int64"),
        pytest.param("uint8", np.uint8, id="uint8"),
        pytest.param("uint16", np.uint16, id="uint16"),
        pytest.param("uint32", np.uint32, id="uint32"),
        pytest.param("uint64", np.uint64, id="uint64"),
        pytest.param("float16", np.float16, id="float16"),
        pytest.param("float32", np.float32, id="float32"),
        pytest.param("float64", np.float64, id="float64"),
    ],
)
def test_to_numpy_pyarrow_array_pyarrow_dtypes_numeric(dtype, expected_dtype):
    """
    Test the _to_numpy function with PyArrow arrays of PyArrow numeric dtypes.
    """
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    if dtype == "float16":  # float16 needs special handling
        # Example from https://arrow.apache.org/docs/python/generated/pyarrow.float16.html
        data = np.array(data, dtype=np.float16)
    array = pa.array(data, type=dtype)[::2]
    result = _to_numpy(array)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, array)


@pytest.mark.skipif(not _HAS_PYARROW, reason="pyarrow is not installed")
@pytest.mark.parametrize(
    ("dtype", "expected_dtype"),
    [
        pytest.param("int8", np.float64, id="int8"),
        pytest.param("int16", np.float64, id="int16"),
        pytest.param("int32", np.float64, id="int32"),
        pytest.param("int64", np.float64, id="int64"),
        pytest.param("uint8", np.float64, id="uint8"),
        pytest.param("uint16", np.float64, id="uint16"),
        pytest.param("uint32", np.float64, id="uint32"),
        pytest.param("uint64", np.float64, id="uint64"),
        pytest.param("float16", np.float16, id="float16"),
        pytest.param("float32", np.float32, id="float32"),
        pytest.param("float64", np.float64, id="float64"),
    ],
)
def test_to_numpy_pyarrow_array_pyarrow_dtypes_numeric_with_na(dtype, expected_dtype):
    """
    Test the _to_numpy function with PyArrow arrays of PyArrow numeric dtypes and NA.
    """
    data = [1.0, 2.0, None, 4.0, 5.0, 6.0]
    if dtype == "float16":  # float16 needs special handling
        # Example from https://arrow.apache.org/docs/python/generated/pyarrow.float16.html
        data = np.array(data, dtype=np.float16)
    array = pa.array(data, type=dtype)[::2]
    result = _to_numpy(array)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, array)
