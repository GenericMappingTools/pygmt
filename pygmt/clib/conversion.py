"""
Functions to convert data types into ctypes friendly formats.
"""
import warnings

import numpy as np
from pygmt.exceptions import GMTInvalidInput


def dataarray_to_matrix(grid):
    """
    Transform an xarray.DataArray into a data 2-D array and metadata.

    Use this to extract the underlying numpy array of data and the region and
    increment for the grid.

    Only allows grids with two dimensions and constant grid spacing (GMT
    doesn't allow variable grid spacing). If the latitude and/or longitude
    increments of the input grid are negative, the output matrix will be
    sorted by the DataArray coordinates to yield positive increments.

    If the underlying data array is not C contiguous, for example if it's a
    slice of a larger grid, a copy will need to be generated.

    Parameters
    ----------
    grid : xarray.DataArray
        The input grid as a DataArray instance. Information is retrieved from
        the coordinate arrays, not from headers.

    Returns
    -------
    matrix : 2-D array
        The 2-D array of data from the grid.
    region : list
        The West, East, South, North boundaries of the grid.
    inc : list
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
    >>> # Using a slice of the grid, the matrix will be copied to guarantee
    >>> # that it's C-contiguous in memory. The increment should be unchanged.
    >>> matrix, region, inc = dataarray_to_matrix(grid[10:41, 30:101])
    >>> matrix.flags.c_contiguous
    True
    >>> print(matrix.shape)
    (31, 71)
    >>> print(region)
    [-150.0, -79.0, -80.0, -49.0]
    >>> print(inc)
    [1.0, 1.0]
    >>> # but not if only taking every other grid point.
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
        raise GMTInvalidInput(
            f"Invalid number of grid dimensions '{len(grid.dims)}'. Must be 2."
        )
    # Extract region and inc from the grid
    region = []
    inc = []
    # Reverse the dims because it is rows, columns ordered. In geographic
    # grids, this would be North-South, East-West. GMT's region and inc are
    # East-West, North-South.
    for dim in grid.dims[::-1]:
        coord = grid.coords[dim].to_numpy()
        coord_incs = coord[1:] - coord[0:-1]
        coord_inc = coord_incs[0]
        if not np.allclose(coord_incs, coord_inc):
            # calculate the increment if irregular spacing is found
            coord_inc = (coord[-1] - coord[0]) / (coord.size - 1)
            msg = (
                f"Grid may have irregular spacing in the '{dim}' dimension, "
                "but GMT only supports regular spacing. Calculated regular spacing "
                f"{coord_inc} is assumed in the '{dim}' dimension."
            )
            warnings.warn(msg, category=RuntimeWarning, stacklevel=2)
        if coord_inc == 0:
            raise GMTInvalidInput(
                f"Grid has a zero increment in the '{dim}' dimension."
            )
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

    matrix = as_c_contiguous(grid[::-1].to_numpy())
    return matrix, region, inc


def vectors_to_arrays(vectors):
    """
    Convert 1-D vectors (lists, arrays, or pandas.Series) to C contiguous 1-D arrays.

    Arrays must be in C contiguous order for us to pass their memory pointers
    to GMT. If any are not, convert them to C order (which requires copying the
    memory). This usually happens when vectors are columns of a 2-D array or
    have been sliced.

    If a vector is a list or pandas.Series, get the underlying numpy array.

    Parameters
    ----------
    vectors : list of lists, 1-D arrays, or pandas.Series
        The vectors that must be converted.

    Returns
    -------
    arrays : list of 1-D arrays
        The converted numpy arrays

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

    >>> data = [[1, 2], (3, 4), range(5, 7)]
    >>> all(isinstance(i, np.ndarray) for i in vectors_to_arrays(data))
    True

    >>> import datetime
    >>> import pytest
    >>> pa = pytest.importorskip("pyarrow")
    >>> vectors = [
    ...     pd.Series(
    ...         data=[datetime.date(2020, 1, 1), datetime.date(2021, 12, 31)],
    ...         dtype="date32[day][pyarrow]",
    ...     ),
    ...     pd.Series(
    ...         data=[datetime.date(2022, 1, 1), datetime.date(2023, 12, 31)],
    ...         dtype="date64[ms][pyarrow]",
    ...     ),
    ... ]
    >>> arrays = vectors_to_arrays(vectors)
    >>> all(a.flags.c_contiguous for a in arrays)
    True
    >>> all(isinstance(a, np.ndarray) for a in arrays)
    True
    >>> all(isinstance(a.dtype, np.dtypes.DateTime64DType) for a in arrays)
    True
    """
    dtypes = {
        "date32[day][pyarrow]": np.datetime64,
        "date64[ms][pyarrow]": np.datetime64,
    }
    arrays = []
    for vector in vectors:
        vec_dtype = str(getattr(vector, "dtype", ""))
        array = np.asarray(a=vector, dtype=dtypes.get(vec_dtype, None))
        arrays.append(as_c_contiguous(array))

    return arrays


def as_c_contiguous(array):
    """
    Ensure a numpy array is C contiguous in memory.

    If the array is not C contiguous, a copy will be necessary.

    Parameters
    ----------
    array : 1-D array
        The numpy array

    Returns
    -------
    array : 1-D array
        Array is C contiguous order.

    Examples
    --------

    >>> import numpy as np
    >>> data = np.array([[1, 2], [3, 4], [5, 6]])
    >>> x = data[:, 0]
    >>> x
    array([1, 3, 5])
    >>> x.flags.c_contiguous
    False
    >>> new_x = as_c_contiguous(x)
    >>> new_x
    array([1, 3, 5])
    >>> new_x.flags.c_contiguous
    True
    >>> x = np.array([8, 9, 10])
    >>> x.flags.c_contiguous
    True
    >>> as_c_contiguous(x).flags.c_contiguous
    True
    """
    if not array.flags.c_contiguous:
        return array.copy(order="C")
    return array


def kwargs_to_ctypes_array(argument, kwargs, dtype):
    """
    Convert an iterable argument from kwargs into a ctypes array variable.

    If the argument is not present in kwargs, returns ``None``.

    Parameters
    ----------
    argument : str
        The name of the argument.
    kwargs : dict
        Dictionary of keyword arguments.
    dtype : ctypes type
        The ctypes array type (e.g., ``ctypes.c_double*4``)

    Returns
    -------
    ctypes_value : ctypes array or None

    Examples
    --------

    >>> import ctypes as ct
    >>> value = kwargs_to_ctypes_array("bla", {"bla": [10, 10]}, ct.c_long * 2)
    >>> type(value)
    <class 'pygmt.clib.conversion.c_long_Array_2'>
    >>> should_be_none = kwargs_to_ctypes_array(
    ...     "swallow", {"bla": 1, "foo": [20, 30]}, ct.c_int * 2
    ... )
    >>> print(should_be_none)
    None
    """
    if argument in kwargs:
        return dtype(*kwargs[argument])
    return None


def array_to_datetime(array):
    """
    Convert a 1-D datetime array from various types into numpy.datetime64.

    If the input array is not in legal datetime formats, raise a ValueError
    exception.

    Parameters
    ----------
    array : list or 1-D array
        The input datetime array in various formats.

        Supported types:

        - str
        - numpy.datetime64
        - pandas.DateTimeIndex
        - datetime.datetime and datetime.date

    Returns
    -------
    array : 1-D datetime array in numpy.datetime64

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
