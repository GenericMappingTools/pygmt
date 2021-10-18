"""
project - Project data onto lines or great circles, or generate tracks.
"""
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    A="azimuth",
    C="center",
    E="endpoint",
    F="flags",
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
def project(data=None, x=None, y=None, z=None, outfile=None, **kwargs):
    r"""
    Project data onto lines or great circles, or generate tracks.

    Project reads arbitrary :math:`(x, y [, z])` data and returns any
    combination of :math:`(x, y, z, p, q, r, s)`, where :math:`(p, q)` are the
    coordinates in the projection, :math:`(r, s)` is the position in the
    :math:`(x, y)` coordinate system of the point on the profile (:math:`q = 0`
    path) closest to :math:`(x, y)`, and :math:`z` is all remaining columns in
    the input (beyond the required :math:`x` and :math:`y` columns).

    Alternatively, :doc:`pygmt.project` may be used to generate
    :math:`(r, s, p)` triples at equal increments along a profile using the
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

    To specify an oblique projection, use the ``pole`` option to set
    the pole. Then the equator of the projection is already determined and the
    ``center`` option is used to locate the :math:`p = 0` meridian. The center
    *cx/cy* will be taken as a point through which the :math:`p = 0` meridian
    passes. If you do not care to choose a particular point, use the South pole
    (*cx* = 0, *cy* = -90).

    Data can be selectively windowed by using the ``length`` and ``width``
    options. If ``width`` is used, the projection width is set to use only
    data with :math:`w_{{min}} < q < w_{{max}}`. If ``length`` is set, then
    the length is set to use only those data with
    :math:`l_{{min}} < p < l_{{max}}`. If the ``endpoint`` option
    has been used to define the projection, then ``length="w"`` may be used to
    window the length of the projection to exactly the span from O to B.

    Flat Earth (Cartesian) coordinate transformations can also be made. Set
    ``flat_earth=True`` and remember that azimuth is clockwise from North (the
    y axis), NOT the usual cartesian theta, which is counterclockwise from the
    x axis. azimuth = 90 - theta.

    No assumptions are made regarding the units for
    :math:`x, y, r, s, p, q, dist, l_{{min}}, l_{{max}}, w_{{min}}, w_{{max}}`.
    If -Q is selected, map units are assumed and :math:`x, y, r, s` must be in
    degrees and :math:`p, q, dist, l_{{min}}, l_{{max}}, w_{{min}}, w_{{max}}`
    will be in km.

    Calculations of specific great-circle and geodesic distances or for
    back-azimuths or azimuths are better done using :gmt-docs:`mapproject` as
    project is strictly spherical.

    :doc:`pygmt.project` is case sensitive: use lower case for the
    **xyzpqrs** letters in ``flags``.

    {aliases}

    Parameters
    ----------
    data : str or {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2D
        {table-classes}.

    center : str or list
        *cx*/*cy*.
        *cx/cy* sets the origin of the projection, in Definition 1 or 2. If
        Definition 3 is used, then *cx/cy* are the coordinates of a
        point through which the oblique zero meridian (:math:`p = 0`) should
        pass. The *cx/cy* is not required to be 90 degrees from the pole.

    azimuth : float or str
        defines the azimuth of the projection (Definition 1).

    endpoint : str or list
        *bx*/*by*.
        *bx/by* defines the end point of the projection path (Definition 2).

    flags : str
        Specify your desired output using any combination of **xyzpqrs**, in
        any order [Default is **xypqrsz**]. Do not space between the letters.
        Use lower case. The output will be columns of values corresponding to
        your ``flags``. The **z** flag is special and refers to all numerical
        columns beyond the leading **x** and **y** in your input record. The
        **z** flag also includes any trailing text (which is placed at the end
        of the record regardless of the order of **z** in ``flags``). **Note**:
        If ``generate`` is True, then the output order is hardwired to be
        **rsp** and ``flags`` is not allowed.

    generate : str
        *dist* [/*colat*][**+c**\|\ **h**].
        Generate mode. No input is read and the value of ``data`` is ignored
        (you can use, e.g., ``data=None``). Create :math:`(r, s, p)` output
        data every *dist* units of :math:`p`. See `unit` option.
        Alternatively, append */colat* for a small circle instead [Default is a
        colatitude of 90, i.e., a great circle]. If setting a pole with
        ``pole`` and you want the small circle to go through *cx*/*cy*,
        append **+c** to compute the required colatitude. Use ``center`` and
        ``endpoint`` to generate a circle that goes through the center and end
        point. Note, in this case the center and end point cannot be farther
        apart than :math:`2|\mbox{{colat}}|`. Finally, if you append **+h**
        then we will report the position of the pole as part of the segment
        header [Default is no header].

    length : str or list
        [**w**\|\ *l_min*/*l_max*].
        Length controls. Project only those data whose *p* coordinate is
        within :math:`l_{{min}} < p < l_{{max}}`. If ``endpoint`` has been set,
        then you may alternatively use **w** to stay within the distance from
        ``center`` to ``endpoint``.

    flat_earth : bool
        If `True`, Make a Cartesian coordinate transformation in the plane.
        [Default uses spherical trigonometry.]

    unit : bool
        If `True`, project assumes :math:`x, y, r, s` are in degrees while
        :math:`p, q, dist, l_{{min}}, l_{{max}}, w_{{min}}, {{w_max}}` are in
        km. If not set (or ``False``), then all these are assumed to be in the
        same units.

    sort : bool
        Sort the output into increasing :math:`p` order. Useful when projecting
        random data into a sequential profile.

    pole : str or list
        *px*/*py*.
        *px/py* sets the position of the rotation pole of the projection.
        (Definition 3).

    {V}

    width : str or list
        *w_min*/*w_max*.
        Width controls. Project only those data whose :math:`q` coordinate is
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
        by appending the unit (e.g., 3d for degrees) [Default is km]; if so we
        assume the increment is also given in the same unit.  **Note**:
        For the Cartesian ellipse (which requires ``flat_earth``), we expect
        *direction* counter-clockwise from the horizontal instead of an
        *azimuth*.

    outfile : str
        The file name for the output ASCII file.

    {f}

    Returns
    -------
    track: pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, ..., newcolname) if
          ``outfile`` is not set
        - None if ``outfile`` is set (output will be stored in file set
          by ``outfile``)
    """

    if "C" not in kwargs:
        raise GMTInvalidInput("The `center` parameter must be specified.")
    if "G" not in kwargs and data is None:
        raise GMTInvalidInput(
            "The `data` parameter must be specified unless `generate` is used."
        )
    if "G" in kwargs and "F" in kwargs:
        raise GMTInvalidInput("The `flags` parameter is not allowed with `generate`.")

    with GMTTempFile(suffix=".csv") as tmpfile:
        if outfile is None:  # Output to tmpfile if outfile is not set
            outfile = tmpfile.name
        with Session() as lib:
            if "G" not in kwargs:
                # Choose how data will be passed into the module
                table_context = lib.virtualfile_from_data(
                    check_kind="vector", data=data, x=x, y=y, z=z, required_z=False
                )

                # Run project on the temporary (csv) data table
                with table_context as infile:
                    arg_str = " ".join(
                        [infile, build_arg_string(kwargs), "->" + outfile]
                    )
            else:
                arg_str = " ".join([build_arg_string(kwargs), "->" + outfile])
            lib.call_module(module="project", args=arg_str)

        # if user did not set outfile, return pd.DataFrame
        if outfile == tmpfile.name:
            if "G" in kwargs:
                column_names = list("rsp")
                result = pd.read_csv(tmpfile.name, sep="\t", names=column_names)
            else:
                result = pd.read_csv(tmpfile.name, sep="\t", header=None, comment=">")
        # return None if outfile set, output in outfile
        elif outfile != tmpfile.name:
            result = None

    return result
