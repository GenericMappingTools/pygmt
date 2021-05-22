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
    R="region",
    I="increment",
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
    increment : str
        *xinc*\ [**+e**\|\ **n**][/\ *yinc*\ [**+e**\|\ **n**]].
        *x_inc* [and optionally *y_inc*] is the grid spacing. **Geographical
        (degrees) coordinates**: Optionally, append a increment unit. Choose
        among **m** to indicate arc minutes or **s** to indicate arc seconds.
        If one of the units **e**, **f**, **k**, **M**, **n** or **u** is
        appended instead, the increment is assumed to be given in meter, foot,
        km, mile, nautical mile or US survey foot, respectively, and will be
        converted to the equivalent degrees longitude at the middle latitude
        of the region. If *y_inc* is given but set to 0 it will be reset equal
        to *x_inc*; otherwise it will be converted to degrees latitude. **All
        coordinates**: If **+e** is appended then the corresponding max
        *x* (*east*) or *y* (*north*) may be slightly adjusted to fit exactly
        the given increment [by default the increment may be adjusted slightly
        to fit the given domain]. Finally, instead of giving an increment you
        may specify the *number of nodes* desired by appending **+n** to the
        supplied integer argument; the increment is then recalculated from the
        number of nodes, the *registration*, and the domain. The resulting
        increment value depends on whether you have selected a
        gridline-registered or pixel-registered grid.
    {R}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    if "I" not in kwargs.keys() or "R" not in kwargs.keys():
        raise GMTInvalidInput("Region and increment must be specified.")

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
