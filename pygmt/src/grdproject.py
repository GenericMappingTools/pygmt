"""
grdproject - Forward and inverse map transformation of grids.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["grdproject"]


@fmt_docstring
@use_alias(
    C="center",
    D="spacing",
    E="dpi",
    F="scaling",
    J="projection",
    I="inverse",
    M="unit",
    R="region",
    V="verbose",
    n="interpolation",
    r="registration",
)
@kwargs_to_strings(C="sequence", D="sequence", R="sequence")
def grdproject(grid, outgrid: str | None = None, **kwargs) -> xr.DataArray | None:
    r"""
    Change projection of gridded data between geographical and rectangular.

    This method will project a geographical gridded data set onto a
    rectangular grid. If ``inverse`` is ``True``, it will project a
    rectangular coordinate system to a geographic system. To obtain the value
    at each new node, its location is inversely projected back onto the input
    grid after which a value is interpolated between the surrounding input
    grid values. By default bi-cubic interpolation is used. Aliasing is
    avoided by also forward projecting the input grid nodes. If two or more
    nodes are projected onto the same new node, their average will dominate in
    the calculation of the new node value. Interpolation and aliasing is
    controlled with the ``interpolation`` parameter. The new node spacing may
    be determined in one of several ways by specifying the grid spacing,
    number of nodes, or resolution. Nodes not constrained by input data are
    set to NaN. The ``region`` parameter can be used to select a map region
    large or smaller than that implied by the extent of the grid file.

    Full option list at :gmt-docs:`grdproject.html`

    {aliases}

    Parameters
    ----------
    {grid}
    {outgrid}
    inverse : bool
        When set to ``True`` transforms grid from rectangular to
        geographical [Default is False].
    {projection}
    {region}
    center : str or list
        [*dx*, *dy*].
        Let projected coordinates be relative to projection center [Default
        is relative to lower left corner]. Optionally, add offsets in the
        projected units to be added (or subtracted when ``inverse`` is set) to
        (from) the projected coordinates, such as false eastings and
        northings for particular projection zones [0/0].
    {spacing}
    dpi : int
        Set the resolution for the new grid in dots per inch.
    scaling : str
        [**c**\|\ **i**\|\ **p**\|\ **e**\|\ **f**\|\
        **k**\|\ **M**\|\ **n**\|\ **u**].
        Force 1:1 scaling, i.e., output or input data are in actual projected
        meters [**e**]. To specify other units, append **f** (feet),
        **k** (kilometers), **M** (statute miles), **n** (nautical miles),
        **u** (US survey feet), **i** (inches), **c** (centimeters), or
        **p** (points).
    unit : str
        Append **c**, **i**, or **p** to indicate that centimeters, inches, or
        points should be the projected measure unit. Cannot be used with
        ``scaling``.
    {verbose}
    {interpolation}
    {registration}

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
    >>> region = [10, 30, 15, 25]
    >>> grid = pygmt.datasets.load_earth_relief(resolution="30m", region=region)
    >>> # Project the geographic gridded data onto a rectangular grid
    >>> new_grid = pygmt.grdproject(grid=grid, projection="M10c", region=region)
    """
    if kwargs.get("J") is None:
        raise GMTInvalidInput("The projection must be specified.")

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="grdproject", args=build_arg_list(kwargs, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
