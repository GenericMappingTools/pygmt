"""
Miscellaneous utilities
"""
import sys
import ctypes

import numpy as np
import pandas

from ..exceptions import GMTOSError, GMTCLibError, GMTCLibNotFoundError


def vectors_to_arrays(vectors):
    """
    Convert 1d vectors (lists, arrays or pandas.Series) to C contiguous 1d
    arrays.

    Arrays must be in C contiguous order for us to pass their memory pointers
    to GMT. If any are not, convert them to C order (which requires copying the
    memory). This usually happens when vectors are columns of a 2d array or
    have been sliced.

    If a vector is a list or pandas.Series, get the underlying numpy array.

    Parameters
    ----------
    vectors : list of lists, 1d arrays or pandas.Series
        The vectors that must be converted.

    Returns
    -------
    arrays : list of 1d arrays
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

    """
    arrays = [_as_c_contiguous(_as_array(i)) for i in vectors]
    return arrays


def _as_c_contiguous(array):
    """
    Ensure a numpy array is C contiguous in memory.

    If the array is not C contiguous, a copy will be necessary.

    Parameters
    ----------
    array : 1d array
        The numpy array

    Returns
    -------
    array : 1d array
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
    >>> new_x = _as_c_contiguous(x)
    >>> new_x
    array([1, 3, 5])
    >>> new_x.flags.c_contiguous
    True
    >>> x = np.array([8, 9, 10])
    >>> x.flags.c_contiguous
    True
    >>> _as_c_contiguous(x).flags.c_contiguous
    True

    """
    if not array.flags.c_contiguous:
        return array.copy(order='C')
    return array


def _as_array(vector):
    """
    Convert a vector (pandas.Series, tuple, list or numpy array) to a numpy
    array.

    If vector is already an array, do nothing.

    Parameters
    ----------
    vector : tuple, list, pandas.Series or numpy 1d array
        The vector to convert.

    Returns
    -------
    array : numpy array

    Examples
    --------

    >>> import pandas as pd
    >>> x_series = pandas.Series(data=[1, 2, 3, 4])
    >>> x_array = _as_array(x_series)
    >>> type(x_array)
    <class 'numpy.ndarray'>
    >>> x_array
    array([1, 2, 3, 4])
    >>> import numpy as np
    >>> type(_as_array(np.array([5, 6, 7])))
    <class 'numpy.ndarray'>
    >>> type(_as_array([3, 4, 5]))
    <class 'numpy.ndarray'>
    >>> type(_as_array((6, 7, 8)))
    <class 'numpy.ndarray'>
    >>> type(_as_array(range(15)))
    <class 'numpy.ndarray'>

    """
    if isinstance(vector, pandas.Series):
        return vector.as_matrix()
    else:
        return np.asarray(vector)


def load_libgmt(libname='libgmt'):
    """
    Find and load ``libgmt`` as a :py:class:`ctypes.CDLL`.

    If not given the full path to the library, it must be in standard places or
    by discoverable by setting the environment variable ``LD_LIBRARY_PATH``.

    Parameters
    ----------
    libname : str
        The name of the GMT shared library **without the extension**. Can be a
        full path to the library or just the library name.

    Returns
    -------
    :py:class:`ctypes.CDLL` object
        The loaded shared library.

    Raises
    ------
    GMTCLibNotFoundError
        If there was any problem loading the library (couldn't find it or
        couldn't access the functions).

    """
    try:
        libgmt = ctypes.CDLL('.'.join([libname, clib_extension()]))
        check_libgmt(libgmt)
    except OSError as err:
        msg = ' '.join([
            "Couldn't find the GMT shared library '{}'.".format(libname),
            "Have you tried setting the LD_LIBRARY_PATH environment variable?",
            "\nOriginal error message:",
            "\n\n    {}".format(str(err)),
        ])
        raise GMTCLibNotFoundError(msg)
    return libgmt


def clib_extension(os_name=None):
    """
    Return the extension for the shared library for the current OS.

    .. warning::

        Currently only works for macOS and Linux.

    Returns
    -------
    os_name : str or None
        The operating system name as given by ``sys.platform``
        (the default if None).

    Returns
    -------
    ext : str
        The extension ('.so', '.dylib', etc).

    """
    if os_name is None:
        os_name = sys.platform
    # Set the shared library extension in a platform independent way
    if os_name.startswith('linux'):
        lib_ext = 'so'
    elif os_name == 'darwin':
        # Darwin is macOS
        lib_ext = 'dylib'
    else:
        raise GMTOSError(
            'Operating system "{}" not supported.'.format(sys.platform))
    return lib_ext


def check_libgmt(libgmt):
    """
    Make sure that libgmt was loaded correctly.

    Checks if it defines some common required functions.

    Does nothing if everything is fine. Raises an exception if any of the
    functions are missing.

    Parameters
    ----------
    libgmt : :py:class:`ctypes.CDLL`
        A shared library loaded using ctypes.

    Raises
    ------
    GMTCLibError

    """
    # Check if a few of the functions we need are in the library
    functions = ['Create_Session', 'Get_Enum', 'Call_Module',
                 'Destroy_Session']
    for func in functions:
        if not hasattr(libgmt, 'GMT_' + func):
            msg = ' '.join([
                "Error loading libgmt.",
                "Couldn't access function GMT_{}.".format(func),
            ])
            raise GMTCLibError(msg)


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
    >>> value = kwargs_to_ctypes_array('bla', {'bla': [10, 10]}, ct.c_int*2)
    >>> type(value)
    <class 'gmt.clib.utils.c_int_Array_2'>
    >>> b = 1
    >>> should_be_none = kwargs_to_ctypes_array(
    ...     'swallow', {'bla': 1, 'foo': [20, 30]}, ct.c_int*2)
    >>> print(should_be_none)
    None

    """
    if argument in kwargs:
        return dtype(*kwargs[argument])
    return None
