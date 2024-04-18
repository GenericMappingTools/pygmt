"""
rose - Plot windrose diagrams or polar histograms.
"""

from pygmt.clib import Session
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    A="sector",
    B="frame",
    C="cmap",
    D="shift",
    Em="vectors",
    F="no_scale",
    G="fill",
    I="inquire",
    JX="diameter",
    L="labels",
    M="vector_params",
    Q="alpha",
    R="region",
    S="norm",
    T="orientation",
    V="verbose",
    W="pen",
    Z="scale",
    b="binary",
    d="nodata",
    e="find",
    h="header",
    i="incols",
    c="panel",
    p="perspective",
    t="transparency",
    w="wrap",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", i="sequence_comma", p="sequence")
def rose(self, data=None, length=None, azimuth=None, **kwargs):
    """
    Plot windrose diagrams or polar histograms.

    Takes a matrix, (length,azimuth) pairs, or a file name as input
    and plots windrose diagrams or polar histograms (sector diagram
    or rose diagram).

    Must provide either ``data`` or ``length`` and ``azimuth``.

    Options include full circle and half circle plots. The outline
    of the windrose is drawn with the same color as
    :gmt-term:`MAP_DEFAULT_PEN`.

    Full option list at :gmt-docs:`rose.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Pass in either a file name to an ASCII data table, a 2-D
        {table-classes}.
        Use parameter ``incols`` to choose which columns are length and
        azimuth, respectively. If a file with only azimuths is given, use
        ``incols`` to indicate the single column with azimuths; then all
        lengths are set to unity (see ``scale="u"`` to set actual
        lengths to unity as well).

    length/azimuth : float or 1-D arrays
        Length and azimuth values, or arrays of length and azimuth
        values.

    orientation : bool
        Specify that the input data are orientation data (i.e., have a
        180 degree ambiguity) instead of true 0-360 degree directions
        [Default is 0-360 degrees]. We compensate by counting each record
        twice: First as azimuth and second as azimuth +180. Ignored if
        ``region`` is given as (-90, 90) or (0, 180).

    region : str or list
        *r0/r1/az0/az1* or [*r0*, *r1*, *az0*, *az1*].
        *Required if this is the first plot command*.
        Specify the ``region`` of interest in (*r*, *azimuth*) space.
        Here, *r0* is 0 and *r1* is the maximal length in units.
        For *az0* and *az1*, specify either (-90, 90) or (0, 180) for
        half circle plot or (0, 360) for full circle.

    diameter : str
         Set the diameter of the rose diagram. If not given,
         then we default to a diameter of 7.5 cm.

    sector : float or str
         Give the sector width in degrees for sector and rose diagram.
         Default ``0`` means windrose diagram. Append **+r** to draw rose
         diagram instead of sector diagram (e.g. ``"10+r"``).

    norm : bool
         Normalize input radii (or bin counts if ``sector`` is used)
         by the largest value so all radii (or bin counts) range from 0
         to 1.

    frame : str
         Set map boundary frame and axes attributes. Remember that *x*
         here is radial distance and *y* is azimuth. The y label may be
         used to plot a figure caption. The scale bar length is determined
         by the radial gridline spacing.

    scale : float or str
         Multiply the data radii by scale. E.g., use ``scale=0.001`` to
         convert your data from m to km. To exclude the radii from
         consideration, set them all to unity with ``scale="u"``
         [Default is no scaling].

    fill : str
         Set color or pattern for filling sectors [Default is no fill].

    cmap : str
        Give a CPT. The *r*-value for each sector is used to look-up the
        sector color. Cannot be used with a rose diagram.

    pen : str
        Set pen attributes for sector outline or rose plot, e.g.
        ``pen="0.5p"``. [Default is no outline]. To change pen used to
        draw vector (requires ``vectors``) [Default is same as sector
        outline] use e.g. ``pen="v0.5p"``.

    labels : str
         *wlabel,elabel,slabel,nlabel*.
         Specify labels for the 0, 90, 180, and 270 degree marks.
         For full-circle plot the default is
         ``"West,East,South,North"`` and for half-circle the default
         is ``"90W,90E,-,0"``. A ``"-"`` in any entry disables that
         label (e.g. ``labels="W,E,-,N"``). Use ``labels=""`` to
         disable all four labels. Note that the
         :gmt-term:`GMT_LANGUAGE` setting will affect the words used.

    no_scale : bool
         Do NOT draw the scale length bar (``no_scale=True``).
         Default plots scale in lower right corner provided ``frame``
         is used.

    shift : bool
         Shift sectors so that they are centered on the bin interval
         (e.g., first sector is centered on 0 degrees).

    vectors : str
          *mode_file*.
          Plot vectors showing the principal directions given in
          the *mode_file* file.
          Alternatively, specify ``vectors`` to compute and plot
          mean direction. See ``vector_params`` to control the vector
          attributes. Finally, to instead save the computed mean
          direction and other statistics, use
          ``vectors="+wmode_file"``. The eight items saved to
          a single record are: *mean_az*, *mean_r*, *mean_resultant*,
          *max_r*, *scaled_mean_r*, *length_sum*, *n*, *sign@alpha*,
          where the last term is 0 or 1 depending on whether the mean
          resultant is significant at the level of confidence set via
          ``alpha``.

    vector_params : str
        Used with ``vectors`` to modify vector parameters. For
        vector heads, append vector head size [Default is 0, i.e., a
        line]. See :gmt-docs:`rose.html#vector-attributes` for
        specifying additional attributes. If ``vectors`` is not
        given and the current plot mode is to draw a windrose diagram
        then using ``vector_params`` will add vector heads to all
        individual directions using the supplied attributes.

    alpha : float or str
        Set the confidence level used to determine if the mean
        resultant is significant (i.e., Lord Rayleigh test for
        uniformity) [Default is ``alpha=0.05``]. **Note**: The
        critical values are approximated [Berens, 2009] and requires
        at least 10 points; the critical resultants are accurate to
        at least 3 significant digits. For smaller data sets you
        should consult exact statistical tables.

        Berens, P., 2009, CircStat: A MATLAB Toolbox for Circular
        Statistics, *J. Stat. Software*, 31(10), 1-21,
        https://doi.org/10.18637/jss.v031.i10.

    {verbose}
    {binary}
    {panel}
    {nodata}
    {find}
    {header}
    {incols}
    {perspective}
    {transparency}
    {wrap}
    """

    kwargs = self._preprocess(**kwargs)

    with Session() as lib:
        with lib.virtualfile_in(
            check_kind="vector", data=data, x=length, y=azimuth
        ) as vintbl:
            lib.call_module(module="rose", args=build_arg_list(kwargs, infile=vintbl))
