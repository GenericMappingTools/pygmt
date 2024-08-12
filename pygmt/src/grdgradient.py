"""
grdgradient - Compute directional gradients from a grid.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    args_in_kwargs,
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["grdgradient"]


@fmt_docstring
@use_alias(
    A="azimuth",
    D="direction",
    E="radiance",
    N="normalize",
    Q="tiles",
    R="region",
    S="slope_file",
    V="verbose",
    f="coltypes",
    n="interpolation",
)
@kwargs_to_strings(A="sequence", E="sequence", R="sequence")
def grdgradient(grid, outgrid: str | None = None, **kwargs) -> xr.DataArray | None:
    r"""
    Compute the directional derivative of the vector gradient of the data.

    Can accept ``azimuth``, ``direction``, and ``radiance`` input to create
    the resulting gradient.

    Full option list at :gmt-docs:`grdgradient.html`

    {aliases}

    Parameters
    ----------
    {grid}
    {outgrid}
    azimuth : float, str, or list
        *azim*\ [/*azim2*].
        Azimuthal direction for a directional derivative; *azim* is the
        angle in the x,y plane measured in degrees positive clockwise from
        north (the +y direction) toward east (the +x direction). The
        negative of the directional derivative,
        :math:`-(\frac{{dz}}{{dx}}\sin(\mbox{{azim}}) + \
        \frac{{dz}}{{dy}}\cos(\mbox{{azim}}))`, is found; negation yields
        positive values when the slope of :math:`z(x,y)` is downhill in the
        *azim* direction, the correct sense for shading the illumination of an
        image by a light source above the x,y plane shining from the *azim*
        direction. Optionally, supply two azimuths, *azim*/*azim2*, in which
        case the gradients in each of these directions are calculated and the
        one larger in magnitude is retained; this is useful for illuminating
        data with two directions of lineated structures, e.g., *0*/*270*
        illuminates from the north (top) and west (left).  Finally, if *azim*
        is a file it must be a grid of the same domain, spacing and
        registration as *grid* that will update the azimuth at each output
        node when computing the directional derivatives.
    direction : str
        [**a**][**c**][**o**][**n**].
        Find the direction of the positive (up-slope) gradient of the data.
        The following options are supported:

        - **a** - Find the aspect (i.e., the down-slope direction)
        - **c** - Use the conventional Cartesian angles measured
          counterclockwise from the positive x (east) direction.
        - **o** - Report orientations (0-180) rather than directions (0-360).
        - **n** - Add 90 degrees to all angles (e.g., to give local strikes of
          the surface).
    radiance : str or list
        [**m**\|\ **s**\|\ **p**]\ *azim/elev*\ [**+a**\ *ambient*][**+d**\
        *diffuse*][**+p**\ *specular*][**+s**\ *shine*].
        Compute Lambertian radiance appropriate to use with
        :meth:`pygmt.Figure.grdimage` and :meth:`pygmt.Figure.grdview`. The
        Lambertian Reflection assumes an ideal surface that reflects all the
        light that strikes it and the surface appears
        equally bright from all viewing directions. Here, *azim* and *elev* are
        the azimuth and elevation of the light vector. Optionally, supply
        *ambient* [0.55], *diffuse* [0.6], *specular* [0.4], or *shine* [10],
        which are parameters that control the reflectance properties of the
        surface. Default values are given in the brackets. Use **s** for a
        simpler Lambertian algorithm. Note that with this form you only have
        to provide azimuth and elevation. Alternatively, use **p** for
        the Peucker piecewise linear approximation (simpler but faster
        algorithm; in this case *azim* and *elev* are hardwired to 315
        and 45 degrees. This means that even if you provide other values
        they will be ignored.).
    normalize : str or bool
        [**e**\|\ **t**][*amp*][**+a**\ *ambient*][**+s**\ *sigma*]\
        [**+o**\ *offset*].
        The actual gradients :math:`g` are offset and scaled to produce
        normalized gradients :math:`g_n` with a maximum output magnitude of
        *amp*. If *amp* is not given, default *amp* = 1. If *offset* is not
        given, it is set to the average of :math:`g`. The following forms are
        supported:

        - **True** - Normalize using :math:`g_n = \mbox{{amp}}\
          (\frac{{g - \mbox{{offset}}}}{{max(|g - \mbox{{offset}}|)}})`
        - **e** - Normalize using a cumulative Laplace distribution yielding:
          :math:`g_n = \mbox{{amp}}(1 - \
          \exp{{(\sqrt{{2}}\frac{{g - \mbox{{offset}}}}{{\sigma}}))}}`, where
          :math:`\sigma` is estimated using the L1 norm of
          :math:`(g - \mbox{{offset}})` if it is not given.
        - **t** - Normalize using a cumulative Cauchy distribution yielding:
          :math:`g_n = \
          \frac{{2(\mbox{{amp}})}}{{\pi}}(\tan^{{-1}}(\frac{{g - \
          \mbox{{offset}}}}{{\sigma}}))` where :math:`\sigma` is estimated
          using the L2 norm of :math:`(g - \mbox{{offset}})` if it is not
          given.

        As a final option, you may add **+a**\ *ambient* to add *ambient* to
        all nodes after gradient calculations are completed.
    tiles : str
        **c**\|\ **r**\|\ **R**.
        Control how normalization via ``normalize`` is carried out. When
        multiple grids should be normalized the same way (i.e., with the same
        *offset* and/or *sigma*),
        we must pass these values via ``normalize``. However, this is
        inconvenient if we compute these values from a grid. Use **c** to
        save the results of *offset* and *sigma* to a statistics file; if
        grid output is not needed for this run then do not specify
        ``outgrid``. For subsequent runs, just use **r** to read these
        values. Using **R** will read then delete the statistics file.
    {region}
    slope_file : str
        Name of output grid file with scalar magnitudes of gradient vectors.
        Requires ``direction`` but makes ``outgrid`` optional.
    {verbose}
    {coltypes}
    {interpolation}

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)


    Example
    -------
    >>> import pygmt
    >>> # Load a grid of @earth_relief_30m data, with a longitude range of
    >>> # 10° E to 30° E, and a latitude range of 15° N to 25° N
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Create a new grid from an input grid, set the azimuth to 10 degrees,
    >>> new_grid = pygmt.grdgradient(grid=grid, azimuth=10)
    """
    if kwargs.get("Q") is not None and kwargs.get("N") is None:
        raise GMTInvalidInput("""Must specify normalize if tiles is specified.""")
    if not args_in_kwargs(args=["A", "D", "E"], kwargs=kwargs):
        raise GMTInvalidInput(
            "At least one of the following parameters must be specified: "
            "azimuth, direction, or radiance."
        )
    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="grdgradient", args=build_arg_list(kwargs, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
