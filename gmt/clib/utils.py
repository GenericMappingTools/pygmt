"""
Miscellaneous utilities
"""
import sys
import ctypes

from ..exceptions import GMTOSError, GMTCLibError, GMTCLibNotFoundError


def load_libgmt(libname='libgmt'):
    """
    Find and load ``libgmt`` as a ctypes.CDLL.

    If not given the full path to the library, it must be in standard places or
    by discoverable by setting the environment variable ``LD_LIBRARY_PATH``.

    Parameters
    ----------
    libname : str
        The name of the GMT shared library **without the extension**. Can be a
        full path to the library or just the library name.

    Returns
    -------
    ctypes.CDLL object
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

        Currently only works for OSX and Linux.

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
        # Darwin is OSX
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
    libgmt : ctypes.CDLL
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


def check_status_code(status, function, logfile=None):
    """
    Check if the status code returned by a function is non-zero.

    Parameters
    ----------
    status : int or None
        The status code returned by a GMT C API function.
    function : str
        The name of the GMT function (used to raise the exception if it's a
        non-zero status code).

    Raises
    ------
    GMTCLibError
        If the status code is non-zero.

    """
    if status is None or status != 0:
        error_msg = ['Failed {} with status code {}.'.format(function, status)]
        if logfile is not None:
            with open(logfile) as log:
                error_msg.extend(log.readlines())
        raise GMTCLibError('\n'.join(error_msg))


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
