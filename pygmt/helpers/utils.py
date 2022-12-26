"""
Utilities and common tasks for wrapping the GMT modules.
"""
import os
import pathlib
import shutil
import subprocess
import sys
import time
import webbrowser
from collections.abc import Iterable
from contextlib import contextmanager

import xarray as xr
from pygmt.exceptions import GMTInvalidInput


def data_kind(data, x=None, y=None, z=None, required_z=False):
    """
    Check what kind of data is provided to a module.

    Possible types:

    * a file name provided as 'data'
    * a pathlib.Path provided as 'data'
    * an xarray.DataArray provided as 'data'
    * a matrix provided as 'data'
    * 1-D arrays x and y (and z, optionally)

    Arguments should be ``None`` if not used. If doesn't fit any of these
    categories (or fits more than one), will raise an exception.

    Parameters
    ----------
    data : str or pathlib.Path or xarray.DataArray or {table-like} or None
        Pass in either a file name or :class:`pathlib.Path` to an ASCII data
        table, an :class:`xarray.DataArray`, a 1-D/2-D
        {table-classes}.
    x/y : 1-D arrays or None
        x and y columns as numpy arrays.
    z : 1-D array or None
        z column as numpy array. To be used optionally when x and y are given.
    required_z : bool
        State whether the 'z' column is required.

    Returns
    -------
    kind : str
        One of: ``'file'``, ``'grid'``, ``'matrix'``, ``'vectors'``.

    Examples
    --------

    >>> import numpy as np
    >>> import xarray as xr
    >>> import pathlib
    >>> data_kind(data=None, x=np.array([1, 2, 3]), y=np.array([4, 5, 6]))
    'vectors'
    >>> data_kind(data=np.arange(10).reshape((5, 2)), x=None, y=None)
    'matrix'
    >>> data_kind(data="my-data-file.txt", x=None, y=None)
    'file'
    >>> data_kind(data=pathlib.Path("my-data-file.txt"), x=None, y=None)
    'file'
    >>> data_kind(data=xr.DataArray(np.random.rand(4, 3)))
    'grid'
    """
    if data is None and x is None and y is None:
        raise GMTInvalidInput("No input data provided.")
    if data is not None and (x is not None or y is not None or z is not None):
        raise GMTInvalidInput("Too much data. Use either data or x and y.")
    if data is None and (x is None or y is None):
        raise GMTInvalidInput("Must provide both x and y.")
    if data is None and required_z and z is None:
        raise GMTInvalidInput("Must provide x, y, and z.")

    if isinstance(data, (str, pathlib.PurePath)):
        kind = "file"
    elif isinstance(data, xr.DataArray):
        kind = "grid"
    elif hasattr(data, "__geo_interface__"):
        kind = "geojson"
    elif data is not None:
        if required_z and (
            getattr(data, "shape", (3, 3))[1] < 3  # np.array, pd.DataFrame
            or len(getattr(data, "data_vars", (0, 1, 2))) < 3  # xr.Dataset
        ):
            raise GMTInvalidInput("data must provide x, y, and z columns.")
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


def build_arg_string(kwdict, infile=None, outfile=None):
    r"""
    Convert a dict and optional input/output files into a GMT argument string.

    Make sure all values in ``kwdict`` have been previously converted to a
    string representation using the ``kwargs_to_strings`` decorator. The only
    exceptions are True, False and None.

    Any lists or tuples left will be interpreted as multiple entries for the
    same command line argument. For example, the kwargs entry ``'B': ['xa',
    'yaf']`` will be converted to ``-Bxa -Byaf`` in the argument string.

    Note that spaces `` `` in arguments are converted to the equivalent octal
    code ``\040``, except in the case of -J (projection) arguments where PROJ4
    strings (e.g. "+proj=longlat +datum=WGS84") will have their spaces removed.
    See https://github.com/GenericMappingTools/pygmt/pull/1487 for more info.

    Parameters
    ----------
    kwdict : dict
        A dict containing parsed keyword arguments.
    infile : str or pathlib.Path
        The input file.
    outfile : str or pathlib.Path
        The output file.

    Returns
    -------
    args : str
        The space-delimited argument string with '-' inserted before each
        keyword. The arguments are sorted alphabetically, with optional input
        file at the beginning and optional output file at the end.

    Examples
    --------

    >>> print(
    ...     build_arg_string(
    ...         dict(
    ...             A=True,
    ...             B=False,
    ...             E=200,
    ...             J="+proj=longlat +datum=WGS84",
    ...             P="",
    ...             R="1/2/3/4",
    ...             X=None,
    ...             Y=None,
    ...             Z=0,
    ...         )
    ...     )
    ... )
    -A -E200 -J+proj=longlat+datum=WGS84 -P -R1/2/3/4 -Z0
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
    >>> print(build_arg_string(dict(R="1/2/3/4", J="X4i", watre=True)))
    Traceback (most recent call last):
      ...
    pygmt.exceptions.GMTInvalidInput: Unrecognized parameter 'watre'.
    >>> print(
    ...     build_arg_string(
    ...         dict(
    ...             B=["af", "WSne+tBlank Space"],
    ...             F='+t"Empty  Spaces"',
    ...             l="'Void Space'",
    ...         ),
    ...     )
    ... )
    -BWSne+tBlank\040Space -Baf -F+t"Empty\040\040Spaces" -l'Void\040Space'
    >>> print(
    ...     build_arg_string(
    ...         dict(A="0", B=True, C="rainbow"),
    ...         infile="input.txt",
    ...         outfile="output.txt",
    ...     )
    ... )
    input.txt -A0 -B -Crainbow ->output.txt
    """
    gmt_args = []

    for key in kwdict:
        if len(key) > 2:  # raise an exception for unrecognized options
            raise GMTInvalidInput(f"Unrecognized parameter '{key}'.")
        if kwdict[key] is None or kwdict[key] is False:
            pass  # Exclude arguments that are None and False
        elif is_nonstr_iter(kwdict[key]):
            for value in kwdict[key]:
                _value = str(value).replace(" ", r"\040")
                gmt_args.append(rf"-{key}{_value}")
        elif kwdict[key] is True:
            gmt_args.append(f"-{key}")
        else:
            if key != "J":  # non-projection parameters
                _value = str(kwdict[key]).replace(" ", r"\040")
            else:
                # special handling if key == "J" (projection)
                # remove any spaces in PROJ4 string
                _value = str(kwdict[key]).replace(" ", "")
            gmt_args.append(rf"-{key}{_value}")
    gmt_args = sorted(gmt_args)
    if infile:
        gmt_args = [str(infile)] + gmt_args
    if outfile:
        gmt_args.append("->" + str(outfile))
    return " ".join(gmt_args)


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


def launch_external_viewer(fname, waiting=0):
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
    if waiting > 0:
        # suspend the execution for a few seconds to avoid the images being
        # deleted when a Python script exits
        time.sleep(waiting)


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

    Examples
    --------

    >>> args_in_kwargs(args=["A", "B"], kwargs={"C": "xyz"})
    False
    >>> args_in_kwargs(args=["A", "B"], kwargs={"B": "af"})
    True
    >>> args_in_kwargs(args=["A", "B"], kwargs={"B": None})
    False
    >>> args_in_kwargs(args=["A", "B"], kwargs={"B": True})
    True
    >>> args_in_kwargs(args=["A", "B"], kwargs={"B": False})
    False
    >>> args_in_kwargs(args=["A", "B"], kwargs={"B": 0})
    True
    """
    return any(
        kwargs.get(arg) is not None and kwargs.get(arg) is not False for arg in args
    )
