"""
colorbar - Plot a colorbar.
"""

from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["colorbar"]


@fmt_docstring
@use_alias(
    B="frame",
    C="cmap",
    D="position",
    F="box",
    G="truncate",
    I="shading",
    J="projection",
    L="equalsize",
    Q="log",
    R="region",
    V="verbose",
    W="scale",
    Z="zfile",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(
    R="sequence", G="sequence", I="sequence", c="sequence_comma", p="sequence"
)
def colorbar(self, **kwargs):
    r"""
    Plot colorbars on figures.

    Both horizontal and vertical colorbars are supported. For CPTs with
    gradational colors (i.e., the lower and upper boundary of an interval
    have different colors) we will interpolate to give a continuous scale.
    Variations in intensity due to shading/illumination may be displayed by
    setting the ``shading`` parameter. Colors may be spaced according to a
    linear scale, all be equal size, or by providing a file with individual
    tile widths.

    Full option list at :gmt-docs:`colorbar.html`

    {aliases}

    Parameters
    ----------
    frame : str or list
        Set colorbar boundary frame, labels, and axes attributes.
    {cmap}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        [**+w**\ *length*\ [/\ *width*]]\ [**+e**\ [**b**\|\ **f**][*length*]]\
        [**+h**\|\ **v**][**+j**\ *justify*]\
        [**+m**\ [**a**\|\ **c**\|\ **l**\|\ **u**]]\
        [**+n**\ [*txt*]][**+o**\ *dx*\ [/*dy*]].
        Define the reference point on the map for the color scale using one of
        four coordinate systems: (1) Use **g** for map (user) coordinates, (2)
        use **j** or **J** for setting *refpoint* via a 2-character
        justification code that refers to the (invisible) map domain rectangle,
        (3) use **n** for normalized (0-1) coordinates, or (4) use **x** for
        plot coordinates (inches, cm, etc.). All but **x** requires both
        ``region`` and ``projection`` to be specified. Append **+w** followed
        by the length and width of the colorbar. If width is not specified
        then it is set to 4% of the given length. Give a negative length to
        reverse the scale bar. Append **+h** to get a horizontal scale
        [Default is vertical (**+v**)]. By default, the anchor point on the
        scale is assumed to be the bottom left corner (**BL**), but this can
        be changed by appending **+j** followed by a 2-character
        justification code *justify*.
    box : bool or str
        [**+c**\ *clearances*][**+g**\ *fill*][**+i**\ [[*gap*/]\ *pen*]]\
        [**+p**\ [*pen*]][**+r**\ [*radius*]][**+s**\ [[*dx*/*dy*/][*shade*]]].
        If set to ``True``, draw a rectangular border around the color scale.
        Alternatively, specify a different pen with **+p**\ *pen*. Add
        **+g**\ *fill* to fill the scale panel [Default is no fill]. Append
        **+c**\ *clearance* where *clearance* is either gap, xgap/ygap, or
        lgap/rgap/bgap/tgap where these items are uniform, separate in x- and
        y-direction, or individual side spacings between scale and border.
        Append **+i** to draw a secondary, inner border as well. We use a
        uniform gap between borders of 2p and the :gmt-term:`MAP_DEFAULTS_PEN`
        unless other values are specified. Append **+r** to draw rounded
        rectangular borders instead, with a 6p corner radius. You can override
        this radius by appending another value. Finally, append **+s** to draw
        an offset background shaded region. Here, *dx/dy* indicates the shift
        relative to the foreground frame [Default is ``"4p/-4p"``] and shade
        sets the fill style to use for shading [Default is ``"gray50"``].
    truncate : list or str
        *zlo*/*zhi*.
        Truncate the incoming CPT so that the lowest and highest z-levels are
        to *zlo* and *zhi*. If one of these equal NaN then we leave that end of
        the CPT alone. The truncation takes place before the plotting.
    scale : float
        Multiply all z-values in the CPT by the provided scale. By default,
        the CPT is used as is.
    shading : str, list, or bool
        Add illumination effects. Passing a single numerical value sets the
        range of intensities from -value to +value. If not specified, 1 is
        used. Alternatively, set ``shading=[low, high]`` to specify an
        asymmetric intensity range from *low* to *high*. [Default is no
        illumination].
    equalsize : float or str
        [**i**]\ [*gap*].
        Equal-sized color rectangles. By default, the rectangles are scaled
        according to the z-range in the CPT (see also ``zfile``). If *gap* is
        appended and the CPT is discrete each annotation is centered on each
        rectangle, using the lower boundary z-value for the annotation. If
        **i** is prepended the interval range is annotated instead. If
        ``shading`` is used each rectangle will have its constant color
        modified by the specified intensity.
    log : bool
        Select logarithmic scale and power of ten annotations. All z-values
        in the CPT will be converted to p = log10(z) and only integer p-values
        will be annotated using the 10^p format [Default is linear scale].
    zfile : str
        File with colorbar-width per color entry. By default, the width of the
        entry is scaled to the color range, i.e., z = 0-100 gives twice the
        width as z = 100-150 (see also ``equalsize``). **Note**: The widths
        may be in plot distance units or given as relative fractions and will
        be automatically scaled so that the sum of the widths equals the
        requested colorbar length.
    {verbose}
    {panel}
    {perspective}
    {transparency}

    Example
    -------
    >>> import pygmt
    >>> # Create a new figure instance with pygmt.Figure()
    >>> fig = pygmt.Figure()
    >>> # Create a basemap
    >>> fig.basemap(region=[0, 10, 0, 3], projection="X10c/3c", frame=True)
    >>> # Call the colorbar method for the plot
    >>> fig.colorbar(
    ...     # Set cmap to the "roma" CPT
    ...     cmap="roma",
    ...     # Label the x-axis "Velocity" and the y-axis "m/s"
    ...     frame=["x+lVelocity", "y+lm/s"],
    ... )
    >>> # Show the plot
    >>> fig.show()
    """
    kwargs = self._preprocess(**kwargs)
    with Session() as lib:
        lib.call_module(module="colorbar", args=build_arg_list(kwargs))
