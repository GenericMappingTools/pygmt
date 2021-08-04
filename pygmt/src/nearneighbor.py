"""
nearneighbor - Grid table data using a "Nearest neighbor" algorithm
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    data_kind,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    E="empty",
    G="outfile",
    I="spacing",
    N="sectors",
    R="region",
    S="search_radius",
    V="verbose",
    a="aspatial",
    f="coltypes",
    r="registration",
)
@kwargs_to_strings(R="sequence")
def nearneighbor(x=None, y=None, z=None, data=None, **kwargs):
    r"""
    Grid table data using a "Nearest neighbor" algorithm

    **nearneighbor** reads arbitrarily located (*x,y,z*\ [,\ *w*]) triples
    [quadruplets] and uses a nearest neighbor algorithm to assign a weighted
    average value to each node that has one or more data points within a search
    radius centered on the node with adequate coverage across a subset of the
    chosen sectors. The node value is computed as a weighted mean of the
    nearest point from each sector inside the search radius. The weighting
    function and the averaging used is given by:

    .. math::
        w(r_i) = \frac{{w_i}}{{1 + d(r_i) ^ 2}},
        \quad d(r) = \frac {{3r}}{{R}},
        \quad \bar{{z}} = \frac{{\sum_i^n w(r_i) z_i}}{{\sum_i^n w(r_i)}}

    where :math:`n` is the number of data points that satisfy the selection
    criteria and :math:`r_i` is the distance from the node to the *i*'th data
    point. If no data weights are supplied then :math:`w_i = 1`.

    Takes a matrix, xyz triples, or a file name as input.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`nearneighbor.html`

    {aliases}

    Parameters
    ----------
    x/y/z : 1d arrays
        Arrays of x and y coordinates and values z of the data points.
    data : str or 2d array
        Either a data file name or a 2d numpy array with the tabular data.

    {I}

    region : str or list
        *xmin/xmax/ymin/ymax*\[**+r**][**+u**\ *unit*].
        Specify the region of interest.

    search_radius : str
        Sets the search radius that determines which data points are considered
        close to a node.

    outfile : str
        Optional. The file name for the output netcdf file with extension .nc
        to store the grid in.

    empty : str
        Optional. Set the value assigned to empty nodes. Defaults to NaN.

    sectors : str
        *sectors*\ [**+m**\ *min_sectors*]\|\ **n**.
        Optional. The circular search area centered on each node is divided
        into *sectors* sectors. Average values will only be computed if there
        is *at least* one value inside each of at least *min_sectors* of the
        sectors for a given node. Nodes that fail this test are assigned the
        value NaN (but see ``empty``). If +m is omitted then *min_sectors* is
        set to be at least 50% of *sectors* (i.e., rounded up to next integer)
        [Default is a quadrant search with 100% coverage, i.e., *sectors* =
        *min_sectors* = 4]. Note that only the nearest value per sector enters
        into the averaging; the more distant points are ignored. Alternatively,
        use ``sectors="n"`` to call GDALʻs nearest neighbor algorithm instead.

    {V}
    {a}
    {f}
    {r}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`xarray.DataArray`: if ``outfile`` is not set
        - None if ``outfile`` is set (grid output will be stored in file set by
          ``outfile``)
    """

    kind = data_kind(data, x, y, z)
    if kind == "vectors" and z is None:
        raise GMTInvalidInput("Must provide z with x and y.")

    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            # Choose how data will be passed into the module
            table_context = lib.virtualfile_from_data(
                check_kind="vector", data=data, x=x, y=y, z=z
            )
            with table_context as infile:
                if "G" not in kwargs.keys():  # if outfile is unset, output to tmpfile
                    kwargs.update({"G": tmpfile.name})
                outfile = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module(module="nearneighbor", args=arg_str)

        if outfile == tmpfile.name:  # if user did not set outfile, return DataArray
            with xr.open_dataarray(outfile) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        elif outfile != tmpfile.name:  # if user sets an outfile, return None
            result = None

    return result
