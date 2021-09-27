"""
xyz2grd - Convert data table to a grid.
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
    I="spacing",
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def xyz2grd(data, **kwargs):
    """
    Create a grid file from table data.

    xyz2grd reads one or more z or xyz tables and creates a binary grid file.
    xyz2grd will report if some of the nodes are not filled in with data. Such
    unconstrained nodes are set to a value specified by the user [Default is
    NaN]. Nodes with more than one value will be set to the mean value.

    Full option list at :gmt-docs:`xyz2grd.html`

    Parameters
    ----------
    data : str or {table-like}
        Pass in either a file name to an ASCII data table, a 1D/2D
        {table-classes}.

    outgrid : str or None
        Optional. The name of the output netCDF file with extension .nc to
        store the grid in.
    {I}
    {R}
    {V}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray`: if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)```
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = build_arg_string(kwargs)
                arg_str = " ".join([infile, arg_str])
                lib.call_module("xyz2grd", arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
