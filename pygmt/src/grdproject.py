"""
grdproject - Forward and inverse map transformation of grids.
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
    G="outgrid",
    J="projection",
    I="inverse",
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def grdproject(grid, **kwargs):
    r"""
    Change projection of gridded data between geographical and rectangular.

    This module will project a geographical gridded data set onto a
    rectangular grid. If ``inverse`` is ``True``, it will project a
    rectangular coordinate system to a geographic system. To obtain the value
    at each new node, its location is inversely projected back onto the input
    grid after which a value is interpolated between the surrounding input
    grid values. By default bi-cubic interpolation is used. Aliasing is
    avoided by also forward projecting the input grid nodes. If two or more
    nodes are projected onto the same new node, their average will dominate in
    the calculation of the new node value. The ``region`` parameter can be
    used to select a map region larger or smaller than that implied by the
    extent of the grid file.

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
    {J}
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
    if "J" not in kwargs.keys():
        raise GMTInvalidInput("The projection must be specified.")
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdproject", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result
