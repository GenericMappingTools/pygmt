"""
Utilities and common tasks for wrapping the GMT modules.
"""

import os
import pathlib
import shutil
import string
import subprocess
import sys
import time
import warnings
import webbrowser
from collections.abc import Iterable, Sequence
from typing import Any, Literal

import xarray as xr
from pygmt.encodings import charset
from pygmt.exceptions import GMTInvalidInput


def _validate_data_input(
    data=None, x=None, y=None, z=None, required_z=False, required_data=True, kind=None
):
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
    ...     kind="matrix",
    ... )
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: data must provide x, y, and z columns.
    >>> _validate_data_input(
    ...     data=xr.Dataset(pd.DataFrame(data, columns=["x", "y"])),
    ...     required_z=True,
    ...     kind="matrix",
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
                raise GMTInvalidInput("No input data provided.")
        elif x is None or y is None:  # either x or y is None
            raise GMTInvalidInput("Must provide both x and y.")
        if required_z and z is None:  # both x and y are not None, now check z
            raise GMTInvalidInput("Must provide x, y, and z.")
    else:  # data is not None
        if x is not None or y is not None or z is not None:
            raise GMTInvalidInput("Too much data. Use either data or x/y/z.")
        # For 'matrix' kind, check if data has the required z column
        if kind == "matrix" and required_z:
            if hasattr(data, "shape"):  # np.ndarray or pd.DataFrame
                if len(data.shape) == 1 and data.shape[0] < 3:
                    raise GMTInvalidInput("data must provide x, y, and z columns.")
                if len(data.shape) > 1 and data.shape[1] < 3:
                    raise GMTInvalidInput("data must provide x, y, and z columns.")
            if hasattr(data, "data_vars") and len(data.data_vars) < 3:  # xr.Dataset
                raise GMTInvalidInput("data must provide x, y, and z columns.")


def _check_encoding(
    argstr: str,
) -> Literal[
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
]:
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
    # Return "ascii" if the string only contains ASCII characters.
    if all(32 <= ord(c) <= 126 for c in argstr):
        return "ascii"
    # Loop through all supported encodings and check if all characters in the string
    # are in the charset of the encoding. If all characters are in the charset, return
    # the encoding. The ISOLatin1+ encoding is checked first because it is the default
    # and most common encoding.
    adobe_chars = set(charset["Symbol"].values()) | set(
        charset["ZapfDingbats"].values()
    )
    for encoding in ["ISOLatin1+"] + [f"ISO-8859-{i}" for i in range(1, 17)]:
        if encoding == "ISO-8859-12":  # ISO-8859-12 was abandoned. Skip it.
            continue
        if all(c in (set(charset[encoding].values()) | adobe_chars) for c in argstr):
            return encoding  # type: ignore[return-value]
    # Return the "ISOLatin1+" encoding if the string contains characters from multiple
    # charset encodings or contains characters that are not in any charset encoding.
    return "ISOLatin1+"


def data_kind(
    data: Any = None, required: bool = True
) -> Literal["arg", "file", "geojson", "grid", "image", "matrix", "vectors"]:
    """
    Check the kind of data that is provided to a module.

    The ``data`` argument can be in any type, but only following types are supported:

    - a string or a :class:`pathlib.PurePath` object or a sequence of them, representing
      a file name or a list of file names
    - a 2-D or 3-D :class:`xarray.DataArray` object
    - a 2-D matrix
    - None, bool, int or float type representing an optional arguments
    - a geo-like Python object that implements ``__geo_interface__`` (e.g.,
      geopandas.GeoDataFrame or shapely.geometry)

    Parameters
    ----------
    data : str, pathlib.PurePath, None, bool, xarray.DataArray or {table-like}
        Pass in either a file name or :class:`pathlib.Path` to an ASCII data
        table, an :class:`xarray.DataArray`, a 1-D/2-D
        {table-classes} or an option argument.
    required
        Set to True when 'data' is required, or False when dealing with
        optional virtual files. [Default is True].

    Returns
    -------
    kind
        The data kind.

    Examples
    --------
    >>> import numpy as np
    >>> import xarray as xr
    >>> import pathlib
    >>> data_kind(data=None)
    'vectors'
    >>> data_kind(data=np.arange(10).reshape((5, 2)))
    'matrix'
    >>> data_kind(data="my-data-file.txt")
    'file'
    >>> data_kind(data=pathlib.Path("my-data-file.txt"))
    'file'
    >>> data_kind(data=None, required=False)
    'arg'
    >>> data_kind(data=2.0, required=False)
    'arg'
    >>> data_kind(data=True, required=False)
    'arg'
    >>> data_kind(data=xr.DataArray(np.random.rand(4, 3)))
    'grid'
    >>> data_kind(data=xr.DataArray(np.random.rand(3, 4, 5)))
    'image'
    """
    kind: Literal["arg", "file", "geojson", "grid", "image", "matrix", "vectors"]
    if isinstance(data, str | pathlib.PurePath) or (
        isinstance(data, list | tuple)
        and all(isinstance(_file, str | pathlib.PurePath) for _file in data)
    ):
        # One or more files
        kind = "file"
    elif isinstance(data, bool | int | float) or (data is None and not required):
        kind = "arg"
    elif isinstance(data, xr.DataArray):
        kind = "image" if len(data.dims) == 3 else "grid"
    elif hasattr(data, "__geo_interface__"):
        # geo-like Python object that implements ``__geo_interface__``
        # (geopandas.GeoDataFrame or shapely.geometry)
        kind = "geojson"
    elif data is not None:
        kind = "matrix"
    else:
        kind = "vectors"
    return kind


def non_ascii_to_octal(
    argstr: str,
    encoding: Literal[
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
    ] = "ISOLatin1+",
) -> str:
    r"""
    Translate non-ASCII characters to their corresponding octal codes.

    Currently, only non-ASCII characters in the Adobe ISOLatin1+, Adobe Symbol, Adobe
    ZapfDingbats, and ISO-8850-x (x can be in 1-11, 13-17) encodings are supported.
    The Adobe Standard encoding is not supported yet.

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
    """  # noqa: RUF002
    # Return the input string if it only contains ASCII characters.
    if encoding == "ascii" or all(32 <= ord(c) <= 126 for c in argstr):
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

    # Remove any printable characters
    mapping = {k: v for k, v in mapping.items() if k not in string.printable}
    return argstr.translate(str.maketrans(mapping))


def build_arg_list(  # noqa: PLR0912
    kwdict: dict[str, Any],
    confdict: dict[str, str] | None = None,
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
    >>> print(
    ...     build_arg_list(
    ...         dict(
    ...             B=["af", "WSne+tBlank Space"],
    ...             F='+t"Empty Spaces"',
    ...             l="'Void Space'",
    ...         )
    ...     )
    ... )
    ['-BWSne+tBlank Space', '-Baf', '-F+t"Empty Spaces"', "-l'Void Space'"]
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
            raise GMTInvalidInput(f"Unrecognized parameter '{key}'.")
        if value is None or value is False:  # Exclude arguments that are None or False
            pass
        elif value is True:
            gmt_args.append(f"-{key}")
        elif is_nonstr_iter(value):
            gmt_args.extend(f"-{key}{_value}" for _value in value)
        else:
            gmt_args.append(f"-{key}{value}")

    # Convert non-ASCII characters (if any) in the arguments to octal codes
    encoding = _check_encoding("".join(gmt_args))
    if encoding != "ascii":
        gmt_args = [non_ascii_to_octal(arg, encoding=encoding) for arg in gmt_args]
    gmt_args = sorted(gmt_args)

    # Set --PS_CHAR_ENCODING=encoding if necessary
    if encoding not in {"ascii", "ISOLatin1+"} and not (
        confdict and "PS_CHAR_ENCODING" in confdict
    ):
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
            raise GMTInvalidInput(f"Invalid output file name '{outfile}'.")
        gmt_args.append(f"->{outfile}")
    return gmt_args


def build_arg_string(kwdict, confdict=None, infile=None, outfile=None):
    r"""
    Convert keyword dictionaries and input/output files into a GMT argument string.

    Make sure all values in ``kwdict`` have been previously converted to a
    string representation using the ``kwargs_to_strings`` decorator. The only
    exceptions are True, False and None.

    Any lists or tuples left will be interpreted as multiple entries for the
    same command line option. For example, the kwargs entry ``'B': ['xa',
    'yaf']`` will be converted to ``-Bxa -Byaf`` in the argument string.

    Note that spaces `` `` in arguments are converted to the equivalent octal
    code ``\040``, except in the case of -J (projection) arguments where PROJ4
    strings (e.g. "+proj=longlat +datum=WGS84") will have their spaces removed.
    See https://github.com/GenericMappingTools/pygmt/pull/1487 for more info.

    .. deprecated:: 0.12.0

       Use :func:`build_arg_list` instead.

    Parameters
    ----------
    kwdict : dict
        A dictionary containing parsed keyword arguments.
    confdict : dict
        A dictionary containing configurable GMT parameters.
    infile : str or pathlib.Path
        The input file.
    outfile : str or pathlib.Path
        The output file.

    Returns
    -------
    args : str
        The space-delimited argument string with '-' inserted before each
        keyword, or '--' inserted before GMT configuration key-value pairs.
        The keyword arguments are sorted alphabetically, followed by GMT
        configuration key-value pairs, with optional input file at the
        beginning and optional output file at the end.

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
    ...         confdict=dict(FORMAT_DATE_MAP="o dd"),
    ...         infile="input.txt",
    ...         outfile="output.txt",
    ...     )
    ... )
    input.txt -A0 -B -Crainbow --FORMAT_DATE_MAP="o dd" ->output.txt
    """
    msg = (
        "Utility function 'build_arg_string()' is deprecated in v0.12.0 and will be "
        "removed in v0.14.0. Use 'build_arg_list()' instead."
    )
    warnings.warn(msg, category=FutureWarning, stacklevel=2)

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

    if confdict:
        gmt_args.extend(f'--{key}="{value}"' for key, value in confdict.items())

    if infile:
        gmt_args = [str(infile), *gmt_args]
    if outfile:
        gmt_args.append("->" + str(outfile))
    return non_ascii_to_octal(" ".join(gmt_args))


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


def launch_external_viewer(fname: str, waiting: float = 0):
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
        case name if (
            (name == "linux" or name.startswith("freebsd"))
            and (xdgopen := shutil.which("xdg-open"))
        ):  # Linux/FreeBSD
            subprocess.run([xdgopen, fname], check=False, **run_args)  # type:ignore[call-overload]
        case "darwin":  # macOS
            subprocess.run([shutil.which("open"), fname], check=False, **run_args)  # type:ignore[call-overload]
        case "win32":  # Windows
            os.startfile(fname)  # type:ignore[attr-defined] # noqa: S606
        case _:  # Fall back to the browser if can't recognize the operating system.
            webbrowser.open_new_tab(f"file://{fname}")
    if waiting > 0:
        # Preview images will be deleted when a GMT modern-mode session ends, but the
        # external viewer program may take a few seconds to open the images.
        # Suspend the execution for a few seconds.
        time.sleep(waiting)


def args_in_kwargs(args, kwargs):
    """
    Take a list and a dictionary, and determine if any entries in the list are keys in
    the dictionary.

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
    -------
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
