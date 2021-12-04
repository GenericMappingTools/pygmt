"""
sphinterpolate - Spherical gridding in tension of data on a sphere
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
@kwargs_to_strings(I="sequence", R="sequence")
def sphinterpolate(data, **kwargs):
    r"""
    Create spherical grid files in tension of data.

    Reads a table containing *lon, lat, z* columns and performs a Delaunay
    triangulation to set up a spherical interpolation in tension. Several
    options may be used to affect the outcome, such as choosing local versus
    global gradient estimation or optimize the tension selection to satisfy one
    of four criteria.

    Full option list at :gmt-docs:`sphinterpolate.html`

    {aliases}

    Parameters
    ----------
    data : str or {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2D
        {table-classes}.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {I}
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
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
            with file_context as infile:
                if "G" not in kwargs:  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("sphinterpolate", arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
