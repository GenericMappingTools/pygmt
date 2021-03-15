"""
Decorators to help wrap the GMT modules.

Apply them to functions wrapping GMT modules to automate: alias generation for
arguments, insert common text into docstrings, transform arguments to strings,
etc.
"""
import functools
import textwrap

import numpy as np
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.utils import is_nonstr_iter

COMMON_OPTIONS = {
    "R": r"""
        region : str or list
            *Required if this is the first plot command*.
            *xmin/xmax/ymin/ymax*\ [**+r**][**+u**\ *unit*].
            Specify the region of interest.""",
    "J": r"""
        projection : str
            *Required if this is the first plot command*.
            *projcode*\[*projparams*/]\ *width*.
            Select map :doc:`projection </projections/index>`.""",
    "B": r"""
        frame : bool or str or list
            Set map boundary frame and axes attributes.""",
    "U": """\
        timestamp : bool or str
            Draw GMT time stamp logo on plot.""",
    "CPT": r"""
        cmap : str
           File name of a CPT file or a series of comma-separated colors
           (e.g., *color1*,\ *color2*,\ *color3*) to build a linear continuous
           CPT from those colors automatically.""",
    "G": """\
        color : str
            Select color or pattern for filling of symbols or polygons. Default
            is no fill.""",
    "V": """\
        verbose : bool or str
            Select verbosity level [Default is **w**], which modulates the messages
            written to stderr. Choose among 7 levels of verbosity:

            - **q** - Quiet, not even fatal error messages are produced
            - **e** - Error messages only
            - **w** - Warnings [Default]
            - **t** - Timings (report runtimes for time-intensive algorithms);
            - **i** - Informational messages (same as ``verbose=True``)
            - **c** - Compatibility warnings
            - **d** - Debugging messages""",
    "W": """\
        pen : str
            Set pen attributes for lines or the outline of symbols.""",
    "XY": r"""
        xshift : str
            [**a**\|\ **c**\|\ **f**\|\ **r**\][*xshift*].
            Shift plot origin in x-direction.
        yshift : str
            [**a**\|\ **c**\|\ **f**\|\ **r**\][*yshift*].
            Shift plot origin in y-direction. Full documentation is at
            :gmt-docs:`gmt.html#xy-full`.
         """,
    "c": r"""
        panel : bool or int or list
            [*row,col*\|\ *index*].
            Selects a specific subplot panel. Only allowed when in subplot
            mode. Use ``panel=True`` to advance to the next panel in the
            selected order. Instead of *row,col* you may also give a scalar
            value *index* which depends on the order you set via ``autolabel``
            when the subplot was defined. **Note**: *row*, *col*, and *index*
            all start at 0.
         """,
    "f": r"""
        coltypes : str
            [**i**\|\ **o**]\ *colinfo*.
            Specify data types of input and/or output columns (time or
            geographical data). Full documentation is at
            :gmt-docs:`gmt.html#f-full`.
         """,
    "j": r"""
        distcalc : str
            **e**\|\ **f**\|\ **g**.
            Determine how spherical distances are calculated.

            - **e** - Ellipsoidal (or geodesic) mode
            - **f** - Flat Earth mode
            - **g** - Great circle distance [Default]

            All spherical distance calculations depend on the current ellipsoid
            (:gmt-term:`PROJ_ELLIPSOID`), the definition of the mean radius
            (:gmt-term:`PROJ_MEAN_RADIUS`), and the specification of latitude type
            (:gmt-term:`PROJ_AUX_LATITUDE`). Geodesic distance calculations is also
            controlled by method (:gmt-term:`PROJ_GEODESIC`).""",
    "n": r"""
        interpolation : str
            [**b**\|\ **c**\|\ **l**\|\ **n**][**+a**][**+b**\ *BC*][**+c**][**+t**\ *threshold*].
            Select interpolation mode for grids. You can select the type of
            spline used:

            - **b** for B-spline
            - **c** for bicubic [Default]
            - **l** for bilinear
            - **n** for nearest-neighbor""",
    "p": r"""
        perspective : list or str
            [**x**\|\ **y**\|\ **z**]\ *azim*\[/*elev*\[/*zlevel*]]\
            [**+w**\ *lon0*/*lat0*\[/*z0*]][**+v**\ *x0*/*y0*].
            Select perspective view and set the azimuth and elevation angle of
            the viewpoint. Default is [180, 90]. Full documentation is at
            :gmt-docs:`gmt.html#perspective-full`.
        """,
    "registration": r"""
        registration : str
            **g**\|\ **p**.
            Force output grid to be gridline (g) or pixel (p) node registered.
            Default is gridline (g).""",
    "t": """\
        transparency : int or float
            Set transparency level, in [0-100] percent range.
            Default is 0, i.e., opaque.
            Only visible when PDF or raster format output is selected.
            Only the PNG format selection adds a transparency layer
            in the image (for further processing). """,
    "x": r"""
        cores : bool or int
            [[**-**]\ *n*].
            Limit the number of cores to be used in any OpenMP-enabled
            multi-threaded algorithms. By default we try to use all available
            cores. Set a number *n* to only use n cores (if too large it will
            be truncated to the maximum cores available). Finally, give a
            negative number *-n* to select (all - *n*) cores (or at least 1 if
            *n* equals or exceeds all).
            """,
}


def fmt_docstring(module_func):
    r"""
    Decorator to insert common text into module docstrings.

    Should be the last decorator (at the top).

    Use any of these placeholders in your docstring to have them substituted:

    * ``{aliases}``: Insert a section listing the parameter aliases defined by
      decorator ``use_alias``.

    The following are places for common parameter descriptions:

    * ``{R}``: region (bounding box as west, east, south, north)
    * ``{J}``: projection (coordinate system to use)
    * ``{B}``: frame (map frame and axes parameters)
    * ``{U}``: timestamp (insert time stamp logo)
    * ``{CPT}``: cmap (the color palette table)
    * ``{G}``: color
    * ``{W}``: pen
    * ``{n}``: interpolation

    Parameters
    ----------
    module_func : function
        The module function.

    Returns
    -------
    module_func
        The same *module_func* but with the docstring formatted.

    Examples
    --------

    >>> @fmt_docstring
    ... @use_alias(R="region", J="projection")
    ... def gmtinfo(**kwargs):
    ...     '''
    ...     My nice module.
    ...
    ...     Parameters
    ...     ----------
    ...     {R}
    ...     {J}
    ...
    ...     {aliases}
    ...     '''
    ...     pass
    >>> print(gmtinfo.__doc__)
    <BLANKLINE>
    My nice module.
    <BLANKLINE>
    Parameters
    ----------
    region : str or list
        *Required if this is the first plot command*.
        *xmin/xmax/ymin/ymax*\ [**+r**][**+u**\ *unit*].
        Specify the region of interest.
    projection : str
        *Required if this is the first plot command*.
        *projcode*\[*projparams*/]\ *width*.
        Select map :doc:`projection </projections/index>`.
    <BLANKLINE>
    **Aliases:**
    <BLANKLINE>
    - J = projection
    - R = region
    <BLANKLINE>
    """
    filler_text = {}

    if hasattr(module_func, "aliases"):
        aliases = ["**Aliases:**\n"]
        for arg in sorted(module_func.aliases):
            alias = module_func.aliases[arg]
            aliases.append("- {} = {}".format(arg, alias))
        filler_text["aliases"] = "\n".join(aliases)

    for marker, text in COMMON_OPTIONS.items():
        # Remove the indentation and the first line break from the multiline
        # strings so that it doesn't mess up the original docstring
        filler_text[marker] = textwrap.dedent(text.lstrip("\n"))

    # Dedent the docstring to make it all match the option text.
    docstring = textwrap.dedent(module_func.__doc__)

    module_func.__doc__ = docstring.format(**filler_text)

    return module_func


def use_alias(**aliases):
    """
    Decorator to add aliases to keyword arguments of a function.

    Use this decorator above the argument parsing decorators, usually only
    below ``fmt_docstring``.

    Replaces the aliases with their desired names before passing them along to
    the module function.

    Keywords passed to this decorator are the desired argument name and their
    value is the alias.

    Adds a dictionary attribute to the function with the aliases. Use in
    conjunction with ``fmt_docstring`` to insert a list of valid aliases in
    your docstring.

    Examples
    --------

    >>> @use_alias(R="region", J="projection")
    ... def my_module(**kwargs):
    ...     print("R =", kwargs["R"], "J =", kwargs["J"])
    >>> my_module(R="bla", J="meh")
    R = bla J = meh
    >>> my_module(region="bla", J="meh")
    R = bla J = meh
    >>> my_module(R="bla", projection="meh")
    R = bla J = meh
    >>> my_module(region="bla", projection="meh")
    R = bla J = meh
    >>> my_module(
    ...     region="bla", projection="meh", J="bla"
    ... )  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    pygmt.exceptions.GMTInvalidInput:
        Arguments in short-form (J) and long-form (projection) can't coexist
    """

    def alias_decorator(module_func):
        """
        Decorator that replaces the aliases for arguments.
        """

        @functools.wraps(module_func)
        def new_module(*args, **kwargs):
            """
            New module that parses and replaces the registered aliases.
            """
            for arg, alias in aliases.items():
                if alias in kwargs and arg in kwargs:
                    raise GMTInvalidInput(
                        f"Arguments in short-form ({arg}) and long-form ({alias}) can't coexist"
                    )
                if alias in kwargs:
                    kwargs[arg] = kwargs.pop(alias)
            return module_func(*args, **kwargs)

        new_module.aliases = aliases

        return new_module

    return alias_decorator


def kwargs_to_strings(convert_bools=True, **conversions):
    """
    Decorator to convert given keyword arguments to strings.

    The strings are what GMT expects from command line arguments.

    Converts all boolean arguments by default. Transforms ``True`` into ``''``
    (empty string) and removes the argument from ``kwargs`` if ``False``.

    You can also specify other conversions to specific arguments.

    Conversions available:

    * 'sequence': transforms a sequence (list, tuple) into a ``'/'`` separated
      string
    * 'sequence_comma': transforms a sequence into a ``','`` separated string
    * 'sequence_plus': transforms a sequence into a ``'+'`` separated string
    * 'sequence_space': transforms a sequence into a ``' '`` separated string

    Parameters
    ----------
    convert_bools : bool
        If ``True``, convert all boolean arguments to strings using the rules
        specified above. If ``False``, leave them as they are.
    conversions : keyword arguments
        Keyword arguments specifying other kinds of conversions that should be
        performed. The keyword is the name of the argument and the value is the
        conversion type (see list above).

    Examples
    --------

    >>> @kwargs_to_strings(
    ...     R="sequence", i="sequence_comma", files="sequence_space"
    ... )
    ... def module(*args, **kwargs):
    ...     "A module that prints the arguments it received"
    ...     print("{", end="")
    ...     print(
    ...         ", ".join(
    ...             "'{}': {}".format(k, repr(kwargs[k]))
    ...             for k in sorted(kwargs)
    ...         ),
    ...         end="",
    ...     )
    ...     print("}")
    ...     if args:
    ...         print("args:", " ".join("{}".format(x) for x in args))
    >>> module(R=[1, 2, 3, 4])
    {'R': '1/2/3/4'}
    >>> # It's already a string, do nothing
    >>> module(R="5/6/7/8")
    {'R': '5/6/7/8'}
    >>> module(P=True)
    {'P': ''}
    >>> module(P=False)
    {}
    >>> module(i=[1, 2])
    {'i': '1,2'}
    >>> module(files=["data1.txt", "data2.txt"])
    {'files': 'data1.txt data2.txt'}
    >>> # Other non-boolean arguments are passed along as they are
    >>> module(123, bla=(1, 2, 3), foo=True, A=False, i=(5, 6))
    {'bla': (1, 2, 3), 'foo': '', 'i': '5,6'}
    args: 123
    >>> import datetime
    >>> module(
    ...     R=[
    ...         np.datetime64("2010-01-01T16:00:00"),
    ...         datetime.datetime(2020, 1, 1, 12, 23, 45),
    ...     ]
    ... )
    {'R': '2010-01-01T16:00:00/2020-01-01T12:23:45.000000'}
    >>> import pandas as pd
    >>> import xarray as xr
    >>> module(
    ...     R=[
    ...         xr.DataArray(data=np.datetime64("2005-01-01T08:00:00")),
    ...         pd.Timestamp("2015-01-01T12:00:00.123456789"),
    ...     ]
    ... )
    {'R': '2005-01-01T08:00:00.000000000/2015-01-01T12:00:00.123456'}
    """
    valid_conversions = [
        "sequence",
        "sequence_comma",
        "sequence_plus",
        "sequence_space",
    ]

    for arg, fmt in conversions.items():
        if fmt not in valid_conversions:
            raise GMTInvalidInput(
                "Invalid conversion type '{}' for argument '{}'.".format(fmt, arg)
            )

    separators = {
        "sequence": "/",
        "sequence_comma": ",",
        "sequence_plus": "+",
        "sequence_space": " ",
    }

    # Make the actual decorator function
    def converter(module_func):
        """
        The decorator that creates our new function with the conversions.
        """

        @functools.wraps(module_func)
        def new_module(*args, **kwargs):
            """
            New module instance that converts the arguments first.
            """
            if convert_bools:
                kwargs = remove_bools(kwargs)
            for arg, fmt in conversions.items():
                if arg in kwargs:
                    value = kwargs[arg]
                    issequence = fmt in separators
                    if issequence and is_nonstr_iter(value):
                        for index, item in enumerate(value):
                            try:
                                # check if there is a space " " when converting
                                # a pandas.Timestamp/xr.DataArray to a string.
                                # If so, use np.datetime_as_string instead.
                                assert " " not in str(item)
                            except AssertionError:
                                # convert datetime-like item to ISO 8601
                                # string format like YYYY-MM-DDThh:mm:ss.ffffff
                                value[index] = np.datetime_as_string(
                                    np.asarray(item, dtype=np.datetime64)
                                )
                        kwargs[arg] = separators[fmt].join(f"{item}" for item in value)
            # Execute the original function and return its output
            return module_func(*args, **kwargs)

        return new_module

    return converter


def remove_bools(kwargs):
    """
    Remove booleans from arguments.

    If ``True``, replace it with an empty string. If ``False``, completely
    remove the entry from the argument list.

    Parameters
    ----------
    kwargs : dict
        Dictionary with the keyword arguments.

    Returns
    -------
    new_kwargs : dict
        A copy of `kwargs` with the booleans parsed.
    """
    new_kwargs = {}
    for arg, value in kwargs.items():
        if isinstance(value, bool):
            if value:
                new_kwargs[arg] = ""
        else:
            new_kwargs[arg] = value
    return new_kwargs
