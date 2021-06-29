"""
grdlandmask - Create a "wet-dry" mask grid from shoreline data base
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
    I="spacing",
    R="region",
    V="verbose",
    r="registration",
)
@kwargs_to_strings(R="sequence")
def grdlandmask(**kwargs):
    r"""
    Create a grid file with set values for land and water.

    Read the selected shoreline database and create a grid to specify which
    nodes in the specified grid are over land or over water. The nodes defined
    by the selected region and lattice spacing
    will be set according to one of two criteria: (1) land vs water, or
    (2) the more detailed (hierarchical) ocean vs land vs lake
    vs island vs pond.

    Full option list at :gmt-docs:`grdlandmask.html`

    {aliases}

    Parameters
    ----------
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {I}
    {R}
    {V}
    {r}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    if "I" not in kwargs.keys() or "R" not in kwargs.keys():
        raise GMTInvalidInput("Both 'region' and 'spacing' must be specified.")

    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                kwargs.update({"G": tmpfile.name})
            outgrid = kwargs["G"]
            arg_str = build_arg_string(kwargs)
            lib.call_module("grdlandmask", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result
