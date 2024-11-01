"""
Test the _to_ndarray function in the clib.conversion module.
"""

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from pygmt.clib.conversion import _to_ndarray

try:
    import pyarrow as pa

    _HAS_PYARROW = True
except ImportError:
    _HAS_PYARROW = False


@pytest.fixture(scope="module", name="dtypes_numpy_numeric")
def fixture_dtypes_numpy_numeric():
    """
    List of NumPy numeric dtypes.

    Reference: https://numpy.org/doc/stable/reference/arrays.scalars.html
    """
    return [
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


@pytest.fixture(scope="module", name="dtypes_pandas_numeric")
def fixture_dtypes_pandas_numeric():
    """
    List of pandas numeric dtypes.

    Reference: https://pandas.pydata.org/docs/reference/arrays.html
    """
    return [
        pd.Int8Dtype(),
        pd.Int16Dtype(),
        pd.Int32Dtype(),
        pd.Int64Dtype(),
        pd.UInt8Dtype(),
        pd.UInt16Dtype(),
        pd.UInt32Dtype(),
        pd.UInt64Dtype(),
        pd.Float32Dtype(),
        pd.Float64Dtype(),
    ]


@pytest.fixture(scope="module", name="dtypes_pandas_numeric_pyarrow_backend")
def fixture_dtypes_pandas_numeric_pyarrow_backend():
    """
    List of pandas dtypes that use pyarrow as the backend.

    Reference: https://pandas.pydata.org/docs/user_guide/pyarrow.html
    """
    return [
        "int8[pyarrow]",
        "int16[pyarrow]",
        "int32[pyarrow]",
        "int64[pyarrow]",
        "uint8[pyarrow]",
        "uint16[pyarrow]",
        "uint32[pyarrow]",
        "uint64[pyarrow]",
        "float32[pyarrow]",
        "float64[pyarrow]",
    ]


@pytest.fixture(scope="module", name="dtypes_pyarrow_numeric")
def fixture_dtypes_pyarrow_numeric():
    """
    List of pyarrow numeric dtypes.

    Reference: https://arrow.apache.org/docs/python/api/datatypes.html
    """
    if not _HAS_PYARROW:
        return []
    return [
        pa.int8(),
        pa.int16(),
        pa.int32(),
        pa.int64(),
        pa.uint8(),
        pa.uint16(),
        pa.uint32(),
        pa.uint64(),
        # pa.float16(), # Need special handling.
        pa.float32(),
        pa.float64(),
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


def test_to_ndarray_numpy_ndarray_numpy_numeric(dtypes_numpy_numeric):
    """
    Test the _to_ndarray function with 1-D NumPy arrays.
    """
    # 1-D array
    for dtype in dtypes_numpy_numeric:
        array = np.array([1, 2, 3], dtype=dtype)
        assert array.dtype == dtype
        result = _to_ndarray(array)
        _check_result(result)
        npt.assert_array_equal(result, array)

    # 2-D array
    for dtype in dtypes_numpy_numeric:
        array = np.array([[1, 2, 3], [4, 5, 6]], dtype=dtype)
        assert array.dtype == dtype
        result = _to_ndarray(array)
        _check_result(result)
        npt.assert_array_equal(result, array)


def test_to_ndarray_pandas_series_numeric(
    dtypes_numpy_numeric, dtypes_pandas_numeric, dtypes_pandas_numeric_pyarrow_backend
):
    """
    Test the _to_ndarray function with pandas Series with NumPy dtypes, pandas dtypes,
    and pandas dtypes with pyarrow backend.
    """
    for dtype in (
        dtypes_numpy_numeric
        + dtypes_pandas_numeric
        + dtypes_pandas_numeric_pyarrow_backend
    ):
        series = pd.Series([1, 2, 3], dtype=dtype)
        assert series.dtype == dtype
        result = _to_ndarray(series)
        _check_result(result)
        npt.assert_array_equal(result, series)


@pytest.mark.skipif(not _HAS_PYARROW, reason="pyarrow is not installed")
def test_to_ndarray_pandas_series_pyarrow_dtype(dtypes_pyarrow_numeric):
    """
    Test the _to_ndarray function with pandas Series with pyarrow dtypes.
    """
    for dtype in dtypes_pyarrow_numeric:
        array = pa.array([1, 2, 3], type=dtype)
        assert array.type == dtype
        result = _to_ndarray(array)
        _check_result(result)
        npt.assert_array_equal(result, array)

    # Special handling for float16.
    # Example from https://arrow.apache.org/docs/python/generated/pyarrow.float16.html
    array = pa.array(np.array([1.5, 2.5, 3.5], dtype=np.float16), type=pa.float16())
    result = _to_ndarray(array)
    _check_result(result)
    npt.assert_array_equal(result, array)
