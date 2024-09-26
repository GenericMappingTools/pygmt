"""
grd2cpt - Create a CPT from a grid file.
"""

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["grd2cpt"]


@fmt_docstring
@use_alias(
    A="transparency",
    C="cmap",
    D="background",
    F="color_model",
    E="nlevels",
    G="truncate",
    H="output",
    I="reverse",
    L="limit",
    M="overrule_bg",
    N="no_bg",
    Q="log",
    R="region",
    T="series",
    V="verbose",
    W="categorical",
    Ww="cyclic",
    Z="continuous",
)
@kwargs_to_strings(G="sequence", L="sequence", R="sequence", T="sequence")
def grd2cpt(grid, **kwargs):
    r"""
    Make GMT color palette tables from a grid file.

    This function will help you to make static color palette tables (CPTs).
    By default, the CPT will be saved as the current CPT of the session,
    figure, subplot, panel, or inset depending on which level
    :func:`pygmt.grd2cpt` is called (for details on how GMT modern mode
    maintains different levels of colormaps please see
    :gmt-docs:`reference/features.html#gmt-modern-mode-hierarchical-levels`).
    You can use ``output`` to save the CPT to a file. The CPT is based on an
    existing dynamic master CPT of your choice, and the mapping from data value
    to colors is through the data's cumulative distribution function (CDF), so
    that the colors are histogram equalized. Thus if the grid(s) and the
    resulting CPT are used in :meth:`pygmt.Figure.grdimage` with a linear
    projection, the colors will be uniformly distributed in area on the plot.
    Let z be the data values in the grid. Define CDF(Z) = (# of z < Z) / (# of
    z in grid). (NaNs are ignored). These z-values are then normalized to the
    master CPT and colors are sampled at the desired intervals.

    The CPT includes three additional colors beyond the range of z-values.
    These are the background color (B) assigned to values lower than the lowest
    *z*-value, the foreground color (F) assigned to values higher than the
    highest *z*-value, and the NaN color (N) painted wherever values are
    undefined. For color tables beyond the standard GMT offerings, visit
    `cpt-city <http://www.seaviewsensing.com/pub/cpt-city/>`_ and
    `Scientific Colour-Maps <http://www.fabiocrameri.ch/colourmaps.php>`_.

    If the master CPT includes B, F, and N entries, these will be copied into
    the new master file. If not, the parameters :gmt-term:`COLOR_BACKGROUND`,
    :gmt-term:`COLOR_FOREGROUND`, and :gmt-term:`COLOR_NAN` from the
    :gmt-docs:`gmt.conf <gmt.conf>` file will be used. This default behavior
    can be overruled using the parameters ``background``, ``overrule_bg``
    or ``no_bg``.

    The color model (RGB, HSV or CMYK) of the palette created by
    :func:`pygmt.grd2cpt` will be the same as specified in the header of the
    master CPT. When there is no :gmt-term:`COLOR_MODEL` entry in the master
    CPT, the :gmt-term:`COLOR_MODEL` specified in the
    :gmt-docs:`gmt.conf <gmt.conf>` file or the ``color_model`` parameter
    will be used.

    Full option list at :gmt-docs:`grd2cpt.html`

    {aliases}

    Parameters
    ----------
    {grid}
    transparency : int or float or str
        Set a constant level of transparency (0-100) for all color slices.
        Append **+a** to also affect the foreground, background, and NaN
        colors [Default is no transparency, i.e., ``0`` (opaque)].
    cmap : str
        Select the master color palette table (CPT) to use in the
        interpolation. Full list of built-in color palette tables can be found
        at :gmt-docs:`reference/cpts.html#built-in-color-palette-tables-cpt`.
    background : bool or str
        Select the back- and foreground colors to match the colors for lowest
        and highest *z*-values in the output CPT [Default (``background=True``
        or ``background="o"``) uses the colors specified in the master file, or
        those defined by the parameters :gmt-term:`COLOR_BACKGROUND`,
        :gmt-term:`COLOR_FOREGROUND`, and :gmt-term:`COLOR_NAN`]. Use
        ``background="i"`` to match the colors for the lowest and highest
        values in the input (instead of the output) CPT.
    color_model : str
        [**R**\|\ **r**\|\ **h**\|\ **c**]\
        [**+c**\ [*label*\|\ *start*\ [**-**]]].
        Force output CPT to be written with r/g/b codes, gray-scale values or
        color name (**R**, default) or r/g/b codes only (**r**), or h-s-v codes
        (**h**), or c/m/y/k codes (**c**).  Optionally or alternatively, append
        **+c** to write discrete palettes in categorical format. If *label* is
        appended then we create labels for each category to be used when the
        CPT is plotted. The *label* may be a comma-separated list of category
        names (you can skip a category by not giving a name), or give
        *start*, where we automatically build monotonically increasing
        labels from *start* (a single letter or an integer). Additionally
        append **-** to build ranges *start*-*start+1* as labels instead.
    nlevels : bool, int, or str
        Set to ``True`` to create a linear color table by using the grid
        z-range as the new limits in the CPT. Alternatively, set *nlevels*
        to resample the color table into *nlevels* equidistant slices.
    series : list or str
        [*min/max/inc*\ [**+b**\|\ **l**\|\ **n**\]|\ *file*\|\ *list*\].
        Define the range of the new CPT by giving the lowest and highest
        z-value (and optionally an interval). If this is not given, the
        existing range in the master CPT will be used intact. The values
        produced defines the color slice boundaries. If **+n** is used it
        refers to the number of such boundaries and not the number of slices.
        For details on array creation, see
        :gmt-docs:`makecpt.html#generate-1d-array`.
    truncate : list or str
        *zlow/zhigh*.
        Truncate the incoming CPT so that the lowest and highest z-levels are
        to *zlow* and *zhigh*. If one of these equal NaN then we leave that
        end of the CPT alone. The truncation takes place before any resampling.
        See also :gmt-docs:`reference/features.html#manipulating-cpts`.
    output : str
        Optional. The file name with extension .cpt to store the generated CPT
        file. If not given or ``False`` [Default], saves the CPT as the current
        CPT of the session, figure, subplot, panel, or inset depending on which
        level :func:`pygmt.grd2cpt` is called.
    reverse : str
        Set this to ``True`` or **c** [Default] to reverse the sense of color
        progression in the master CPT. Set this to **z** to reverse the sign
        of z-values in the color table. Note that this change of z-direction
        happens before ``truncate`` and ``series`` values are used so the
        latter must be compatible with the changed z-range. See also
        :gmt-docs:`reference/features.html#manipulating-cpts`.
    overrule_bg : str
        Overrule background, foreground, and NaN colors specified in the master
        CPT with the values of the parameters :gmt-term:`COLOR_BACKGROUND`,
        :gmt-term:`COLOR_FOREGROUND`, and :gmt-term:`COLOR_NAN` specified in
        the :gmt-docs:`gmt.conf <gmt.conf>` file. When combined with
        ``background``, only :gmt-term:`COLOR_NAN` is considered.
    no_bg : bool
        Do not write out the background, foreground, and NaN-color fields
        [Default will write them, i.e. ``no_bg=False``].
    log : bool
        For logarithmic interpolation scheme with input given as logarithms.
        Expects input z-values provided via ``series`` to be log10(*z*),
        assigns colors, and writes out *z*.
    continuous : bool
        Force a continuous CPT when building from a list of colors and a list
        of z-values [Default is None, i.e. discrete values].
    categorical : bool
        Do not interpolate the input color table but pick the output colors
        starting at the beginning of the color table, until colors for all
        intervals are assigned. This is particularly useful in combination with
        a categorical color table, like ``cmap="categorical"``.
    cyclic : bool
        Produce a wrapped (cyclic) color table that endlessly repeats its
        range. Note that ``cyclic=True`` cannot be set together with
        ``categorical=True``.
    {verbose}

    Example
    -------
    >>> import pygmt
    >>> # load the 30 arc-minutes grid with "gridline" registration
    >>> grid = pygmt.datasets.load_earth_relief("30m", registration="gridline")
    >>> # create a plot
    >>> fig = pygmt.Figure()
    >>> # create a CPT from the grid object with grd2cpt
    >>> pygmt.grd2cpt(grid=grid)
    >>> # plot the grid object, the CPT will be automatically used
    >>> fig.grdimage(grid=grid)
    >>> # show the plot
    >>> fig.show()
    """
    if kwargs.get("W") is not None and kwargs.get("Ww") is not None:
        raise GMTInvalidInput("Set only categorical or cyclic to True, not both.")

    if (output := kwargs.pop("H", None)) is not None:
        kwargs["H"] = True

    with Session() as lib:
        with lib.virtualfile_in(check_kind="raster", data=grid) as vingrd:
            lib.call_module(
                module="grd2cpt",
                args=build_arg_list(kwargs, infile=vingrd, outfile=output),
            )
