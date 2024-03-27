"""
project - Project data onto lines or great circles, or generate tracks.
"""

from typing import Literal

import numpy as np
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
    validate_output_table_type,
)


@fmt_docstring
@use_alias(
    A="azimuth",
    C="center",
    E="endpoint",
    F="convention",
    G="generate",
    L="length",
    N="flat_earth",
    Q="unit",
    S="sort",
    T="pole",
    V="verbose",
    W="width",
    Z="ellipse",
    f="coltypes",
)
@kwargs_to_strings(E="sequence", L="sequence", T="sequence", W="sequence", C="sequence")
def project(
    data=None,
    x=None,
    y=None,
    z=None,
    output_type: Literal["pandas", "numpy", "file"] = "pandas",
    outfile: str | None = None,
    **kwargs,
) -> pd.DataFrame | np.ndarray | None:
    r"""
    Project data onto lines or great circles, or generate tracks.

    Project reads arbitrary :math:`(x, y [, z])` data and returns any
    combination of :math:`(x, y, z, p, q, r, s)`, where :math:`(p, q)` are the
    coordinates in the projection, :math:`(r, s)` is the position in the
    :math:`(x, y)` coordinate system of the point on the profile (:math:`q = 0`
    path) closest to :math:`(x, y)`, and :math:`z` is all remaining columns in
    the input (beyond the required :math:`x` and :math:`y` columns).

    Alternatively, ``project`` may be used to generate
    :math:`(r, s, p)` triplets at equal increments along a profile using the
    ``generate`` parameter. In this case, the value of ``data`` is ignored
    (you can use, e.g., ``data=None``).

    Projections are defined in any (but only) one of three ways:

    1. By a ``center`` and an ``azimuth`` in degrees clockwise from North.
    2. By a ``center`` and ``endpoint`` of the projection path.
    3. By a ``center`` and a ``pole`` position.

    To spherically project data along a great circle path, an oblique
    coordinate system is created which has its equator along that path, and the
    zero meridian through the Center. Then the oblique longitude (:math:`p`)
    corresponds to the distance from the Center along the great circle, and the
    oblique latitude (:math:`q`) corresponds to the distance perpendicular to
    the great circle path. When moving in the increasing (:math:`p`) direction,
    (toward B or in the azimuth direction), the positive (:math:`q`) direction
    is to your left. If a Pole has been specified, then the positive
    (:math:`q`) direction is toward the pole.

    To specify an oblique projection, use the ``pole`` parameter to set
    the pole. Then the equator of the projection is already determined and the
    ``center`` parameter is used to locate the :math:`p = 0` meridian. The
    center *cx/cy* will be taken as a point through which the :math:`p = 0`
    meridian passes. If you do not care to choose a particular point, use the
    South pole (*cx* = 0, *cy* = -90).

    Data can be selectively windowed by using the ``length`` and ``width``
    parameters. If ``width`` is used, the projection width is set to use only
    data with :math:`w_{{min}} < q < w_{{max}}`. If ``length`` is set, then
    the length is set to use only those data with
    :math:`l_{{min}} < p < l_{{max}}`. If the ``endpoint`` parameter
    has been used to define the projection, then ``length="w"`` may be used to
    window the length of the projection to exactly the span from O to B.

    Flat Earth (Cartesian) coordinate transformations can also be made. Set
    ``flat_earth=True`` and remember that azimuth is clockwise from North (the
    y axis), NOT the usual cartesian theta, which is counterclockwise from the
    x axis. azimuth = 90 - theta.

    No assumptions are made regarding the units for
    :math:`x, y, r, s, p, q, dist, l_{{min}}, l_{{max}}, w_{{min}}, w_{{max}}`.
    If ``unit`` is selected, map units are assumed and :math:`x, y, r, s` must
    be in degrees and
    :math:`p, q, dist, l_{{min}}, l_{{max}}, w_{{min}}, w_{{max}}`
    will be in km.

    Calculations of specific great-circle and geodesic distances or for
    back-azimuths or azimuths are better done using :gmt-docs:`mapproject` as
    project is strictly spherical.

    Full option list at :gmt-docs:`project.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    {output_type}
    {outfile}

    center : str or list
        *cx*/*cy*.
        Set the origin of the projection, in Definition 1 or 2. If
        Definition 3 is used, then *cx/cy* are the coordinates of a
        point through which the oblique zero meridian (:math:`p = 0`) should
        pass. The *cx/cy* is not required to be 90 degrees from the pole.

    azimuth : float or str
        Define the azimuth of the projection (Definition 1).

    endpoint : str or list
        *bx*/*by*.
        Define the end point of the projection path (Definition 2).

    convention : str
        Specify the desired output using any combination of **xyzpqrs**, in
        any order [Default is **xypqrsz**]. Do not space between the letters.
        Use lower case. The output will be columns of values corresponding to
        your ``convention``. The **z** flag is special and refers to all
        numerical columns beyond the leading **x** and **y** in your input
        record. The **z** flag also includes any trailing text (which is
        placed at the end of the record regardless of the order of **z** in
        ``convention``). **Note**: If ``generate`` is True, then the output
        order is hardwired to be **rsp** and ``convention`` is not allowed.

    generate : str
        *dist* [/*colat*][**+c**\|\ **h**].
        Create :math:`(r, s, p)` output data every *dist* units of :math:`p`
        (See ``unit`` parameter). Alternatively, append */colat* for a small
        circle instead [Default is a colatitude of 90, i.e., a great circle].
        If setting a pole with ``pole`` and you want the small circle to go
        through *cx*/*cy*, append **+c** to compute the required colatitude.
        Use ``center`` and ``endpoint`` to generate a circle that goes
        through the center and end point. Note, in this case the center and
        end point cannot be farther apart than :math:`2|\mbox{{colat}}|`.
        Finally, if you append **+h** then we will report the position of
        the pole as part of the segment header [Default is no header].
        **Note**: No input is read and the value of ``data``, ``x``, ``y``,
        and ``z`` is ignored if ``generate`` is used.

    length : str or list
        [**w**\|\ *l_min*/*l_max*].
        Project only those data whose *p* coordinate is
        within :math:`l_{{min}} < p < l_{{max}}`. If ``endpoint`` has been set,
        then you may alternatively use **w** to stay within the distance from
        ``center`` to ``endpoint``.

    flat_earth : bool
        Make a Cartesian coordinate transformation in the plane.
        [Default is ``False``; plane created with spherical trigonometry.]

    unit : bool
        Set units for :math:`x, y, r, s` to degrees and
        :math:`p, q, dist, l_{{min}}, l_{{max}}, w_{{min}}, w_{{max}}` to km.
        [Default is ``False``; all arguments use the same units]

    sort : bool
        Sort the output into increasing :math:`p` order. Useful when projecting
        random data into a sequential profile.

    pole : str or list
        *px*/*py*.
        Set the position of the rotation pole of the projection.
        (Definition 3).

    {verbose}

    width : str or list
        *w_min*/*w_max*.
        Project only those data whose :math:`q` coordinate is
        within :math:`w_{{min}} < q < w_{{max}}`.

    ellipse : str
        *major*/*minor*/*azimuth* [**+e**\|\ **n**].
        Used in conjunction with ``center`` (sets its center) and ``generate``
        (sets the distance increment) to create the coordinates of an ellipse
        with *major* and *minor* axes given in km (unless ``flat_earth`` is
        given for a Cartesian ellipse) and the *azimuth* of the major axis in
        degrees. Append **+e** to adjust the increment set via ``generate`` so
        that the the ellipse has equal distance increments [Default uses the
        given increment and closes the ellipse].  Instead, append **+n** to set
        a specific number of unique equidistant data via ``generate``. For
        degenerate ellipses you can just supply a single *diameter* instead.  A
        geographic diameter may be specified in any desired unit other than km
        by appending the unit (e.g., 3-D for degrees) [Default is km];
        the increment is assumed to be in the same unit.  **Note**:
        For the Cartesian ellipse (which requires ``flat_earth``), the
        *direction* is counter-clockwise from the horizontal instead of an
        *azimuth*.

    {coltypes}

    Returns
    -------
    ret
        Return type depends on ``outfile`` and ``output_type``:

        - ``None`` if ``outfile`` is set (output will be stored in file set by
          ``outfile``)
        - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile`` is not set
          (depends on ``output_type``)
    """
    if kwargs.get("C") is None:
        raise GMTInvalidInput("The `center` parameter must be specified.")
    if kwargs.get("G") is None and data is None:
        raise GMTInvalidInput(
            "The `data` parameter must be specified unless `generate` is used."
        )
    if kwargs.get("G") is not None and kwargs.get("F") is not None:
        raise GMTInvalidInput(
            "The `convention` parameter is not allowed with `generate`."
        )

    output_type = validate_output_table_type(output_type, outfile=outfile)

    column_names = None
    if output_type == "pandas" and kwargs.get("G") is not None:
        column_names = list("rsp")

    with Session() as lib:
        with (
            lib.virtualfile_in(
                check_kind="vector",
                data=data,
                x=x,
                y=y,
                z=z,
                required_z=False,
                required_data=False,
            ) as vintbl,
            lib.virtualfile_out(kind="dataset", fname=outfile) as vouttbl,
        ):
            lib.call_module(
                module="project",
                args=build_arg_list(kwargs, infile=vintbl, outfile=vouttbl),
            )
        return lib.virtualfile_to_dataset(
            vfname=vouttbl,
            output_type=output_type,
            column_names=column_names,
        )
