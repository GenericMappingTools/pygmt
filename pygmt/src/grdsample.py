"""
grdsample - Resample a grid onto a new lattice
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    G="outgrid",
    J="projection",
    I="increment",
    R="region",
    T="translate",
    V="verbose",
    n="interpolation",
    r="registration",
)
@kwargs_to_strings(I="sequence", R="sequence")
def grdsample(grid, **kwargs):
    r"""
    Change the registration, spacing, or nodes in a grid file.

    This reads a grid file and interpolates it to create a new grid
    file. It can change the registration with ``translate`` or
    ``registration``, change the grid-spacing or number of nodes with
    ``increment``, and set a new sub-region using ``region``. A bicubic
    [Default], bilinear, B-spline or nearest-neighbor interpolation is set
    with ``interpolation``.

    When ``region`` is omitted, the output grid will cover the same region as
    the input grid. When ``increment`` is omitted, the grid spacing of the
    output grid will be the same as the input grid. Either ``registration`` or
    ``translate`` can be used to change the grid registration. When omitted,
    the output grid will have the same registration as the input grid.

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {I}
    {R}
    translate : bool
        Translate between grid and pixel registration; if the input is
        grid-registered, the output will be pixel-registered and vice-versa.
    interpolation : str
        [**b**\|\ **c**\|\ **l**\|\ **n**][**+a**][**+b**\ *BC*][**+c**]
        [**+t**\ *threshold*].
        Select interpolation mode for grids.

        - **b** to use B-spline smoothing.
        - **c** to use bicubic interpolation.
        - **l** to use bilinear interpolation.
        - **n** to use nearest-neighbor value (for example to plot
        categorical data).

        The following modifiers are supported:

        - **+a** to switch off antialiasing (where supported) [default uses
        antialiasing].
        - **+b** to override boundary conditions used, by appending *g* for
        geographic, *p* for periodic, or *n* for natural boundary conditions.
        For the latter two you may append **x** or **y** to specify just one
        direction, otherwise   both are assumed.
        - **+c** to clip the interpolated grid to input z-min/z-max
        [default may exceed limits].
        - **+t** to control how close to nodes with NaNs the interpolation
        will go based on *threshold*. A *threshold* of 1.0 requires all
        (4 or 16) nodes involved in interpolation to be non-NaN. For example,
        0.5 will interpolate about half way from a non-NaN value and 0.1 will
        go about 90% of the way [default is 0.5].
    registration : str
        [**g**\ |\ **p**\ ].
        Set registrationg to **g**\ ridline or **p**\ ixel.

    {V}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdsample", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result
