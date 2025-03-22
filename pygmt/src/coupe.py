"""
coupe - Plot cross-sections of focal mechanisms.
"""

import numpy as np
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    data_kind,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.src.meca import _get_focal_convention, _preprocess_spec, _auto_offset

def section_convention_code(section_format):

    codes = {
        "lonlat_lonlat": "a",
        "lonlat_strlen": "b",
        "xy_xy": "c",
        "xy_strlen": "d"
    }

    if section_format not in codes:
        msg = f"Invalid section format '{section_format}'."
        raise GMTInvalidInput(msg)
    return codes[section_format]
        

@fmt_docstring
@use_alias(
    A="section",
    B="frame",
    C="cmap",
    E="extensionfill",
    Fa="pt_axes",
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
    Plot focal mechanisms in a cross section.

    This function/method is copied from `pygmt.src.meca.meca()`

    The following focal mechanism conventions are supported:

    .. list-table:: Supported focal mechanism conventions.
       :widths: 15 15 40 30
       :header-rows: 1

       * - Convention
         - Description
         - Focal parameters
         - Remark
       * - ``"aki"``
         - Aki and Richard
         - *strike*, *dip*, *rake*, *magnitude*
         - angles in degrees
       * - ``"gcmt"``
         - global centroid moment tensor
         - | *strike1*, *dip1*, *rake1*,
           | *strike2*, *dip2*, *rake2*,
           | *mantissa*, *exponent*
         - | angles in degrees;
           | seismic moment is
           | :math:`mantissa * 10 ^ {{exponent}}`
           | in dyn cm
       * - ``"mt"``
         - seismic moment tensor
         - | *mrr*, *mtt*, *mff*,
           | *mrt*, *mrf*, *mtf*,
           | *exponent*
         - | moment components
           | in :math:`10 ^ {{exponent}}` dyn cm
       * - ``"partial"``
         - partial focal mechanism
         - | *strike1*, *dip1*, *strike2*,
           | *fault_type*, *magnitude*
         - | angles in degrees;
           | *fault_type* means +1/-1 for
           | normal/reverse fault
       * - ``"principal_axis"``
         - principal axis
         - | *t_value*, *t_azimuth*, *t_plunge*,
           | *n_value*, *n_azimuth*, *n_plunge*,
           | *p_value*, *p_azimuth*, *p_plunge*,
           | *exponent*
         - | values in :math:`10 ^ {{exponent}}` dyn cm;
           | azimuths and plunges in degrees

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
        - *dict* or :class:`pandas.DataFrame`: The dict keys or
          :class:`pandas.DataFrame` column names determine the focal mechanism
          convention. For the different conventions, the combination of keys /
          column names as given in the table above are required.

          A dict may contain values for a single focal mechanism or lists of
          values for multiple focal mechanisms.

          Both dict and :class:`pandas.DataFrame` may optionally contain the keys /
          column names: ``latitude``, ``longitude``, ``depth``, ``plot_longitude``,
          ``plot_latitude``, and/or ``event_name``.

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
    section : list or str
        Cross-section parameters.
        *section*\ a|b|c|dparams[+c[n|t]][+ddip][+r[a|e|dx]][+wwidth]\
        [+z[s]a|e|dz|min/max]. 
        a, b, c, and d are specified by *section_format*.

        - a: List of four float values of the longitude and latitude of points 1 and 2
        limiting the length of the cross-section.
        - b: List of four float values of the longitude and latitude of
        the beginning of the cross-section, strike is the azimuth of
        the direction of the cross-section, and length is the length 
        along which the cross-section is made (in km).
        - c: List of four float values the same as `a` option
        with x and y given as Cartesian coordinates.
        - d: List of four float values the same as `b` option 
        with x and y given as Cartesian coordinates.
    section_format : str
        
        - ``"lonlat_lonlat"``: a
        - ``"lonlat_strlen"``: b
        - ``"xy_xy"``: c
        - ``"xy_strlen"``: d
    no_file : bool
        If True, creates no output files in the current path. [Default is ``False``].
    convention : str
        Focal mechanism convention. See the table above for the supported conventions.
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
    pt_axes : bool or str
        [*size*[/*Psymbol*[*Tsymbol*]]]
        Compute and plot P and T axes with symbols. Optionally specify size and 
        (separate) P and T axis symbols from the following: (c) circle, 
        (d) diamond, (h) hexagon, (i) inverse triangle, (p) point, (s) square, 
        (t) triangle, (x) cross. [Default is ``"6p/cc"``]
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

    # Determine the focal mechanism convention from the input data or parameters.
    _convention = _get_focal_convention(spec, convention, component)
    # Preprocess the input data.
    spec = _preprocess_spec(
        spec,
        # The minimum expected columns for the input data.
        colnames=["longitude", "latitude", "depth", *_convention.params],
        override_cols={
            "longitude": longitude,
            "latitude": latitude,
            "depth": depth,
            "plot_longitude": plot_longitude,
            "plot_latitude": plot_latitude,
            "event_name": event_name,
        },
    )
    
    # Determine the offset parameter if not provided.
    if kwargs.get("A") is None:
        kwargs["A"] = _auto_offset(spec)
    kwargs["S"] = f"{_convention.code}{scale}"
    
    with Session() as lib:
        # Choose how data will be passed into the module
        file_context = lib.virtualfile_in(check_kind="vector", data=spec)
        with file_context as fname:
            lib.call_module(module="coupe", args=build_arg_list(kwargs, infile=fname))
            