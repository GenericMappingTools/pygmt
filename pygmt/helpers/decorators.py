"""
Decorators to help wrap the GMT modules.

Apply them to functions wrapping GMT modules to automate: alias generation for
arguments, insert common text into docstrings, transform arguments to strings,
etc.
"""
import functools
import textwrap
import warnings
from inspect import Parameter, signature

import numpy as np
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers.utils import is_nonstr_iter

COMMON_OPTIONS = {
    "R": r"""
        region : str or list
            *Required if this is the first plot command*.
            *xmin/xmax/ymin/ymax*\ [**+r**][**+u**\ *unit*].
            Specify the :doc:`region </tutorials/regions>` of interest.""",
    "J": r"""
        projection : str
            *Required if this is the first plot command*.
            *projcode*\[*projparams*/]\ *width*.
            Select map :doc:`projection </projections/index>`.""",
    "B": r"""
        frame : bool or str or list
            Set map boundary
            :doc:`frame and axes attributes </tutorials/frames>`. """,
    "U": """\
        timestamp : bool or str
            Draw GMT time stamp logo on plot.""",
    "CPT": r"""
        cmap : str
           File name of a CPT file or a series of comma-separated colors
           (e.g., *color1*,\ *color2*,\ *color3*) to build a linear continuous
           CPT from those colors automatically.""",
    "G": """\
        color : str or 1d array
            Select color or pattern for filling of symbols or polygons. Default
            is no fill.""",
    "I": r"""
        spacing : str
            *xinc*\ [**+e**\|\ **n**][/\ *yinc*\ [**+e**\|\ **n**]].
            *x_inc* [and optionally *y_inc*] is the grid spacing.

            - **Geographical (degrees) coordinates**: Optionally, append an
              increment unit. Choose among **m** to indicate arc minutes or
              **s** to indicate arc seconds. If one of the units **e**, **f**,
              **k**, **M**, **n** or **u** is appended instead, the increment
              is assumed to be given in meter, foot, km, mile, nautical mile or
              US survey foot, respectively, and will be converted to the
              equivalent degrees longitude at the middle latitude of the region
              (the conversion depends on :gmt-term:`PROJ_ELLIPSOID`). If
              *y_inc* is given but set to 0 it will be reset equal to *x_inc*;
              otherwise it will be converted to degrees latitude.

            - **All coordinates**: If **+e** is appended then the corresponding
              max *x* (*east*) or *y* (*north*) may be slightly adjusted to fit
              exactly the given increment [by default the increment may be
              adjusted slightly to fit the given domain]. Finally, instead of
              giving an increment you may specify the *number of nodes* desired
              by appending **+n** to the supplied integer argument; the
              increment is then recalculated from the number of nodes, the
              *registration*, and the domain. The resulting increment value
              depends on whether you have selected a gridline-registered or
              pixel-registered grid; see :gmt-docs:`GMT File Formats
              <cookbook/file-formats.html#gmt-file-formats>` for details.

            **Note**: If ``region=grdfile`` is used then the grid spacing and
            the registration have already been initialized; use ``spacing`` and
            ``registration`` to override these values.""",
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
    "a": r"""
        aspatial : bool or str
            [*col*\ =]\ *name*\ [,...].
            Control how aspatial data are handled during input and output.
            Full documentation is at :gmt-docs:`gmt.html#aspatial-full`.
         """,
    "b": r"""
        binary : bool or str
            **i**\|\ **o**\ [*ncols*][*type*][**w**][**+l**\|\ **b**].
            Select native binary input (using ``binary="i"``) or output
            (using ``binary="o"``), where *ncols* is the number of data columns
            of *type*, which must be one of:

                - **c** - int8_t (1-byte signed char)
                - **u** - uint8_t (1-byte unsigned char)
                - **h** - int16_t (2-byte signed int)
                - **H** - uint16_t (2-byte unsigned int)
                - **i** - int32_t (4-byte signed int)
                - **I** - uint32_t (4-byte unsigned int)
                - **l** - int64_t (8-byte signed int)
                - **L** - uint64_t (8-byte unsigned int)
                - **f** - 4-byte single-precision float
                - **d** - 8-byte double-precision float
                - **x** - use to skip *ncols* anywhere in the record

            For records with mixed types, append additional comma-separated
            combinations of *ncols* *type* (no space). The following modifiers
            are supported:

                - **w** after any item to force byte-swapping.
                - **+l**\|\ **b** to indicate that the entire data file should
                  be read as little- or big-endian, respectively.

            Full documentation is at :gmt-docs:`gmt.html#bi-full`.""",
    "d": r"""
        nodata : str
            **i**\|\ **o**\ *nodata*.
            Substitute specific values with NaN (for tabular data). For
            example, ``d="-9999"`` will replace all values equal to -9999 with
            NaN during input and all NaN values with -9999 during output.
            Prepend **i** to the *nodata* value for input columns only. Prepend
            **o** to the *nodata* value for output columns only.""",
    "c": r"""
        panel : bool or int or list
            [*row,col*\|\ *index*].
            Select a specific subplot panel. Only allowed when in subplot
            mode. Use ``panel=True`` to advance to the next panel in the
            selected order. Instead of *row,col* you may also give a scalar
            value *index* which depends on the order you set via ``autolabel``
            when the subplot was defined. **Note**: *row*, *col*, and *index*
            all start at 0.
         """,
    "e": r"""
        find : str
            [**~**]\ *"pattern"* \| [**~**]/\ *regexp*/[**i**].
            Only pass records that match the given *pattern* or regular
            expressions [Default processes all records]. Prepend **~** to
            the *pattern* or *regexp* to instead only pass data expressions
            that do not match the pattern. Append **i** for case insensitive
            matching. This does not apply to headers or segment headers.""",
    "f": r"""
        coltypes : str
            [**i**\|\ **o**]\ *colinfo*.
            Specify data types of input and/or output columns (time or
            geographical data). Full documentation is at
            :gmt-docs:`gmt.html#f-full`.""",
    "g": r"""
        gap : str or list
            [**a**]\ **x**\|\ **y**\|\ **d**\|\ **X**\|\ **Y**\|\
            **D**\|[*col*]\ **z**\ *gap*\ [**+n**\|\ **p**].
            Examine the spacing between consecutive data points in order to
            impose breaks in the line. To specify multiple critera, provide
            a list with each item containing a string describing one set of
            critera. Prepend **a** to specify that all the criteria must be
            met [Default is to impose breaks if any criteria are met]. The
            following modifiers are supported:

                - **x**\|\ **X** - define a gap when there is a large enough
                  change in the x coordinates (upper case to use projected
                  coordinates).
                - **y**\|\ **Y** - define a gap when there is a large enough
                  change in the y coordinates (upper case to use projected
                  coordinates).
                - **d**\|\ **D** - define a gap when there is a large enough
                  distance between coordinates (upper case to use projected
                  coordinates).
                - [*col*]\ **z** - define a gap when there is a large enough
                  change in the data in column *col* [default *col* is 2 (i.e.,
                  3rd column)].

            A unit **u** may be appended to the specified *gap*:

                - For geographic data (**x**\|\ **y**\|\ **d**), the unit may
                  be arc **d**\ (egree), **m**\ (inute), and **s**\ (econd), or
                  (m)\ **e**\ (ter), **f**\ (eet), **k**\ (ilometer),
                  **M**\ (iles), or **n**\ (autical miles) [Default is
                  (m)\ **e**\ (ter)].
                - For projected data (**X**\|\ **Y**\|\ **D**), the unit may be
                  **i**\ (nch), **c**\ (entimeter), or **p**\ (oint).

            One of the following modifiers can be appended to *gap* [Default
            imposes breaks based on the absolute value of the difference
            between the current and previous value]:

                - **+n** - specify that the previous value minus the current
                  column value must exceed *gap* for a break to be imposed.
                - **+p** - specify that the current value minus the previous
                  value must exceed *gap* for a break to be imposed.""",
    "h": r"""
        header : str
            [**i**\|\ **o**][*n*][**+c**][**+d**][**+m**\ *segheader*][**+r**\
            *remark*][**+t**\ *title*].
            Specify that input and/or output file(s) have *n* header records
            [Default is 0]. Prepend **i** if only the primary input should have
            header records. Prepend **o** to control the writing of header
            records, with the following modifiers supported:

                - **+d** to remove existing header records.
                - **+c** to add a header comment with column names to the
                  output [Default is no column names].
                - **+m** to add a segment header *segheader* to the output
                  after the header block [Default is no segment header].
                - **+r** to add a *remark* comment to the output [Default is no
                  comment]. The *remark* string may contain \\n to indicate
                  line-breaks.
                - **+t** to add a *title* comment to the output [Default is no
                  title]. The *title* string may contain \\n to indicate
                  line-breaks.

            Blank lines and lines starting with \# are always skipped.""",
    "i": r"""
        incols : str or 1d array
            Specify data columns for primary input in arbitrary order. Columns
            can be repeated and columns not listed will be skipped [Default
            reads all columns in order, starting with the first (i.e., column
            0)].

            - For *1d array*: specify individual columns in input order (e.g.,
              ``incols=[1,0]`` for the 2nd column followed by the 1st column).
            - For :py:class:`str`: specify individual columns or column
              ranges in the format *start*\ [:*inc*]:*stop*, where *inc*
              defaults to 1 if not specified, with columns and/or column ranges
              separated by commas (e.g., ``incols="0:2,4+l"`` to input the
              first three columns followed by the log-transformed 5th column).
              To read from a given column until the end of the record, leave
              off *stop* when specifying the column range. To read trailing
              text, add the column **t**. Append the word number to **t** to
              ingest only a single word from the trailing text. Instead of
              specifying columns, use ``incols="n"`` to simply read numerical
              input and skip trailing text. Optionally, append one of the
              following modifiers to any column or column range to transform
              the input columns:

                - **+l** to take the *log10* of the input values.
                - **+d** to divide the input values by the factor *divisor*
                  [Default is 1].
                - **+s** to multiple the input values by the factor *scale*
                  [Default is 1].
                - **+o** to add the given *offset* to the input values [Default
                  is 0].""",
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
    "l": r"""
        label : str
            Add a legend entry for the symbol or line being plotted. Full
            documentation is at :gmt-docs:`gmt.html#l-full`.""",
    "n": r"""
        interpolation : str
            [**b**\|\ **c**\|\ **l**\|\ **n**][**+a**][**+b**\ *BC*][**+c**][**+t**\ *threshold*].
            Select interpolation mode for grids. You can select the type of
            spline used:

            - **b** for B-spline
            - **c** for bicubic [Default]
            - **l** for bilinear
            - **n** for nearest-neighbor""",
    "o": r"""
        outcols : str or 1d array
            *cols*\ [,...][,\ **t**\ [*word*]].
            Specify data columns for primary output in arbitrary order. Columns
            can be repeated and columns not listed will be skipped [Default
            writes all columns in order, starting with the first (i.e., column
            0)].

            - For *1d array*: specify individual columns in output order (e.g.,
              ``outcols=[1,0]`` for the 2nd column followed by the 1st column).
            - For :py:class:`str`: specify individual columns or column
              ranges in the format *start*\ [:*inc*]:*stop*, where *inc*
              defaults to 1 if not specified, with columns and/or column ranges
              separated by commas (e.g., ``outcols="0:2,4"`` to output the
              first three columns followed by the 5th column).
              To write from a given column until the end of the record, leave
              off *stop* when specifying the column range. To write trailing
              text, add the column **t**. Append the word number to **t** to
              write only a single word from the trailing text. Instead of
              specifying columns, use ``outcols="n"`` to simply read numerical
              input and skip trailing text. Note: if ``incols`` is also used
              then the columns given to ``outcols`` correspond to the order
              after the ``incols`` selection has taken place.""",
    "p": r"""
        perspective : list or str
            [**x**\|\ **y**\|\ **z**]\ *azim*\[/*elev*\[/*zlevel*]]\
            [**+w**\ *lon0*/*lat0*\[/*z0*]][**+v**\ *x0*/*y0*].
            Select perspective view and set the azimuth and elevation angle of
            the viewpoint. Default is [180, 90]. Full documentation is at
            :gmt-docs:`gmt.html#perspective-full`.
        """,
    "r": r"""
        registration : str
            **g**\|\ **p**.
            Force gridline (**g**) or pixel (**p**) node registration.
            [Default is **g**\ (ridline)].
        """,
    "s": r"""
        skiprows : bool or str
            [*cols*][**+a**][**+r**].
            Suppress output for records whose *z*-value equals NaN [Default
            outputs all records]. Optionally, supply a comma-separated list of
            all columns or column ranges to consider for this NaN test [Default
            only considers the third data column (i.e., *cols = 2*)]. Column
            ranges must be given in the format *start*\ [:*inc*]:*stop*, where
            *inc* defaults to 1 if not specified. The following modifiers are
            supported:

                - **+r** to reverse the suppression, i.e., only output the
                  records whose *z*-value equals NaN.
                - **+a** to suppress the output of the record if just one or
                  more of the columns equal NaN [Default skips record only
                  if values in all specified *cols* equal NaN].""",
    "t": """\
        transparency : int or float
            Set transparency level, in [0-100] percent range.
            Default is 0, i.e., opaque.
            Only visible when PDF or raster format output is selected.
            Only the PNG format selection adds a transparency layer
            in the image (for further processing). """,
    "w": r"""
        wrap : str
            **y**\|\ **a**\|\ **w**\|\ **d**\|\ **h**\|\ **m**\|\ **s**\|\
            **c**\ *period*\ [/*phase*][**+c**\ *col*].
            Convert the input *x*-coordinate to a cyclical coordinate, or a
            different column if selected via **+c**\ *col*. The following
            cyclical coordinate transformations are supported:

                - **y** - yearly cycle (normalized)
                - **a** - annual cycle (monthly)
                - **w** - weekly cycle (day)
                - **d** - daily cycle (hour)
                - **h** - hourly cycle (minute)
                - **m** - minute cycle (second)
                - **s** - second cycle (second)
                - **c** - custom cycle (normalized)

            Full documentation is at :gmt-docs:`gmt.html#w-full`.""",
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
    ...     data : str or {table-like}
    ...         Pass in either a file name to an ASCII data table, a 2D
    ...         {table-classes}.
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
    data : str or numpy.ndarray or pandas.DataFrame or xarray.Dataset or geo...
        Pass in either a file name to an ASCII data table, a 2D
        :class:`numpy.ndarray`, a :class:`pandas.DataFrame`, an
        :class:`xarray.Dataset` made up of 1D :class:`xarray.DataArray`
        data variables, or a :class:`geopandas.GeoDataFrame` containing the
        tabular data.
    region : str or list
        *Required if this is the first plot command*.
        *xmin/xmax/ymin/ymax*\ [**+r**][**+u**\ *unit*].
        Specify the :doc:`region </tutorials/regions>` of interest.
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

    filler_text["table-like"] = " or ".join(
        [
            "numpy.ndarray",
            "pandas.DataFrame",
            "xarray.Dataset",
            "geopandas.GeoDataFrame",
        ]
    )
    filler_text["table-classes"] = (
        ":class:`numpy.ndarray`, a :class:`pandas.DataFrame`, an\n"
        "    :class:`xarray.Dataset` made up of 1D :class:`xarray.DataArray`\n"
        "    data variables, or a :class:`geopandas.GeoDataFrame` containing the\n"
        "    tabular data"
    )

    for marker, text in COMMON_OPTIONS.items():
        # Remove the indentation and the first line break from the multiline
        # strings so that it doesn't mess up the original docstring
        filler_text[marker] = textwrap.dedent(text.lstrip("\n"))

    # Dedent the docstring to make it all match the option text.
    docstring = textwrap.dedent(module_func.__doc__)

    module_func.__doc__ = docstring.format(**filler_text)

    return module_func


def _insert_alias(module_func, default_value=None):
    """
    Function to insert PyGMT long aliases into the signature of a method.
    """

    # Get current signature and parameters
    sig = signature(module_func)
    wrapped_params = list(sig.parameters.values())
    kwargs_param = wrapped_params.pop(-1)
    # Add new parameters from aliases
    for alias in module_func.aliases.values():
        if alias not in sig.parameters.keys():
            new_param = Parameter(
                alias, kind=Parameter.KEYWORD_ONLY, default=default_value
            )
            wrapped_params = wrapped_params + [new_param]
    all_params = wrapped_params + [kwargs_param]
    # Update method signature
    sig_new = sig.replace(parameters=all_params)
    module_func.__signature__ = sig_new

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
        Parameters in short-form (J) and long-form (projection) can't coexist.
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
            for short_param, long_alias in aliases.items():
                if long_alias in kwargs and short_param in kwargs:
                    raise GMTInvalidInput(
                        f"Parameters in short-form ({short_param}) and "
                        f"long-form ({long_alias}) can't coexist."
                    )
                if long_alias in kwargs:
                    kwargs[short_param] = kwargs.pop(long_alias)
                elif short_param in kwargs:
                    msg = (
                        f"Short-form parameter ({short_param}) is not recommended. "
                        f"Use long-form parameter '{long_alias}' instead."
                    )
                    warnings.warn(msg, category=SyntaxWarning, stacklevel=2)
            return module_func(*args, **kwargs)

        new_module.aliases = aliases

        new_module = _insert_alias(new_module)

        return new_module

    return alias_decorator


def kwargs_to_strings(**conversions):
    """
    Decorator to convert given keyword arguments to strings.

    The strings are what GMT expects from command line arguments.

    Boolean arguments and None are not converted and will be processed in the
    ``build_arg_string`` function.

    You can also specify other conversions to specific arguments.

    Conversions available:

    * 'sequence': transforms a sequence (list, tuple) into a ``'/'`` separated
      string
    * 'sequence_comma': transforms a sequence into a ``','`` separated string
    * 'sequence_plus': transforms a sequence into a ``'+'`` separated string
    * 'sequence_space': transforms a sequence into a ``' '`` separated string

    Parameters
    ----------
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
    {'P': True}
    >>> module(P=False)
    {'P': False}
    >>> module(P=None)
    {'P': None}
    >>> module(i=[1, 2])
    {'i': '1,2'}
    >>> module(files=["data1.txt", "data2.txt"])
    {'files': 'data1.txt data2.txt'}
    >>> # Other non-boolean arguments are passed along as they are
    >>> module(123, bla=(1, 2, 3), foo=True, A=False, i=(5, 6))
    {'A': False, 'bla': (1, 2, 3), 'foo': True, 'i': '5,6'}
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


def deprecate_parameter(oldname, newname, deprecate_version, remove_version):
    """
    Decorator to deprecate a parameter.

    The old parameter name will be automatically swapped to the new parameter
    name, and users will receive a FutureWarning to inform them of the pending
    deprecation.

    Use this decorator above the ``use_alias`` decorator.

    Parameters
    ----------
    oldname : str
        The old, deprecated parameter name.
    newname : str
        The new parameter name.
    deprecate_version : str
        The PyGMT version when the old parameter starts to be deprecated.
    remove_version : str
        The PyGMT version when the old parameter will be fully removed.

    Examples
    --------
    >>> @deprecate_parameter("sizes", "size", "v0.0.0", "v9.9.9")
    ... @deprecate_parameter("colors", "color", "v0.0.0", "v9.9.9")
    ... @deprecate_parameter("infile", "data", "v0.0.0", "v9.9.9")
    ... def module(data, size=0, **kwargs):
    ...     "A module that prints the arguments it received"
    ...     print(f"data={data}, size={size}, color={kwargs['color']}")
    >>> # new names are supported
    >>> module(data="table.txt", size=5.0, color="red")
    data=table.txt, size=5.0, color=red
    >>> # old names are supported, FutureWarning warnings are reported
    >>> with warnings.catch_warnings(record=True) as w:
    ...     module(infile="table.txt", sizes=5.0, colors="red")
    ...     # check the number of warnings
    ...     assert len(w) == 3
    ...     for i in range(len(w)):
    ...         assert issubclass(w[i].category, FutureWarning)
    ...         assert "deprecated" in str(w[i].message)
    ...
    data=table.txt, size=5.0, color=red
    >>> # using both old and new names will raise an GMTInvalidInput exception
    >>> import pytest
    >>> with pytest.raises(GMTInvalidInput):
    ...     module(data="table.txt", size=5.0, sizes=4.0)
    ...
    """

    def deprecator(module_func):
        """
        The decorator that creates the new function to work with both old and
        new parameters.
        """

        @functools.wraps(module_func)
        def new_module(*args, **kwargs):
            """
            New module instance that converts old parameters to new parameters.
            """
            if oldname in kwargs:
                if newname in kwargs:
                    raise GMTInvalidInput(
                        f"Can't provide both '{newname}' and '{oldname}'."
                    )
                msg = (
                    f"The '{oldname}' parameter has been deprecated since {deprecate_version}"
                    f" and will be removed in {remove_version}."
                    f" Please use '{newname}' instead."
                )
                warnings.warn(msg, category=FutureWarning, stacklevel=2)
                kwargs[newname] = kwargs.pop(oldname)
            return module_func(*args, **kwargs)

        return new_module

    return deprecator
