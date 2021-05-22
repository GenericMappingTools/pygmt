"""
grd2xyz - Convert grid to data table
"""
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
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def grd2xyz(grid, **kwargs):
    r"""
    Create xyz tables from grid files.

    Read a binary 2-D grid files and write out
    xyz-triplets in ASCII [or binary] format to a standard output.

    Full option list at :gmt-docs:`grd2xyz.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
        This is the only required parameter.
    {R}
    {V}

    Returns
    -------
    info : str
        A string with information about the grid.
    """
    with GMTTempFile() as outfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                arg_str = " ".join(
                    [infile, build_arg_string(kwargs), "->" + outfile.name]
                )
                lib.call_module("grd2xyz", arg_str)
        result = outfile.read()
    return result
