"""
Functions to convert data types into ctypes friendly formats.
"""

import contextlib
import ctypes as ctp
import warnings
from collections.abc import Sequence
from typing import Any

import numpy as np
import pandas as pd
import xarray as xr
from packaging.version import Version
from pygmt.exceptions import GMTInvalidInput


def dataarray_to_matrix(
    grid: xr.DataArray,
) -> tuple[np.ndarray, list[float], list[float]]:
    """
    Transform an xarray.DataArray into a 2-D numpy array and metadata.

    Use this to extract the underlying numpy array of data and the region and increment
    for the grid.

    Only allows grids with two dimensions and constant grid spacings (GMT doesn't allow
    variable grid spacings). If the latitude and/or longitude increments of the input
    grid are negative, the output matrix will be sorted by the DataArray coordinates to
    yield positive increments.

    If the underlying data array is not C contiguous, for example, if it's a slice of a
    larger grid, a copy will need to be generated.

    Parameters
    ----------
    grid
        The input grid as a DataArray instance. Information is retrieved from the
        coordinate arrays, not from headers.

    Returns
    -------
    matrix
        The 2-D array of data from the grid.
    region
        The West, East, South, North boundaries of the grid.
    inc
        The grid spacing in East-West and North-South, respectively.

    Raises
    ------
    GMTInvalidInput
        If the grid has more than two dimensions or variable grid spacing.

    Examples
    --------

    >>> from pygmt.datasets import load_earth_relief
    >>> # Use the global Earth relief grid with 1 degree spacing
    >>> grid = load_earth_relief(resolution="01d", registration="pixel")
    >>> matrix, region, inc = dataarray_to_matrix(grid)
    >>> print(region)
    [-180.0, 180.0, -90.0, 90.0]
    >>> print(inc)
    [1.0, 1.0]
    >>> type(matrix)
    <class 'numpy.ndarray'>
    >>> print(matrix.shape)
    (180, 360)
    >>> matrix.flags.c_contiguous
    True
    >>> # Using a slice of the grid, the matrix will be copied to guarantee that it's
    >>> # C-contiguous in memory. The increment should be unchanged.
    >>> matrix, region, inc = dataarray_to_matrix(grid[10:41, 30:101])
    >>> matrix.flags.c_contiguous
    True
    >>> print(matrix.shape)
    (31, 71)
    >>> print(region)
    [-150.0, -79.0, -80.0, -49.0]
    >>> print(inc)
    [1.0, 1.0]
    >>> # The increment should change accordingly if taking every other grid point.
    >>> matrix, region, inc = dataarray_to_matrix(grid[10:41:2, 30:101:2])
    >>> matrix.flags.c_contiguous
    True
    >>> print(matrix.shape)
    (16, 36)
    >>> print(region)
    [-150.5, -78.5, -80.5, -48.5]
    >>> print(inc)
    [2.0, 2.0]
    """
    if len(grid.dims) != 2:
        msg = f"Invalid number of grid dimensions 'len({grid.dims})'. Must be 2."
        raise GMTInvalidInput(msg)

    # Extract region and inc from the grid
    region, inc = [], []
    # Reverse the dims because it is rows, columns ordered. In geographic grids, this
    # would be North-South, East-West. GMT's region and inc are East-West, North-South.
    for dim in grid.dims[::-1]:
        coord = grid.coords[dim].to_numpy()
        coord_incs = coord[1:] - coord[:-1]
        coord_inc = coord_incs[0]
        if not np.allclose(coord_incs, coord_inc):
            # Calculate the increment if irregular spacing is found.
            coord_inc = (coord[-1] - coord[0]) / (coord.size - 1)
            msg = (
                f"Grid may have irregular spacing in the '{dim}' dimension, "
                "but GMT only supports regular spacing. Calculated regular spacing "
                f"{coord_inc} is assumed in the '{dim}' dimension."
            )
            warnings.warn(msg, category=RuntimeWarning, stacklevel=2)
        if coord_inc == 0:
            msg = f"Grid has a zero increment in the '{dim}' dimension."
            raise GMTInvalidInput(msg)
        region.extend(
            [
                coord.min() - coord_inc / 2 * grid.gmt.registration,
                coord.max() + coord_inc / 2 * grid.gmt.registration,
            ]
        )
        inc.append(coord_inc)

    if any(i < 0 for i in inc):  # Sort grid when there are negative increments
        inc = [abs(i) for i in inc]
        grid = grid.sortby(variables=list(grid.dims), ascending=True)

    matrix = np.ascontiguousarray(grid[::-1].to_numpy())
    region = [float(i) for i in region]
    inc = [float(i) for i in inc]
    return matrix, region, inc


def _to_numpy(data: Any) -> np.ndarray:
    """
    Convert an array-like object to a C contiguous NumPy array.

    The function aims to convert any array-like objects (e.g., Python lists or tuples,
    NumPy arrays with various dtypes, pandas.Series with NumPy/pandas/PyArrow dtypes,
    PyArrow arrays with various dtypes) to a NumPy array.

    The function is internally used in the ``vectors_to_arrays`` function, which is
    responsible for converting a sequence of vectors to a list of C contiguous NumPy
    arrays. Thus, the function uses the :numpy:func:`numpy.ascontiguousarray` function
    rather than the :numpy:func:`numpy.asarray`/:numpy::func:`numpy.asanyarray`
    functions, to ensure the returned NumPy array is C contiguous.

    Parameters
    ----------
    data
        The array-like object to convert.

    Returns
    -------
    array
        The C contiguous NumPy array.
    """
    # Mapping of unsupported dtypes to expected NumPy dtypes.
    dtypes: dict[str, type | str] = {
        # For string dtypes.
        "large_string": np.str_,  # pa.large_string and pa.large_utf8
        "string": np.str_,  # pa.string, pa.utf8, pd.StringDtype
        "string_view": np.str_,  # pa.string_view
        # For datetime dtypes.
        "date32[day][pyarrow]": "datetime64[D]",
        "date64[ms][pyarrow]": "datetime64[ms]",
    }

    # The dtype for the input object.
    dtype = getattr(data, "dtype", getattr(data, "type", ""))
    # The numpy dtype for the result numpy array, but can be None.
    numpy_dtype = dtypes.get(str(dtype))

    # TODO(pandas>=2.2): Remove the workaround for pandas<2.2.
    #
    # pandas numeric dtypes were converted to np.object_ dtype prior pandas 2.2, and are
    # converted to suitable NumPy dtypes since pandas 2.2. Refer to the following link
    # for details: https://pandas.pydata.org/docs/whatsnew/v2.2.0.html#to-numpy-for-numpy-nullable-and-arrow-types-converts-to-suitable-numpy-dtype
    if (
        Version(pd.__version__) < Version("2.2")  # pandas < 2.2 only.
        and hasattr(data, "dtype")  # NumPy array or pandas objects only.
        and hasattr(data.dtype, "numpy_dtype")  # pandas dtypes only.
        and data.dtype.kind in "iuf"  # Numeric dtypes only.
    ):  # pandas Series/Index with pandas nullable numeric dtypes.
        # The numpy dtype of the result numpy array.
        numpy_dtype = data.dtype.numpy_dtype
        if getattr(data, "hasnans", False):
            if data.dtype.kind in "iu":
                # Integers with missing values are converted to float64.
                numpy_dtype = np.float64
            data = data.to_numpy(na_value=np.nan)

    array = np.ascontiguousarray(data, dtype=numpy_dtype)

    # Check if a np.object_ or np.str_ array can be converted to np.datetime64.
    if array.dtype.type in {np.object_, np.str_}:
        with contextlib.suppress(TypeError, ValueError):
            return np.ascontiguousarray(array, dtype=np.datetime64)

    # Check if a np.object_ array can be converted to np.str_.
    if array.dtype == np.object_:
        with contextlib.suppress(TypeError, ValueError):
            return np.ascontiguousarray(array, dtype=np.str_)
    return array


def vectors_to_arrays(vectors: Sequence[Any]) -> list[np.ndarray]:
    """
    Convert 1-D vectors (scalars, lists, or array-like) to C contiguous 1-D arrays.

    Arrays must be in C contiguous order for us to pass their memory pointers to GMT.
    If any are not, convert them to C order (which requires copying the memory). This
    usually happens when vectors are columns of a 2-D array or have been sliced.

    The returned arrays are guaranteed to be C contiguous and at least 1-D.

    Parameters
    ----------
    vectors
        The vectors that must be converted.

    Returns
    -------
    arrays
        List of converted numpy arrays.

    Examples
    --------

    >>> import numpy as np
    >>> import pandas as pd
    >>> data = np.array([[1, 2], [3, 4], [5, 6]])
    >>> vectors = [data[:, 0], data[:, 1], pd.Series(data=[-1, -2, -3])]
    >>> all(i.flags.c_contiguous for i in vectors)
    False
    >>> all(isinstance(i, np.ndarray) for i in vectors)
    False
    >>> arrays = vectors_to_arrays(vectors)
    >>> all(i.flags.c_contiguous for i in arrays)
    True
    >>> all(isinstance(i, np.ndarray) for i in arrays)
    True
    >>> all(i.ndim == 1 for i in arrays)
    True
    """
    return [_to_numpy(vector) for vector in vectors]


def sequence_to_ctypes_array(
    sequence: Sequence[int | float] | np.ndarray | None, ctype, size: int
) -> ctp.Array | None:
    """
    Convert a sequence of numbers into a ctypes array variable.

    If the sequence is ``None``, returns ``None``. Otherwise, returns a ctypes array.
    The function only works for sequences of numbers. For converting a sequence of
    strings, use ``strings_to_ctypes_array`` instead.

    Parameters
    ----------
    sequence
        The sequence to convert. If ``None``, returns ``None``. Otherwise, it must be a
        sequence (e.g., list, tuple, numpy array).
    ctype
        The ctypes type of the array (e.g., ``ctypes.c_int``).
    size
        The size of the array. If the sequence is smaller than the size, the remaining
        elements will be filled with zeros. If the sequence is larger than the size, an
        exception will be raised.

    Returns
    -------
    ctypes_array
        The ctypes array variable.

    Examples
    --------
    >>> import ctypes as ctp
    >>> ctypes_array = sequence_to_ctypes_array([1, 2, 3], ctp.c_long, 3)
    >>> type(ctypes_array)
    <class 'pygmt.clib.conversion.c_long_Array_3'>
    >>> ctypes_array[:]
    [1, 2, 3]
    >>> ctypes_array = sequence_to_ctypes_array([1, 2], ctp.c_long, 5)
    >>> type(ctypes_array)
    <class 'pygmt.clib.conversion.c_long_Array_5'>
    >>> ctypes_array[:]
    [1, 2, 0, 0, 0]
    >>> ctypes_array = sequence_to_ctypes_array(None, ctp.c_long, 5)
    >>> print(ctypes_array)
    None
    >>> ctypes_array = sequence_to_ctypes_array([1, 2, 3, 4, 5, 6], ctp.c_long, 5)
    Traceback (most recent call last):
    ...
    IndexError: invalid index
    """
    if sequence is None:
        return None
    return (ctype * size)(*sequence)


def strings_to_ctypes_array(strings: Sequence[str] | np.ndarray) -> ctp.Array:
    """
    Convert a sequence (e.g., a list) of strings or numpy.ndarray of strings into a
    ctypes array.

    Parameters
    ----------
    strings
        A sequence of strings, or a numpy.ndarray of str dtype.

    Returns
    -------
    ctypes_array
        A ctypes array of strings.

    Examples
    --------
    >>> strings = ["first", "second", "third"]
    >>> ctypes_array = strings_to_ctypes_array(strings)
    >>> type(ctypes_array)
    <class 'pygmt.clib.conversion.c_char_p_Array_3'>
    >>> [s.decode() for s in ctypes_array]
    ['first', 'second', 'third']

    >>> strings = np.array(["first", "second", "third"])
    >>> ctypes_array = strings_to_ctypes_array(strings)
    >>> type(ctypes_array)
    <class 'pygmt.clib.conversion.c_char_p_Array_3'>
    >>> [s.decode() for s in ctypes_array]
    ['first', 'second', 'third']
    """
    return (ctp.c_char_p * len(strings))(*[s.encode() for s in strings])


def array_to_datetime(array: Sequence[Any] | np.ndarray) -> np.ndarray:
    """
    Convert a 1-D datetime array from various types into numpy.datetime64.

    If the input array is not in legal datetime formats, raise a ValueError exception.

    Parameters
    ----------
    array
        The input datetime array in various formats.

        Supported types:

        - str
        - numpy.datetime64
        - pandas.DateTimeIndex
        - datetime.datetime and datetime.date

    Returns
    -------
    array
        1-D datetime array in numpy.datetime64.

    Raises
    ------
    ValueError
        If the datetime string is invalid.

    Examples
    --------
    >>> import datetime
    >>> # numpy.datetime64 array
    >>> x = np.array(
    ...     ["2010-06-01", "2011-06-01T12", "2012-01-01T12:34:56"],
    ...     dtype="datetime64[ns]",
    ... )
    >>> array_to_datetime(x)
    array(['2010-06-01T00:00:00.000000000', '2011-06-01T12:00:00.000000000',
           '2012-01-01T12:34:56.000000000'], dtype='datetime64[ns]')

    >>> # pandas.DateTimeIndex array
    >>> import pandas as pd
    >>> x = pd.date_range("2013", freq="YS", periods=3)
    >>> array_to_datetime(x)
    array(['2013-01-01T00:00:00.000000000', '2014-01-01T00:00:00.000000000',
           '2015-01-01T00:00:00.000000000'], dtype='datetime64[ns]')

    >>> # Python's built-in date and datetime
    >>> x = [datetime.date(2018, 1, 1), datetime.datetime(2019, 1, 1)]
    >>> array_to_datetime(x)
    array(['2018-01-01T00:00:00.000000', '2019-01-01T00:00:00.000000'],
          dtype='datetime64[us]')

    >>> # Raw datetime strings in various format
    >>> x = [
    ...     "2018",
    ...     "2018-02",
    ...     "2018-03-01",
    ...     "2018-04-01T01:02:03",
    ... ]
    >>> array_to_datetime(x)
    array(['2018-01-01T00:00:00', '2018-02-01T00:00:00',
           '2018-03-01T00:00:00', '2018-04-01T01:02:03'],
          dtype='datetime64[s]')

    >>> # Mixed datetime types
    >>> x = [
    ...     "2018-01-01",
    ...     np.datetime64("2018-01-01"),
    ...     datetime.datetime(2018, 1, 1),
    ... ]
    >>> array_to_datetime(x)
    array(['2018-01-01T00:00:00.000000', '2018-01-01T00:00:00.000000',
           '2018-01-01T00:00:00.000000'], dtype='datetime64[us]')
    """
    return np.asarray(array, dtype=np.datetime64)
