"""
Tests for the _to_numpy function in the clib.conversion module.
"""

import sys
from datetime import date, datetime

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
from packaging.version import Version
from pygmt.clib.conversion import _to_numpy
from pygmt.helpers.testing import skip_if_no

try:
    import pyarrow as pa

    _HAS_PYARROW = True
except ImportError:

    class pa:  # noqa: N801
        """
        A dummy class to mimic pyarrow.
        """

        __version__ = "0.0.0"

        @staticmethod
        def timestamp(unit: str, tz: str | None = None):
            """
            A dummy function to mimic pyarrow.timestamp.
            """

    _HAS_PYARROW = False

# Mark tests that require pyarrow
pa_marks = {"marks": skip_if_no(package="pyarrow")}


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
        # TODO(NumPy>=2.0): Remove the if-else statement after NumPy>=2.0.
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
        pytest.param(["abc", "defg", "12345"], np.str_, id="string"),
    ],
)
def test_to_numpy_python_types(data, expected_dtype):
    """
    Test the _to_numpy function with Python built-in types.
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
def test_to_numpy_numpy_numeric(dtype, expected_dtype):
    """
    Test the _to_numpy function with NumPy arrays of numeric dtypes.

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


@pytest.mark.parametrize("dtype", [None, np.str_, "U10"])
def test_to_numpy_numpy_string(dtype):
    """
    Test the _to_numpy function with NumPy arrays of string dtypes.
    """
    array = np.array(["abc", "defg", "12345"], dtype=dtype)
    result = _to_numpy(array)
    _check_result(result, np.str_)
    npt.assert_array_equal(result, array)


########################################################################################
# Test the _to_numpy function with pandas.Series.
#
# In pandas, dtype can be specified by
#
# 1. NumPy dtypes (see above)
# 2. pandas dtypes
# 3. PyArrow types (see below)
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
# In pandas, PyArrow types can be specified using the following formats:
#
# - Prefixed with the name of the dtype and "[pyarrow]" (e.g., "int8[pyarrow]")
# - Specified using ``ArrowDType`` (e.g., "pd.ArrowDtype(pa.int8())")
#
# References:
# 1. https://pandas.pydata.org/docs/reference/arrays.html
# 2. https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes
# 3. https://pandas.pydata.org/docs/user_guide/pyarrow.html
########################################################################################
@pytest.mark.parametrize(
    ("dtype", "expected_dtype"),
    [
        *np_dtype_params,
        pytest.param(pd.Int8Dtype(), np.int8, id="Int8"),
        pytest.param(pd.Int16Dtype(), np.int16, id="Int16"),
        pytest.param(pd.Int32Dtype(), np.int32, id="Int32"),
        pytest.param(pd.Int64Dtype(), np.int64, id="Int64"),
        pytest.param(pd.UInt8Dtype(), np.uint8, id="UInt8"),
        pytest.param(pd.UInt16Dtype(), np.uint16, id="UInt16"),
        pytest.param(pd.UInt32Dtype(), np.uint32, id="UInt32"),
        pytest.param(pd.UInt64Dtype(), np.uint64, id="UInt64"),
        pytest.param(pd.Float32Dtype(), np.float32, id="Float32"),
        pytest.param(pd.Float64Dtype(), np.float64, id="Float64"),
        pytest.param("int8[pyarrow]", np.int8, id="int8[pyarrow]", **pa_marks),
        pytest.param("int16[pyarrow]", np.int16, id="int16[pyarrow]", **pa_marks),
        pytest.param("int32[pyarrow]", np.int32, id="int32[pyarrow]", **pa_marks),
        pytest.param("int64[pyarrow]", np.int64, id="int64[pyarrow]", **pa_marks),
        pytest.param("uint8[pyarrow]", np.uint8, id="uint8[pyarrow]", **pa_marks),
        pytest.param("uint16[pyarrow]", np.uint16, id="uint16[pyarrow]", **pa_marks),
        pytest.param("uint32[pyarrow]", np.uint32, id="uint32[pyarrow]", **pa_marks),
        pytest.param("uint64[pyarrow]", np.uint64, id="uint64[pyarrow]", **pa_marks),
        pytest.param("float16[pyarrow]", np.float16, id="float16[pyarrow]", **pa_marks),
        pytest.param("float32[pyarrow]", np.float32, id="float32[pyarrow]", **pa_marks),
        pytest.param("float64[pyarrow]", np.float64, id="float64[pyarrow]", **pa_marks),
    ],
)
def test_to_numpy_pandas_numeric(dtype, expected_dtype):
    """
    Test the _to_numpy function with pandas.Series of numeric dtypes.
    """
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    # TODO(pandas>=2.2): Remove the workaround for float16 dtype in pandas<2.2.
    # float16 needs special handling for pandas < 2.2.
    # Example from https://arrow.apache.org/docs/python/generated/pyarrow.float16.html
    if dtype == "float16[pyarrow]" and Version(pd.__version__) < Version("2.2"):
        data = np.array(data, dtype=np.float16)
    series = pd.Series(data, dtype=dtype)[::2]  # Not C-contiguous
    result = _to_numpy(series)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, series)


@pytest.mark.parametrize(
    ("dtype", "expected_dtype"),
    [
        pytest.param(np.float16, np.float16, id="float16"),
        pytest.param(np.float32, np.float32, id="float32"),
        pytest.param(np.float64, np.float64, id="float64"),
        pytest.param(np.longdouble, np.longdouble, id="longdouble"),
        pytest.param(pd.Int8Dtype(), np.float64, id="Int8"),
        pytest.param(pd.Int16Dtype(), np.float64, id="Int16"),
        pytest.param(pd.Int32Dtype(), np.float64, id="Int32"),
        pytest.param(pd.Int64Dtype(), np.float64, id="Int64"),
        pytest.param(pd.UInt8Dtype(), np.float64, id="UInt8"),
        pytest.param(pd.UInt16Dtype(), np.float64, id="UInt16"),
        pytest.param(pd.UInt32Dtype(), np.float64, id="UInt32"),
        pytest.param(pd.UInt64Dtype(), np.float64, id="UInt64"),
        pytest.param(pd.Float32Dtype(), np.float32, id="Float32"),
        pytest.param(pd.Float64Dtype(), np.float64, id="Float64"),
        pytest.param("int8[pyarrow]", np.float64, id="int8[pyarrow]", **pa_marks),
        pytest.param("int16[pyarrow]", np.float64, id="int16[pyarrow]", **pa_marks),
        pytest.param("int32[pyarrow]", np.float64, id="int32[pyarrow]", **pa_marks),
        pytest.param("int64[pyarrow]", np.float64, id="int64[pyarrow]", **pa_marks),
        pytest.param("uint8[pyarrow]", np.float64, id="uint8[pyarrow]", **pa_marks),
        pytest.param("uint16[pyarrow]", np.float64, id="uint16[pyarrow]", **pa_marks),
        pytest.param("uint32[pyarrow]", np.float64, id="uint32[pyarrow]", **pa_marks),
        pytest.param("uint64[pyarrow]", np.float64, id="uint64[pyarrow]", **pa_marks),
        pytest.param("float16[pyarrow]", np.float16, id="float16[pyarrow]", **pa_marks),
        pytest.param("float32[pyarrow]", np.float32, id="float32[pyarrow]", **pa_marks),
        pytest.param("float64[pyarrow]", np.float64, id="float64[pyarrow]", **pa_marks),
    ],
)
def test_to_numpy_pandas_numeric_with_na(dtype, expected_dtype):
    """
    Test the _to_numpy function with pandas.Series of NumPy/pandas/PyArrow numeric
    dtypes and missing values (NA).
    """
    data = [1.0, 2.0, None, 4.0, 5.0, 6.0]
    # TODO(pandas>=2.2): Remove the workaround for float16 dtype in pandas<2.2.
    # float16 needs special handling for pandas < 2.2.
    # Example from https://arrow.apache.org/docs/python/generated/pyarrow.float16.html
    if dtype == "float16[pyarrow]" and Version(pd.__version__) < Version("2.2"):
        data = np.array(data, dtype=np.float16)
    series = pd.Series(data, dtype=dtype)[::2]  # Not C-contiguous
    assert series.isna().any()
    result = _to_numpy(series)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, np.array([1.0, np.nan, 5.0], dtype=expected_dtype))


@pytest.mark.parametrize(
    "dtype",
    [
        None,
        np.str_,
        "U10",
        "string[python]",
        pytest.param("string[pyarrow]", marks=skip_if_no(package="pyarrow")),
        pytest.param(
            "string[pyarrow_numpy]",
            marks=[
                skip_if_no(package="pyarrow"),
                # TODO(pandas>=2.1): Remove the skipif marker for pandas<2.1.
                pytest.mark.skipif(
                    Version(pd.__version__) < Version("2.1"),
                    reason="string[pyarrow_numpy] was added since pandas 2.1",
                ),
            ],
        ),
    ],
)
def test_to_numpy_pandas_string(dtype):
    """
    Test the _to_numpy function with pandas.Series of string dtypes.

    In pandas, string arrays can be specified in multiple ways.

    Reference: https://pandas.pydata.org/docs/reference/api/pandas.StringDtype.html
    """
    array = pd.Series(["abc", "defg", "12345"], dtype=dtype)
    result = _to_numpy(array)
    _check_result(result, np.str_)
    npt.assert_array_equal(result, array)


@pytest.mark.skipif(not _HAS_PYARROW, reason="pyarrow is not installed")
@pytest.mark.parametrize(
    ("dtype", "expected_dtype"),
    [
        pytest.param("date32[day][pyarrow]", "datetime64[D]", id="date32[day]"),
        pytest.param("date64[ms][pyarrow]", "datetime64[ms]", id="date64[ms]"),
    ],
)
def test_to_numpy_pandas_date(dtype, expected_dtype):
    """
    Test the _to_numpy function with pandas.Series of PyArrow date32/date64 types.
    """
    series = pd.Series(pd.date_range(start="2024-01-01", periods=3), dtype=dtype)
    result = _to_numpy(series)
    _check_result(result, np.datetime64)
    assert result.dtype == expected_dtype  # Explicitly check the date unit.
    npt.assert_array_equal(
        result,
        np.array(["2024-01-01", "2024-01-02", "2024-01-03"], dtype=expected_dtype),
    )


########################################################################################
# Test the _to_numpy function with PyArrow arrays.
#
# PyArrow provides the following types:
#
# - Numeric types:
#   - int8, int16, int32, int64
#   - uint8, uint16, uint32, uint64
#   - float16, float32, float64
# - String types: string/utf8, large_string/large_utf8, string_view
# - Date types:
#   - date32[day]
#   - date64[ms]
# - Timestamp types: timestamp[unit], timestamp[unit, tz]
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
def test_to_numpy_pyarrow_numeric(dtype, expected_dtype):
    """
    Test the _to_numpy function with PyArrow arrays of numeric types.
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
def test_to_numpy_pyarrow_numeric_with_na(dtype, expected_dtype):
    """
    Test the _to_numpy function with PyArrow arrays of numeric types and NA.
    """
    data = [1.0, 2.0, None, 4.0, 5.0, 6.0]
    if dtype == "float16":  # float16 needs special handling
        # Example from https://arrow.apache.org/docs/python/generated/pyarrow.float16.html
        data = np.array(data, dtype=np.float16)
    array = pa.array(data, type=dtype)[::2]
    result = _to_numpy(array)
    _check_result(result, expected_dtype)
    npt.assert_array_equal(result, array)


@pytest.mark.skipif(not _HAS_PYARROW, reason="pyarrow is not installed")
@pytest.mark.parametrize(
    "dtype",
    [
        None,
        "string",
        "utf8",  # alias for string
        "large_string",
        "large_utf8",  # alias for large_string
        pytest.param(
            "string_view",
            # TODO(pyarrow>=16): Remove the skipif marker for pyarrow<16.
            marks=pytest.mark.skipif(
                Version(pa.__version__) < Version("16"),
                reason="string_view type was added since pyarrow 16",
            ),
        ),
    ],
)
def test_to_numpy_pyarrow_string(dtype):
    """
    Test the _to_numpy function with PyArrow arrays of string types.
    """
    array = pa.array(["abc", "defg", "12345"], type=dtype)
    result = _to_numpy(array)
    _check_result(result, np.str_)
    npt.assert_array_equal(result, array)


@pytest.mark.skipif(not _HAS_PYARROW, reason="pyarrow is not installed")
@pytest.mark.parametrize(
    ("dtype", "expected_dtype"),
    [
        pytest.param("date32[day]", "datetime64[D]", id="date32[day]"),
        pytest.param("date64[ms]", "datetime64[ms]", id="date64[ms]"),
    ],
)
def test_to_numpy_pyarrow_date(dtype, expected_dtype):
    """
    Test the _to_numpy function with PyArrow arrays of date32/date64 types.

    date32[day] and date64[ms] are stored as 32-bit and 64-bit integers, respectively,
    representing the number of days and milliseconds since the UNIX epoch (1970-01-01).

    Here we explicitly check the dtype and date unit of the result.
    """
    data = [
        date(2024, 1, 1),
        datetime(2024, 1, 2),
        datetime(2024, 1, 3),
    ]
    array = pa.array(data, type=dtype)
    result = _to_numpy(array)
    _check_result(result, np.datetime64)
    assert result.dtype == expected_dtype  # Explicitly check the date unit.
    npt.assert_array_equal(
        result,
        np.array(["2024-01-01", "2024-01-02", "2024-01-03"], dtype=expected_dtype),
    )


@pytest.mark.skipif(not _HAS_PYARROW, reason="pyarrow is not installed")
@pytest.mark.parametrize(
    ("dtype", "expected_dtype"),
    [
        pytest.param(None, "datetime64[us]", id="None"),
        pytest.param("timestamp[s]", "datetime64[s]", id="timestamp[s]"),
        pytest.param("timestamp[ms]", "datetime64[ms]", id="timestamp[ms]"),
        pytest.param("timestamp[us]", "datetime64[us]", id="timestamp[us]"),
        pytest.param("timestamp[ns]", "datetime64[ns]", id="timestamp[ns]"),
        pytest.param(
            pa.timestamp("s", tz="UTC"), "datetime64[s]", id="timestamp[s, tz=UTC]"
        ),  # pa.timestamp with tz has no string alias.
        pytest.param(
            pa.timestamp("s", tz="America/New_York"),
            "datetime64[s]",
            id="timestamp[s, tz=America/New_York]",
        ),
        pytest.param(
            pa.timestamp("s", tz="+07:30"),
            "datetime64[s]",
            id="timestamp[s, tz=+07:30]",
        ),
    ],
)
def test_to_numpy_pyarrow_timestamp(dtype, expected_dtype):
    """
    Test the _to_numpy function with PyArrow arrays of PyArrow timestamp types.

    pyarrow.timestamp(unit, tz=None) can accept units "s", "ms", "us", and "ns".

    Reference: https://arrow.apache.org/docs/python/generated/pyarrow.timestamp.html
    """
    data = [datetime(2024, 1, 2, 3, 4, 5), datetime(2024, 1, 2, 3, 4, 6)]
    array = pa.array(data, type=dtype)
    result = _to_numpy(array)
    _check_result(result, np.datetime64)
    assert result.dtype == expected_dtype
    assert result[0] == np.datetime64("2024-01-02T03:04:05")
    assert result[1] == np.datetime64("2024-01-02T03:04:06")
