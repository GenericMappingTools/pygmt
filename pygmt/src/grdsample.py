"""
grdsample - Resample a grid onto a new lattice
"""

from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray

__doctest_skip__ = ["grdsample"]


@fmt_docstring
@use_alias(
    G="outgrid",
    I="spacing",
    R="region",
    T="translate",
    V="verbose",
    f="coltypes",
    n="interpolation",
    r="registration",
    x="cores",
)
@kwargs_to_strings(I="sequence", R="sequence")
def grdsample(grid, **kwargs):
    r"""
    Change the registration, spacing, or nodes in a grid file.

    This reads a grid file and interpolates it to create a new grid
    file. It can change the registration with ``translate`` or
    ``registration``, change the grid-spacing or number of nodes with
    ``spacing``, and set a new sub-region using ``region``. A bicubic
    [Default], bilinear, B-spline or nearest-neighbor interpolation is set
    with ``interpolation``.

    When ``region`` is omitted, the output grid will cover the same region as
    the input grid. When ``spacing`` is omitted, the grid spacing of the
    output grid will be the same as the input grid. Either ``registration`` or
    ``translate`` can be used to change the grid registration. When omitted,
    the output grid will have the same registration as the input grid.

    Full option list at :gmt-docs:`grdsample.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {spacing}
    {region}
    translate : bool
        Translate between grid and pixel registration; if the input is
        grid-registered, the output will be pixel-registered and vice-versa.
    registration : str or bool
        [**g**\|\ **p**\ ].
        Set registration to **g**\ ridline or **p**\ ixel.
    {verbose}
    {coltypes}
    {interpolation}
    {cores}

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
    >>> # Create a new grid from an input grid, change the registration,
    >>> # and set both x- and y-spacing to 0.5 degrees
    >>> new_grid = pygmt.grdsample(
    ...     grid=grid, translate=True, spacing=[0.5, 0.5]
    ... )
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if (outgrid := kwargs.get("G")) is None:
                    kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
                lib.call_module(
                    module="grdsample", args=build_arg_string(kwargs, infile=infile)
                )

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
