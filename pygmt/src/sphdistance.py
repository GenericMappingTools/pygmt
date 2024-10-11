"""
sphdistance - Create Voronoi distance, node,
or natural nearest-neighbor grid on a sphere
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["sphdistance"]


@fmt_docstring
@use_alias(
    C="single_form",
    D="duplicate",
    E="quantity",
    I="spacing",
    L="unit",
    N="node_table",
    Q="voronoi",
    R="region",
    V="verbose",
)
@kwargs_to_strings(I="sequence", R="sequence")
def sphdistance(
    data=None, x=None, y=None, outgrid: str | None = None, **kwargs
) -> xr.DataArray | None:
    r"""
    Create Voronoi distance, node, or natural nearest-neighbor grid on a sphere.

    Reads a table containing *lon, lat* columns and performs
    the construction of Voronoi polygons. These polygons are
    then processed to calculate the nearest distance to each
    node of the lattice and written to the specified grid.

    Full option list at :gmt-docs:`sphdistance.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Pass in (x, y) or (longitude, latitude) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    x/y : 1-D arrays
        Arrays of x and y coordinates.
    {outgrid}
    {spacing}
    {region}
    {verbose}
    single_form : bool
        For large data sets you can save some memory (at the expense of more
        processing) by only storing one form of location coordinates
        (geographic or Cartesian 3-D vectors) at any given time, translating
        from one form to the other when necessary [Default keeps both arrays
        in memory]. Not applicable with ``voronoi``.
    duplicate : bool
        Used to skip duplicate points since the algorithm cannot handle them.
        [Default assumes there are no duplicates].
    quantity : str
        **d**\|\ **n**\|\ **z**\ [*dist*].
        Specify the quantity that should be assigned to the grid nodes [Default
        is **d**]:

        - **d** - compute distances to the nearest data point
        - **n** - assign the ID numbers of the Voronoi polygons that each
          grid node is inside
        - **z** - assign all nodes inside the polygon the z-value of the center
          node for a natural nearest-neighbor grid.

        Optionally, append the resampling interval along Voronoi arcs in
        spherical degrees.
    unit : str
        Specify the unit used for distance calculations. Choose among **d**
        (spherical degrees), **e** (meters), **f** (feet), **k** (kilometers),
        **M** (miles), **n** (nautical miles), or **u** (survey feet).
    node_table : str
        Read the information pertaining to each Voronoi
        polygon (the unique node lon, lat and polygon area) from a separate
        file [Default acquires this information from the ASCII segment
        headers of the output file]. Required if binary input via `voronoi`
        is used.
    voronoi : str
        Append the name of a file with pre-calculated Voronoi polygons
        [Default performs the Voronoi construction on input data].

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import numpy as np
    >>> import pygmt
    >>> # Create an array of longitude/latitude coordinates
    >>> coords_list = [[85.5, 22.3], [82.3, 22.6], [85.8, 22.4], [86.5, 23.3]]
    >>> coords_array = np.array(coords_list)
    >>> # Perform a calculation of the distance to
    >>> # each point from Voronoi polygons
    >>> grid = pygmt.sphdistance(
    ...     data=coords_array, spacing=[1, 2], region=[82, 87, 22, 24]
    ... )
    """
    if kwargs.get("I") is None or kwargs.get("R") is None:
        raise GMTInvalidInput("Both 'region' and 'spacing' must be specified.")
    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="vector", data=data, x=x, y=y) as vintbl,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="sphdistance", args=build_arg_list(kwargs, infile=vintbl)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
