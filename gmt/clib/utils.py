"""
Miscellaneous utilities
"""
import sys

from ..exceptions import GMTOSError, GMTCLibError


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
        raise GMTOSError('Unknown operating system: {}'.format(sys.platform))
    return lib_ext


def check_status_code(status, function):
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
        raise GMTCLibError(
            'Failed {} with status code {}.'.format(function, status))
