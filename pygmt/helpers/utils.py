"""
Utilities and common tasks for wrapping the GMT modules.
"""
# ruff: noqa: RUF001
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


def data_kind(data=None, x=None, y=None, z=None, required_z=False, required_data=True):
    """
    Check what kind of data is provided to a module.

    Possible types:

    * a file name provided as 'data'
    * a pathlib.PurePath object provided as 'data'
    * an xarray.DataArray object provided as 'data'
    * a 2-D matrix provided as 'data'
    * 1-D arrays x and y (and z, optionally)
    * an optional argument (None, bool, int or float) provided as 'data'

    Arguments should be ``None`` if not used. If doesn't fit any of these
    categories (or fits more than one), will raise an exception.

    Parameters
    ----------
    data : str, pathlib.PurePath, None, bool, xarray.DataArray or {table-like}
        Pass in either a file name or :class:`pathlib.Path` to an ASCII data
        table, an :class:`xarray.DataArray`, a 1-D/2-D
        {table-classes} or an option argument.
    x/y : 1-D arrays or None
        x and y columns as numpy arrays.
    z : 1-D array or None
        z column as numpy array. To be used optionally when x and y are given.
    required_z : bool
        State whether the 'z' column is required.
    required_data : bool
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
    >>> data_kind(data=None, x=np.array([1, 2, 3]), y=np.array([4, 5, 6]))
    'vectors'
    >>> data_kind(data=np.arange(10).reshape((5, 2)), x=None, y=None)
    'matrix'
    >>> data_kind(data="my-data-file.txt", x=None, y=None)
    'file'
    >>> data_kind(data=pathlib.Path("my-data-file.txt"), x=None, y=None)
    'file'
    >>> data_kind(data=None, x=None, y=None, required_data=False)
    'arg'
    >>> data_kind(data=2.0, x=None, y=None, required_data=False)
    'arg'
    >>> data_kind(data=True, x=None, y=None, required_data=False)
    'arg'
    >>> data_kind(data=xr.DataArray(np.random.rand(4, 3)))
    'grid'
    >>> data_kind(data=xr.DataArray(np.random.rand(3, 4, 5)))
    'image'
    """
    # determine the data kind
    if isinstance(data, (str, pathlib.PurePath)):
        kind = "file"
    elif isinstance(data, (bool, int, float)) or (data is None and not required_data):
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
    _validate_data_input(
        data=data,
        x=x,
        y=y,
        z=z,
        required_z=required_z,
        required_data=required_data,
        kind=kind,
    )
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
    """  # noqa: RUF002
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
                "0123456789:;<=>?"  # \06x-07x
                "≅ΑΒΧΔΕΦΓΗΙϑΚΛΜΝΟ"  # \10x-11x
                "ΠΘΡΣΤΥςΩΞΨΖ[∴]⊥_"  # \12x-13x
                "αβχδεφγηιϕκλμνο"  # \14x-15x
                "πθρστυϖωξψζ{|}∼"  # \16x-17x. \177 is undefined
                "€ϒ′≤⁄∞ƒ♣♦♥♠↔←↑→↓"  # \24x-\25x
                "°±″≥×∝∂•÷≠≡≈…↵"  # \26x-27x
                "ℵℑℜ℘⊗⊕∅∩∪⊃⊇⊄⊂⊆∈∉"  # \30x-31x
                "∠∇®©™∏√⋅¬∧∨⇔⇐⇑⇒⇓"  # \32x-33x
                "◊〈®©™∑"  # \34x-35x
                "〉∫⌠⌡",  # \36x-37x. \360 and \377 are undefined
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
                "✐✑✒✓✔✕✖✗✘✙✚✛✜✝✞✟"  # \06x-\07x
                "✠✡✢✣✤✥✦✧★✩✪✫✬✭✮✯"  # \10x-\11x
                "✰✱✲✳✴✵✶✷✸✹✺✻✼✽✾✿"  # \12x-\13x
                "❀❁❂❃❄❅❆❇❈❉❊❋●❍■❏"  # \14x-\15x
                "❐❑❒▲▼◆❖◗❘❙❚❛❜❝❞"  # \16x-\17x. \177 is undefined
                "❡❢❣❤❥❦❧♣♦♥♠①②③④"  # \24x-\25x. \240 is undefined
                "⑤⑥⑦⑧⑨⑩❶❷❸❹❺❻❼❽❾❿"  # \26x-\27x
                "➀➁➂➃➄➅➆➇➈➉➊➋➌➍➎➏"  # \30x-\31x
                "➐➑➒➓➔→↔↕➘➙➚➛➜➝➞➟"  # \32x-\33x
                "➠➡➢➣➤➥➦➧➨➩➪➫➬➭➮➯"  # \34x-\35x
                "➱➲➳➴➵➶➷➸➹➺➻➼➽➾",  # \36x-\37x. \360 and \377 are undefined
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
                "š"  # \177
                "Œ†‡Ł⁄‹Š›œŸŽł‰„“”"  # \20x-\21x
                "ı`´ˆ˜¯˘˙¨‚˚¸'˝˛ˇ",  # \22x-\23x
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
    if os_name.startswith(("linux", "freebsd")) and (
        xdgopen := shutil.which("xdg-open")
    ):
        subprocess.run([xdgopen, fname], check=False, **run_args)
    elif os_name == "darwin":  # Darwin is macOS
        subprocess.run([shutil.which("open"), fname], check=False, **run_args)
    elif os_name == "win32":
        os.startfile(fname)  # noqa: S606
    else:
        webbrowser.open_new_tab(f"file://{fname}")
    if waiting > 0:
        # suspend the execution for a few seconds to avoid the images being
        # deleted when a Python script exits
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
