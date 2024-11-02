"""
Test the _to_ndarray function in the clib.conversion module.
"""

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt.clib.conversion import _to_ndarray
from pygmt.helpers.testing import skip_if_no

try:
    import pyarrow as pa

    _HAS_PYARROW = True
except ImportError:
    _HAS_PYARROW = False

dtypes_numpy = [
    np.int8,
    np.int16,
    np.int32,
    np.int64,
    np.longlong,
    np.uint8,
    np.uint16,
    np.uint32,
    np.uint64,
    np.ulonglong,
    np.float16,
    np.float32,
    np.float64,
    np.longdouble,
    np.complex64,
    np.complex128,
    np.clongdouble,
]


def _check_result(result):
    """
    A helper function to check the result of the _to_ndarray function.

    Check the following:

    1. The result is a NumPy array.
    2. The result is C-contiguous.
    3. The result dtype is not np.object_.
    """
    assert isinstance(result, np.ndarray)
    assert result.flags.c_contiguous is True
    assert result.dtype != np.object_


@pytest.mark.parametrize("dtype", dtypes_numpy)
def test_to_ndarray_numpy_ndarray_numpy_numeric(dtype):
    """
    Test the _to_ndarray function with 1-D NumPy arrays.
    """
    # 1-D array
    array = np.array([1, 2, 3], dtype=dtype)
    assert array.dtype == dtype
    result = _to_ndarray(array)
    _check_result(result)
    npt.assert_array_equal(result, array)

    # 2-D array
    array = np.array([[1, 2, 3], [4, 5, 6]], dtype=dtype)
    assert array.dtype == dtype
    result = _to_ndarray(array)
    _check_result(result)
    npt.assert_array_equal(result, array)


@pytest.mark.parametrize(
    "dtype",
    [
        *dtypes_numpy,
        pytest.param(pd.Int8Dtype(), id="Int8"),
        pytest.param(pd.Int16Dtype(), id="Int16"),
        pytest.param(pd.Int32Dtype(), id="Int32"),
        pytest.param(pd.Int64Dtype(), id="Int64"),
        pytest.param(pd.UInt8Dtype(), id="UInt8"),
        pytest.param(pd.UInt16Dtype(), id="UInt16"),
        pytest.param(pd.UInt32Dtype(), id="UInt32"),
        pytest.param(pd.UInt64Dtype(), id="UInt64"),
        pytest.param(pd.Float32Dtype(), id="Float32"),
        pytest.param(pd.Float64Dtype(), id="Float64"),
        pytest.param("int8[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("int16[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("int32[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("int64[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("uint8[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("uint16[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("uint32[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("uint64[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("float32[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("float64[pyarrow]", marks=skip_if_no(package="pyarrow")),
    ],
)
def test_to_ndarray_pandas_series_numeric(dtype):
    """
    Test the _to_ndarray function with pandas Series with NumPy dtypes, pandas dtypes,
    and pandas dtypes with pyarrow backend.
    """
    series = pd.Series([1, 2, 3], dtype=dtype)
    assert series.dtype == dtype
    result = _to_ndarray(series)
    _check_result(result)
    npt.assert_array_equal(result, series)


@pytest.mark.parametrize(
    "dtype",
    [
        pytest.param(pd.Int8Dtype(), id="Int8"),
        pytest.param(pd.Int16Dtype(), id="Int16"),
        pytest.param(pd.Int32Dtype(), id="Int32"),
        pytest.param(pd.Int64Dtype(), id="Int64"),
        pytest.param(pd.UInt8Dtype(), id="UInt8"),
        pytest.param(pd.UInt16Dtype(), id="UInt16"),
        pytest.param(pd.UInt32Dtype(), id="UInt32"),
        pytest.param(pd.UInt64Dtype(), id="UInt64"),
        pytest.param(pd.Float32Dtype(), id="Float32"),
        pytest.param(pd.Float64Dtype(), id="Float64"),
        pytest.param("int8[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("int16[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("int32[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("int64[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("uint8[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("uint16[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("uint32[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("uint64[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("float32[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param("float64[pyarrow]", marks=skip_if_no(package="pyarrow")),
    ],
)
def test_to_ndarray_pandas_series_numeric_with_na(dtype):
    """
    Test the _to_ndarray function with pandas Series with NumPy dtypes and pandas NA.
    """
    series = pd.Series([1, pd.NA, 3], dtype=dtype)
    assert series.dtype == dtype
    result = _to_ndarray(series)
    _check_result(result)
    npt.assert_array_equal(result, np.array([1, np.nan, 3], dtype=np.float64))


@pytest.mark.skipif(not _HAS_PYARROW, reason="pyarrow is not installed")
@pytest.mark.parametrize(
    "dtype",
    [
        "int8",
        "int16",
        "int32",
        "int64",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "float32",
        "float64",
    ],
)
def test_to_ndarray_pyarrow_array(dtype):
    """
    Test the _to_ndarray function with pandas Series with pyarrow dtypes.
    """
    array = pa.array([1, 2, 3], type=dtype)
    assert array.type == dtype
    result = _to_ndarray(array)
    _check_result(result)
    npt.assert_array_equal(result, array)


@pytest.mark.skipif(not _HAS_PYARROW, reason="pyarrow is not installed")
def test_to_ndarray_pyarrow_array_float16():
    """
    Test the _to_ndarray function with pyarrow float16 array.

    Example from https://arrow.apache.org/docs/python/generated/pyarrow.float16.html
    """
    array = pa.array(np.array([1.5, 2.5, 3.5], dtype=np.float16), type=pa.float16())
    result = _to_ndarray(array)
    _check_result(result)
    npt.assert_array_equal(result, array)
