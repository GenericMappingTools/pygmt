"""
grdfill - Fill blank areas from a grid.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    A="mode",
    G="outgrid",
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def grdfill(grid, **kwargs):
    r"""
    Fill blank areas from a grid file.

    Read a grid that presumably has unfilled holes that the user
    wants to fill in some fashion. Holes are identified by NaN values but
    this criteria can be changed. There are several different algorithms that
    can be used to replace the hole values.

    Full option list at :gmt-docs:`grdfill.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    mode : str
        Specify the hole-filling algorithm to use.  Choose from **c** for
        constant fill and append the constant value, **n** for nearest
        neighbor (and optionally append a search radius in
        pixels [default radius is :math:`r^2 = \sqrt{{ X^2 + Y^2 }}`,
        where (*X,Y*) are the node dimensions of the grid]), or
        **s** for bicubic spline (optionally append a *tension*
        parameter [Default is no tension]).

    {R}
    {V}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    if "A" not in kwargs.keys() and "L" not in kwargs.keys():
        raise GMTInvalidInput("At least parameter 'mode' or 'L' must be specified.")
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdfill", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result
