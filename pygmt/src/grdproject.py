"""
grdproject - Forward and inverse map transformation of grids.
"""
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray

__doctest_skip__ = ["grdproject"]


@fmt_docstring
@use_alias(
    C="center",
    D="spacing",
    E="dpi",
    F="scaling",
    G="outgrid",
    J="projection",
    I="inverse",
    M="unit",
    R="region",
    V="verbose",
    n="interpolation",
    r="registration",
)
@kwargs_to_strings(C="sequence", D="sequence", R="sequence")
def grdproject(grid, **kwargs):
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
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
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
        Force 1:1 scaling, i.e., output or output data are in actual projected
        meters [**e**]. To specify other units, append **f** (foot),
        **k** (km), **M** (statute mile), **n** (nautical mile), **u**
        (US survey foot), **i** (inch), **c** (cm), or **p** (point).
    unit : str
        Append **c**, **i**, or **p** to indicate that cm, inch, or point
        should be the projected measure unit. Cannot be used with ``scaling``.
    {verbose}
    {interpolation}
    {registration}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Load a grid of @earth_relief_30m data, with an x-range of 10 to 30,
    >>> # and a y-range of 15 to 25
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Create a new grid from the input grid, set the projection to
    >>> # Mercator, and set inverse to "True" to change from "geographic"
    >>> # to "rectangular"
    >>> new_grid = pygmt.grdproject(grid=grid, projection="M10c", inverse=True)
    """
    if kwargs.get("J") is None:
        raise GMTInvalidInput("The projection must be specified.")
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if (outgrid := kwargs.get("G")) is None:
                    kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
                lib.call_module(
                    module="grdproject", args=build_arg_string(kwargs, infile=infile)
                )

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
