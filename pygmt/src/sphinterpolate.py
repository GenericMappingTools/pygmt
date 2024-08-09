"""
sphinterpolate - Spherical gridding in tension of data on a sphere
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["sphinterpolate"]


@fmt_docstring
@use_alias(
    I="spacing",
    R="region",
    V="verbose",
)
@kwargs_to_strings(I="sequence", R="sequence")
def sphinterpolate(data, outgrid: str | None = None, **kwargs) -> xr.DataArray | None:
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
    data : str, {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    {outgrid}
    {spacing}
    {region}
    {verbose}

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Load a table of Mars with longitude/latitude/radius columns
    >>> mars_shape = pygmt.datasets.load_sample_data(name="mars_shape")
    >>> # Perform Delaunay triangulation on the table data
    >>> # to produce a grid with a 1 arc-degree spacing
    >>> grid = pygmt.sphinterpolate(data=mars_shape, spacing=1, region="g")
    """
    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="vector", data=data) as vintbl,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="sphinterpolate", args=build_arg_list(kwargs, infile=vintbl)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
