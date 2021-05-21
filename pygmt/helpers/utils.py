"""
Utilities and common tasks for wrapping the GMT modules.
"""
import os
import shutil
import subprocess
import sys
import time
import webbrowser
from collections.abc import Iterable
from contextlib import contextmanager

import xarray as xr
from pygmt.exceptions import GMTInvalidInput


def data_kind(data, x=None, y=None, z=None):
    """
    Check what kind of data is provided to a module.

    Possible types:

    * a file name provided as 'data'
    * an xarray.DataArray provided as 'data'
    * a matrix provided as 'data'
    * 1D arrays x and y (and z, optionally)

    Arguments should be ``None`` if not used. If doesn't fit any of these
    categories (or fits more than one), will raise an exception.

    Parameters
    ----------
    data : str or xarray.DataArray or {table-like} or None
        Pass in either a file name to an ASCII data table, an
        :class:`xarray.DataArray`, a 1D/2D
        {table-classes}.
    x/y : 1d arrays or None
        x and y columns as numpy arrays.
    z : 1d array or None
        z column as numpy array. To be used optionally when x and y
        are given.

    Returns
    -------
    kind : str
        One of: ``'file'``, ``'grid'``, ``'matrix'``, ``'vectors'``.

    Examples
    --------

    >>> import numpy as np
    >>> import xarray as xr
    >>> data_kind(data=None, x=np.array([1, 2, 3]), y=np.array([4, 5, 6]))
    'vectors'
    >>> data_kind(data=np.arange(10).reshape((5, 2)), x=None, y=None)
    'matrix'
    >>> data_kind(data="my-data-file.txt", x=None, y=None)
    'file'
    >>> data_kind(data=xr.DataArray(np.random.rand(4, 3)))
    'grid'
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
    elif hasattr(data, "__geo_interface__"):
        kind = "geojson"
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

    >>> with dummy_context("some argument") as temp:
    ...     print(temp)
    ...
    some argument
    """
    yield arg


def build_arg_string(kwargs):
    """
    Transform keyword arguments into a GMT argument string.

    Make sure all arguments have been previously converted to a string
    representation using the ``kwargs_to_strings`` decorator. The only
    exceptions are True, False and None.

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

    >>> print(
    ...     build_arg_string(
    ...         dict(
    ...             A=True,
    ...             B=False,
    ...             E=200,
    ...             J="X4c",
    ...             P="",
    ...             R="1/2/3/4",
    ...             X=None,
    ...             Y=None,
    ...             Z=0,
    ...         )
    ...     )
    ... )
    -A -E200 -JX4c -P -R1/2/3/4 -Z0
    >>> print(
    ...     build_arg_string(
    ...         dict(
    ...             R="1/2/3/4",
    ...             J="X4i",
    ...             B=["xaf", "yaf", "WSen"],
    ...             I=("1/1p,blue", "2/0.25p,blue"),
    ...         )
    ...     )
    ... )
    -BWSen -Bxaf -Byaf -I1/1p,blue -I2/0.25p,blue -JX4i -R1/2/3/4
    """
    gmt_args = []
    # Exclude arguments that are None and False
    filtered_kwargs = {
        k: v for k, v in kwargs.items() if (v is not None and v is not False)
    }
    for key in filtered_kwargs:
        if is_nonstr_iter(kwargs[key]):
            for value in kwargs[key]:
                gmt_args.append(f"-{key}{value}")
        elif kwargs[key] is True:
            gmt_args.append(f"-{key}")
        else:
            gmt_args.append(f"-{key}{kwargs[key]}")
    return " ".join(sorted(gmt_args))


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

    >>> is_nonstr_iter("abc")
    False
    >>> is_nonstr_iter(10)
    False
    >>> is_nonstr_iter([1, 2, 3])
    True
    >>> is_nonstr_iter((1, 2, 3))
    True
    >>> import numpy as np
    >>> is_nonstr_iter(np.array([1.0, 2.0, 3.0]))
    True
    >>> is_nonstr_iter(np.array(["abc", "def", "ghi"]))
    True
    """
    return isinstance(value, Iterable) and not isinstance(value, str)


def launch_external_viewer(fname):
    """
    Open a file in an external viewer program.

    Uses the ``xdg-open`` command on Linux, the ``open`` command on macOS, the
    associated application on Windows, and the default web browser on other
    systems.

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
    os_name = sys.platform
    if os_name.startswith(("linux", "freebsd")) and shutil.which("xdg-open"):
        subprocess.run(["xdg-open", fname], check=False, **run_args)
    elif os_name == "darwin":  # Darwin is macOS
        subprocess.run(["open", fname], check=False, **run_args)
    elif os_name == "win32":
        os.startfile(fname)  # pylint: disable=no-member
    else:
        webbrowser.open_new_tab(f"file://{fname}")
    # suspend the execution for 0.5 s to avoid the images being deleted
    # when a Python script exits
    time.sleep(0.5)


def args_in_kwargs(args, kwargs):
    """
    Take a list and a dictionary, and determine if any entries in the list are
    keys in the dictionary.

    This function is used to determine if at least one of the required
    arguments is passed to raise a GMTInvalidInput Error.

    Parameters
    ----------
    args : list
        List of required arguments, using the GMT short-form aliases.

    kwargs : dict
        The dictionary of kwargs is the format returned by the _preprocess
        function of the BasePlotting class. The keys are the GMT
        short-form aliases of the parameters.

    Returns
    --------
    bool
        If one of the required arguments is in ``kwargs``.
    """
    return any(arg in kwargs for arg in args)
