"""
grdclip - Change the range and extremes of grid values.
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
    R="region",
    Sa="above",
    Sb="below",
    Si="between",
    Sr="new",
    V="verbose",
)
@kwargs_to_strings(
    R="sequence",
    Sa="sequence",
    Sb="sequence",
    Si="sequence",
    Sr="sequence",
)
def grdclip(grid, **kwargs):
    r"""
    Sets values in a grid that meet certain criteria to a new value.

    Produce a clipped ``outgrid`` or :class:`xarray.DataArray` version of the
    input ``grid`` file.

    The parameters ``above`` and ``below`` allow for a given value to be set
    for values above or below a set amount, respectively. This allows for
    extreme values in a grid, such as points below a certain depth when
    plotting Earth relief, to all be set to the same value.

    Full option list at :gmt-docs:`grdclip.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {R}
    above : str or list or tuple
        [*high*, *above*].
        Set all data[i] > *high* to *above*.
    below : str or list or tuple
        [*low*, *below*].
        Set all data[i] < *low* to *below*.
    between : str or list or tuple
        [*low*, *high*, *between*].
        Set all data[i] >= *low* and <= *high* to *between*.
    new : str or list or tuple
        [*old*, *new*].
        Set all data[i] == *old* to *new*. This is mostly useful when
        your data are known to be integer values.
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
                lib.call_module("grdclip", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result
