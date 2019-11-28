"""
Utilities and common tasks for wrapping the GMT modules.
"""
import sys
import shutil
import subprocess
import webbrowser
from contextlib import contextmanager

import xarray as xr

from ..exceptions import GMTInvalidInput


def data_kind(data, x=None, y=None, z=None):
    """
    Check what kind of data is provided to a module.

    Possible types:

    * a file name provided as 'data'
    * a matrix provided as 'data'
    * 1D arrays x and y (and z, optionally)

    Arguments should be ``None`` if not used. If doesn't fit any of these
    categories (or fits more than one), will raise an exception.

    Parameters
    ----------
    data : str, 2d array, or None
       Data file name or numpy array.
    x, y : 1d arrays or None
        x and y columns as numpy arrays.
    z    : 1d array or None
        z column as numpy array. To be used optionally when x and y
        are given.

    Returns
    -------
    kind : str
        One of: ``'file'``, ``'matrix'``, ``'vectors'``.

    Examples
    --------

    >>> import numpy as np
    >>> data_kind(data=None, x=np.array([1, 2, 3]), y=np.array([4, 5, 6]))
    'vectors'
    >>> data_kind(data=np.arange(10).reshape((5, 2)), x=None, y=None)
    'matrix'
    >>> data_kind(data='my-data-file.txt', x=None, y=None)
    'file'

    """
    if data is None and x is None and y is None:
        raise GMTInvalidInput("No input data provided.")
    if data is not None and (x is not None or y is not None or z is not None):
        raise GMTInvalidInput("Too much data. Use either data or x and y.")
    if data is None and (x is None or y is None):
        raise GMTInvalidInput("Must provided both x and y.")

    if isinstance(data, str):
        kind = "file"
    elif isinstance(data, xr.DataArray):
        kind = "grid"
    elif data is not None:
        kind = "matrix"
    else:
        kind = "vectors"
    return kind


@contextmanager
def dummy_context(arg):
    """
    Dummy context manager.

    Does nothing when entering or exiting a ``with`` block and yields the
    argument passed to it.

    Useful when you have a choice of context managers but need one that does
    nothing.

    Parameters
    ----------
    arg : anything
        The argument that will be returned by the context manager.

    Examples
    --------

    >>> with dummy_context('some argument') as temp:
    ...     print(temp)
    some argument

    """
    yield arg


def build_arg_string(kwargs):
    """
    Transform keyword arguments into a GMT argument string.

    Make sure all arguments have been previously converted to a string
    representation using the ``kwargs_to_strings`` decorator.

    Any lists or tuples left will be interpreted as multiple entries for the
    same command line argument. For example, the kwargs entry ``'B': ['xa',
    'yaf']`` will be converted to ``-Bxa -Byaf`` in the argument string.

    Parameters
    ----------
    kwargs : dict
        Parsed keyword arguments.

    Returns
    -------
    args : str
        The space-delimited argument string with '-' inserted before each
        keyword. The arguments are sorted alphabetically.

    Examples
    --------

    >>> print(build_arg_string(dict(R='1/2/3/4', J="X4i", P='', E=200)))
    -E200 -JX4i -P -R1/2/3/4
    >>> print(build_arg_string(dict(R='1/2/3/4', J="X4i",
    ...                             B=['xaf', 'yaf', 'WSen'],
    ...                             I=('1/1p,blue', '2/0.25p,blue'))))
    -Bxaf -Byaf -BWSen -I1/1p,blue -I2/0.25p,blue -JX4i -R1/2/3/4

    """
    sorted_args = []
    for key in sorted(kwargs):
        if is_nonstr_iter(kwargs[key]):
            for value in kwargs[key]:
                sorted_args.append("-{}{}".format(key, value))
        else:
            sorted_args.append("-{}{}".format(key, kwargs[key]))

    arg_str = " ".join(sorted_args)
    return arg_str


def is_nonstr_iter(value):
    """
    Check if the value is not a string but is iterable (list, tuple, array)

    Parameters
    ----------
    value
        What you want to check.

    Returns
    -------
    is_iterable : bool
        Whether it is a non-string iterable or not.

    Examples
    --------

    >>> is_nonstr_iter('abc')
    False
    >>> is_nonstr_iter(10)
    False
    >>> is_nonstr_iter([1, 2, 3])
    True
    >>> is_nonstr_iter((1, 2, 3))
    True

    """
    try:
        [item for item in value]  # pylint: disable=pointless-statement
        is_iterable = True
    except TypeError:
        is_iterable = False
    return bool(not isinstance(value, str) and is_iterable)


def launch_external_viewer(fname):
    """
    Open a file in an external viewer program.

    Uses the ``xdg-open`` command on Linux, the ``open`` command on macOS, and
    the default web browser on other systems.

    Parameters
    ----------
    fname : str
        The file name of the file (preferably a full path).

    """
    # Redirect stdout and stderr to devnull so that the terminal isn't filled
    # with noise
    run_args = dict(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Open the file with the default viewer.
    # Fall back to the browser if can't recognize the operating system.
    if sys.platform.startswith("linux") and shutil.which("xdg-open"):
        subprocess.run(["xdg-open", fname], **run_args)
    elif sys.platform == "darwin":  # Darwin is macOS
        subprocess.run(["open", fname], **run_args)
    else:
        webbrowser.open_new_tab("file://{}".format(fname))
