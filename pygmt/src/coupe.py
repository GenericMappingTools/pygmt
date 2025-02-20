"""
coupe - Plot cross-sections of focal mechanisms.
"""

import numpy as np
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTError, GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.src.meca import convention_params, convention_code, convention_name

def section_convention_code(section_format):

    codes = {
        "lonlat_lonlat": "a",
        "lonlat_strlen": "b",
        "xy_xy": "c",
        "xy_strlen": "d"
    }

    if section_format in codes:
        return codes[section_format]
    else:
        raise GMTInvalidInput(f"Invalid section format '{section_format}'.")

@fmt_docstring
@use_alias(
    A="section",
    B="frame",
    C="cmap",
    E="extensionfill",
    Fa="PTaxis",
    Fr="labelbox",
    G="compressionfill",
    J="projection",
    L="outline",
    N="no_clip",
    Q="no_file",
    R="region",
    T="nodal",
    V="verbose",
    W="pen",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(A="sequence", R="sequence", c="sequence_comma", p="sequence")
def coupe(
    self,
    spec,
    scale,
    convention=None,
    component="full",
    longitude=None,
    latitude=None,
    depth=None,
    section_format='lonlat_lonlat',
    plot_longitude=None,
    plot_latitude=None,
    event_name=None,
    **kwargs
):
    r"""
    Plot focal mechanisms in a vertical cross section.
    This function/method is copied from `pygmt.src.meca.meca()`
    Full option list at :gmt-docs:`supplements/seis/coupe.html`
    {aliases}
    Parameters
    ----------
    spec : str, 1-D array, 2-D array, dict, or pd.DataFrame
        Data that contains focal mechanism parameters.
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
          columns. If ``spec`` is a dict or a :class:`pandas.DataFrame`, 
          ``convention`` is not needed and ignored if specified.
        
    scale : int, float, or str
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
    section : list, or str
        Cross-section parameters.
        *section*\ a|b|c|dparams[+c[n|t]][+ddip][+r[a|e|dx]][+wwidth]\
        [+z[s]a|e|dz|min/max]. 
        a, b, c, and d are specified by *section_format*.
        a: List of four float values of the longitude and latitude of points 1 and 2
        limiting the length of the cross-section.
        b: List of four float values of the longitude and latitude of 
        the beginning of the cross-section, strike is the azimuth of 
        the direction of the cross-section, and length is the length 
        along which the cross-section is made (in km).
        c: List of four float values the same as `a` option 
        with x and y given as Cartesian coordinates.
        d: List of four float values the same as `b` option 
        with x and y given as Cartesian coordinates.
    section_format : str, `"lonlat_lonlat"`
        `"lonlat_lonlat"`: a
        `"lonlat_strlen"`: b
        `"xy_xy"`: c
        `"xy_strlen"`: d
    no_file : bool, default to False
        If True, creates no output files in the current path.
    convention : str
        Focal mechanism convention. Choose from:
        - ``"aki"`` (Aki & Richards)
        - ``"gcmt"`` (global CMT)
        - ``"mt"`` (seismic moment tensor)
        - ``"partial"`` (partial focal mechanism)
        - ``"principal_axis"`` (principal axis)
        Ignored if ``spec`` is a dict or :class:`pandas.DataFrame`.
    component : str
        The component of the seismic moment tensor to plot.
        - ``"full"``: the full seismic moment tensor
        - ``"dc"``: the closest double couple defined from the moment tensor
          (zero trace and zero determinant)
        - ``"deviatoric"``: deviatoric part of the moment tensor (zero trace)
    longitude/latitude/depth : float, list, or 1-D numpy array
        Longitude(s) / latitude(s) / depth(s) of the event(s). Length must match the
        number of events. Overrides the ``longitude`` / ``latitude`` / ``depth`` values
        in ``spec`` if ``spec`` is a dict or :class:`pandas.DataFrame`.
    event_name : str or list of str, or 1-D numpy array
        Text string(s), e.g., event name(s) to appear near the beachball(s).
        List must be the same length as the number of events. Will override
        the ``event_name`` labels in ``spec`` if ``spec`` is a dict or :class:`pandas.DataFrame`.
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

    ## The cross-sectional profile
    if kwargs.get("A") is None:
        raise GMTInvalidInput("The `section` parameter must be specified.")
    kwargs["A"] = section_convention_code(section_format) + kwargs["A"]

    # Convert spec to pandas.DataFrame unless it's a file
    if isinstance(spec, (dict, pd.DataFrame)):  # spec is a dict or pd.DataFrame
        # determine convention from dict keys or pd.DataFrame column names
        for conv in ["aki", "gcmt", "mt", "partial", "pricipal_axis"]:
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
            msg = "'convention' must be specified for an array input."
            raise GMTInvalidInput(msg)
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
            msg = (
                f"Input array must have {len(colnames)} to {len(colnames) + 3} columns."
            )
            raise GMTInvalidInput(msg)
        spec.columns = colnames

    # Now spec is a pd.DataFrame or a file
    if isinstance(spec, pd.DataFrame):
        # override the values in pd.DataFrame if parameters are given
        if longitude is not None:
            spec["longitude"] = np.atleast_1d(longitude)
        if latitude is not None:
            spec["latitude"] = np.atleast_1d(latitude)
        if depth is not None:
            spec["depth"] = np.atleast_1d(depth)
        if event_name is not None:
            spec["event_name"] = np.atleast_1d(event_name)

        # Due to the internal implementation of the meca module, we need to
        # convert the following columns to strings if they exist
        if "event_name" in spec.columns:
            spec["event_name"] = spec["event_name"].astype(str)

        # Reorder columns in DataFrame to match convention if necessary
        # expected columns are:
        # longitude, latitude, depth, focal_parameters,
        #   [event_name]
        newcols = ["longitude", "latitude", "depth"] + convention_params(convention)
        if "event_name" in spec.columns:
            newcols += ["event_name"]
        # reorder columns in DataFrame
        if spec.columns.tolist() != newcols:
            spec = spec.reindex(newcols, axis=1)

    data_format = convention_code(convention=convention, component=component)
    kwargs["S"] = f"{data_format}{scale}"

    with Session() as lib:
        # Choose how data will be passed into the module
        file_context = lib.virtualfile_in(check_kind="vector", data=spec)
        with file_context as fname:
            lib.call_module(module="coupe", args=build_arg_list(kwargs, infile=fname))
            