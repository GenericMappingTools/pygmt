# Supported Array Dtypes

PyGMT uses NumPy arrays as its core data structure for storing data and exchanging data
with the GMT C API. This design allows PyGMT to support a wide range of array-like
objects and data types (*dtypes*), as long as they can be converted to NumPy arrays.
This page provides a comprehensive overview of the array dtypes supported by PyGMT.

## Numeric Dtypes

In addition to Python's built-in numeric types (`int` and `float`), PyGMT supports most
of the numeric dtypes provided by NumPy, pandas, and PyArrow.

**Signed Integers**

- `numpy.int8`, `numpy.int16`, `numpy.int32`, `numpy.int64`, `numpy.longlong`
- `pandas.Int8Dtype`, `pandas.Int16Dtype`, `pandas.Int32Dtype`, `pandas.Int64Dtype`
- `pyarrow.int8`, `pyarrow.int16`, `pyarrow.int32`, `pyarrow.int64`

**Unsigned Integers**

- `numpy.uint8`, `numpy.uint16`, `numpy.uint32`, `numpy.uint64`, `numpy.ulonglong`
- `pandas.UInt8Dtype`, `pandas.UInt16Dtype`, `pandas.UInt32Dtype`, `pandas.UInt64Dtype`
- `pyarrow.uint8`, `pyarrow.uint16`, `pyarrow.uint32`, `pyarrow.uint64`

**Floating-point numbers**

- `numpy.float32`, `numpy.float64`
- `pandas.Float32Dtype`, `pandas.Float64Dtype`
- `pyarrow.float32`, `pyarrow.float64`

:::{note}
1. The numeric dtypes `numpy.float16`, `numpy.longdouble`, and `pyarrow.float16` are not
   supported and should be cast to one of the supported dtypes before passing them to
   PyGMT.
2. Complex numeric dtypes such as `numpy.complex64` are not supported.
3. Signed and unsigned integer dtypes from pandas and PyArrow (e.g., `pandas.Int8Dtype`,
   `pyarrow.int8`) support missing values like `None` or `pandas.NA`, whereas NumPy's
   corrresponding dtypes (e.g., `numpy.int8`) don't. Arrays of these dtypes containing
   missing values are automatically cast to `numpy.float64` internally.
4. For 3-D {class}`xarray.DataArray` objects representing raster images, only 8-bit
   unsigned integers (i.e., `numpy.uint8`) are supported.
:::

:::{note}
Examples of numeric arrays supported by PyGMT:

```python
# A list of integers
[1, 2, 3]

# A NumPy array with dtype int32
np.array([1, 2, 3], dtype=np.int32)

# A pandas Series with nullable Int32 dtype
pd.Series([1, 2, 3], dtype="Int32")

# A pandas Series with nullable Int32 dtype and missing values
pd.Series([1, 2, pd.NA], dtype="Int32")

# A pandas Series using a PyArrow-backed float64 dtype
pd.Series([1, 2, 3], dtype="float64[pyarrow]")

# A PyArrow array with dtype uint8
pa.array([1, 2, 3], type=pa.uint8())
```
:::

## String Dtypes

In addition to Python's built-in `str` type, PyGMT also support following string dtypes:

- NumPy: `numpy.str_` or fixed-width Unicode string dtype (e.g., ``"U10"``)
- pandas: `pandas.StringDtype`, with different storage backends, including
  `string[python]`, `string[pyarrow]`, and `string[pyarrow_numpy]`
- PyArrow: `pyarrow.string`/`pyarrow.utf8`, `pyarrow.large_string`/`pyarrow.large_utf8`,
  and `pyarrow.string_view`

PyGMT also tries to convert arrays of `np.object_` dtype into string arrays if possible.

:::{note}
Examples of string arrays supported by PyGMT:

```python
# A list of strings
["a", "b", "c"]

# A NumPy string array
np.array(["a", "b", "c"])
np.array(["a", "b", "c"], dtype=np.str_)

# A pandas.Series string array
pd.Series(["a", "b", "c"], dtype="string")
pd.Series(["a", "b", "c"], dtype="string[python]")
pd.Series(["a", "b", "c"], dtype="string[pyarrow]")
pd.Series(["a", "b", "c"], dtype="string[pyarrow_numpy]")

# A PyArrow array with pyarrow.string dtype
pa.array(["a", "b", "c"], type=pa.string())
```

## Datetime Dtypes

PyGMT supports a variety of datetime types:

- A list/tuple of elements in Python's built-in `datetime.datetime` or `datetime.date`,
  NumPy's `numpy.datetime64`, panda's `pandas.Timestamp` types, datetime-like strings,
  or mixed.
- NumPy arrays: `numpy.datetime64` with various resolutions
- pandas objects with `numpy.datetime64`, `pandas.DatetimeTZDtype`,
  `pyarrow.timestamp` with various resolution and timezone support, and
  pyarrow-backend dtypes like `date32[day][pyarrow]` and `date64[ms][pyarrow]`,
- PyArrow: `pyarrow.date32`, `pyarrow.date64` and `pyarrow.timestamp` with various
  resolutions and timezone support.

<!-- Internally GMT stores datetimes as intergers, so not all resolutions are supported. Need to explain it in details. -->

## Bool Dtypes

Currently, `numpy.bool` is not supported.
