"""
nearneighbor - Grid table data using a "Nearest neighbor" algorithm.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["nearneighbor"]


@fmt_docstring
@use_alias(
    E="empty",
    I="spacing",
    N="sectors",
    R="region",
    S="search_radius",
    V="verbose",
    a="aspatial",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    g="gap",
    h="header",
    i="incols",
    r="registration",
    w="wrap",
)
@kwargs_to_strings(I="sequence", R="sequence", i="sequence_comma")
def nearneighbor(
    data=None, x=None, y=None, z=None, outgrid: str | None = None, **kwargs
) -> xr.DataArray | None:
    r"""
    Grid table data using a "Nearest neighbor" algorithm.

    **nearneighbor** reads arbitrarily located (*x*, *y*, *z*\ [, *w*])
    triplets [quadruplets] and uses a nearest neighbor algorithm to assign a
    weighted average value to each node that has one or more data points within
    a search radius centered on the node with adequate coverage across a subset
    of the chosen sectors. The node value is computed as a weighted mean of the
    nearest point from each sector inside the search radius. The weighting
    function and the averaging used is given by:

    .. math::
        w(r_i) = \frac{{w_i}}{{1 + d(r_i) ^ 2}},
        \quad d(r) = \frac {{3r}}{{R}},
        \quad \bar{{z}} = \frac{{\sum_i^n w(r_i) z_i}}{{\sum_i^n w(r_i)}}

    where :math:`n` is the number of data points that satisfy the selection
    criteria and :math:`r_i` is the distance from the node to the *i*'th data
    point. If no data weights are supplied then :math:`w_i = 1`.

    .. figure:: https://docs.generic-mapping-tools.org/dev/_images/GMT_nearneighbor.png
       :width: 300 px
       :align: center

       Search geometry includes the search radius (R) which limits the points
       considered and the number of sectors (here 4), which restricts how
       points inside the search radius contribute to the value at the node.
       Only the closest point in each sector (red circles) contribute to the
       weighted estimate.

    Takes a matrix, (x, y, z) triplets, or a file name as input.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`nearneighbor.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    x/y/z : 1-D arrays
        Arrays of x and y coordinates and values z of the data points.

    {spacing}

    {region}

    search_radius : str
        Set the search radius that determines which data points are considered
        close to a node.
    {outgrid}
    empty : str
        Optional. Set the value assigned to empty nodes. Defaults to NaN.

    sectors : str
        *sectors*\ [**+m**\ *min_sectors*]\|\ **n**.
        Optional. The circular search area centered on each node is divided
        into *sectors* sectors. Average values will only be computed if there
        is *at least* one value inside each of at least *min_sectors* of the
        sectors for a given node. Nodes that fail this test are assigned the
        value NaN (but see ``empty``). If **+m** is omitted then *min_sectors*
        is set to be at least 50% of *sectors* (i.e., rounded up to next
        integer) [Default is a quadrant search with 100% coverage, i.e.,
        *sectors* = *min_sectors* = 4]. Note that only the nearest value per
        sector enters into the averaging; the more distant points are ignored.
        Alternatively, use ``sectors="n"`` to call GDAL's nearest neighbor
        algorithm instead.

    {verbose}
    {aspatial}
    {binary}
    {nodata}
    {find}
    {coltypes}
    {gap}
    {header}
    {incols}
    {registration}
    {wrap}

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray`: if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    Example
    -------
    >>> import pygmt
    >>> # Load a sample dataset of bathymetric x, y, and z values
    >>> data = pygmt.datasets.load_sample_data(name="bathymetry")
    >>> # Create a new grid with 5 arc-minutes spacing in the designated region
    >>> # Set search_radius to only take points within 10 arc-minutes of a node
    >>> output = pygmt.nearneighbor(
    ...     data=data,
    ...     spacing="5m",
    ...     region=[245, 255, 20, 30],
    ...     search_radius="10m",
    ... )
    """
    with Session() as lib:
        with (
            lib.virtualfile_in(
                check_kind="vector", data=data, x=x, y=y, z=z, required_z=True
            ) as vintbl,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="nearneighbor", args=build_arg_list(kwargs, infile=vintbl)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
