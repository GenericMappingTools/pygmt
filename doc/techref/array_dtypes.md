# Supported Array Dtypes

PyGMT uses NumPy arrays as its core data structure for storing data and exchanging data
with the GMT C API. This design allows PyGMT to support a wide range of array-like
objects and data types (*dtypes*), as long as they can be converted to NumPy arrays.
This page provides a comprehensive overview of the array dtypes supported by PyGMT.

## Numeric Dtypes

In addition to Python's built-in numeric types ({class}`int` and {class}`float`), PyGMT
supports most of the numeric dtypes provided by NumPy, pandas, and PyArrow.

**Signed Integers**

- {class}`numpy.int8`, {class}`numpy.int16`, {class}`numpy.int32`, {class}`numpy.int64`,
  {class}`numpy.longlong`
- {class}`pandas.Int8Dtype`, {class}`pandas.Int16Dtype`, {class}`pandas.Int32Dtype`,
  {class}`pandas.Int64Dtype`
- {func}`pyarrow.int8`, {func}`pyarrow.int16`, {func}`pyarrow.int32`,
  {func}`pyarrow.int64`

**Unsigned Integers**

- {class}`numpy.uint8`, {class}`numpy.uint16`, {class}`numpy.uint32`,
  {class}`numpy.uint64`, {class}`numpy.ulonglong`
- {class}`pandas.UInt8Dtype`, {class}`pandas.UInt16Dtype`, {class}`pandas.UInt32Dtype`,
  {class}`pandas.UInt64Dtype`
- {func}`pyarrow.uint8`, {func}`pyarrow.uint16`, {func}`pyarrow.uint32`,
  {func}`pyarrow.uint64`

**Floating-point numbers**

- {class}`numpy.float32`, {class}`numpy.float64`
- {class}`pandas.Float32Dtype`, {class}`pandas.Float64Dtype`
- {func}`pyarrow.float32`, {func}`pyarrow.float64`

:::{note}
1. The numeric dtypes {class}`numpy.float16`, {class}`numpy.longdouble`, and
   {func}`pyarrow.float16` are not supported and should be cast to one of the supported
   dtypes before passing them to PyGMT.
2. Complex numeric dtypes such as {class}`numpy.complex64` are not supported.
3. Signed and unsigned integer dtypes from pandas and PyArrow (e.g.,
   {class}`pandas.Int8Dtype`, {func}`pyarrow.int8`) support missing values like `None`
   or {class}`pandas.NA`, whereas NumPy's corrresponding dtypes (e.g.,
   {class}`numpy.int8`) don't. Arrays of these dtypes containing missing values are
   automatically cast to {class}`numpy.float64` internally.
4. For 3-D {class}`xarray.DataArray` objects representing raster images, only 8-bit
   unsigned integers (i.e., {class}`numpy.uint8`) are supported.
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

- NumPy: {class}`numpy.str_` or fixed-width Unicode string dtype (e.g., `"U10"`)
- pandas: {class}`pandas.StringDtype`, with different storage backends, including
  `string[python]`, `string[pyarrow]`, and `string[pyarrow_numpy]`
- PyArrow: {func}`pyarrow.string`/{func}`pyarrow.utf8`,
  {func}`pyarrow.large_string`/{func}`pyarrow.large_utf8`, and
  {func}`pyarrow.string_view`

PyGMT also tries to convert arrays of {class}`numpy.object_` dtype into string arrays if
possible.

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

- A list/tuple of elements in Python's built-in {class}`datetime.datetime` or
  {class}`datetime.date`, NumPy's {class}`numpy.datetime64`, pandas' {class}`pandas.Timestamp`
  types, datetime-like strings, or mixed.
- NumPy arrays: {class}`numpy.datetime64` with various resolutions
- pandas objects with {class}`numpy.datetime64`, {class}`pandas.DatetimeTZDtype`,
  {func}`pyarrow.timestamp` with various resolution and timezone support, and
  pyarrow-backend dtypes like `date32[day][pyarrow]` and `date64[ms][pyarrow]`,
- PyArrow: {func}`pyarrow.date32`, {func}`pyarrow.date64` and {func}`pyarrow.timestamp`
  with various resolutions and timezone support.

<!-- Internally GMT stores datetimes as intergers, so not all resolutions are supported. Need to explain it in details. -->

## Bool Dtypes

Currently, `numpy.bool` is not supported.
