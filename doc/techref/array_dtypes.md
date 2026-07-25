# Supported Array Dtypes

PyGMT uses NumPy arrays as its core data structure for storing data and exchanging data
with the GMT C API. This page provides a comprehensive overview of the dtypes accepted
by PyGMT's array-conversion and GMT virtual-file interfaces.

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
1. Signed and unsigned integer dtypes from pandas and PyArrow (e.g.,
   {class}`pandas.Int8Dtype`, {func}`pyarrow.int8`) support missing values like `None`
   or {class}`pandas.NA`, whereas NumPy's corresponding dtypes (e.g.,
   {class}`numpy.int8`) don't. Arrays of these dtypes containing missing values are
   automatically cast to {class}`numpy.float64` internally.
2. For 3-D {class}`xarray.DataArray` objects representing raster images, only 8-bit
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

In addition to Python's built-in {class}`str` type, PyGMT also supports the following
string dtypes:

- NumPy: {class}`numpy.str_` or fixed-width Unicode string dtype (e.g., `"U10"`)
- pandas: {class}`pandas.StringDtype`, with different storage backends, including
  `string[python]` and `string[pyarrow]`
- PyArrow: {func}`pyarrow.string`/{func}`pyarrow.utf8`,
  {func}`pyarrow.large_string`/{func}`pyarrow.large_utf8`, and
  {func}`pyarrow.string_view`

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

# A PyArrow array with pyarrow.string dtype
pa.array(["a", "b", "c"], type=pa.string())
```
:::

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

## Timedelta Dtypes

PyGMT supports NumPy arrays with the {class}`numpy.timedelta64` dtype. Timedelta values
are passed to GMT as their underlying integer values, so their unit determines the
numeric scale. For example, a `timedelta64[D]` array is interpreted as days, whereas a
`timedelta64[s]` array is interpreted as seconds.

Timedelta values can also be used in sequence-valued parameters such as ``region``.
The timedelta dtype does not, by itself, configure a GMT relative-time axis; configure
GMT time settings explicitly when a relative-time axis is required.

## Unsupported Dtypes

The following dtypes are intentionally unsupported, and should be cast to an appropriate
supported dtype before passing to PyGMT:

- Floating-point dtypes: {class}`numpy.float16`, {func}`pyarrow.float16`, {class}`numpy.longdouble`
- Boolean dtypes: {class}`numpy.bool_`, {class}`pandas.BooleanDtype`, {func}`pyarrow.bool_`
- Complex dtypes: {class}`numpy.complex64`, {class}`numpy.complex128`
- {class}`numpy.bytes_` and {class}`numpy.void`

The {class}`numpy.object_` dtype is also not supported. PyGMT may convert object arrays
that can be interpreted as datetimes or text, but applications should create arrays with
an explicit supported dtype instead.
