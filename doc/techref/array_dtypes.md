# Supported Array Dtypes

PyGMT uses NumPy arrays to store data and passes them to the GMT C library. In this way,
PyGMT can support a wide range of dtypes. This page documents array dtypes supported by
PyGMT.

## Numeric Dtypes

For 1-D and 2-D arrays, PyGMT supports most numeric dtypes provided by NumPy, pandas, and
PyArrow.

**Signed Integers:**

- `numpy.int8`, `numpy.int16`, `numpy.int32`, `numpy.int64`
- `pandas.Int8`, `pandas.Int16`, `pandas.Int32`, `pandas.Int64`
- `pyarrow.int8`, `pyarrow.int16`, `pyarrow.int32`, `pyarrow.int64`

**Unsigned Integers:**

- `numpy.uint8`, `numpy.uint16`, `numpy.uint32`, `numpy.uint64`
- `pandas.UInt8`, `pandas.UInt16`, `pandas.UInt32`, `pandas.UInt64`
- `pyarrow.uint8`, `pyarrow.uint16`, `pyarrow.uint32`, `pyarrow.uint64`

**Floating-point numbers:**

- `numpy.float32`, `numpy.float64`
- `pandas.Float32`, `pandas.Float64`
- `pyarrow.float32`, `pyarrow.float64`

For 3-D {class}`xarray.DataArray` objects representing raster images, only 8-bit unsigned
intergers (i.e., `numpy.uint8`) are supported.

## String Dtypes

## Datetime Dtypes
