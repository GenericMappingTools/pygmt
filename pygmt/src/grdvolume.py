"""
grdvolume - Calculate grid volume and area constrained by a contour.
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
    C="above",
    Cr="below",
    R="region",
    V="verbose",
)
@kwargs_to_strings(C="sequence", R="sequence")
def grdvolume(grid, **kwargs):
    r"""
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
    volume : str
        A string with the volume between the surface and specified plane.
    """
    with GMTTempFile() as outfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdvolume", arg_str)
        result = outfile.read()
    return result
