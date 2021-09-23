"""
sphdistance - Create Voronoi distance, node,
or natural nearest-neighbor grid on a sphere
"""
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
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
def sphdistance(data, **kwargs):
    r"""
    Create Voroni polygons from lat/lon coordinates.

    Reads one or more ASCII [or binary] files (or standard
    input) containing lon, lat and performs the construction of Voronoi
    polygons. These polygons are then processed to calculate the nearest
    distance to each node of the lattice and written to the specified grid.

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
    if "I" not in kwargs.keys() or "R" not in kwargs.keys():
        raise GMTInvalidInput("Both 'region' and 'spacing' must be specified.")
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = build_arg_string(kwargs)
                arg_str = " ".join([infile, arg_str])
                lib.call_module("sphdistance", arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
