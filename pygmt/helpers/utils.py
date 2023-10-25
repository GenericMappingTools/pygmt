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
import webbrowser
from collections.abc import Iterable

import xarray as xr
from pygmt.exceptions import GMTInvalidInput


def validate_data_input(
    data=None, vectors=None, names="xy", required_data=True, kind=None
):
    """
    Check if the data input is valid.

    Parameters
    ----------
    data : str, pathlib.PurePath, None, bool, xarray.DataArray or {table-like}
        Pass in either a file name or :class:`pathlib.Path` to an ASCII data
        table, an :class:`xarray.DataArray`, a 1-D/2-D
        {table-classes} or an option argument.
    vectors : list of 1-D arrays
        A list of 1-D arrays with the data columns.
    names : list of str
        List of column names.
    required_data : bool
        Set to True when 'data' is required, or False when dealing with
        optional virtual files [Default is True].
    kind : str or None
        The kind of data that will be passed to a module. If not given, it
        will be determined by calling :func:`data_kind`.

    Examples
    --------
    >>> validate_data_input(data="infile")
    >>> validate_data_input(vectors=[[1, 2, 3], [4, 5, 6]], names="xy")
    >>> validate_data_input(
    ...     vectors=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], names="xyz"
    ... )
    >>> validate_data_input(data=None, required_data=False)
    >>> validate_data_input()
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: No input data provided.
    >>> validate_data_input(vectors=[[1, 2, 3], None], names="xy")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Column 1 ('y') can't be None.
    >>> validate_data_input(vectors=[None, [4, 5, 6]], names="xy")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Column 0 ('x') can't be None.
    >>> validate_data_input(vectors=[[1, 2, 3], [4, 5, 6], None], names="xyz")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Column 2 ('z') can't be None.
    >>> import numpy as np
    >>> import pandas as pd
    >>> import xarray as xr
    >>> data = np.arange(8).reshape((4, 2))
    >>> validate_data_input(data=data, names="xyz", kind="matrix")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: data must have at least 3 columns.
    x y z
    >>> validate_data_input(
    ...     data=pd.DataFrame(data, columns=["x", "y"]),
    ...     names="xyz",
    ...     kind="matrix",
    ... )
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: data must have at least 3 columns.
    x y z
    >>> validate_data_input(
    ...     data=xr.Dataset(pd.DataFrame(data, columns=["x", "y"])),
    ...     names="xyz",
    ...     kind="matrix",
    ... )
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: data must have at least 3 columns.
    x y z
    >>> validate_data_input(data="infile", vectors=[[1, 2, 3], None])
    Traceback (most recent call last):
        ...
    pygmt...GMTInvalidInput: Too much data. Use either 'data' or 1-D arrays.
    >>> validate_data_input(data="infile", vectors=[None, [4, 5, 6]])
    Traceback (most recent call last):
        ...
    pygmt...GMTInvalidInput: Too much data. Use either 'data' or 1-D arrays.
    >>> validate_data_input(data="infile", vectors=[None, None, [7, 8, 9]])
    Traceback (most recent call last):
        ...
    pygmt...GMTInvalidInput: Too much data. Use either 'data' or 1-D arrays.

    Raises
    ------
    GMTInvalidInput
        If the data input is not valid.
    """
    if kind is None:
        kind = data_kind(data=data, required=required_data)

    if kind == "vectors":  # From data_kind, we know that data is None
        if vectors is None:
            raise GMTInvalidInput("No input data provided.")
        if len(vectors) < len(names):
            raise GMTInvalidInput(
                f"Requires {len(names)} 1-D arrays but got {len(vectors)}."
            )
        for i, v in enumerate(vectors[: len(names)]):
            if v is None:
                raise GMTInvalidInput(f"Column {i} ('{names[i]}') can't be None.")
    else:
        if vectors is not None and any(v is not None for v in vectors):
            raise GMTInvalidInput("Too much data. Use either 'data' or 1-D arrays.")
        if kind == "matrix":  # check number of columns for matrix-like data
            msg = f"data must have at least {len(names)} columns.\n" + " ".join(names)
            if hasattr(data, "shape"):  # np.ndarray or pd.DataFrame
                if len(data.shape) == 1 and data.shape[0] < len(names):
                    raise GMTInvalidInput(msg)
                if len(data.shape) > 1 and data.shape[1] < len(names):
                    raise GMTInvalidInput(msg)
            if hasattr(data, "data_vars") and len(data.data_vars) < len(
                names
            ):  # xr.Dataset
                raise GMTInvalidInput(msg)


def data_kind(data=None, required=True):
    """
    Determine the kind of data that will be passed to a module.

    It checks the type of the ``data`` argument and determines the kind of
    data. Falls back to ``"vectors"`` if ``data`` is None but required.

    Possible data kinds:

    - ``'file'``: a file name or a pathlib.PurePath object provided as 'data'
    - ``'arg'``: an optional argument (None, bool, int or float) provided
      as 'data'
    - ``'grid'``: an xarray.DataArray with 2 dimensions provided as 'data'
    - ``'image'``: an xarray.DataArray with 3 dimensions provided as 'data'
    - ``'geojson'``: a geo-like Python object that implements
      ``__geo_interface__`` (geopandas.GeoDataFrame or shapely.geometry)
      provided as 'data'
    - ``'matrix'``: a 2-D array provided as 'data'
    - ``'vectors'``: a list of 1-D arrays provided as 'vectors'

    Parameters
    ----------
    data : str, pathlib.PurePath, None, bool, xarray.DataArray or {table-like}
        Pass in either a file name or :class:`pathlib.Path` to an ASCII data
        table, an :class:`xarray.DataArray`, a 1-D/2-D
        {table-classes} or an option argument.
    required : bool
        Set to True when 'data' is required, or False when dealing with
        optional virtual files. [Default is True].

    Returns
    -------
    kind : str
        One of ``'arg'``, ``'file'``, ``'grid'``, ``image``, ``'geojson'``,
        ``'matrix'``, or ``'vectors'``.

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
    if isinstance(data, (str, pathlib.PurePath)):
        kind = "file"
    elif isinstance(data, (bool, int, float)) or (data is None and not required):
        kind = "arg"
    elif isinstance(data, xr.DataArray):
        kind = "image" if len(data.dims) == 3 else "grid"
    elif hasattr(data, "__geo_interface__"):
        # geo-like Python object that implements ``__geo_interface__``
        # (geopandas.GeoDataFrame or shapely.geometry)
        kind = "geojson"
    elif data is not None:  # anything but None is taken as a matrix
        kind = "matrix"
    else:  # fallback to vectors if data is None but required
        kind = "vectors"
    return kind


def non_ascii_to_octal(argstr):
    r"""
    Translate non-ASCII characters to their corresponding octal codes.

    Currently, only characters in the ISOLatin1+ charset and
    Symbol/ZapfDingbats fonts are supported.

    Parameters
    ----------
    argstr : str
        The string to be translated.

    Returns
    -------
    translated_argstr : str
        The translated string.

    Examples
    --------
    >>> non_ascii_to_octal("•‰“”±°ÿ")
    '\\31\\214\\216\\217\\261\\260\\377'
    >>> non_ascii_to_octal("αζΔΩ∑π∇")
    '@~\\141@~@~\\172@~@~\\104@~@~\\127@~@~\\345@~@~\\160@~@~\\321@~'
    >>> non_ascii_to_octal("✁❞❡➾")
    '@%34%\\41@%%@%34%\\176@%%@%34%\\241@%%@%34%\\376@%%'
    >>> non_ascii_to_octal("ABC ±120° DEF α ♥")
    'ABC \\261120\\260 DEF @~\\141@~ @%34%\\252@%%'
    """
    # Dictionary mapping non-ASCII characters to octal codes
    mapping = {}

    # Adobe Symbol charset
    # References:
    # 1. https://en.wikipedia.org/wiki/Symbol_(typeface)
    # 2. https://unicode.org/Public/MAPPINGS/VENDORS/ADOBE/symbol.txt
    # Notes:
    # 1. \322 and \342 are "REGISTERED SIGN SERIF" and
    #    "REGISTERED SIGN SANS SERIF" respectively, but only "REGISTERED SIGN"
    #    is available in the unicode table. So both are mapped to
    #    "REGISTERED SIGN". \323, \343, \324 and \344 also have the same
    #    problem.
    # 2. Characters for \140, \275, \276 are incorrect.
    mapping.update(
        {
            c: "@~\\" + format(i, "o") + "@~"
            for c, i in zip(
                " !∀#∃%&∋()∗+,−./"  # \04x-05x
                + "0123456789:;<=>?"  # \06x-07x
                + "≅ΑΒΧΔΕΦΓΗΙϑΚΛΜΝΟ"  # \10x-11x
                + "ΠΘΡΣΤΥςΩΞΨΖ[∴]⊥_"  # \12x-13x
                + "αβχδεφγηιϕκλμνο"  # \14x-15x
                + "πθρστυϖωξψζ{|}∼"  # \16x-17x. \177 is undefined
                + "€ϒ′≤⁄∞ƒ♣♦♥♠↔←↑→↓"  # \24x-\25x
                + "°±″≥×∝∂•÷≠≡≈…↵"  # \26x-27x
                + "ℵℑℜ℘⊗⊕∅∩∪⊃⊇⊄⊂⊆∈∉"  # \30x-31x
                + "∠∇®©™∏√⋅¬∧∨⇔⇐⇑⇒⇓"  # \32x-33x
                + "◊〈®©™∑"  # \34x-35x
                + "〉∫⌠⌡",  # \36x-37x. \360 and \377 are undefined
                [*range(32, 127), *range(160, 240), *range(241, 255)],
            )
        }
    )

    # Adobe ZapfDingbats charset
    # References:
    # 1. https://en.wikipedia.org/wiki/Zapf_Dingbats
    # 2. https://unicode.org/Public/MAPPINGS/VENDORS/ADOBE/zdingbat.txt
    mapping.update(
        {
            c: "@%34%\\" + format(i, "o") + "@%%"
            for c, i in zip(
                " ✁✂✃✄☎✆✇✈✉☛☞✌✍✎✏"  # \04x-\05x
                + "✐✑✒✓✔✕✖✗✘✙✚✛✜✝✞✟"  # \06x-\07x
                + "✠✡✢✣✤✥✦✧★✩✪✫✬✭✮✯"  # \10x-\11x
                + "✰✱✲✳✴✵✶✷✸✹✺✻✼✽✾✿"  # \12x-\13x
                + "❀❁❂❃❄❅❆❇❈❉❊❋●❍■❏"  # \14x-\15x
                + "❐❑❒▲▼◆❖◗❘❙❚❛❜❝❞"  # \16x-\17x. \177 is undefined
                + "❡❢❣❤❥❦❧♣♦♥♠①②③④"  # \24x-\25x. \240 is undefined
                + "⑤⑥⑦⑧⑨⑩❶❷❸❹❺❻❼❽❾❿"  # \26x-\27x
                + "➀➁➂➃➄➅➆➇➈➉➊➋➌➍➎➏"  # \30x-\31x
                + "➐➑➒➓➔→↔↕➘➙➚➛➜➝➞➟"  # \32x-\33x
                + "➠➡➢➣➤➥➦➧➨➩➪➫➬➭➮➯"  # \34x-\35x
                + "➱➲➳➴➵➶➷➸➹➺➻➼➽➾",  # \36x-\37x. \360 and \377 are undefined
                [*range(32, 127), *range(161, 240), *range(241, 255)],
            )
        }
    )

    # Adobe ISOLatin1+ charset (i.e., ISO-8859-1 with extensions)
    # References:
    # 1. https://en.wikipedia.org/wiki/ISO/IEC_8859-1
    # 2. https://docs.generic-mapping-tools.org/dev/reference/octal-codes.html
    # 3. https://www.adobe.com/jp/print/postscript/pdfs/PLRM.pdf
    mapping.update(
        {
            c: "\\" + format(i, "o")
            for c, i in zip(
                "•…™—–ﬁž"  # \03x. \030 is undefined
                + "š"  # \177
                + "Œ†‡Ł⁄‹Š›œŸŽł‰„“”"  # \20x-\21x
                + "ı`´ˆ˜¯˘˙¨‚˚¸'˝˛ˇ",  # \22x-\23x
                [*range(25, 32), *range(127, 160)],
            )
        }
    )
    # \240-\377
    mapping.update({chr(i): "\\" + format(i, "o") for i in range(160, 256)})

    # Remove any printable characters
    mapping = {k: v for k, v in mapping.items() if k not in string.printable}
    return argstr.translate(str.maketrans(mapping))


def build_arg_string(kwdict, confdict=None, infile=None, outfile=None):
    r"""
    Convert keyword dictionaries and input/output files into a GMT argument
    string.

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
        gmt_args = [str(infile)] + gmt_args
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
    run_args = {
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }

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
