"""
Utilities and common tasks for wrapping the GMT modules.
"""

import io
import os
import pathlib
import shutil
import string
import subprocess
import sys
import time
import webbrowser
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any, Literal

import xarray as xr
from pygmt.encodings import charset
from pygmt.exceptions import GMTInvalidInput

# Type hints for the list of encodings supported by PyGMT.
Encoding = Literal[
    "ascii",
    "ISOLatin1+",
    "ISO-8859-1",
    "ISO-8859-2",
    "ISO-8859-3",
    "ISO-8859-4",
    "ISO-8859-5",
    "ISO-8859-6",
    "ISO-8859-7",
    "ISO-8859-8",
    "ISO-8859-9",
    "ISO-8859-10",
    "ISO-8859-11",
    "ISO-8859-13",
    "ISO-8859-14",
    "ISO-8859-15",
    "ISO-8859-16",
]


def _validate_data_input(
    data=None, x=None, y=None, z=None, required_z=False, required_data=True, kind=None
) -> None:
    """
    Check if the combination of data/x/y/z is valid.

    Examples
    --------
    >>> _validate_data_input(data="infile")
    >>> _validate_data_input(x=[1, 2, 3], y=[4, 5, 6])
    >>> _validate_data_input(x=[1, 2, 3], y=[4, 5, 6], z=[7, 8, 9])
    >>> _validate_data_input(data=None, required_data=False)
    >>> _validate_data_input()
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: No input data provided.
    >>> _validate_data_input(x=[1, 2, 3])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Must provide both x and y.
    >>> _validate_data_input(y=[4, 5, 6])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Must provide both x and y.
    >>> _validate_data_input(x=[1, 2, 3], y=[4, 5, 6], required_z=True)
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Must provide x, y, and z.
    >>> import numpy as np
    >>> import pandas as pd
    >>> import xarray as xr
    >>> data = np.arange(8).reshape((4, 2))
    >>> _validate_data_input(data=data, required_z=True, kind="matrix")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: data must provide x, y, and z columns.
    >>> _validate_data_input(
    ...     data=pd.DataFrame(data, columns=["x", "y"]),
    ...     required_z=True,
    ...     kind="vectors",
    ... )
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: data must provide x, y, and z columns.
    >>> _validate_data_input(
    ...     data=xr.Dataset(pd.DataFrame(data, columns=["x", "y"])),
    ...     required_z=True,
    ...     kind="vectors",
    ... )
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: data must provide x, y, and z columns.
    >>> _validate_data_input(data="infile", x=[1, 2, 3])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Too much data. Use either data or x/y/z.
    >>> _validate_data_input(data="infile", y=[4, 5, 6])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Too much data. Use either data or x/y/z.
    >>> _validate_data_input(data="infile", x=[1, 2, 3], y=[4, 5, 6])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Too much data. Use either data or x/y/z.
    >>> _validate_data_input(data="infile", z=[7, 8, 9])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Too much data. Use either data or x/y/z.

    Raises
    ------
    GMTInvalidInput
        If the data input is not valid.
    """
    if data is None:  # data is None
        if x is None and y is None:  # both x and y are None
            if required_data:  # data is not optional
                msg = "No input data provided."
                raise GMTInvalidInput(msg)
        elif x is None or y is None:  # either x or y is None
            msg = "Must provide both x and y."
            raise GMTInvalidInput(msg)
        if required_z and z is None:  # both x and y are not None, now check z
            msg = "Must provide x, y, and z."
            raise GMTInvalidInput(msg)
    else:  # data is not None
        if x is not None or y is not None or z is not None:
            msg = "Too much data. Use either data or x/y/z."
            raise GMTInvalidInput(msg)
        # check if data has the required z column
        if required_z:
            msg = "data must provide x, y, and z columns."
            if kind == "matrix" and data.shape[1] < 3:
                raise GMTInvalidInput(msg)
            if kind == "vectors":
                if hasattr(data, "shape") and (
                    (len(data.shape) == 1 and data.shape[0] < 3)
                    or (len(data.shape) > 1 and data.shape[1] < 3)
                ):  # np.ndarray or pd.DataFrame
                    raise GMTInvalidInput(msg)
                if hasattr(data, "data_vars") and len(data.data_vars) < 3:  # xr.Dataset
                    raise GMTInvalidInput(msg)


def _is_printable_ascii(argstr: str) -> bool:
    """
    Check if a string only contains printable ASCII characters.

    Here, printable ASCII characters are defined as the characters in the range of 32 to
    126 in the ASCII table. It's different from the ``string.printable`` constant that
    it doesn't include the control characters that are considered whitespace (tab,
    linefeed, return, formfeed, and vertical tab).

    Parameters
    ----------
    argstr
        The string to be checked.

    Returns
    -------
    ``True`` if the string only contains printable ASCII characters. Otherwise, return
    ``False``.

    Examples
    --------
    >>> _is_printable_ascii("123ABC+-?!")
    True
    >>> _is_printable_ascii("12AB±β①②")
    False
    """
    return all(32 <= ord(c) <= 126 for c in argstr)


def _contains_apostrophe_or_backtick(argstr: str) -> bool:
    """
    Check if a string contains apostrophe (') or backtick (`).

    For typographical reasons, apostrophe (') and backtick (`) are mapped to left and
    right single quotation marks (‘ and ’) in Adobe ISOLatin1+ encoding. To ensure that
    what you type is what you get (issue #3476), they need special handling in the
    ``_check_encoding`` and ``non_ascii_to_octal`` functions. More specifically, a
    string containing printable ASCII characters with apostrophe (') and backtick (`)
    will not be considered as "ascii" encoding.

    Parameters
    ----------
    argstr
        The string to be checked.

    Returns
    -------
    ``True`` if the string contains apostrophe (') or backtick (`). Otherwise, return
    ``False``.

    Examples
    --------
    >>> _contains_apostrophe_or_backtick("12AB±β①②")
    False
    >>> _contains_apostrophe_or_backtick("12AB`")
    True
    >>> _contains_apostrophe_or_backtick("12AB'")
    True
    >>> _contains_apostrophe_or_backtick("12AB'`")
    True
    """  # noqa: RUF002
    return "'" in argstr or "`" in argstr


def _check_encoding(argstr: str) -> Encoding:
    """
    Check the charset encoding of a string.

    All characters in the string must be in the same charset encoding, otherwise the
    default ``ISOLatin1+`` encoding is returned. Characters in the Adobe Symbol and
    ZapfDingbats encodings are also checked because they're independent on the choice of
    encodings.

    Parameters
    ----------
    argstr
        The string to be checked.

    Returns
    -------
    encoding
        The encoding of the string.

    Examples
    --------
    >>> _check_encoding("123ABC+-?!")  # ASCII characters only
    'ascii'
    >>> _check_encoding("12AB±β①②")  # Characters in ISOLatin1+
    'ISOLatin1+'
    >>> _check_encoding("12ABāáâãäåβ①②")  # Characters in ISO-8859-4
    'ISO-8859-4'
    >>> _check_encoding("12ABŒā")  # Mix characters in ISOLatin1+ (Œ) and ISO-8859-4 (ā)
    'ISOLatin1+'
    >>> _check_encoding("123AB中文")  # Characters not in any charset encoding
    'ISOLatin1+'
    """
    # Return "ascii" if the string only contains printable ASCII characters, excluding
    # apostrophe (') and backtick (`).
    if _is_printable_ascii(argstr) and not _contains_apostrophe_or_backtick(argstr):
        return "ascii"
    # Loop through all supported encodings and check if all characters in the string
    # are in the charset of the encoding. If all characters are in the charset, return
    # the encoding. The ISOLatin1+ encoding is checked first because it is the default
    # and most common encoding.
    adobe_chars = set(charset["Symbol"].values()) | set(
        charset["ZapfDingbats"].values()
    )
    for encoding in ["ISOLatin1+"] + [f"ISO-8859-{i}" for i in range(1, 17) if i != 12]:
        chars = set(charset[encoding].values()) | adobe_chars
        if all(c in chars for c in argstr):
            return encoding  # type: ignore[return-value]
    # Return the "ISOLatin1+" encoding if the string contains characters from multiple
    # charset encodings or contains characters that are not in any charset encoding.
    return "ISOLatin1+"


def data_kind(
    data: Any, required: bool = True
) -> Literal[
    "arg", "empty", "file", "geojson", "grid", "image", "matrix", "stringio", "vectors"
]:
    r"""
    Check the kind of data that is provided to a module.

    The argument passed to the ``data`` parameter can have any data type. The following
    data kinds are recognized and returned as ``kind``:

    - ``"arg"``: ``data`` is ``None`` and ``required=False``, or bool, int, float,
      representing an optional argument, used for dealing with optional virtual files
    - ``"empty"`: ``data`` is ``None`` and ``required=True``. It means the data is given
      via a series of vectors like x/y/z
    - ``"file"``: a string or a :class:`pathlib.PurePath` object or a sequence of them,
      representing one or more file names
    - ``"geojson"``: a geo-like Python object that implements ``__geo_interface__``
      (e.g., geopandas.GeoDataFrame or shapely.geometry)
    - ``"grid"``: a :class:`xarray.DataArray` object that is not 3-D
    - ``"image"``: a 3-D :class:`xarray.DataArray` object
    - ``"stringio"``: a :class:`io.StringIO` object
    - ``"matrix"``: a 2-D array-like object that implements ``__array_interface__``
      (e.g., :class:`numpy.ndarray`)
    - ``"vectors"``: any unrecognized data. Common data types include, a
      :class:`pandas.DataFrame` object, a dictionary with array-like values, a 1-D/3-D
      :class:`numpy.ndarray` object, or array-like objects

    Parameters
    ----------
    data
        The data to be passed to a GMT module.
    required
        Whether 'data' is required. Set to ``False`` when dealing with optional virtual
        files.

    Returns
    -------
    kind
        The data kind.

    Examples
    --------
    >>> import io
    >>> from pathlib import Path
    >>> import numpy as np
    >>> import pandas as pd
    >>> import xarray as xr

    The "arg" kind:

    >>> [data_kind(data=data, required=False) for data in (2, 2.0, True, False)]
    ['arg', 'arg', 'arg', 'arg']
    >>> data_kind(data=None, required=False)
    'arg'

    The "empty" kind:

    >>> data_kind(data=None, required=True)
    'empty'

    The "file" kind:

    >>> [data_kind(data=data) for data in ("file.txt", ("file1.txt", "file2.txt"))]
    ['file', 'file']
    >>> data_kind(data=Path("file.txt"))
    'file'
    >>> data_kind(data=(Path("file1.txt"), Path("file2.txt")))
    'file'

    The "grid" kind:

    >>> data_kind(data=xr.DataArray(np.random.rand(4, 3)))  # 2-D xarray.DataArray
    'grid'
    >>> data_kind(data=xr.DataArray(np.arange(12)))  # 1-D xarray.DataArray
    'grid'
    >>> data_kind(data=xr.DataArray(np.random.rand(2, 3, 4, 5)))  # 4-D xarray.DataArray
    'grid'

    The "image" kind:

    >>> data_kind(data=xr.DataArray(np.random.rand(3, 4, 5)))  # 3-D xarray.DataArray
    'image'

    The "stringio" kind:

    >>> data_kind(data=io.StringIO("TEXT1\nTEXT23\n"))
    'stringio'

    The "matrix" kind:

    >>> data_kind(data=np.arange(10).reshape((5, 2)))  # 2-D numpy.ndarray
    'matrix'

    The "vectors" kind:

    >>> data_kind(data=np.arange(10))  # 1-D numpy.ndarray
    'vectors'
    >>> data_kind(data=np.arange(60).reshape((3, 4, 5)))  # 3-D numpy.ndarray
    'vectors'
    >>> data_kind(xr.DataArray(np.arange(12), name="x").to_dataset())  # xarray.Dataset
    'vectors'
    >>> data_kind(data=[1, 2, 3])  # 1-D sequence
    'vectors'
    >>> data_kind(data=[[1, 2, 3], [4, 5, 6]])  # sequence of sequences
    'vectors'
    >>> data_kind(data={"x": [1, 2, 3], "y": [4, 5, 6]})  # dictionary
    'vectors'
    >>> data_kind(data=pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]}))  # pd.DataFrame
    'vectors'
    >>> data_kind(data=pd.Series([1, 2, 3], name="x"))  # pd.Series
    'vectors'
    """
    match data:
        case None if required:  # No data provided and required=True.
            kind = "empty"
        case str() | pathlib.PurePath():  # One file.
            kind = "file"
        case list() | tuple() if all(
            isinstance(_file, str | pathlib.PurePath) for _file in data
        ):  # A list/tuple of files.
            kind = "file"
        case io.StringIO():
            kind = "stringio"
        case (bool() | int() | float()) | None if not required:
            # An option argument, mainly for dealing with optional virtual files.
            kind = "arg"
        case xr.DataArray():
            # An xarray.DataArray object, representing either a grid or an image.
            kind = "image" if len(data.dims) == 3 else "grid"
        case x if hasattr(x, "__geo_interface__"):
            # Geo-like Python object that implements ``__geo_interface__`` (e.g.,
            # geopandas.GeoDataFrame or shapely.geometry).
            # Reference: https://gist.github.com/sgillies/2217756
            kind = "geojson"
        case x if hasattr(x, "__array_interface__") and data.ndim == 2:
            # 2-D Array-like objects that implements ``__array_interface__`` (e.g.,
            # numpy.ndarray).
            # Reference: https://numpy.org/doc/stable/reference/arrays.interface.html
            kind = "matrix"
        case _:  # Fall back to "vectors" if data is None and required=True.
            kind = "vectors"
    return kind  # type: ignore[return-value]


def non_ascii_to_octal(argstr: str, encoding: Encoding = "ISOLatin1+") -> str:
    r"""
    Translate non-ASCII characters to their corresponding octal codes.

    Currently, only non-ASCII characters in the Adobe ISOLatin1+, Adobe Symbol, Adobe
    ZapfDingbats, and ISO-8850-x (x can be in 1-11, 13-17) encodings are supported.
    The Adobe Standard+ encoding is not supported.

    Parameters
    ----------
    argstr
        The string to be translated.
    encoding
        The encoding of characters in the string.

    Returns
    -------
    translated_argstr
        The translated string.

    Examples
    --------
    >>> non_ascii_to_octal("•‰“”±°ÿ")
    '\\031\\214\\216\\217\\261\\260\\377'
    >>> non_ascii_to_octal("αζ∆Ω∑π∇")
    '@~\\141@~@~\\172@~@~\\104@~@~\\127@~@~\\345@~@~\\160@~@~\\321@~'
    >>> non_ascii_to_octal("✁❞❡➾")
    '@%34%\\041@%%@%34%\\176@%%@%34%\\241@%%@%34%\\376@%%'
    >>> non_ascii_to_octal("ABC ±120° DEF α ♥")
    'ABC \\261120\\260 DEF @~\\141@~ @%34%\\252@%%'
    >>> non_ascii_to_octal("12ABāáâãäåβ①②", encoding="ISO-8859-4")
    '12AB\\340\\341\\342\\343\\344\\345@~\\142@~@%34%\\254@%%@%34%\\255@%%'
    >>> non_ascii_to_octal("'‘’\"“”")
    '\\234\\140\\047"\\216\\217'
    """  # noqa: RUF002
    # Return the input string if it only contains printable ASCII characters, excluding
    # apostrophe (') and backtick (`).
    if encoding == "ascii" or (
        _is_printable_ascii(argstr) and not _contains_apostrophe_or_backtick(argstr)
    ):
        return argstr

    # Dictionary mapping non-ASCII characters to octal codes
    mapping: dict = {}
    # Adobe Symbol charset.
    mapping.update({c: f"@~\\{i:03o}@~" for i, c in charset["Symbol"].items()})
    # Adobe ZapfDingbats charset. Font number is 34.
    mapping.update(
        {c: f"@%34%\\{i:03o}@%%" for i, c in charset["ZapfDingbats"].items()}
    )
    # ISOLatin1+ or ISO-8859-x charset.
    mapping.update({c: f"\\{i:03o}" for i, c in charset[encoding].items()})

    # Remove any printable characters.
    mapping = {k: v for k, v in mapping.items() if k not in string.printable}

    if encoding == "ISOLatin1+":
        # Map apostrophe (') and backtick (`) to correct octal codes.
        # See _contains_apostrophe_or_backtick() for explanations.
        mapping.update({"'": "\\234", "`": "\\221"})
    return argstr.translate(str.maketrans(mapping))


def build_arg_list(  # noqa: PLR0912
    kwdict: dict[str, Any],
    confdict: Mapping[str, Any] | None = None,
    infile: str | pathlib.PurePath | Sequence[str | pathlib.PurePath] | None = None,
    outfile: str | pathlib.PurePath | None = None,
) -> list[str]:
    r"""
    Convert keyword dictionaries and input/output files into a list of GMT arguments.

    Make sure all values in ``kwdict`` have been previously converted to a string
    representation using the ``kwargs_to_strings`` decorator. The only exceptions are
    ``True``, ``False`` and ``None``.

    Any remaining lists or tuples will be interpreted as multiple entries for the same
    parameter. For example, the kwargs entry ``"B": ["xa", "yaf"]`` will be
    converted to ``["-Bxa", "-Byaf"]``.

    Parameters
    ----------
    kwdict
        A dictionary containing parsed keyword arguments.
    confdict
        A dictionary containing configurable GMT parameters.
    infile
        The input file or a list of input files.
    outfile
        The output file.

    Returns
    -------
    args
        The list of command line arguments that will be passed to GMT modules. The
        keyword arguments are sorted alphabetically, followed by GMT configuration
        key-value pairs, with optional input file(s) at the beginning and optional
        output file at the end.

    Examples
    --------
    >>> build_arg_list(dict(A=True, B=False, C=None, D=0, E=200, F="", G="1/2/3/4"))
    ['-A', '-D0', '-E200', '-F', '-G1/2/3/4']
    >>> build_arg_list(dict(A="1/2/3/4", B=["xaf", "yaf", "WSen"], C=("1p", "2p")))
    ['-A1/2/3/4', '-BWSen', '-Bxaf', '-Byaf', '-C1p', '-C2p']
    >>> build_arg_list(dict(B=["af", "WSne+tBlank Space"]))
    ['-BWSne+tBlank Space', '-Baf']
    >>> build_arg_list(dict(F='+t"Empty Spaces"'))
    ['-F+t"Empty Spaces"']
    >>> build_arg_list(dict(l="'Void Space'"))
    ['-l\\234Void Space\\234', '--PS_CHAR_ENCODING=ISOLatin1+']
    >>> print(
    ...     build_arg_list(
    ...         dict(A="0", B=True, C="rainbow"),
    ...         confdict=dict(FORMAT_DATE_MAP="o dd"),
    ...         infile="input.txt",
    ...         outfile="output.txt",
    ...     )
    ... )
    ['input.txt', '-A0', '-B', '-Crainbow', '--FORMAT_DATE_MAP=o dd', '->output.txt']
    >>> print(
    ...     build_arg_list(
    ...         dict(A="0", B=True),
    ...         confdict=dict(FORMAT_DATE_MAP="o dd"),
    ...         infile=["f1.txt", "f2.txt"],
    ...         outfile="out.txt",
    ...     )
    ... )
    ['f1.txt', 'f2.txt', '-A0', '-B', '--FORMAT_DATE_MAP=o dd', '->out.txt']
    >>> build_arg_list(dict(B="12ABāβ①②"))
    ['-B12AB\\340@~\\142@~@%34%\\254@%%@%34%\\255@%%', '--PS_CHAR_ENCODING=ISO-8859-4']
    >>> build_arg_list(dict(B="12ABāβ①②"), confdict=dict(PS_CHAR_ENCODING="ISO-8859-5"))
    ['-B12AB\\340@~\\142@~@%34%\\254@%%@%34%\\255@%%', '--PS_CHAR_ENCODING=ISO-8859-5']
    >>> print(build_arg_list(dict(R="1/2/3/4", J="X4i", watre=True)))
    Traceback (most recent call last):
      ...
    pygmt.exceptions.GMTInvalidInput: Unrecognized parameter 'watre'.
    """
    gmt_args = []
    for key, value in kwdict.items():
        if len(key) > 2:  # Raise an exception for unrecognized options
            msg = f"Unrecognized parameter '{key}'."
            raise GMTInvalidInput(msg)
        if value is None or value is False:  # Exclude arguments that are None or False
            pass
        elif value is True:
            gmt_args.append(f"-{key}")
        elif is_nonstr_iter(value):
            gmt_args.extend(f"-{key}{_value}" for _value in value)
        else:
            gmt_args.append(f"-{key}{value}")

    gmt_args = sorted(gmt_args)

    # Convert non-ASCII characters (if any) in the arguments to octal codes and set
    # --PS_CHAR_ENCODING=encoding if necessary
    if (encoding := _check_encoding("".join(gmt_args))) != "ascii":
        gmt_args = [non_ascii_to_octal(arg, encoding=encoding) for arg in gmt_args]
        if not (confdict and "PS_CHAR_ENCODING" in confdict):
            gmt_args.append(f"--PS_CHAR_ENCODING={encoding}")

    if confdict:
        gmt_args.extend(f"--{key}={value}" for key, value in confdict.items())

    if infile:  # infile can be a single file or a list of files
        if isinstance(infile, str | pathlib.PurePath):
            gmt_args = [str(infile), *gmt_args]
        else:
            gmt_args = [str(_file) for _file in infile] + gmt_args
    if outfile is not None:
        if (
            not isinstance(outfile, str | pathlib.PurePath)
            or str(outfile) in {"", ".", ".."}
            or str(outfile).endswith(("/", "\\"))
        ):
            msg = f"Invalid output file name '{outfile}'."
            raise GMTInvalidInput(msg)
        gmt_args.append(f"->{outfile}")
    return gmt_args


def is_nonstr_iter(value: Any) -> bool:
    """
    Check if the value is iterable (e.g., list, tuple, array) but not a string.

    Parameters
    ----------
    value
        What you want to check.

    Returns
    -------
    is_iterable
        Whether it is a non-string iterable or not.

    Examples
    --------
    >>> is_nonstr_iter("abc")
    False
    >>> is_nonstr_iter(10)
    False
    >>> is_nonstr_iter(None)
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


def launch_external_viewer(fname: str, waiting: float = 0) -> None:
    """
    Open a file in an external viewer program.

    Uses the ``xdg-open`` command on Linux/FreeBSD, the ``open`` command on macOS, the
    associated application on Windows, and the default web browser on other systems.

    Parameters
    ----------
    fname
        The file name of the file (preferably a full path).
    waiting
        Wait for a few seconds before exiting the function, to allow the external viewer
        open the file before it's deleted.
    """
    # Redirect stdout and stderr to devnull so that the terminal isn't filled with noise
    run_args = {
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }

    match sys.platform:
        case name if (name == "linux" or name.startswith("freebsd")) and (
            xdgopen := shutil.which("xdg-open")
        ):  # Linux/FreeBSD
            subprocess.run([xdgopen, fname], check=False, **run_args)  # type:ignore[call-overload]
        case "darwin":  # macOS
            subprocess.run([shutil.which("open"), fname], check=False, **run_args)  # type:ignore[call-overload]
        case "win32":  # Windows
            os.startfile(fname)  # type:ignore[attr-defined] # noqa: S606
        case _:  # Fall back to the browser if can't recognize the operating system.
            webbrowser.open_new_tab(f"file://{Path(fname).resolve()}")
    if waiting > 0:
        # Preview images will be deleted when a GMT modern-mode session ends, but the
        # external viewer program may take a few seconds to open the images.
        # Suspend the execution for a few seconds.
        time.sleep(waiting)


def args_in_kwargs(args: Sequence[str], kwargs: dict[str, Any]) -> bool:
    """
    Take a sequence and a dictionary, and determine if any entries in the sequence are
    keys in the dictionary.

    This function is used to determine if at least one of the required arguments is
    passed to raise a GMTInvalidInput Error.

    Parameters
    ----------
    args
        Sequence of required arguments, using the GMT short-form aliases.
    kwargs
        The dictionary of GMT options and arguments. The keys are the GMT short-form
        aliases of the parameters.

    Returns
    -------
    bool
        Whether one of the required arguments is in ``kwargs``.

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
