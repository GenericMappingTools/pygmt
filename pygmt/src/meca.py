"""
meca - Plot focal mechanisms.
"""

from collections.abc import Sequence
from typing import Literal

import numpy as np
import pandas as pd
from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput, GMTValueError
from pygmt.helpers import (
    build_arg_list,
    data_kind,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.src._common import _FocalMechanismConvention


def _get_focal_convention(spec, convention, component) -> _FocalMechanismConvention:
    """
    Determine the focal mechanism convention from the input data or parameters.
    """
    # Determine the convention from dictionary keys or pandas.DataFrame column names.
    if hasattr(spec, "keys"):  # Dictionary or pandas.DataFrame
        return _FocalMechanismConvention.from_params(spec.keys(), component=component)

    # Determine the convention from the 'convention' parameter.
    if convention is None:
        msg = "Parameter 'convention' must be specified."
        raise GMTInvalidInput(msg)
    return _FocalMechanismConvention(convention=convention, component=component)


def _preprocess_spec(spec, colnames, override_cols):
    """
    Preprocess the input data.

    Parameters
    ----------
    spec
        The input data to be preprocessed.
    colnames
        The minimum required column names of the input data.
    override_cols
        Dictionary of column names and values to override in the input data. Only makes
        sense if ``spec`` is a dict or :class:`pandas.DataFrame`.
    """
    kind = data_kind(spec)  # Determine the kind of the input data.

    # Convert pandas.DataFrame and numpy.ndarray to dict.
    if isinstance(spec, pd.DataFrame):
        spec = {k: v.to_numpy() for k, v in spec.items()}
    elif isinstance(spec, np.ndarray):
        spec = np.atleast_2d(spec)
        # Optional columns that are not required by the convention. The key is the
        # number of extra columns, and the value is a list of optional column names.
        extra_cols = {
            0: [],
            1: ["event_name"],
            2: ["plot_longitude", "plot_latitude"],
            3: ["plot_longitude", "plot_latitude", "event_name"],
        }
        ndiff = spec.shape[1] - len(colnames)
        if ndiff not in extra_cols:
            raise GMTValueError(
                spec.shape[1],
                description="input array shape",
                reason=f"Input array must have {len(colnames)} or two/three more columns.",
            )
        spec = dict(zip([*colnames, *extra_cols[ndiff]], spec.T, strict=False))

    # Now, the input data is a dict or an ASCII file.
    if isinstance(spec, dict):
        # The columns can be overridden by the parameters given in the function
        # arguments. Only makes sense for dict/pandas.DataFrame input.
        if kind != "matrix" and override_cols is not None:
            spec.update({k: v for k, v in override_cols.items() if v is not None})
        # Due to the internal implementation of the meca module, we need to convert the
        # ``plot_longitude``, ``plot_latitude``, and ``event_name`` columns into strings
        # if they exist.
        for key in ["plot_longitude", "plot_latitude", "event_name"]:
            if key in spec:
                spec[key] = np.array(spec[key], dtype=str)

        # Reorder columns to match convention if necessary. The expected columns are:
        # longitude, latitude, depth, focal_parameters, [plot_longitude, plot_latitude],
        # [event_name].
        extra_cols = []
        if "plot_longitude" in spec and "plot_latitude" in spec:
            extra_cols.extend(["plot_longitude", "plot_latitude"])
        if "event_name" in spec:
            extra_cols.append("event_name")
        cols = [*colnames, *extra_cols]
        if list(spec.keys()) != cols:
            spec = {k: spec[k] for k in cols}
    return spec


def _auto_offset(spec) -> bool:
    """
    Determine if offset should be set based on the input data.

    If the input data contains ``plot_longitude`` and ``plot_latitude``, then we set the
    ``offset`` parameter to ``True`` automatically.
    """
    return (
        isinstance(spec, dict | pd.DataFrame)
        and "plot_longitude" in spec
        and "plot_latitude" in spec
    )


@fmt_docstring
@use_alias(
    A="offset",
    B="frame",
    C="cmap",
    E="extensionfill",
    Fr="labelbox",
    G="compressionfill",
    L="outline",
    T="nodal",
    W="pen",
    p="perspective",
)
@kwargs_to_strings(p="sequence")
def meca(  # noqa: PLR0913
    self,
    spec: PathLike | TableLike,
    scale,
    convention: Literal["aki", "gcmt", "mt", "partial", "principal_axis"] | None = None,
    component: Literal["full", "dc", "deviatoric"] = "full",
    longitude: float | Sequence[float] | None = None,
    latitude: float | Sequence[float] | None = None,
    depth: float | Sequence[float] | None = None,
    plot_longitude: float | Sequence[float] | None = None,
    plot_latitude: float | Sequence[float] | None = None,
    event_name: str | Sequence[str] | None = None,
    no_clip: bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot focal mechanisms.

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

    Full GMT docs at :gmt-docs:`supplements/seis/meca.html`.

    {aliases}
       - J = projection
       - N = no_clip
       - R = region
       - S = scale/convention/component
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    spec : str, 1-D numpy array, 2-D numpy array, dict, or pandas.DataFrame
        Data that contain focal mechanism parameters.

        ``spec`` can be specified in either of the following types:

        - *str*: a file name containing focal mechanism parameters as columns. The
          meaning of each column is:

          - Columns 1 and 2: event longitude and latitude
          - Column 3: event depth (in kilometers)
          - Columns 4 to 3+n: focal mechanism parameters. The number of columns *n*
            depends on the choice of ``convention`` (see the table above for the
            supported conventions).
          - Columns 4+n and 5+n: longitude and latitude at which to place the
            beachball. ``0 0`` plots the beachball at the longitude and latitude
            given in the columns 1 and 2. [optional; requires ``offset=True``].
          - Last Column: text string to appear near the beachball [optional].

        - *1-D np.array*: focal mechanism parameters of a single event.
          The meanings of columns are the same as above.
        - *2-D np.array*: focal mechanism parameters of multiple events.
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

        If ``spec`` is either a str or a 1-D or 2-D numpy array, the ``convention``
        parameter is required to interpret the columns. If ``spec`` is a dict or
        a :class:`pandas.DataFrame`, ``convention`` is not needed and ignored if
        specified.
    scale : float or str
        *scale*\ [**+a**\ *angle*][**+f**\ *font*][**+j**\ *justify*]\
        [**+l**][**+m**][**+o**\ *dx*\ [/\ *dy*]][**+s**\ *reference*].
        Adjust scaling of the radius of the beachball, which is  proportional to the
        magnitude. By default, *scale* defines the size for magnitude = 5 (i.e., scalar
        seismic moment M0 = 4.0E23 dyn cm). If **+l** is used the radius will be
        proportional to the seismic moment instead. Use **+s** and give a *reference*
        to change the reference magnitude (or moment), and use **+m** to plot all
        beachballs with the same size. A text string can be specified to appear near
        the beachball (corresponding to column or parameter ``event_name``). Append
        **+a**\ *angle* to change the angle of the text string; append **+f**\ *font*
        to change its font (size,fontname,color); append **+j**\ *justify* to change
        the text location relative to the beachball [Default is ``"TC"``, i.e., Top
        Center]; append **+o** to offset the text string by *dx*\ /*dy*.
    convention
        Specify the focal mechanism convention of the input data. Ignored if ``spec`` is
        a dict or :class:`pandas.DataFrame`. See the table above for the supported
        conventions.
    component
        The component of the seismic moment tensor to plot. Valid values are:

        - ``"full"``: the full seismic moment tensor
        - ``"dc"``: the closest double couple defined from the moment tensor (zero trace
          and zero determinant)
        - ``"deviatoric"``: deviatoric part of the moment tensor (zero trace)
    longitude/latitude/depth
        Longitude(s), latitude(s), and depth(s) of the event(s). The length of each must
        match the number of events. These parameters are only used if ``spec`` is a
        dictionary or a :class:`pandas.DataFrame`, and they override any existing
        ``longitude``, ``latitude``, or ``depth`` values in ``spec``.
    plot_longitude/plot_latitude
        Longitude(s) and latitude(s) at which to place the beachball(s). The length of
        each must match the number of events. These parameters are only used if ``spec``
        is a dictionary or a :class:`pandas.DataFrame`, and they override any existing
        ``plot_longitude`` or ``plot_latitude`` values in ``spec``.
    event_name
        Text string(s), such as event name(s), to appear near the beachball(s). The
        length must match the number of events. This parameter is only used if ``spec``
        is a dictionary or a :class:`pandas.DataFrame`, and it overrides any existing
        ``event_name`` labels in ``spec``.
    labelbox : bool or str
        [*fill*].
        Draw a box behind the label if given via ``event_name``. Use *fill* to give a
        fill color [Default is ``"white"``].
    offset : bool or str
        [**+p**\ *pen*][**+s**\ *size*].
        Offset beachball(s) to the longitude(s) and latitude(s) specified in the last
        two columns of the input file or array, or by ``plot_longitude`` and
        ``plot_latitude`` if provided. A line from the beachball to the initial location
        is drawn. Use **+s**\ *size* to plot a small circle at the initial location and
        to set the diameter of this circle [Default is no circle]. Use **+p**\ *pen* to
        set the pen attributes for this feature [Default is set via ``pen``]. The fill
        of the circle is set via ``compressionfill`` or ``cmap``, i.e., corresponds to
        the fill of the compressive quadrants.
    compressionfill : str
        Set color or pattern for filling compressive quadrants [Default is ``"black"``].
        This setting also applies to the fill of the circle defined via ``offset``.
    extensionfill : str
        Set color or pattern for filling extensive quadrants [Default is ``"white"``].
    pen : str
        Set (default) pen attributes for all lines related to the beachball [Default is
        ``"0.25p,black,solid"``]. This setting applies to ``outline``, ``nodal``, and
        ``offset``, unless overruled by arguments passed to those parameters. Draws the
        circumference of the beachball.
    outline : bool or str
        [*pen*].
        Draw circumference and nodal planes of the beachball. Use *pen* to set  the pen
        attributes for this feature [Default is set via ``pen``].
    nodal : bool, int, or str
        [*nplane*][/*pen*].
        Plot the nodal planes and outline the bubble which is transparent. If *nplane*
        is

        - ``0`` or ``True``: both nodal planes are plotted [Default].
        - ``1``: only the first nodal plane is plotted.
        - ``2``: only the second nodal plane is plotted.

        Use /*pen* to set the pen attributes for this feature [Default is set via
        ``pen``].
        For double couple mechanisms, ``nodal`` renders the beachball transparent by
        drawing only the nodal planes and the circumference. For non-double couple
        mechanisms, ``nodal=0`` overlays best double couple transparently.
    cmap : str
        File name of a CPT file or a series of comma-separated colors (e.g.,
        *color1,color2,color3*) to build a linear continuous CPT from those colors
        automatically. The color of the compressive quadrants is determined by the
        z-value (i.e., event depth or the third column for an input file). This setting
        also applies to the fill of the circle defined via ``offset``.
    no_clip
        Do **not** skip symbols that fall outside the frame boundaries [Default is
        ``False``, i.e., plot symbols inside the frame boundaries only].
    {projection}
    {region}
    {frame}
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    self._activate_figure()
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

    aliasdict = AliasSystem(
        N=Alias(no_clip, name="no_clip"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(check_kind="vector", data=spec) as vintbl:
            lib.call_module(
                module="meca", args=build_arg_list(aliasdict, infile=vintbl)
            )
