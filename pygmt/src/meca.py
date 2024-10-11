"""
meca - Plot focal mechanisms.
"""

import numpy as np
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTError, GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


def convention_code(convention, component="full"):
    """
    Determine the convention code for focal mechanisms.

    The convention code can be used in meca's -S option.

    Parameters
    ----------
    convention : str
        The focal mechanism convention. Can be one of the following:

        - ``"aki"``: Aki and Richards
        - ``"gcmt"``: Global Centroid Moment Tensor
        - ``"partial"``: Partial focal mechanism
        - ``"mt"``: Moment tensor
        - ``"principal_axis"``: Principal axis

        Single letter convention codes like ``"a"`` and ``"c"`` are also
        supported but undocumented.

    component : str
        The component of the focal mechanism. Only used when ``convention`` is
        ``"mt"`` or ``"principal_axis"``. Can be one of the following:

        - ``"full"``: Full moment tensor
        - ``"deviatoric"``: Deviatoric moment tensor
        - ``"dc"``: Double couple

    Returns
    -------
    str
        The single-letter convention code used in meca's -S option.

    Examples
    --------
    >>> convention_code("aki")
    'a'
    >>> convention_code("gcmt")
    'c'
    >>> convention_code("partial")
    'p'

    >>> convention_code("mt", component="full")
    'm'
    >>> convention_code("mt", component="deviatoric")
    'z'
    >>> convention_code("mt", component="dc")
    'd'
    >>> convention_code("principal_axis", component="full")
    'x'
    >>> convention_code("principal_axis", component="deviatoric")
    't'
    >>> convention_code("principal_axis", component="dc")
    'y'

    >>> for code in ["a", "c", "m", "d", "z", "p", "x", "y", "t"]:
    ...     assert convention_code(code) == code

    >>> convention_code("invalid")
    Traceback (most recent call last):
      ...
    pygmt.exceptions.GMTInvalidInput: Invalid convention 'invalid'.

    >>> convention_code("mt", "invalid")  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    pygmt.exceptions.GMTInvalidInput:
        Invalid component 'invalid' for convention 'mt'.
    """
    # Codes for focal mechanism formats determined by "convention"
    codes1 = {"aki": "a", "gcmt": "c", "partial": "p"}
    # Codes for focal mechanism formats determined by both "convention" and
    # "component"
    codes2 = {
        "mt": {"deviatoric": "z", "dc": "d", "full": "m"},
        "principal_axis": {"deviatoric": "t", "dc": "y", "full": "x"},
    }

    if convention in codes1:
        return codes1[convention]
    if convention in codes2:
        if component not in codes2[convention]:
            raise GMTInvalidInput(
                f"Invalid component '{component}' for convention '{convention}'."
            )
        return codes2[convention][component]
    if convention in {"a", "c", "m", "d", "z", "p", "x", "y", "t"}:
        return convention
    raise GMTInvalidInput(f"Invalid convention '{convention}'.")


def convention_name(code):
    """
    Determine the name of a focal mechanism convention from its code.

    Parameters
    ----------
    code : str
        The single-letter convention code.

    Returns
    -------
    str
        The name of the focal mechanism convention.

    Examples
    --------
    >>> convention_name("a")
    'aki'
    >>> convention_name("aki")
    'aki'
    """
    name = {
        "a": "aki",
        "c": "gcmt",
        "p": "partial",
        "z": "mt",
        "d": "mt",
        "m": "mt",
        "x": "principal_axis",
        "y": "principal_axis",
        "t": "principal_axis",
    }.get(code)
    return name if name is not None else code


def convention_params(convention):
    """
    Return the list of focal mechanism parameters for a given convention.

    Parameters
    ----------
    convention : str
        The focal mechanism convention. Can be one of the following:

        - ``"aki"``: Aki and Richards
        - ``"gcmt"``: Global Centroid Moment Tensor
        - ``"partial"``: Partial focal mechanism
        - ``"mt"``: Moment tensor
        - ``"principal_axis"``: Principal axis

    Returns
    -------
    list
        The list of focal mechanism parameters.
    """
    return {
        "aki": ["strike", "dip", "rake", "magnitude"],
        "gcmt": [
            "strike1",
            "dip1",
            "rake1",
            "strike2",
            "dip2",
            "rake2",
            "mantissa",
            "exponent",
        ],
        "mt": ["mrr", "mtt", "mff", "mrt", "mrf", "mtf", "exponent"],
        "partial": ["strike1", "dip1", "strike2", "fault_type", "magnitude"],
        "principal_axis": [
            "t_value",
            "t_azimuth",
            "t_plunge",
            "n_value",
            "n_azimuth",
            "n_plunge",
            "p_value",
            "p_azimuth",
            "p_plunge",
            "exponent",
        ],
    }[convention]


@fmt_docstring
@use_alias(
    A="offset",
    B="frame",
    C="cmap",
    E="extensionfill",
    Fr="labelbox",
    G="compressionfill",
    J="projection",
    L="outline",
    N="no_clip",
    R="region",
    T="nodal",
    V="verbose",
    W="pen",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def meca(  # noqa: PLR0912, PLR0913, PLR0915
    self,
    spec,
    scale,
    convention=None,
    component="full",
    longitude=None,
    latitude=None,
    depth=None,
    plot_longitude=None,
    plot_latitude=None,
    event_name=None,
    **kwargs,
):
    r"""
    Plot focal mechanisms.

    Full option list at :gmt-docs:`supplements/seis/meca.html`

    {aliases}

    Parameters
    ----------
    spec : str, 1-D array, 2-D array, dict, or pd.DataFrame
        Data that contain focal mechanism parameters.

        ``spec`` can be specified in either of the following types:

        - *str*: a file name containing focal mechanism parameters as
          columns. The meaning of each column is:

          - Columns 1 and 2: event longitude and latitude
          - Column 3: event depth (in km)
          - Columns 4 to 3+n: focal mechanism parameters. The number of columns
            *n* depends on the choice of ``convention``, which will be
            described below.
          - Columns 4+n and 5+n: longitude, latitude at which to place
            beachball. Using ``0 0`` will plot the beachball at the longitude,
            latitude given in columns 1 and 2. [optional and requires
            ``offset=True`` to take effect].
          - Text string to appear near the beachball [optional].

        - *1-D array*: focal mechanism parameters of a single event.
          The meanings of columns are the same as above.
        - *2-D array*: focal mechanism parameters of multiple events.
          The meanings of columns are the same as above.
        - *dictionary or pd.DataFrame*: The dictionary keys or pd.DataFrame
          column names determine the focal mechanism convention. For
          different conventions, the following combination of keys are allowed:

          - ``"aki"``: *strike, dip, rake, magnitude*
          - ``"gcmt"``: *strike1, dip1, rake1, strike2, dip2, rake2, mantissa,*
            *exponent*
          - ``"mt"``: *mrr, mtt, mff, mrt, mrf, mtf, exponent*
          - ``"partial"``: *strike1, dip1, strike2, fault_type, magnitude*
          - ``"principal_axis"``: *t_value, t_azimuth, t_plunge, n_value,
            n_azimuth, n_plunge, p_value, p_azimuth, p_plunge, exponent*

          A dictionary may contain values for a single focal mechanism or
          lists of values for multiple focal mechanisms.

          Both dictionary and pd.DataFrame may optionally contain
          keys/column names: ``latitude``, ``longitude``, ``depth``,
          ``plot_longitude``, ``plot_latitude``, and/or ``event_name``.

        If ``spec`` is either a str, a 1-D array or a 2-D array, the
        ``convention`` parameter is required so we know how to interpret the
        columns. If ``spec`` is a dictionary or a pd.DataFrame,
        ``convention`` is not needed and is ignored if specified.
    scale : float or str
        *scale*\ [**+a**\ *angle*][**+f**\ *font*][**+j**\ *justify*]\
        [**+l**][**+m**][**+o**\ *dx*\ [/\ *dy*]][**+s**\ *reference*].
        Adjust scaling of the radius of the beachball, which is
        proportional to the magnitude. By default, *scale* defines the
        size for magnitude = 5 (i.e., scalar seismic moment
        M0 = 4.0E23 dynes-cm). If **+l** is used the radius will be
        proportional to the seismic moment instead. Use **+s** and give
        a *reference* to change the reference magnitude (or moment), and
        use **+m** to plot all beachballs with the same size. A text
        string can be specified to appear near the beachball
        (corresponding to column or parameter ``event_name``).
        Append **+a**\ *angle* to change the angle of the text string;
        append **+f**\ *font* to change its font (size,fontname,color);
        append **+j**\ *justify* to change the text location relative
        to the beachball [Default is ``"TC"``, i.e., Top Center];
        append **+o** to offset the text string by *dx*\ /*dy*.
    convention : str
        Focal mechanism convention. Choose from:

        - ``"aki"`` (Aki & Richards)
        - ``"gcmt"`` (global CMT)
        - ``"mt"`` (seismic moment tensor)
        - ``"partial"`` (partial focal mechanism)
        - ``"principal_axis"`` (principal axis)

        Ignored if ``spec`` is a dictionary or pd.DataFrame.
    component : str
        The component of the seismic moment tensor to plot.

        - ``"full"``: the full seismic moment tensor
        - ``"dc"``: the closest double couple defined from the moment tensor
          (zero trace and zero determinant)
        - ``"deviatoric"``: deviatoric part of the moment tensor (zero trace)
    longitude : float, list, or 1-D numpy array
        Longitude(s) of event location(s). Must be the same length as the
        number of events. Will override the ``longitude`` values
        in ``spec`` if ``spec`` is a dictionary or pd.DataFrame.
    latitude : float, list, or 1-D numpy array
        Latitude(s) of event location(s). Must be the same length as the
        number of events. Will override the ``latitude`` values
        in ``spec`` if ``spec`` is a dictionary or pd.DataFrame.
    depth : float, list, or 1-D numpy array
        Depth(s) of event location(s) in kilometers. Must be the same length
        as the number of events. Will override the ``depth`` values in ``spec``
        if ``spec`` is a dictionary or pd.DataFrame.
    plot_longitude : float, str, list, or 1-D numpy array
        Longitude(s) at which to place beachball(s). Must be the same length
        as the number of events. Will override the ``plot_longitude`` values
        in ``spec`` if ``spec`` is a dictionary or pd.DataFrame.
    plot_latitude : float, str, list, or 1-D numpy array
        Latitude(s) at which to place beachball(s). List must be the same
        length as the number of events. Will override the ``plot_latitude``
        values in ``spec`` if ``spec`` is a dictionary or pd.DataFrame.
    event_name : str, list of str, or 1-D numpy array
        Text string(s), e.g., event name(s) to appear near the beachball(s).
        List must be the same length as the number of events. Will override
        the ``event_name`` labels in ``spec`` if ``spec`` is a dictionary
        or pd.DataFrame.
    labelbox : bool or str
        [*fill*].
        Draw a box behind the label if given. Use *fill* to give a fill color
        [Default is ``"white"``].
    offset : bool or str
        [**+p**\ *pen*][**+s**\ *size*].
        Offset beachball(s) to longitude(s) and latitude(s) specified in the
        the last two columns of the input file or array, or by
        ``plot_longitude`` and ``plot_latitude`` if provided. A small circle
        is plotted at the initial location and a line connects the beachball
        to the circle. Use **+s**\ *size* to set the diameter of the circle
        [Default is no circle]. Use **+p**\ *pen* to set the pen attributes
        for this feature [Default is set via ``pen``]. The fill of the
        circle is set via ``compressionfill`` or ``cmap``, i.e.,
        corresponds to the fill of the compressive quadrants.
    compressionfill : str
        Set color or pattern for filling compressive quadrants
        [Default is ``"black"``]. This setting also applies to the fill of
        the circle defined via ``offset``.
    extensionfill : str
        Set color or pattern for filling extensive quadrants
        [Default is ``"white"``].
    pen : str
        Set pen attributes for all lines related to beachball [Default is
        ``"0.25p,black,solid"``]. This setting applies to ``outline``,
        ``nodal``, and ``offset``, unless overruled by arguments passed to
        those parameters. Draws circumference of beachball.
    outline : bool or str
        [*pen*].
        Draw circumference and nodal planes of beachball. Use *pen* to set
        the pen attributes for this feature [Default is set via ``pen``].
    nodal : bool, int, or str
        [*nplane*][/*pen*].
        Plot the nodal planes and outline the bubble which is transparent.
        If *nplane* is

        - ``0`` or ``True``: both nodal planes are plotted [Default].
        - ``1``: only the first nodal plane is plotted.
        - ``2``: only the second nodal plane is plotted.

        Use /*pen* to set the pen attributes for this feature [Default is
        set via ``pen``].
        For double couple mechanisms, ``nodal`` renders the beachball
        transparent by drawing only the nodal planes and the circumference.
        For non-double couple mechanisms, ``nodal=0`` overlays best
        double couple transparently.
    cmap : str
        File name of a CPT file or a series of comma-separated colors (e.g.,
        *color1,color2,color3*) to build a linear continuous CPT from those
        colors automatically. The color of the compressive quadrants is
        determined by the z-value (i.e., event depth or the third column for
        an input file). This setting also applies to the fill of the circle
        defined via ``offset``.
    no_clip : bool
        Do **not** skip symbols that fall outside the frame boundaries
        [Default is ``False``, i.e., plot symbols inside the frame
        boundaries only].
    {projection}
    {region}
    {frame}
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    kwargs = self._preprocess(**kwargs)

    # Convert spec to pandas.DataFrame unless it's a file
    if isinstance(spec, dict | pd.DataFrame):  # spec is a dict or pd.DataFrame
        # determine convention from dict keys or pd.DataFrame column names
        for conv in ["aki", "gcmt", "mt", "partial", "principal_axis"]:
            if set(convention_params(conv)).issubset(set(spec.keys())):
                convention = conv
                break
        else:
            if isinstance(spec, dict):
                msg = "Keys in dict 'spec' do not match known conventions."
            else:
                msg = "Column names in pd.DataFrame 'spec' do not match known conventions."
            raise GMTError(msg)

        # convert dict to pd.DataFrame so columns can be reordered
        if isinstance(spec, dict):
            # convert values to ndarray so pandas doesn't complain about "all
            # scalar values". See
            # https://github.com/GenericMappingTools/pygmt/pull/2174
            spec = pd.DataFrame(
                {key: np.atleast_1d(value) for key, value in spec.items()}
            )
    elif isinstance(spec, np.ndarray):  # spec is a numpy array
        if convention is None:
            raise GMTInvalidInput("'convention' must be specified for an array input.")
        # make sure convention is a name, not a code
        convention = convention_name(convention)

        # Convert array to pd.DataFrame and assign column names
        spec = pd.DataFrame(np.atleast_2d(spec))
        colnames = ["longitude", "latitude", "depth", *convention_params(convention)]
        # check if spec has the expected number of columns
        ncolsdiff = len(spec.columns) - len(colnames)
        if ncolsdiff == 0:
            pass
        elif ncolsdiff == 1:
            colnames += ["event_name"]
        elif ncolsdiff == 2:
            colnames += ["plot_longitude", "plot_latitude"]
        elif ncolsdiff == 3:
            colnames += ["plot_longitude", "plot_latitude", "event_name"]
        else:
            raise GMTInvalidInput(
                f"Input array must have {len(colnames)} to {len(colnames) + 3} columns."
            )
        spec.columns = colnames

    # Now spec is a pd.DataFrame or a file
    if isinstance(spec, pd.DataFrame):
        # override the values in pd.DataFrame if parameters are given
        for arg, name in [
            (longitude, "longitude"),
            (latitude, "latitude"),
            (depth, "depth"),
            (plot_longitude, "plot_longitude"),
            (plot_latitude, "plot_latitude"),
            (event_name, "event_name"),
        ]:
            if arg is not None:
                spec[name] = np.atleast_1d(arg)

        # Due to the internal implementation of the meca module, we need to
        # convert the following columns to strings if they exist
        if "plot_longitude" in spec.columns and "plot_latitude" in spec.columns:
            spec["plot_longitude"] = spec["plot_longitude"].astype(str)
            spec["plot_latitude"] = spec["plot_latitude"].astype(str)
        if "event_name" in spec.columns:
            spec["event_name"] = spec["event_name"].astype(str)

        # Reorder columns in DataFrame to match convention if necessary
        # expected columns are:
        # longitude, latitude, depth, focal_parameters,
        #   [plot_longitude, plot_latitude] [event_name]
        newcols = ["longitude", "latitude", "depth", *convention_params(convention)]
        if "plot_longitude" in spec.columns and "plot_latitude" in spec.columns:
            newcols += ["plot_longitude", "plot_latitude"]
            if kwargs.get("A") is None:
                kwargs["A"] = True
        if "event_name" in spec.columns:
            newcols += ["event_name"]
        # reorder columns in DataFrame
        if spec.columns.tolist() != newcols:
            spec = spec.reindex(newcols, axis=1)

    # determine data_format from convention and component
    data_format = convention_code(convention=convention, component=component)

    # Assemble -S flag
    kwargs["S"] = f"{data_format}{scale}"
    with Session() as lib:
        with lib.virtualfile_in(check_kind="vector", data=spec) as vintbl:
            lib.call_module(module="meca", args=build_arg_list(kwargs, infile=vintbl))
