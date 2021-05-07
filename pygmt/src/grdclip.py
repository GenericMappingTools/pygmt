"""
Grdclip - Clip a grid.
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
    Si="interval",
    Sr="old",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def grdclip(grid, **kwargs):
    r"""
    Sets specific values, or values above/below a set number, to a given value.

    Produce a new ``outgrid`` file clipped version of``grid``.

    The parameters ``above`` and ``below`` allow for a given value to be set
    for values above or below a set amount, respectively. This allows for
    extreme values in a grid, such as points below a certain depth when
    plotting Earth relief, to all be set to the same value.
    subregion is specified with ``region``; the specified range must not exceed
    the range of ``grid`` (but see ``extend``). If in doubt, run
    :meth:`pygmt.grdinfo` to check range. Alternatively, define the subregion
    indirectly via a range check on the node values or via distances from a
    given point. Finally, you can give ``projection`` for oblique projections
    to determine the corresponding rectangular ``region`` that will give a grid
    that fully covers the oblique domain.

    Full option list at :gmt-docs:`grdcut.html`

    {aliases}
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
