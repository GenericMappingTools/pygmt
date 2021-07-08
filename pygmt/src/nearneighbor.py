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
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    I="spacing",
    R="region",
    V="verbose",
    G="outfile",
    a="aspatial",
    f="coltypes",
    r="registration",
    S="search_radius",
    E="empty",
    N="sectors",
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
    nearest point from each sector inside the search radius. 

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
        Sets the search radius that determines which data points are considered close to a node.

    outfile : str
        Optional. The file name for the output netcdf file with extension .nc
        to store the grid in.

    {V}
    {a}
    {f}
    {r}

    empty : str
        Optional. Set the value assigned to empty nodes. Defaults to NaN.

    sectors : str
        Optional. **\ *sectors*\ [**+m**\ *min_sectors*]\|\ **n**
        The circular search area centered on each node is divided into sectors
        sectors. Average values will only be computed if there is at least one
        value inside each of at least min_sectors of the sectors for a given
        node. Nodes that fail this test are assigned the value NaN (but see
        -E). If +m is omitted then min_sectors is set to be at least 50% of
        sectors (i.e., rounded up to next integer) [Default is a quadrant
        search with 100% coverage, i.e., sectors = min_sectors = 4]. Note that
        only the nearest value per sector enters into the averaging; the more
        distant points are ignored. Alternatively, use -Nn to call GDALʻs
        nearest neighbor algorithm instead.

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
            if kind == "file":
                file_context = dummy_context(data)
            elif kind == "matrix":
                file_context = lib.virtualfile_from_matrix(data)
            elif kind == "vectors":
                file_context = lib.virtualfile_from_vectors(x, y, z)
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(data)))
            with file_context as infile:
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
