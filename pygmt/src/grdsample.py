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


@fmt_docstring
@use_alias(
    G="outgrid",
    J="projection",
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
    registration : str or bool
        [**g**\|\ **p**\ ].
        Set registration to **g**\ ridline or **p**\ ixel.
    {V}
    {f}
    {n}
    {x}

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

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
