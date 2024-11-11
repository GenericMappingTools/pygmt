# Supported Array Dtypes

PyGMT uses NumPy arrays as its fundamental data structure for storing data, as well as
for exchanging data with the GMT C library. In this way, PyGMT can support a wide
range of dtypes, as long as they can be converted to a NumPy array. This page provides
a comprehensive overview of the dtypes supported by PyGMT.

## Numeric Dtypes

In addition to the Python built-in numeric types (i.e., `int` and `float`), PyGMT
supports most of the numeric dtypes provided by NumPy, pandas, and PyArrow.

**Signed Integers**

- `numpy.int8`, `numpy.int16`, `numpy.int32`, `numpy.int64`
- `pandas.Int8`, `pandas.Int16`, `pandas.Int32`, `pandas.Int64`
- `pyarrow.int8`, `pyarrow.int16`, `pyarrow.int32`, `pyarrow.int64`

**Unsigned Integers**

- `numpy.uint8`, `numpy.uint16`, `numpy.uint32`, `numpy.uint64`
- `pandas.UInt8`, `pandas.UInt16`, `pandas.UInt32`, `pandas.UInt64`
- `pyarrow.uint8`, `pyarrow.uint16`, `pyarrow.uint32`, `pyarrow.uint64`

**Floating-point numbers**

- `numpy.float32`, `numpy.float64`
- `pandas.Float32`, `pandas.Float64`
- `pyarrow.float32`, `pyarrow.float64`

:::{note}

1. Currently, `numpy.float16`, `numpy.longdouble` and `pyarrow.float16` are not
   supported.
2. For 3-D {class}`xarray.DataArray` objects representing raster images, only 8-bit
   unsigned integers (i.e., `numpy.uint8`) are supported.
:::

:::{note}

Here are some examples for creating array-like objects that PyGMT supports:

```python
# A list of integers
[1, 2, 3]

# A NumPy array with np.int32 dtype
np.array([1, 2, 3], dtype=np.int32)

# A pandas.Series with pandas's Int32 dtype
pd.Series([1, 2, 3], dtype="Int32")

# A pandas.Series with pandas's nullable Int32 dtype
pd.Series([1, 2, pd.NA], dtype="Int32")

# A pandas.Series with PyArrow-backed float64 dtype
pd.Series([1, 2, 3], dtype="float64[pyarrow]")

# A PyArrow array with pyarrow.uint8 dtype
pa.array([1, 2, 3], type=pa.uint8())
```
:::

## String Dtypes

## Datetime Dtypes
