"""
colorbar - Plot gray scale or color scale bar.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.params import Box

__doctest_skip__ = ["colorbar"]


@fmt_docstring
@use_alias(
    B="frame",
    C="cmap",
    D="position",
    G="truncate",
    I="shading",
    L="equalsize",
    Q="log",
    W="scale",
    Z="zfile",
    p="perspective",
)
@kwargs_to_strings(G="sequence", I="sequence", p="sequence")
def colorbar(
    self,
    projection: str | None = None,
    box: Box | bool = False,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot gray scale or color scale bar.

    Both horizontal and vertical colorbars are supported. For CPTs with
    gradational colors (i.e., the lower and upper boundary of an interval
    have different colors) we will interpolate to give a continuous scale.
    Variations in intensity due to shading/illumination may be displayed by
    setting the ``shading`` parameter. Colors may be spaced according to a
    linear scale, all be equal size, or by providing a file with individual
    tile widths.

    .. note::
       For GMT >=6.5.0, the fontsizes of the colorbar x-label, x-annotations,
       and y-label are scaled based on the width of the colorbar following
       :math:`\sqrt{{colorbar\_width / 15}}`). To set a desired fontsize via the
       GMT default parameters :gmt-term:`FONT_ANNOT_PRIMARY`,
       :gmt-term:`FONT_ANNOT_SECONDARY`, and :gmt-term:`FONT_LABEL` (or jointly
       :gmt-term:`FONT`) users have to divide the desired fontsize by the value
       calculated with the formula given above before passing it to the default
       parameters. To only affect fontsizes related to the colorbar, the
       defaults can be changed locally only using ``with pygmt.config(...):``.

    Full GMT docs at :gmt-docs:`colorbar.html`.

    {aliases}
       - F = box
       - J = projection
       - R = region
       - V = verbose
       - c = panel
       - t = transparency

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
        use **j** or **J** for setting *refpoint* via a
        :doc:`2-character justification code </techref/justification_codes>`
        that refers to the (invisible) map domain rectangle,
        (3) use **n** for normalized (0-1) coordinates, or (4) use **x** for
        plot coordinates (inches, cm, etc.). All but **x** requires both
        ``region`` and ``projection`` to be specified. Append **+w** followed
        by the length and width of the colorbar. If width is not specified
        then it is set to 4% of the given length. Give a negative length to
        reverse the scale bar. Append **+h** to get a horizontal scale
        [Default is vertical (**+v**)]. By default, the anchor point on the
        scale is assumed to be the bottom left corner (**BL**), but this can
        be changed by appending **+j** followed by a
        :doc:`2-character justification code </techref/justification_codes>`
        *justify*.
    box
        Draw a background box behind the colorbar. If set to ``True``, a simple
        rectangular box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box
        appearance, pass a :class:`pygmt.params.Box` object to control style, fill, pen,
        and other box properties.
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
    self._activate_figure()

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="colorbar", args=build_arg_list(aliasdict))
